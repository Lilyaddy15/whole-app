# WHOLE

A clickable prototype of a phone app: a weekly health and beauty magazine for women 25–40, built on the [Anthropologic](https://anthropologic.quilt.ai) research pipelines.

**Live prototype:** https://lilyaddy15.github.io/whole-app/

> **Prototype with sample data.** Every number, quote, product, price and verdict is invented to look like pipeline output. Nothing here is real research or medical advice. Brand names appear only to make the mockup realistic.

## What's in the app

- **Intro and setup**: pick your cards, tune your angle (age, goals, budget, values), hormone lens, privacy.
- **Home**: your weekly "quilt" summary, your issue cards, threads that connect topics, Real or hype?, Asking not posting, Where are they now?
- **Issues** (Nutrition, Beauty, Exercise, Sleep): nine swipeable pages, each mapped to a pipeline.

| Page | Source |
|---|---|
| Cover | Trends |
| The conversation | Discourse |
| Asking, not posting | Discourse (posted vs searched) |
| Real or hype? | Discourse + WHOLE Evidence Agent |
| Who's talking | Digital Segmentation |
| Shop the issue | Brand Performance (affiliate links, ranked by conversation, not commission) |
| Where are they now? | Trends, re-run monthly |
| What's next | Foresight Simulator |
| Ask | Ask an Anthropologist |

- **New card**: add any topic. Adding **Sleep** runs a mock pipeline and finishes into a full issue.
- **About**: an in-app explainer of every section (tap the *i* on the home screen).

## The Evidence Agent

The pipelines say what people *say*. The Evidence Agent adds what the *research* says, for every "Real or hype?" verdict.

`agents/evidence_check/evidence_check.py`:

1. **Research**: Claude Opus 5.5 with web search and web fetch, limited to trusted medical sources (PubMed, Cochrane, NIH, CDC, medical societies…).
2. **Grade**: a structured verdict (real / mixed / early / hype), a plain-language summary, confidence, sources and caveats.
3. **Queue for review**: results go to `data/evidence.json` as `pending`. The Editor Agent reviews them next. The app shows "Being checked" until a verdict is approved.

```bash
pip install -r requirements.txt
node scripts/export_claims.mjs                                         # claims from data/issues.js
python3 agents/evidence_check/evidence_check.py --dry-run              # see the prompts, no API calls
python3 agents/evidence_check/evidence_check.py --only sleep-mouth-taping
python3 agents/evidence_check/evidence_check.py --approve sleep-mouth-taping --editor "Your name"   # manual override
```

Needs `ANTHROPIC_API_KEY` (or `ant auth login`). Each claim costs one research call (up to 8 searches) plus one short grading call. The `data/evidence.json` in this repo is **sample output** created by `node scripts/export_claims.mjs --seed`; it has no real sources.

## The Editor Agent

Every issue is written and signed off by the Editor Agent. It thinks like a magazine editor: find the story, write it so people want to read it, and never let a number or claim go further than the research.

`agents/editor/editor_agent.py`:

1. **Write**: turns raw Anthropologic pipeline output (written for strategists) into WHOLE copy: cover lines, the headline answer, lede, themes, private questions, audience groups, what's next and reader Q&A.
2. **Fact-check**: checks its own draft against the source. Every number, quote and claim must trace back to the pipeline output; overstated claims, medical advice, body shaming and house-style breaks are flagged. Drafts that fail go back for a rewrite (up to 3 rounds).
3. **Review verdicts**: reads each pending Evidence Agent verdict, checks the grade matches the sources, and approves it, tightens the wording, or sends it back to be re-checked.

```bash
python3 agents/editor/editor_agent.py --dry-run --topic nutrition       # see the prompts, no API calls
python3 agents/editor/editor_agent.py --topic nutrition                 # write + fact-check + review verdicts
python3 agents/editor/editor_agent.py --topic nutrition --review-only   # only review verdicts
node scripts/apply_drafts.mjs nutrition                                  # publish a passed draft into data/issues.js
```

Input is `agents/editor/pipeline/<topic>.json` (a sample for Nutrition is included). Drafts and their fact-check log go to `data/drafts/<topic>.json`; only drafts that pass the fact-check are applied. Products, brands and Real or hype claims are kept as they are.

## How the pieces fit

```
Anthropologic pipelines ──► Editor Agent (write + fact-check) ──► data/drafts ──► data/issues.js ──► app
          │
          └─► Real or hype claims ──► Evidence Agent ──► Editor Agent review ──► data/evidence.json ──► app
```

## Project layout

```
index.html                      the app (no build step)
data/issues.js                  all issue content (sample)
data/evidence.json              Evidence Agent output the app reads (sample)
agents/evidence_check/          the Evidence Agent and its claims list
agents/editor/                  the Editor Agent and sample pipeline input
scripts/export_claims.mjs       exports claims for the Evidence Agent
scripts/apply_drafts.mjs        publishes Editor Agent drafts into the app
```

Run locally: `python3 -m http.server` in this folder, then open http://localhost:8000.

## Not built yet

Live Anthropologic pipeline runs, accounts, notifications, real retailer and affiliate links.
