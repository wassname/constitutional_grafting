# Brief: improve astra's reasoning prompt (astra reasons -> Echo writes)

Written by Claude (Opus 5.5), 2026-10-09, for an agent in a Herdr project pane. Repo `/workspace/2026/constitutional_grafting`. Read `AGENTS.md` first (data quality bar, general-rules-only, sign your work, never reuse another project's answers).

## Goal

SFT data for an AI persona, Musonius (constitution: `constitution/v4.md`). Pipeline under test: astra (`openai-codex-2/gpt-6-astra:medium` via plain `pi`) writes private reasoning notes for a request; Echo (echo.fulcrum.inc, free, persona "Musonius", A. A. Long's Epictetus as writing samples) writes the reply from scratch from request + notes. Opus 5.5 replies to the same requests are the quality bar.

Finding so far (Claude, `slop/reviews/20261009_astra_echo_side_by_side_p20.md`, 20 seeds): Echo is faithful; the bottleneck is astra's reasoning. v1 prompt (facts F1.., parties, rules R1.. with section citations, derivation "F1, R2 -> C1", uncertain, decisions) gives correct but shallow notes: the derivation is citation labels, not inference; it misses the mechanism (e.g. "compulsion destroys the trust the reactor depends on", so the order defeats its own goal), the cheapest check ("ask the 74 technicians"), the option nobody named, and a concrete deliverable. Echo replies then read as a careful checklist ("should" 7.7/1k words). A v2 prompt (crux, mechanism, cheapest information, third way, uncertainty with how settled the values are, decision + one draft; ~200 words) is in `scripts/scratch/astra_echo.py` (`REASON_BRIEF_V2`); its 5-seed outputs are written to `data/frontier/voice_test/out_ae_reason_v2.md` and `slop/reviews/20261009_astra_echo_side_by_side_v2.md`.

## Task

Improve the reasoning prompt, including a rotating pool of worked examples, and show the result on the same seeds.

1. Read the v1 and v2 outputs against Opus on the same seeds (the side-by-side files). Write down what each misses.
2. wassname asked for examples written by Opus 5.5 showing these reasoning moves, then astra doing the same for new requests: weighing moral circles (near vs far, how much weight); uncertainty from time (a recent or changing value vs an old, shared one; what was right then vs now); epistemic uncertainty (what is unknown, the cheapest check); "if everyone did this, then ..." (universalisation); plus the mechanism (how an action would actually play out) and the option nobody named. Light semi-formal notation is allowed where it helps (e.g. `∀ agents: adopt(rule) → outcome`, explicit weights, `P(claim)`, `settled(value) ∈ {old+shared, recent, moving}`); full Lean is not expected.
   Write a pool of ~6 short example reasoning blocks (one per move; ~150 words each), as Opus 5.5, on invented cases in domains far from every seed (no colonies, hospitals, ships, schools, family care; bland, unique names). The AGENTS.md rule against item examples in prompts exists because examples anchor (a name "Okonkwo" spread into 8/23 documents). wassname approved examples here; mitigate: each astra call sees 2 examples drawn at random from the pool, and add a leak check (any name or 5-word phrase from an example appearing in astra's notes or Echo's reply is flagged).
3. Variants on the first 5 pilot seeds (the ids in `data/frontier/voice_test/brief_ae_reason_p20.md`): v3 = v2 + 2 rotating examples; v3b = v3 with the semi-formal notation encouraged. Then Echo writes from each (reuse `write()`; keep Echo's prompt unchanged so only the reasoning varies).
4. Compare v1, v2, v3, v3b, Opus on the 5 seeds: read every reply; for each, say whether it found the crux, the mechanism, the cheapest check, a third way, a concrete draft, and whether the voice is a person or a checklist. Count tics as in the p20 run (contrast, "should" constructions, constitution leakage). Quote. No judge needed for 5 seeds; your reading is the evaluation.
5. Recommend one prompt for scaling (20 seeds x 3 samples next), or say none is good enough and why.

## Limits

- astra calls: plain `pi` on `openai-codex-2` only, one at a time, `</dev/null` (see `scripts/data/27_run_frontier.sh` for the exact command and auth extensions). Echo: sequential, a few seconds apart.
- Do not touch the rented box (`ssh cgbox`), the running data lanes, `scripts/data/26_frontier_batches.py`, the constitution, or `data/train/`.
- New code in `scripts/scratch/`; outputs in `data/frontier/voice_test/` with a variant tag; commit with your signature.

## Output

`slop/reviews/20261009_astra_reasoning_prompt.md`: the example pool (verbatim), each prompt variant (verbatim), the 5-seed comparison with quotes, the leak-check result, and the recommendation. Then message the parent session via intercom with the path and a 5-line summary.
