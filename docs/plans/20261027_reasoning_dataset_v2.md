# Reasoning chat dataset v2 (plan goal D)

Approved by wassname 2026-10-27 (decisions below). Planner: PI/Claude (litreview). Generate/judge code: cg_reasoning (`scripts/data/moral_deliberation/`); seeds, screens, layout, export: litreview. Layout: `docs/data_pipeline.md` "Layout for new builds".

wassname (spelling corrected): "make sure we cache Kimi and Haiku judge"; "check everything properly: refusals, reverse reasoning, the whole thing"; "seed it properly!! we have so much data: WildChat, Machiavelli, tiny-virtues, Stoic text! we don't need to reuse"; "writing it in Greek or Latin and translating removes verbal tics? need to try with Kimi"; "rejection might be 50%".

- [ ] goal A: fresh seeds, one row per seed (`data/02_seeds/v2/`)
  - [ ] pools: WildChat, Machiavelli scenes, tiny-virtues vignettes (private books if needed), Stoic and other-tradition passages as situations, LASR difficult advice, competition; each row keeps `seed_id`, `source:source_id`, `shape`
  - [ ] dedup across pools (Unicode 5-gram + read top pairs); no seed used twice; identity share capped by rows and words; held-out eval items excluded (tiny-character `leak.py`, AIRiskDilemmas, daily_dilemmas)
  - failure modes: a pool that is also an eval (tiny-virtues is used by decision 2; its eval is then invalid for this model); near-identical seeds under different ids
  - deliverable: seeds file + counts by source and shape; 0 seeds reused
- [ ] goal B: generation pilot with caching, then scale (`data/03_generate/v2/`)
  - [ ] Kimi K3.1 Pro, constitution in context, no guide; every request and response cached by request hash, so nothing paid is repeated
  - [ ] A/B on 50 seeds: direct English vs written in Ancient Greek or Latin then translated to English; compare tic rates, keep rate on full read, reasoning quality
  - failure modes: translation loses facts or changes the decision; translated version keeps fewer rows (2026-10-26 pilot: 10/20 vs 14-15/20 kept)
  - deliverable: pilot table; then ~2,000 generations for ~1,000 kept rows at a 50% rejection rate (budget: decision 4)
- [ ] goal C: check everything (`04_screen/`, `05_judge/`, `06_read/`)
  - [ ] regex screen: tics, constitution/persona/instruction talk, format talk (flags to read, not deletions)
  - [ ] judge, cached: refusal warranted?; reverse reasoning (trace notices a cost and then explains it away, as in the bee-monopoly letters); facts preserved; reasoning matches answer and actions; rules without reasons; validated against hand labels first (Scout-pilot method)
  - [ ] full read of every kept candidate; the judge only orders the queue
  - failure modes: judge agrees on easy rows only; Haiku refuses as Opus did
  - deliverable: verdicts + signed decisions; per-check precision/recall on the hand-labelled set
- [ ] goal D: export and test (`07_train/`)
  - [ ] think block with real reasoning earns loss; `<|im_end|>` labelled; `check_loss_mask.py` passes; one sha256
  - deliverable: `chat_v2.jsonl`, ready for a chat adapter on θ_B + Δ_docs; training is a separate approval

- [ ] goal E: regenerate the constitution documents with Kimi (wassname: "yes regen Kimi, filter, classic to eng")
  - [ ] fresh seeds from the goal A pools, not the chat seeds; written in Ancient Greek or Latin, translated to English; same screens, judge checks and full read as the chats
  - [ ] training text is the finished document only (plain-text loss on Base); Kimi's hidden reasoning while writing is kept for review, not trained
  - failure modes: translation drops facts; the clean-hands arc or verdict-first habit survives the language change; documents lose the reason-to-act link the papers say matters
  - deliverable: `data/07_train/docs_v2.jsonl` (~1,500 documents), tic rates beside the human Stoic baseline; budget not yet set (estimate ~$70-140)

## UAT / Verification

- A: `seeds.jsonl` with 0 repeated `seed_id` and 0 eval overlaps (leak check output).
- B: pilot table; tic rates per 1,000 words for both versions beside the human Stoic baseline (likely failure: translated version has fewer tics but invented facts; check fact-preservation column).
- C: hand-label agreement table; sneaky failure: judge passes fluent reverse reasoning, so at least 10 known reverse-reasoning traces must be in the validation set.

## Decisions (wassname, 2026-10-27)

1. Thinking on: "we're trying to get thinking working!" All v2 rows carry real reasoning; the graft is served with thinking on.
2. tiny-virtues is a seed pool: "do it anyway, it's not a great eval but could be good training data". Vignettes first; the private books in `/workspace/2026/tiny-virtues/private/sources/` if the vignettes are not enough. That eval is then not valid for this model.
3. Haiku judge allowed, with the true purpose stated; if it refuses after one retry, use a non-Anthropic judge (AGENTS.md data rules).
4. Budget (wassname): "$10 to prototype and check, $100 for big run". Prototype = the 50-seed A/B plus judge calibration. Big run = generation + judging for ~1,000 kept rows; at $0.043 per Kimi row (cg_reasoning batch: "$1.718" for 40) direct English fits, the classical route for every row may not.
5. Constitution documents: regenerate with Kimi, filtered, classical then English (goal E). Documents carry reasons tied to the act in plain prose, not reasoning traces (appendix).

## Appendix: do documents need reasoning? (context, not approved)

Papers say documents need reasons tied to the act, not chain-of-thought traces. Cho §4.3-4.4: explicit reasoning blocks gave "small, non-persistent effects" and "DR models blackmailed significantly more than noDR at post-BFT". Li §5.1.1: "value explanations being more effective" than rules; Li C.4: shuffling which reason goes with which act "preserves co-occurrence but breaks attribution" and removed most of the gain. Tan §3.3: removing worked examples cut held-out uplift. Sources: `slop/research/paper_guides/README.md` ("What the papers say matters most").

Tic check on the 2026-10-26 pilot (Kimi, 20 rows per version, final English text, per 1,000 words): "plain" 1.06 / 1.21 direct vs 0.00 classical; "I won't" 0.70 / 0.87 vs 0.00; "honest" 1.41 / 1.04 vs 0.62; em dash 6.52 / 4.85 vs 1.71; "not ... but" 0.53 / 0.52 vs 2.96 (human Stoic text 1.29). Small counts; computed this session from `slop/data/20261026_reasoning_pilot/raw.jsonl`.
