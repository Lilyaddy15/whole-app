#!/usr/bin/env python3
"""
editor_agent.py  —  the WHOLE Editor Agent.

Sits between the research and the reader. It thinks and acts like a magazine
editor: find the story, write it so people want to read it, and never let a
number or a claim go further than the research does.

Three jobs:

  1. WRITE    Turn raw Anthropologic pipeline output (written for strategists)
              into a WHOLE issue in magazine voice: cover lines, the headline
              answer, lede, themes, private questions, audience groups,
              what's next and reader Q&A.
  2. CHECK    Fact-check its own draft against the source. Every number, quote
              and claim must trace back to the pipeline output. If anything
              doesn't, the draft goes back for a rewrite (up to --rounds times).
  3. REVIEW   Review the Evidence Agent's "Real or hype?" verdicts for this
              topic. Approve them, tighten the wording, or send them back with
              notes. Nothing reaches the app without this sign-off.

Usage
-----
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY=...            # or `ant auth login`
  python3 agents/editor/editor_agent.py --dry-run --topic nutrition
  python3 agents/editor/editor_agent.py --topic nutrition            # write + check + review
  python3 agents/editor/editor_agent.py --topic nutrition --review-only
  node scripts/apply_drafts.mjs nutrition                              # publish the draft into data/issues.js

Input:   agents/editor/pipeline/<topic>.json   (pipeline output; a sample is included)
Output:  data/drafts/<topic>.json              (issue copy + fact-check log)
         data/evidence.json                    (verdict reviews)

Each run calls Claude and costs money: one writing call and one fact-check call
per round, plus one review call per pending verdict.
"""

import argparse
import datetime as dt
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PIPELINE_DIR = HERE / "pipeline"
DRAFTS = ROOT / "data" / "drafts"
EVIDENCE = ROOT / "data" / "evidence.json"

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"

EDITOR_SYSTEM = """You are the editor of WHOLE, a weekly health and beauty magazine app for US women 25 to 40.
You have edited glossy magazines for years. You know what makes someone stop scrolling, and you know that
trust is the whole business: one overstated claim and the reader is gone.

How you think:
- Find the story first. What changed, who it matters to, and why now. Lead with that.
- Write for a smart friend, not a strategist. Swap jargon for the words readers use ("protein fatigue", not "category saturation").
- Make it vivid with specifics: real numbers, real quotes, concrete products and habits. Specific beats clever.
- Keep it short. Short sentences. One idea per sentence. Cut anything the reader doesn't need.
- Be warm and a little witty, never snarky about the reader or about women's bodies.

What you never do:
- Never invent or round a number into something new. Every figure must appear in the source.
- Never make a claim stronger than the research. "Linked to" stays "linked to"; "small studies" stays small.
- Never give personal medical advice or tell a reader what she should take, stop or buy.
- Never shame bodies, weight or ageing. No "flaws", "fix your", "bikini body", "anti-ageing miracle".
- Never present a sponsored or commercial claim as fact.
- No em dashes. No "not X, but Y" constructions. No scare quotes around ordinary words.

House format:
- Cover lines: a short punchy kicker (2 to 5 words) plus one line that makes her want to open the issue.
- The answer: one sentence, the single most important thing that changed.
- Lede: 3 to 4 sentences that explain it.
- Themes: a short headline and one plain sentence each. Keep the posted and searched shares exactly as given.
- Quotes from people stay in their words; trim with "…" only, never rewrite them."""

CHECKER_SYSTEM = """You are the WHOLE fact-checker. You compare an edited draft with the research it came from.
Be strict and literal. A claim is supported only if the source says it or directly implies it."""

REVIEW_SYSTEM = EDITOR_SYSTEM + """

Today you are reviewing verdicts from the WHOLE Evidence Agent, which grades trends as real, mixed, early or hype
from published research. Your job is the final read before publication."""

STR = {"type": "string"}
def obj(props, req=None):
    return {"type": "object", "properties": props, "required": req or list(props), "additionalProperties": False}
