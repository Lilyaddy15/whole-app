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
  3. QUEUE     — every verdict is written to data/evidence.json with
                 review.status = "pending". Nothing is shown as checked in the
                 app until an editor approves it (human in the loop).

Usage
-----
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY=...            # or `ant auth login`
  python3 agents/evidence_check/evidence_check.py --dry-run          # print prompts, no API calls
  python3 agents/evidence_check/evidence_check.py --only nutrition-seed-oils
  python3 agents/evidence_check/evidence_check.py                    # check every claim
  python3 agents/evidence_check/evidence_check.py --approve nutrition-seed-oils --editor "Lily"

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
5. The URLs you actually read."""

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
Only list sources that appear in the research notes, with their real URLs."""

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
                },
                "required": ["title", "publisher", "year", "type", "url"],
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
        except (anthropic.APIStatusError, anthropic.APIConnectionError, RuntimeError) as e:
            print(f"  skipped: {e}", file=sys.stderr)
            continue
        out["claims"][c["id"]] = {
            **verdict,
            "checked_at": dt.date.today().isoformat(),
            "model": MODEL,
            "review": {"status": "pending", "editor": None},
        }
        save_out(out)
        print(f"  {verdict['verdict']} ({verdict['confidence']} confidence) — waiting for editor review")
    print(f"Wrote {OUT.relative_to(ROOT)}")


def approve(args):
    out = load_out()
    for cid in args.approve:
        if cid not in out["claims"]:
            sys.exit(f"No checked claim with id {cid}")
        out["claims"][cid]["review"] = {"status": "approved", "editor": args.editor,
                                        "reviewed_at": dt.date.today().isoformat()}
        print(f"Approved {cid}")
    save_out(out)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--only", nargs="+", help="claim ids to check")
    p.add_argument("--dry-run", action="store_true", help="print prompts without calling the API")
    p.add_argument("--approve", nargs="+", help="mark checked claim ids as editor-approved")
    p.add_argument("--editor", default="editor", help="name recorded on approval")
    a = p.parse_args()
    approve(a) if a.approve else run(a)
