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

- [/] goal: make the comparison interpretable
  - [x] Preserve existing results and five trained adapters; verify final hashes and close the idle rental.
  - [x] Check chat-template/token IDs; the checked 179 contexts match.
  - [ ] Add the tested optional answer-now cutoff protocol to our actual GSM8K runner, not only tiny-character.
  - [ ] Keep original bounded-budget scores and rescued-answer scores separate; test both completion and correctness, with all questions retained.
  - [ ] Freeze the evaluation code/settings and repeat untouched Instruct on the same host as the next graft evaluations.
  - failure mode: a cap, parser, template or serving change is reported as changed reasoning.
  - deliverable: raw two-call traces, unchanged original-score checks and a same-host baseline.
- [ ] goal: complete the requested dose-and-healing comparison
  - [ ] Reuse completed unhealed 1× cells; retain norm-matched cells as extras, not substitutes.
  - [ ] Evaluate each subset at exact 2×, 4× and 8×, preserving failures and full fixed demos.
  - [ ] Read every own-maths teacher attempt, including failures, before training. Use a shared128-question train pool for reviewability, accept at least64 sound replies, then apply16 updates of the existing self-SFT repair to each1× parent and combined1×. Frozen parent/training/merge all fp16.
  - [ ] Compare healed models with their exact unhealed parent at the same precision; judge character as well as maths.
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

Use `slop/eval/run9/demo_panel.md` as the current review entry point, then the canonical results page. Existing spending counts against $50 Vast and $60 API total. No new data generation, donor training, full fine-tuning or judge study. The user approved this restart and autonomous continuation; the cutoff runner's five offline regressions passed. The exact1 lease runs a real production smoke before scaling.
