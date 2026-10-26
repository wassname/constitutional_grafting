# Thinking-mode heal (goal 2 of `.pi/goals/ad3e95-v12.md`), preparation

Approved by wassname 2026-10-26 ("also try heal as goal"; "$20 is ok"; parallel helper, lower priority). Planner: PI/Claude opus. This brief covers only CPU/API preparation; GPU training waits for a lease decision.

## Key goal

Test whether a small "heal" adapter, trained on top of the frozen D graft, restores thinking mode (think, close the block, answer) without losing D's character. D = `θ_I + Δ_docs + 1·Δsft_rewr|docs` (`r10_stoic0.5_const1_other1_cx_chatr121`). Run 13 found D writes its answer inside an unclosed think block with thinking on: 176/214 blank finals, mostly on character turns (175/192) not ordinary ones (1/22) (`slop/eval/run13_thinking/results.md`).

Design source: `slop/research/20261026_healing_reasoning_after_merges.md` (recommendation 5). Warning: heals can undo the change (wassname's steer-heal-love).

## Preparation steps (this brief)

1. Instruct thinking traces, API only: untouched Instruct `qwen/qwen3.5-35b-a3b` on OpenRouter (verify it is the same Instruct checkpoint family and that thinking is on and returned; record the served provider). About 600 neutral prompts: GSM8K train questions, No Robots prompts, ordinary help. No moral dilemmas, no persona/identity, no frozen eval items (`slop/eval/run8/items.jsonl`, GSM60), no overlap with Box A's control prompts (`scripts/data/90_generic_control.py` pools). Keep only complete replies: non-empty think block that closes, then a final answer, finish=stop. Store the full native reasoning and final.
2. Character prompts for D's own thinking-off answers: choose about 300 training-only prompts from `data/train/run10/chatr12.jsonl` prompt side (never eval items). These are answered by D on a GPU later; only select and save them now.
3. Heal training data format: Qwen3.5 chat template, thinking on; loss on `<think>{reasoning}</think>{answer}<|im_end|>` for the Instruct traces; for D's answers, the native thinking-off template (empty think block in the unlabelled prompt segment, per `scripts/train/check_loss_mask.py`). Write the builder and a CPU test that renders 3 rows of each kind and shows exactly which tokens get loss.
4. Training and eval plan (not run): frozen D merged, new LoRA rank 8, about 500–2,000 rows, one epoch, early checkpoints; variants: traces-only heal, mixed heal, optional KL to frozen D on thinking-off prefixes. Eval in both modes with run 13's recorder (`scripts/eval/54_run13_thinking_box.py`): blank finals, close-before-EOS, loops/cutoffs, visible-final character, maths, fridge tool actions. Estimate GPU hours and cost; must fit $20.

## Limits

API cap $5. No GPU, no training. Write only `scripts/data/92_thinking_heal_data.py`, `slop/data/20261026_thinking_heal/`, and one CPU test under `tests/regression/`. Read `constitution/v4.md` sections 1–5 and AGENTS.md first. Commit scoped files only, signed; do not push. Report to const_v2 (intercom "01a11a85").
