# Kimi reasoning-distillation pilot

Approved by wassname 2026-10-27: "yes approved do it", "I'd try one batch first", "use opus batch or subagent", "make sure to spot check", "at end show me some examples", and "make this a clean subdir, with good path, reusable code etc" (spelling corrected). Main session switched from Claude to Sol during execution.

Goal: test whether Kimi K3.1 Pro, with our constitution in context and no guide or visible-reasoning instructions, returns reasoning and answers worth training into a Base LoRA and grafting onto Instruct. This batch tests candidate quality only, not learned moral reasoning.

1. [x] Freeze 50 chatr12 training prompts, seed 27, excluding the earlier pilot rows and run8 evaluation turns.
2. [x] Run only batch 0: 10 prompts, two constitution framings, two draws each. Original role-specific system prompts remain in the conversation.
   - Evidence: `slop/data/reasoning_distill/20261027_pilot/generation.log`, 40 normal-stop replies, Moonshot AI, $1.7180616.
3. [x] Spot-check all four candidates of four seeded prompt groups, blind to external labels.
   - Evidence: `spot_check_selection.json`, `reader_verdicts.jsonl`, `reading_notes.md` in the run. Sol read 16/40 traces; 7 provisional candidates, 9 need revision. No training release.
4. [ ] Obtain independent Opus judgments and check agreement.
   - Blocked: OpenRouter Opus 5.5 subagent returned the same duplication/ToS block on the initial request and one honest clarification that only Kimi outputs would be trained on. No labels returned. Route stopped; no provider or reviewer substitution. `judge/attempts.json` records $0.244588 reported usage.
5. [x] Keep the implementation reusable and show complete examples.
   - Code: `scripts/data/reasoning_distill/README.md`.
   - Results: `slop/data/reasoning_distill/20261027_pilot/report.md`, rebuilt with `just reasoning-distill-report 20261027_pilot`.
   - Tests: 9 maintained regressions passed; cached 40-call replay costs $0; report hashes agree on two rebuilds (`tests.log`, `replay.log`).
6. [ ] Remaining full reads, independent judgments and possible later batches.
   - Batches 1–4 remain unrun. Do not scale while the required judge route is blocked. Another route or reviewer needs an explicit decision.

Failure modes and checks:
- Coherent reasoning can still rationalise: inspect weighing against contrary facts, not just output style; transfer/faithfulness remains untested.
- Filtering can discard hard advice while rewarding generic refusals: report cases and prompt shapes, allow useful help, and require exact evidence for defects.
- A reference to instructions can be harmless planning: regex matches are flags to read, not rejection rules.
- Stale or invented verdicts can enter a release: packet hashes, quote checks, complete coverage, and separate reader/Opus labels are enforced in code.

Budget: the discussion estimated $3–5 for a pilot. The initial agent configured a $10 run cap; this is preserved as executed config, not treated as approval. Actual first-batch plus reported blocked-judge usage totals $1.9626496. The full 200-draw design would exceed the original generation estimate at the observed average, before judging. No GPU training, rentals or additional sampling occurred.

-- PI/Claude; updated PI/OpenAI (Sol)
