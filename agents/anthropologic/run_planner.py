#!/usr/bin/env python3
"""
run_planner.py  —  decides which Anthropologic runs WHOLE needs, then runs them.

Give it a topic (a weekly issue), a reader question, or a thread. Claude reads it
and writes the exact Anthropologic run requests: which pipelines, with every input
filled in, kept inside a credit budget. You see the plan and its credit total
before anything is submitted.

  PLAN     Claude writes the runs (one Claude call; no credits)
  FOCUS    for Discourse/Trends, fetches Anthropologic's focus options (free)
           and Claude picks the one that matches the plan
  SUBMIT   all runs at once, after you type y (charges Anthropologic credits)
  COLLECT  waits for every run, saves each output, and writes the combined
           file the Editor Agent reads: agents/editor/pipeline/<slug>.json

Usage
-----
  python3 agents/anthropologic/run_planner.py --topic Beauty --dry-run       # print the prompt only
  python3 agents/anthropologic/run_planner.py --topic Beauty                 # plan (Claude call, no credits)
  python3 agents/anthropologic/run_planner.py --topic Beauty --submit        # plan, confirm, run, collect
  python3 agents/anthropologic/run_planner.py --question "Do LED masks work?" --budget 20
  python3 agents/anthropologic/run_planner.py --thread "Hormones across beauty, sleep and exercise" --submit
  python3 agents/anthropologic/run_planner.py --collect runs/beauty           # finish collecting after a stop
  then: python3 agents/editor/editor_agent.py --topic beauty
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "agents"))
import keys  # noqa: E402
from client import PIPELINES, DATE_RANGES, MARKETS, GO_BROAD, DONE, Client, cost, payload, validate  # noqa: E402

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"
RUNS = ROOT / "runs"
EDITOR_INPUT = ROOT / "agents" / "editor" / "pipeline"

SYSTEM = f"""You plan research runs for WHOLE, a health and beauty magazine app for US women 25 to 40.
The research comes from Anthropologic, a social-listening platform. You turn a request into the exact runs to submit.

Pipelines you can use (credits per run):
- discourse (10): what people think, say and feel about a topic: themes, tensions, the shape of the debate.
  Inputs: topic (short noun phrase people would search), cohort, country, date_range, focus.
  Feeds: the issue's conversation pages, "asking, not posting", reader Q&A. A second discourse run with a
  products-and-brands angle feeds product verdicts and brand cards.
- trends (10): what is moving in a category, with social proof and search patterns.
  Inputs: category, cohort, country, date_range, focus. Feeds: cover stat, trend lifecycle ("where are they now"),
  and the Real-or-hype shortlist.
- segmentation (100): psychographic audience segments in their own words.
  Inputs: category, country, client_question (one or two sentences: who the segments are among this cohort,
  their mindset, what triggers a purchase, which brands they own), research_depth (quick or deep).
  Feeds: "who's talking". Expensive; use only for a full issue or when the request is about who.
- futures (200, deep 5000): forces reshaping a category over 3 to 10 years.
  Inputs: category, research_depth. Feeds: "what's next". Very expensive; only when the request is about the future
  and the budget allows. Never plan deep.

Markets must be one of: {", ".join(MARKETS)}.
date_range must be one of: {", ".join(DATE_RANGES)}.

Rules:
- Stay inside the credit budget. Prefer fewer, sharper runs. Never plan two runs that would return the same thing.
- A full weekly issue usually needs: discourse (go broad), trends, segmentation; add a products discourse run and
  futures only if the budget allows. A reader question usually needs one or two cheap runs.
- A thread cuts across topics: plan runs on the shared idea, not one run per topic.
- Keep the request's own words for topic and category where they are searchable. Don't steer the research toward
  an answer: no conclusions inside the inputs.
- focus_hint: "broad" to scan everything, or a few words on the angle you want (e.g. "brands and products").
  Only discourse and trends use it; leave it empty for the others.
- Fill only the inputs a pipeline takes; leave the others as empty strings.
- title: a short label like "Beauty · Discourse · broad"."""

INPUT_KEYS = ["topic", "category", "cohort", "country", "date_range", "client_question", "research_depth"]
PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "runs": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "pipeline": {"type": "string", "enum": list(PIPELINES)},
                "title": {"type": "string"},
                "why": {"type": "string"},
                "focus_hint": {"type": "string"},
                "inputs": {"type": "object", "properties": {k: {"type": "string"} for k in INPUT_KEYS},
                           "required": INPUT_KEYS, "additionalProperties": False},
            },
            "required": ["pipeline", "title", "why", "focus_hint", "inputs"],
            "additionalProperties": False,
        }},
    },
    "required": ["summary", "runs"],
    "additionalProperties": False,
}
PICK_SCHEMA = {"type": "object", "properties": {"focus": {"type": "string"}},
               "required": ["focus"], "additionalProperties": False}


def call(client, system, prompt, schema, effort="low"):
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=8000,
        system=system,
        messages=[{"role": "user", "content": prompt}],
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
        betas=[FALLBACK_BETA],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(f"declined: {response.stop_details}")
    return json.loads(next(b.text for b in response.content if b.type == "text"))


def plan_prompt(a):
    kind, text = (("weekly issue topic", a.topic) if a.topic else
                  ("reader question", a.question) if a.question else ("thread across topics", a.thread))
    return f"""Request ({kind}): {text}

Reader angle: cohort "{a.cohort}", market "{a.market}", window "{a.window}".
Credit budget: {a.budget}.

