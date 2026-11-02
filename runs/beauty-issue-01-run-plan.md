# Anthro Run Plan — WHOLE Issue No. 01: Beauty

**Goal:** one finished, visually punchy Beauty issue for Anurag (~Nov 2), built from real Anthropologic output instead of the mock copy in `data/issues.js`.
**Market:** US · **Cohort:** women 25–40 · **Window:** last 3 months (Aug 1 – Oct 31, 2026) · **Depth:** STANDARD on every run (coffee round 1 showed quick runs come back too thin).
**Rule:** inputs stay open. Don't feed the mock headlines ("shelf edit", "Peri at 38") into the runs; the issue follows what comes back. Segment text is used verbatim, trimmed only with "…".

**US signal block** (paste into every Client Question): Only include posts from US-based creators: $ prices, US retailers (Sephora, Ulta, Target, Walmart, Amazon US, TikTok Shop US), US drugstore brands (CeraVe, e.l.f., Neutrogena). Exclude £/€ prices, UK/EU retailers (Boots, Superdrug, Douglas), and posts whose country can't be determined.

Fields marked *(confirm)* are guesses until we see that pipeline's launch form signed in.

---

## Run 1 — Trends → cover stat + "Where are they now"

**Category:** skincare and beauty routines for US women 25–40
**Question:** What is moving in skincare and beauty for US women aged 25–40 right now? For each trend: is it rising, peaking, holding as a habit, or fading; the social proof behind it; and how search interest compares with posting.
*Feeds:* cover stat, trend-lifecycle curve, the "Real or hype" shortlist (any trend making a health or results claim).

## Run 2 — Discourse → "The conversation" + "Asking, not posting"

**Topic:** skincare and beauty routines · **Cohort:** US women 25–40 · **Market:** US · **Window:** last 3 months
**Angle:** What do women 25–40 believe, argue about and worry about in their skincare right now? Where does what they search for differ from what they post about?
*Feeds:* "The Answer" headline, 5–6 themes with posted-vs-searched split (the mirrored bar chart), the debate map, the "Asking, not posting" questions.

## Run 3 — Discourse (products) → "Word on the street"

**Topic:** skincare and beauty products being bought, praised or returned · **Cohort/Market/Window:** as Run 2
**Angle:** Which specific products and devices are women 25–40 talking about this quarter, what do they love and complain about, which are called worth it vs overpriced, and which cheaper dupes come up?
*Feeds:* product verdict cards (worth / dupe / try / skip), prices are checked by hand afterward.

## Run 4 — Digital Segmentation → "Who's talking"

**Query:** US audience segments among women 25–40 in skincare and beauty routines
**Category:** US skincare and beauty — skincare routines, devices, makeup, haircare, beauty spending
**Client Question:** Who are the distinct audience segments among US women aged 25–40 talking about their skincare and beauty routines? For each: mindset in their own words, what triggers a purchase, which brands they own. [US signal block]
*Feeds:* the pinned-character, step-by-step "Who's talking" section (one character per segment).

## Run 5 — Brand Performance → "Brands"

**Brands:** pick 3–4 from what Runs 1–3 surface (don't pre-pick) *(confirm form)*
*Feeds:* brand cards with Social / Search / LLM split. The LLM column also feeds the AI-distribution work.

## Run 6 — Foresight Simulator → "What's next"

**Category:** US skincare and beauty for women 25–40 · **Depth:** standard
*Feeds:* Now / Next / Later strip and the 2×2 of four future "worlds".

## Run 7 — Ask an Anthropologist → hormone lens / cultural read (optional)

**Insight to interpret:** the strongest search-vs-post gap from Run 2 (whatever women search far more than they post).
*Feeds:* the one-paragraph cultural read on that page. Run only after Run 2 returns.

---

## After the runs (no Anthropologic needed)

- **Real or hype:** take the 4–5 claims from Runs 1–3, run them through `agents/evidence_check` (needs the Anthropic credits from Yash) or check them by hand with `agents/citations/verify_sources.py`. Every verdict links 2+ verified studies.
- **Copy:** Editor Agent writes the magazine copy from the raw output once credits land; until then, write it by hand from the output, keeping the numbers.
- **Vet:** same as the coffee digest. Flag geo bleed, off-cohort posts and thin post counts before anything goes in the issue.

## Run order

1–4 in parallel → 5 (needs brands from 1–3) → 6 → 7 (needs Run 2).