def arr(items):
    return {"type": "array", "items": items}

ISSUE_SCHEMA = obj({
    "stat": STR, "statLine": STR,
    "cover": arr(arr(STR)),
    "answer": STR, "lede": STR,
    "themes": arr(obj({"h": STR, "p": STR, "posted": {"type": "number"}, "searched": {"type": "number"}})),
    "hormone": obj({"b": STR, "p": STR}),
    "asking": arr(obj({"q": STR, "mult": STR, "a": STR})),
    "segments": arr(obj({"n": STR, "q": STR, "share": {"type": "number"}, "trigger": STR, "buys": STR})),
    "next": arr(obj({"w": STR, "s": STR, "h": STR, "p": STR})),
    "worlds": arr(arr(STR)),
    "qa": arr(obj({"q": STR, "a": STR})),
    "editor_note": STR,
})

CHECK_SCHEMA = obj({
    "passed": {"type": "boolean"},
    "problems": arr(obj({
        "field": STR,
        "draft_text": STR,
        "issue": {"type": "string", "enum": ["unsupported number", "overstated claim", "invented quote",
                                              "medical advice", "body shaming", "missing context", "style"]},
        "fix": STR,
    })),
})

REVIEW_SCHEMA = obj({
    "decision": {"type": "string", "enum": ["approve", "approve_with_edits", "return_to_evidence_agent"]},
    "evidence": STR,
    "notes": STR,
})


