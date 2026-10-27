# Kimi moral-deliberation pilot

Approved by wassname 2026-10-27: "yes approved do it", "I'd try one batch first", "use opus batch or subagent", "make sure to spot check", "at end show me some examples", and "make this a clean subdir, with good path, reusable code etc" (spelling corrected). Main session switched from Claude to Sol during execution.

Goal: test whether Kimi K3.1 Pro, with our constitution in context and no guide or visible-reasoning instructions, returns reasoning and answers worth training into a Base LoRA and grafting onto Instruct. This batch tests candidate quality only, not learned moral reasoning.

1. [x] Freeze 50 chatr12 training prompts, seed 27, excluding the earlier pilot rows and run8 evaluation turns.
2. [x] Run only batch 0: 10 prompts, two constitution framings, two draws each. Original role-specific system prompts remain in the conversation.
   - Evidence: `slop/data/moral_deliberation/20261027_pilot/generation.log`, 40 normal-stop replies, Moonshot AI, $1.7180616.
3. [x] Spot-check all four candidates of four seeded prompt groups, blind to external labels.
   - Evidence: `spot_check_selection.json`, `reader_verdicts.jsonl`, `reading_notes.md` in the run. Sol read 16/40 traces; 7 provisional candidates, 9 need revision. No training release.
4. [x] Obtain independent reviews and check the native-process labels.
   - Opus routes blocked; the user explicitly approved Haiku. All 40 native-process reviews and 40 full-pair quality labels returned. The latter recommend 31 unchanged, 5 hold and 4 regenerate; these are not release approval. Process coarse agreement is 38/40, exact class agreement 4/40. `review_summary.md` and `reading_notes.md` record the evidence and limits.
5. [x] Keep the implementation reusable and show complete examples.
   - Code: `scripts/data/moral_deliberation/README.md`.
   - Results: `slop/data/moral_deliberation/20261027_pilot/report.md`, rebuilt with `just moral-deliberation-report 20261027_pilot`.
   - Original verification: 9 maintained regressions and a zero-cost 40-call replay. Current code has 15 maintained regressions, shared request caching and an offline incomplete-run guard; see the subsequent cost prototype's `verification.json` and the journal.
6. [ ] Remaining full reads, independent judgments and possible later batches.
   - Original batches 1–4 remain unrun. Subsequent low/max diagnostics and the four-fresh-question cost comparison are separate runs. No scaling or training release follows from their model verdicts. Current build authority: `docs/plans/20261027_reasoning_dataset_v2.md`.

Failure modes and checks:
- Coherent reasoning can still rationalise: inspect the hidden trace's weighing against contrary facts, not just output style. A conclusion-first final reply is fine; even an early tentative hidden verdict may be genuinely checked. Wassname clarified this on 2026-10-27. Litreview's 31/60 concerns selected final prose, not hidden deliberation. The full 40-trace audit is complete; it measures textual deliberation, not causal faithfulness.
- Filtering can discard hard advice while rewarding generic refusals: report cases and prompt shapes, allow useful help, and require exact evidence for defects.
- A reference to instructions can be harmless planning: regex matches are flags to read, not rejection rules.
- Stale or invented verdicts can enter a release: packet hashes, quote checks, complete coverage, and separate reader/Opus labels are enforced in code.

Budget: the discussion estimated $3–5 for a pilot. The initial agent configured a $10 run cap; this is preserved as executed config, not treated as approval. Actual first-batch plus reported blocked-judge usage totals $1.9626496. The full 200-draw design would exceed the original generation estimate at the observed average, before judging. No GPU training, rentals or additional sampling occurred.

-- PI/Claude; updated PI/OpenAI (Sol)
