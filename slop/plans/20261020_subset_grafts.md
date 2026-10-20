# Restart: subset grafts, exact doses and healing

PI/Sol. Reuse the saved work; do not restart donor training. This supersedes the earlier norm-matched-only evaluation plan.

## Goal

Deliver a striking, repeatable character change grounded in our constitution, with better reasons, speech or decisions and retained maths and ordinary usefulness. Identify which document subsets contribute. Distinctive but undesirable character is a finding, not the desired endpoint.

## User requirements

- Echo, pure Stoic, Opus and Greek: each at exact 1×, 2×, 4×, 8×, plus 1× healed.
- All four updates combined at 1× each, also healed: 22 conditions including that preferred combined heal.
- Spectral regularization during donor training; λ=50 is now the default.
- Fix cutoff handling before more paid evaluation. Keep the report readable and judge actual responses.

## Plan

- [x] goal: make the comparison interpretable
  - [x] Preserve existing results and five trained adapters; verify final hashes and close the idle rental.
  - [x] Check chat-template/token IDs; the checked 179 contexts match.
  - [x] Add the optional answer-now cutoff protocol to the actual GSM8K runner; five offline regressions and real cutoff traces checked.
  - [x] Keep bounded and answer-now scores separate, with completion and correctness on the full denominator.
  - [x] Freeze evaluation source/settings and repeat untouched Instruct on the same host. Fresh control:55/60 bounded,57/60 answer-now; old53/60 not pooled.
  - failure mode: a cap, parser, template or serving change is reported as changed reasoning.
  - deliverable: raw two-call traces, unchanged original-score checks and a same-host baseline.
- [x] goal: complete the requested dose-and-healing comparison
  - [x] Repeat every unhealed1× on the new host; retain norm-matched cells as separate extras.
  - [x] Evaluate each subset at exact2×,4×,8× with failures and full fixed demos retained.
  - [x] Read every own-maths teacher attempt, including failures, before training. Shared128-question train pool; accepted115/115/114/116/117 unchanged replies for Echo/Stoic/Opus/Greek/all-four. Full request/text/mask/hash checks recorded.
  - [x] Run16trainer steps of the existing self-SFT maths repair for each1× parent and combined1×. All five heals are evaluated. Frozen parent and merge fp16; LoRA tensors float32. Nonfinite-gradient skips mean fewer learned updates, not16verified successful updates.
  - [x] Compare healed models with their exact unhealed parent at the same precision, including character.22/22 generated/graded;161 fixed turns personally read.
  - failure mode: healing restores maths by undoing character, or dose labels disguise a different intervention.
  - deliverable: all 22 named conditions, actual coefficients/stage order, maths/task results and full before/after replies.
- [ ] goal: choose a useful character change and show its data contribution
  - [ ] Read actual decisions and reasons; distinguish recognisable character, desirable judgement and ordinary usefulness.
  - [ ] Use the completed limited blind review as a diagnostic only. Do not expand the judge sideline or claim the cancelled full-panel review succeeded.
  - [ ] Compare subsets and combined/leave-one-out updates; trace useful examples to source documents without claiming document-level causality.
  - [ ] Update one report with the comparison table, character-versus-capability plot, navigable demo excerpts, full dialogues, failures, recommendation and spend.
  - failure mode: a flattering grade or one selected reply is presented as repeatable wise character.
  - deliverable: a concrete saved model/recipe and checkable demonstrations; leave the success goal open if no model meets it.

## Verification and budget

Success: requested conditions exist, same-input full replies support the character claim, and maths/ordinary help remain useful. Likely failure: stronger doses or heals lose coherence/character; show those replies and diagnose before choosing. Subtle failure: improved exact match only reflects finishing sooner; bounded and answer-now results expose this separately.

Use `slop/eval/run9/exact1/demo_panel.md` for the requested comparison, or `docs/results/20261017_spectral_heal.md` for the synthesis. `slop/eval/run9/demo_panel.md` is the earlier diagnostic grid. Existing spending counts against $50 Vast and $60 API total. No new data generation, donor training, full fine-tuning or judge study. The user approved this restart and autonomous continuation; the cutoff runner's five offline regressions passed. The exact1 lease runs a real production smoke before scaling.
