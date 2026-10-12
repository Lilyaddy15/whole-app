#!/usr/bin/env python3
"""
evidence_check.py  —  WHOLE "Real or hype?" Evidence Agent.

The Anthropologic pipelines tell us what people SAY about a trend. This agent
fills in the other half of a "Real or hype?" verdict: what the EVIDENCE says.

For each claim in claims.json it:
  1. RESEARCH  — Claude searches and reads trusted medical / research sources
                 (web search + web fetch, restricted to an allow-list of domains),
  2. GRADE     — a second call turns the research notes into a structured verdict
                 (real / mixed / early / hype) with a consumer-friendly summary,
                 confidence, source list and caveats,
  3. VERIFY    — every cited article is looked up in PubMed or Crossref
                 (agents/citations/verify_sources.py). Titles and years must match
                 the official record. A verdict needs 2+ verified sources, and
                 "real" / "hype" need a verified review, guideline or expert body.
                 If it falls short, the agent researches once more with notes.
  4. QUEUE     — verdicts that pass go to data/evidence.json as "pending" for the
                 WHOLE Editor Agent (agents/editor/editor_agent.py), which reads the
                 abstracts and approves or returns them. Verdicts that still lack
                 sources are saved as "needs_sources" and never shown as a verdict.

Usage
-----
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY=...            # or `ant auth login`
  python3 agents/evidence_check/evidence_check.py --dry-run          # print prompts, no API calls
  python3 agents/evidence_check/evidence_check.py --only nutrition-seed-oils
  python3 agents/evidence_check/evidence_check.py                    # check every claim
  python3 agents/editor/editor_agent.py --topic nutrition --review-only     # Editor Agent review

Each run calls Claude and costs money: roughly one research call (with up to
8 searches) plus one short grading call per claim.
"""

import argparse
import datetime as dt
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "agents" / "citations"))
from verify_sources import verify_source, publishable  # noqa: E402
CLAIMS = HERE / "claims.json"
OUT = ROOT / "data" / "evidence.json"

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"

# Only search places an editor would accept as evidence.
TRUSTED_DOMAINS = [
    "pubmed.ncbi.nlm.nih.gov", "ncbi.nlm.nih.gov", "nih.gov", "cochranelibrary.com",
    "who.int", "cdc.gov", "fda.gov", "heart.org", "aad.org", "acog.org",
    "menopause.org", "eatright.org", "acsm.org", "health.harvard.edu",
    "mayoclinic.org", "clevelandclinic.org", "nhs.uk", "bmj.com", "thelancet.com",
    "jamanetwork.com", "nejm.org", "nature.com", "examine.com",
]

SYSTEM = """You are the Evidence Agent for WHOLE, a health and beauty magazine app for US women 25 to 40.
Readers see a trend, what people say about it on social media, and your read on what the evidence says.

How to work:
- Search for the strongest evidence first: systematic reviews, meta-analyses, clinical guidelines, then randomized trials.
- Read the sources you rely on. Do not cite anything you have not opened.
- Separate what is studied (e.g. clinic injections) from what is sold (e.g. a topical serum).
- Note who was studied. Evidence in men, older adults or people with a condition may not transfer to healthy women 25 to 40.
- If the evidence is thin, say so plainly. "Not enough research yet" is a valid finding.
- Every source you cite must be a real article you opened. Record its PubMed ID (PMID) and/or DOI exactly as
  shown on the page. Never guess an identifier: each one is checked against PubMed and Crossref.
- You give general information, never personal medical advice."""

RESEARCH_PROMPT = """Check this trend.

Trend: {trend}
What people say: {says}
Topic: {topic}

Find and read the best available evidence, then write research notes covering:
1. The specific claim being made, stated precisely.
2. The strongest evidence for and against it, with the source of each point.
3. How strong and how recent that evidence is, and who it was studied in.
4. Any safety concerns.
5. For each source you actually read: title, journal, year, type, URL, PMID and DOI."""