Plan the runs."""


def to_params(run):
    return {k: run["inputs"].get(k, "") for k in PIPELINES[run["pipeline"]]["params"]}


def show(plan, budget):
    total = 0
    print(f"\n{plan['summary']}\n")
    for i, r in enumerate(plan["runs"], 1):
        c = cost(r["pipeline"], r["params"])
        total += c
        print(f"{i}. {r['title']}  ({c} credits)\n   why: {r['why']}")
        for k, v in r["params"].items():
            print(f"   {k}: {v or ('(chosen from Anthropologic options: ' + (r['focus_hint'] or 'broad') + ')')}")
    print(f"\nTotal: {total} credits (budget {budget})")
    return total


def pick_focus(claude, anthro, run):
    hint = (run["focus_hint"] or "broad").strip().lower()
    if hint == "broad":
        return GO_BROAD
    options = anthro.focus_options(run["pipeline"], {k: v for k, v in run["params"].items() if v})
    if len(options) == 1:
        return options[0]
    r = call(claude, "Pick the focus option that best matches the angle. Return it exactly as written.",
             f"Angle: {run['focus_hint']}\nOptions:\n" + "\n".join(options), PICK_SCHEMA)
    return r["focus"] if r["focus"] in options else GO_BROAD


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:48]


def collect(folder):
    manifest = json.loads((folder / "manifest.json").read_text())
    anthro = Client()
    for r in manifest["runs"]:
        if r.get("saved"):
            continue
        print(f"waiting on {r['title']} ({r['run_id']}) …", flush=True)
        run = anthro.wait(r["run_id"])
        r["status"] = run.get("status")
        if r["status"] in DONE:
            out = folder / f"{slug(r['title'])}.json"
            out.write_text(json.dumps(payload(run), indent=2, ensure_ascii=False))
            r["saved"] = out.name
            print(f"  saved → {out.relative_to(ROOT)}")
        else:
            print(f"  {r['status']}: not saved")
        (folder / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    done = [r for r in manifest["runs"] if r.get("saved")]
    combined = {
        "topic": manifest["request"], "cohort": manifest["cohort"], "market": manifest["market"],
        "window": manifest["window"], "collected_at": dt.date.today().isoformat(),
        "runs": [{"pipeline": r["pipeline"], "title": r["title"], "inputs": r["params"], "run_id": r["run_id"],
                  "output": json.loads((folder / r["saved"]).read_text())} for r in done],
    }
    EDITOR_INPUT.mkdir(parents=True, exist_ok=True)
    out = EDITOR_INPUT / f"{folder.name}.json"
    out.write_text(json.dumps(combined, indent=2, ensure_ascii=False))
    print(f"\n{len(done)}/{len(manifest['runs'])} runs collected → {out.relative_to(ROOT)}")
    print(f"Next: python3 agents/editor/editor_agent.py --topic {folder.name}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--topic", help="a weekly issue topic, e.g. Beauty")
    src.add_argument("--question", help="a reader's search question")
    src.add_argument("--thread", help="a cross-topic thread")
    src.add_argument("--collect", metavar="FOLDER", help="finish collecting runs listed in FOLDER/manifest.json")
    ap.add_argument("--cohort", default="US women aged 25-40")
    ap.add_argument("--market", default="United States", choices=MARKETS, metavar="MARKET")
    ap.add_argument("--window", default="Last 3 months", choices=DATE_RANGES)
    ap.add_argument("--budget", type=int, default=130, help="max Anthropologic credits (default 130)")
    ap.add_argument("--submit", action="store_true", help="after you confirm, submit the runs and collect results")
    ap.add_argument("--dry-run", action="store_true", help="print the planning prompt without calling Claude")
    a = ap.parse_args()

    try:
        if a.collect:
            return collect(ROOT / a.collect)
        if a.dry_run:
            print(SYSTEM, "\n\n---\n", plan_prompt(a))
            return

        import anthropic
        keys.load()
        claude = anthropic.Anthropic()
        plan = call(claude, SYSTEM, plan_prompt(a), PLAN_SCHEMA)
        for r in plan["runs"]:
            r["params"] = to_params(r)
        total = show(plan, a.budget)
        if total > a.budget:
            sys.exit("Over budget. Raise --budget or ask for fewer runs.")
        if not a.submit:
            print("\nPlan only. Add --submit to run it.")
            return

        anthro = Client()
        for r in plan["runs"]:
            if "focus" in r["params"]:
                r["params"]["focus"] = pick_focus(claude, anthro, r)
                print(f"focus for {r['title']}: {r['params']['focus']}")
            validate(r["pipeline"], r["params"])
        if input(f"\nSubmit {len(plan['runs'])} runs for {total} Anthropologic credits? [y/N] ").strip().lower() != "y":
            sys.exit("Not submitted.")

        name = slug(a.topic or a.question or a.thread)
        folder = RUNS / name
        folder.mkdir(parents=True, exist_ok=True)
        manifest = {"request": a.topic or a.question or a.thread, "cohort": a.cohort, "market": a.market,
                    "window": a.window, "planned_at": dt.datetime.now().isoformat(timespec="seconds"),
                    "summary": plan["summary"], "runs": []}
        for r in plan["runs"]:  # submit everything first, then wait (runs go in parallel)
            res = anthro.submit(r["pipeline"], r["params"], r["title"])
            print(f"submitted {r['title']}: {res.get('run_id')} ({res.get('credits_used')} credits)")
            manifest["runs"].append({**{k: r[k] for k in ("pipeline", "title", "why", "params")},
                                     "run_id": res["run_id"]})
            (folder / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
        collect(folder)
    except (RuntimeError, ValueError) as e:
        sys.exit(f"Stopped: {e}")
    except Exception as e:
        if type(e).__module__.startswith("anthropic"):
            sys.exit(f"Stopped: {e}")
        raise


if __name__ == "__main__":
    main()
