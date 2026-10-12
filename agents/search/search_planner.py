#!/usr/bin/env python3
"""
search_planner.py  —  the WHOLE search agent (planning step).

A reader types anything into Search. This agent decides how to answer it:

  1. CLASSIFY  what kind of question it is (is it real? what are people saying?
               is it worth it? where is it heading? why? who is into it?)
  2. PLAN      the smallest set of Anthropologic tools that answers it, with each
               tool's inputs filled in from the question and the reader's angle
               (topic, cohort, market, time window, angle), plus the WHOLE
               Evidence Agent for any health claim
  3. REUSE     any recent run on the same topic instead of paying for a new one
  4. RUN       the plan, then hand results to the Editor Agent  <- STUBBED

Status: the Anthropologic pipelines are not integrated yet, so run_plan() is a
stub and the app simulates the runs. The planning call is real and can be tried
with --plan (it calls Claude; no pipelines run).

Usage
-----
  python3 agents/search/search_planner.py --dry-run "Is creatine safe for women?"
  python3 agents/search/search_planner.py --plan "Why is everyone doing Pilates?"
"""

import argparse
import json
import sys

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"

# The Anthropologic tools the agent can choose from, as listed on anthropologic.quilt.ai.
# Credit costs marked "est." are placeholders until we have the real price list.
TOOLS = {
    "Trends": {"inputs": ["topic", "market", "window"], "credits": "10 (est.)",
               "use_for": "Whether something is growing, peaking or fading, with social proof and search patterns."},
    "Discourse": {"inputs": ["topic", "cohort", "market", "window", "angle"], "credits": "10",
                  "use_for": "What people think, say and feel: themes, tensions, and what is searched vs. posted."},
    "Digital Segmentation": {"inputs": ["topic", "cohort", "market"], "credits": "20 (est.)",
                             "use_for": "Who is in the conversation: audience groups in their own words."},
    "Brand Performance": {"inputs": ["brand", "market"], "credits": "20 (est.)",
                          "use_for": "How a brand or product performs across social, search and AI answers."},
    "Foresight Simulator": {"inputs": ["category", "depth"], "credits": "200",
                            "use_for": "Where a category is heading: forces, tensions and possible futures."},
    "Ask an Anthropologist": {"inputs": ["question"], "credits": "5 (est.)",
                              "use_for": "The cultural reason behind a behavior, using cultural codes."},
    "Cultural Semiotics": {"inputs": ["topic", "market"], "credits": "30 (est.)",
                           "use_for": "The codes, status signals and tensions that govern a space."},
    "Synthetic Survey": {"inputs": ["question", "cohort"], "credits": "est.",
                         "use_for": "Simulated responses at scale; only when a question asks what people would choose."},
    "Evidence Agent": {"inputs": ["claim"], "credits": "WHOLE",
                       "use_for": "What published research says about a health or beauty claim, with verified studies."},
}

SYSTEM = f"""You are the WHOLE search agent. WHOLE is a health and beauty magazine app for women.
A reader has typed a question. Plan how to answer it with the research tools below.

Tools:
{json.dumps(TOOLS, indent=2)}

Rules:
- Pick the smallest set of tools that fully answers the question. Every run costs credits and time.
- Any question about whether something is safe, works, or is healthy must include the Evidence Agent.
- Fill each tool's inputs. Use the reader's cohort and market unless the question names others.
  Default window: last 3 months. Topic should be the short noun phrase people would search.
- If a recent run in the cache covers a tool's need, reuse it instead of running the tool again.
- Never plan to give personal medical advice. If the question asks for it (dosing, diagnosis,
  "should I stop my medication"), set needs_professional to true.
- Write the quick_answer_hint as what the instant answer should cover from existing WHOLE content."""

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string", "enum": ["real", "talk", "worth", "future", "why", "who", "other"]},
        "topic": {"type": "string"},
        "health_claim": {"type": "boolean"},
        "needs_professional": {"type": "boolean"},
        "quick_answer_hint": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tool": {"type": "string", "enum": list(TOOLS)},
                    "inputs": {"type": "array", "items": {
                        "type": "object",
                        "properties": {"name": {"type": "string"}, "value": {"type": "string"}},
                        "required": ["name", "value"], "additionalProperties": False}},
                    "why": {"type": "string"},
                    "reuse_run_id": {"type": "string"},
                },
                "required": ["tool", "inputs", "why", "reuse_run_id"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["intent", "topic", "health_claim", "needs_professional", "quick_answer_hint", "steps"],
    "additionalProperties": False,
}


def plan_prompt(question, reader, cache):
    return f"""Reader question: {question}

Reader angle: {json.dumps(reader)}

Recent runs you may reuse (run_id, tool, topic, date):
{json.dumps(cache, indent=2) if cache else "none"}

Return the plan. Use an empty string for reuse_run_id when a tool must run fresh."""


def make_plan(client, question, reader, cache):
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=SYSTEM,
        messages=[{"role": "user", "content": plan_prompt(question, reader, cache)}],
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": PLAN_SCHEMA}},
        betas=[FALLBACK_BETA],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(f"declined: {response.stop_details}")
    return json.loads(next(b.text for b in response.content if b.type == "text"))


def run_plan(plan):
    """STUB. Launch each Anthropologic pipeline in the plan, wait for results,
    run the Evidence Agent for health claims, then pass everything to the
    Editor Agent to write the deep dive. Connect once the Anthropologic API is available."""
    raise NotImplementedError("Anthropologic pipelines are not integrated yet; the app simulates this step.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("question")
    p.add_argument("--plan", action="store_true", help="call Claude to make the plan (no pipelines run)")
    p.add_argument("--dry-run", action="store_true", help="print the prompt only")
    a = p.parse_args()
    reader = {"cohort": "women 25-40", "market": "US", "angle": "science-backed", "budget": "mix it up"}
    cache = [{"run_id": "disc-nutrition-2026w41", "tool": "Discourse", "topic": "Nutrition", "date": "2026-10-05"},
             {"run_id": "trends-exercise-2026w41", "tool": "Trends", "topic": "Exercise", "date": "2026-10-05"}]
    if a.dry_run or not a.plan:
        print(SYSTEM, "\n\n---\n", plan_prompt(a.question, reader, cache))
        sys.exit(0)
    import anthropic
    try:
        print(json.dumps(make_plan(anthropic.Anthropic(), a.question, reader, cache), indent=2))
    except (anthropic.APIStatusError, anthropic.APIConnectionError, RuntimeError) as e:
        sys.exit(f"Stopped: {e}")