def call(client, system, prompt, schema, effort):
    """One Claude call with structured output; returns parsed JSON."""
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=system,
        messages=[{"role": "user", "content": prompt}],
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
        betas=[FALLBACK_BETA],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(f"declined: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("ran out of tokens")
    return json.loads(next(b.text for b in response.content if b.type == "text"))


def write_prompt(topic, source, feedback=None):
    p = f"""Edit this week's {topic} issue.

Below is the raw output from the Anthropologic research pipelines for this topic, written for brand strategists.
Turn it into WHOLE copy for our readers. Keep every number exactly as the source gives it.

<pipeline_output>
{json.dumps(source, indent=2, ensure_ascii=False)}
</pipeline_output>

Write: stat and statLine for the cover, three cover lines, the answer, the lede, six themes, a hormone-lens note,
three "asking, not posting" questions with short answers, the audience groups, three "what's next" items
(Now / Next / Later), two possible futures, three reader questions with answers, and a one-line editor_note
explaining the angle you chose."""
    if feedback:
        p += f"""

Your fact-checker sent the last draft back. Fix every problem below and keep everything else.

<fact_check>
{json.dumps(feedback, indent=2, ensure_ascii=False)}
</fact_check>"""
    return p


def check_prompt(source, draft):
    return f"""Fact-check this WHOLE draft against its source.

For every number, quote and factual claim in the draft, confirm it appears in or follows directly from the source.
Flag: numbers not in the source, claims stronger than the source, quotes not in the source, anything that reads as
personal medical advice, body shaming, missing context that would mislead a reader, and breaks of the house style
(em dashes, "not X, but Y"). Set passed to true only if there are no problems other than minor style notes.

<source>
{json.dumps(source, indent=2, ensure_ascii=False)}
</source>

<draft>
{json.dumps(draft, indent=2, ensure_ascii=False)}
</draft>"""


def review_prompt(trend, says, verdict):
    return f"""Review this Real or hype? verdict before it goes in the issue.

Trend: {trend}
What people say: {says}

Evidence Agent verdict:
{json.dumps(verdict, indent=2, ensure_ascii=False)}

Check:
- Does the verdict (real / mixed / early / hype) match what the summary and sources actually show?
- Are there sources, and do they look like real research or expert bodies? If there are none, return it.
- Is the summary accurate, plain and short enough for our reader (2 to 3 sentences)? If you can say it better
  without changing its meaning or strength, put your version in "evidence".
- Does anything read as personal medical advice?

Decide approve, approve_with_edits (with your rewrite in "evidence"), or return_to_evidence_agent (with notes on
what to re-check). If you approve without edits, copy the original summary into "evidence"."""


def edit_issue(client, topic, rounds):
    source = json.loads((PIPELINE_DIR / f"{topic}.json").read_text())
    log, feedback = [], None
    for r in range(1, rounds + 1):
        print(f"  round {r}: writing", flush=True)
        draft = call(client, EDITOR_SYSTEM, write_prompt(topic, source, feedback), ISSUE_SCHEMA, "high")
        print(f"  round {r}: fact-checking", flush=True)
        check = call(client, CHECKER_SYSTEM, check_prompt(source, draft), CHECK_SCHEMA, "high")
        log.append({"round": r, "passed": check["passed"], "problems": check["problems"]})
        if check["passed"]:
            break
        feedback = check["problems"]
    status = "ready" if log[-1]["passed"] else "needs_attention"
    out = {"topic": topic, "status": status, "edited_at": dt.date.today().isoformat(), "model": MODEL,
           "issue": draft, "fact_check": log}
    DRAFTS.mkdir(parents=True, exist_ok=True)
    path = DRAFTS / f"{topic}.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"  {status} after {len(log)} round(s) -> {path.relative_to(ROOT)}")


def review_verdicts(client, topic):
    if not EVIDENCE.exists():
        print("  no data/evidence.json yet; run the Evidence Agent first")
        return
    claims = {c["id"]: c for c in json.loads((ROOT / "agents" / "evidence_check" / "claims.json").read_text())}
    data = json.loads(EVIDENCE.read_text())
    pending = [cid for cid, v in data["claims"].items()
               if cid.startswith(topic + "-") and v.get("review", {}).get("status") == "pending"]
    if not pending:
        print("  no pending verdicts for this topic")
    for cid in pending:
        v, c = data["claims"][cid], claims.get(cid, {})
        verdict = {k: v.get(k) for k in ("verdict", "evidence", "confidence", "caveats", "sources")}
        print(f"  reviewing {cid}", flush=True)
        r = call(client, REVIEW_SYSTEM, review_prompt(c.get("trend", cid), c.get("says", ""), verdict), REVIEW_SCHEMA, "high")
        today = dt.date.today().isoformat()
        if r["decision"] == "return_to_evidence_agent":
            v["review"] = {"status": "returned", "editor": "Editor Agent", "notes": r["notes"], "reviewed_at": today}
        else:
            v["evidence"] = r["evidence"]
            v["review"] = {"status": "approved", "editor": "Editor Agent", "notes": r["notes"], "reviewed_at": today}
        EVIDENCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(f"    {r['decision']}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--topic", required=True, help="topic key, e.g. nutrition (needs agents/editor/pipeline/<topic>.json)")
    p.add_argument("--rounds", type=int, default=3, help="max write + fact-check rounds")
    p.add_argument("--review-only", action="store_true", help="only review Evidence Agent verdicts")
    p.add_argument("--dry-run", action="store_true", help="print the writing prompt without calling the API")
    a = p.parse_args()

    src = PIPELINE_DIR / f"{a.topic}.json"
    if not a.review_only and not src.exists():
        sys.exit(f"No pipeline output at {src.relative_to(ROOT)}")
    if a.dry_run:
        print(EDITOR_SYSTEM, "\n\n---\n")
        print(write_prompt(a.topic, json.loads(src.read_text())))
        return

    import anthropic  # imported here so --dry-run works without the SDK
    client = anthropic.Anthropic()
    try:
        if not a.review_only:
            print(f"Editing {a.topic} issue")
            edit_issue(client, a.topic, a.rounds)
        print(f"Reviewing {a.topic} verdicts")
        review_verdicts(client, a.topic)
    except (anthropic.APIStatusError, anthropic.APIConnectionError, RuntimeError) as e:
        sys.exit(f"Stopped: {e}")


if __name__ == "__main__":
    main()