GRADE_PROMPT = """Turn these research notes into a WHOLE verdict.

Trend: {trend}
What people say: {says}

Research notes:
{notes}

Verdict meanings:
- real: consistent support from good-quality human studies for the claim as people make it.
- mixed: some support, but limited, inconsistent, or smaller than people claim.
- early: plausible, but too little human research to say.
- hype: the evidence does not support the claim, or contradicts it.

Write "evidence" in WHOLE's voice: plain, specific, two or three short sentences, no medical jargon, no advice to a specific person.
Only list sources that appear in the research notes, with their real URLs, PMIDs and DOIs (empty string if none).
List at least two sources. For "real" or "hype", include at least one systematic review, meta-analysis,
clinical guideline or expert-body statement."""

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["real", "mixed", "early", "hype"]},
        "evidence": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "caveats": {"type": "string"},
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "publisher": {"type": "string"},
                    "year": {"type": "string"},
                    "type": {"type": "string", "enum": [
                        "Systematic review", "Meta-analysis", "Clinical guideline",
                        "Randomized trial", "Observational study", "Expert body", "Other"]},
                    "url": {"type": "string"},
                    "pmid": {"type": "string"},
                    "doi": {"type": "string"},
                    "supports": {"type": "string"},
                },
                "required": ["title", "publisher", "year", "type", "url", "pmid", "doi", "supports"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["verdict", "evidence", "confidence", "caveats", "sources"],
    "additionalProperties": False,
}

TOOLS = [
    {"type": "web_search_20260209", "name": "web_search", "max_uses": 8, "allowed_domains": TRUSTED_DOMAINS},
    {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 8, "allowed_domains": TRUSTED_DOMAINS},
]


def research(client, claim, max_continuations=5):
    """Step 1: let Claude search and read; resume if the server pauses the turn."""
    messages = [{"role": "user", "content": RESEARCH_PROMPT.format(**claim)}]
    for _ in range(max_continuations + 1):
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
            output_config={"effort": "high"},
            betas=[FALLBACK_BETA],
            fallbacks="default",
        )
        if response.stop_reason == "refusal":
            raise RuntimeError(f"declined: {response.stop_details}")
        if response.stop_reason != "pause_turn":
            return "\n".join(b.text for b in response.content if b.type == "text")
        # Server-side tool loop paused: send the turn back and it resumes.
        messages = [messages[0], {"role": "assistant", "content": response.content}]
    raise RuntimeError("research still paused after max continuations")


def grade(client, claim, notes):
    """Step 2: structured verdict from the research notes."""
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=SYSTEM,
        messages=[{"role": "user", "content": GRADE_PROMPT.format(notes=notes, **claim)}],
        output_config={"effort": "medium", "format": {"type": "json_schema", "schema": VERDICT_SCHEMA}},
        betas=[FALLBACK_BETA],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(f"declined: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("grading ran out of tokens")
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)


def check_citations(verdict):
    """Look every source up in PubMed / Crossref and apply the publishing rule."""
    for s in verdict["sources"]:
        ok, why = verify_source(s)
        print(f"    {'✓' if ok else '✗'} {s['title'][:60]} ({why})")
    return publishable(verdict)


def load_out():
    if OUT.exists():
        return json.loads(OUT.read_text())
    return {"generated_by": "evidence_check.py", "claims": {}}


def save_out(data):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def run(args):
    claims = json.loads(CLAIMS.read_text())
    if args.only:
        claims = [c for c in claims if c["id"] in args.only]
        if not claims:
            sys.exit(f"No claims match {args.only}. IDs are listed in {CLAIMS.name}.")

    if args.dry_run:
        for c in claims:
            print(f"--- {c['id']} ---\n{RESEARCH_PROMPT.format(**c)}\n")
        print(f"{len(claims)} claim(s). Search limited to {len(TRUSTED_DOMAINS)} trusted domains.")
        return

    import anthropic  # imported here so --dry-run works without the SDK
    client = anthropic.Anthropic()
    out = load_out()
    for c in claims:
        print(f"Checking {c['id']} …", flush=True)
        try:
            notes = research(client, c)
            verdict = grade(client, c, notes)
            ok, reason = check_citations(verdict)
            if not ok:
                print(f"  citations fell short ({reason}); researching again", flush=True)
                notes = research(client, {**c, "says": c["says"] + f"\n(Previous attempt was rejected: {reason}. "
                                         "Find stronger, verifiable sources with exact PMIDs or DOIs.)"})
                verdict = grade(client, c, notes)
                ok, reason = check_citations(verdict)
        except (anthropic.APIStatusError, anthropic.APIConnectionError, RuntimeError) as e:
            print(f"  skipped: {e}", file=sys.stderr)
            continue
        out["claims"][c["id"]] = {
            **verdict,
            "checked_at": dt.date.today().isoformat(),
            "model": MODEL,
            "citations_ok": ok,
            "review": {"status": "pending", "editor": None} if ok else {"status": "needs_sources", "editor": None, "notes": reason},
        }
        save_out(out)
        print(f"  {verdict['verdict']} ({verdict['confidence']} confidence) — "
              + ("sent to the Editor Agent" if ok else f"held back: {reason}"))
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--only", nargs="+", help="claim ids to check")
    p.add_argument("--dry-run", action="store_true", help="print prompts without calling the API")
    a = p.parse_args()
    run(a)
