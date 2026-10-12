# WHOLE

A clickable prototype of a phone app: a weekly health and beauty magazine for women 25–40, built on the [Anthropologic](https://anthropologic.quilt.ai) research pipelines.

**Live prototype:** https://lilyaddy15.github.io/whole-app/

> **Prototype with sample data.** Issue numbers, quotes, products and prices are invented to look like pipeline output, and brand names appear only to make the mockup realistic. The **Real or hype? verdicts are real**: each one links to published studies that were checked against PubMed or Crossref. WHOLE gives general information, not medical advice.

## What's in the app

- **Today**: a short daily edition (what moved, a new study, a private question, who's talking) that ends when you're caught up; a Real or hype of the day guessing game; updates on everything you follow; a mock morning notification.
- **Search**: a quick answer in seconds from WHOLE's issues and verified research, plus the search agent's plan (which Anthropologic tools, with what inputs, at what cost) and a simulated deep dive. Five example searches have full sample answers.
- **Follow anything**: trends, verdicts, products and questions; changes show up in Today.
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
2. **Grade**: a structured verdict (real / mixed / early / hype), a plain-language summary, confidence, caveats, and sources with PubMed IDs and DOIs.
3. **Verify citations**: `agents/citations/verify_sources.py` looks every source up in PubMed (or Crossref for DOIs) and checks the title and year against the official record. It saves the abstract for the editor. A verdict needs **at least 2 verified studies**, and "real" or "hype" needs **a verified systematic review, meta-analysis, guideline or expert-body statement**. Anything short of that is held back as `needs_sources` and never shown as a verdict.
4. **Editor Agent review**: reads each study's abstract to confirm it says what the verdict claims, then approves, tightens the wording, or sends it back.

No person signs off. The safeguard is the citation rule: every published verdict links to real, verified research.

```bash
pip install -r requirements.txt
node scripts/export_claims.mjs                                         # claims from data/issues.js
python3 agents/evidence_check/evidence_check.py --dry-run              # see the prompts, no API calls
python3 agents/evidence_check/evidence_check.py --only sleep-mouth-taping
python3 agents/citations/verify_sources.py                             # re-check every citation (no API key needed)
```

Needs `ANTHROPIC_API_KEY` (or `ant auth login`). Each claim costs one research call (up to 8 searches) plus one short grading call. `data/evidence.json` holds the 16 current verdicts with 46 published studies, all verified against PubMed or Crossref on 2026-10-11.

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

## The search agent

`agents/search/search_planner.py` plans how to answer a reader's search: it classifies the question (is it real, what are people saying, is it worth it, where is it heading, why, who), picks the smallest set of Anthropologic tools, fills in their inputs from the reader's angle, reuses recent runs, and always includes the Evidence Agent for health claims. The planning call works today (`--plan`); running the pipelines is a stub until the Anthropologic API is integrated, and the app simulates it.

```bash
python3 agents/search/search_planner.py --dry-run "Is creatine safe for women?"
python3 agents/search/search_planner.py --plan "Why is everyone doing Pilates?"   # calls Claude; no pipelines run
```

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
data/daily.js                   Today edition, follow updates, search examples (sample)
data/evidence.json              verdicts + verified studies the app reads
agents/citations/               citation checker (PubMed / Crossref)
agents/evidence_check/          the Evidence Agent and its claims list
agents/editor/                  the Editor Agent and sample pipeline input
agents/search/                  the search planning agent
scripts/export_claims.mjs       exports claims for the Evidence Agent
scripts/apply_drafts.mjs        publishes Editor Agent drafts into the app
```

Run locally: `python3 -m http.server` in this folder, then open http://localhost:8000.

## Not built yet

Live Anthropologic pipeline runs and search deep dives, accounts, real push notifications, real retailer and affiliate links.
