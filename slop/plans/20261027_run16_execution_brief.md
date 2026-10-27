# Run 16 execution brief: v2 best-practice run

Planner: const_v2 (PI/Claude opus, session 01a11a85). Executor: a fresh Sol worker. wassname approved this run on 2026-10-27 (goals file `.pi/goals/ad3e95-v13.md`, cap **$65 total** including GPU, judge and traffic). Read that goals file, AGENTS.md and this brief first.

## What wassname wants to see

One results page scored on tiny-char v2 with replies we read. It answers two questions:
1. D retrained with end-of-turn tokens ("new D"), with and without the projection: does it keep the character with fewer maths/small-task losses than old D at matched character?
2. The anchored document base (generic web text subtracted): is it better at matched effect, alone and as the base under the chat adapter?

Use the layout in the goals file's `## Review preview`.

## Notation (AGENTS shorthand)

- old D = `θ_I + Δ_docs + 1·Δsft_rewr|docs` (`r10_stoic0.5_const1_other1_cx_chatr121`), with Δ_docs = ½·Δtxt_stoic + 1·Δtxt_const + 1·Δtxt_other.
- new D = `θ_I + Δ_docs + c·Δsft_rewr_eos|docs`.
- P_k = run-14 projection (`scripts/train/16_project_chat_adapter.py`): removes the top-k singular directions of θ_I − θ_B from the chat adapter, both sides unless stated.
- Δ_docs_anch = ½·(Δmix_stoic − Δctl) + 1·(Δmix_const − Δctl) + 1·Δtxt_other. Adapters: `r10_x11_mix_stoic`, `r10_x11_mix_const`, `r10_x11_replay_ctl`, `r10_other`.

Adapters are in `~/.local/share/cg_run10_adapters/`. Verify their hashes against the run-10/11/14 receipts.

## Inputs

- Fixed chat data: `/workspace/2026/constitutional_grafting/data/train/eos_fixed/chatr12.jsonl` (gitignored; 1,636 rows, 903 with EOS appended). It comes from the run-14 executed copy `.local/run14_executed_chatr12/chatr12.jsonl` and was built by `scripts/data/93_fix_missing_eos.py`; `manifest.json` next to it has the hashes. `check_loss_mask.py` must pass **without** `ALLOW_MISSING_EOS`.
- Eval: tiny-char v2 `/workspace/2026/tiny-character/data/versions/20261026_v2/items.jsonl`, sha256 `5ea2684bc8e8743ad469d57e584622057af399fc8603033e89978053ac08f444`, 196 items; pass it with `--items`. Check the sha before use. Never commit in the tiny-character repo; it validated v2 in `results/v2_validation.md`.
- cg_exp_curve's cells: exact commands in `slop/plans/20261027_run16_selector_cells_cg_exp_curve.md`. Use `18_project_char_vs_cap.py` at aaaf1599 or later, and copy to the box `data/train/run14/ctlgen.jsonl` (or `slop/eval/run14_box_a/lease/box_runs/ctlgen.jsonl`).
- Templates to fork, not rewrite: `scripts/eval/55_run14_box_a_rental.py`, `56_run14_box_a.py`, `57_run14_results.py`; `scripts/train/14_run10_chat_box.sh` (chat training); the run-15 rental's guard fixes (`58_run15_heal_rental.py`).

## Steps (in order)

0. Worktree `.local/worktrees/run16` on new branch `run16-v2-best-practice` from main HEAD. Run `just --list` before writing scripts. Do a local preflight with CPU and tiny models. Arm the exact-instance deadline guard as in runs 14 and 15, then rent one box.
1. Train `Δsft_rewr_eos|docs` on θ_B + Δ_docs: the same config as run-10 `cx_chatr12`, with spectral regularisation, 2 epochs, the same rank and targets. Diff the resolved config against run 10's and record it: only the dataset path may differ. Check the training text and loss mask, including that the last labelled token is `<|im_end|>`. Then send const_v2 and cg_exp_curve the adapter path and sha256 via intercom.
2. Projections of the new adapter: P64 both sides, P128 both sides, P64 output side only (cg_exp_curve's (a)), and the char/cap selector (cg_exp_curve's (b), with its SHOULD checks; if a check fails, don't graft that cell and message cg_exp_curve).
3. Thinking-off evaluation of each cell: v2 items × 2 samples with the pinned judge, GSM60, small tasks, coherence flags (loops, cutoffs, language), and the fixed T0 demo panel. Same protocol as run 14 apart from the items. Cells:
   - Instruct (v2 reference)
   - new D ×½, ×1
   - new D + P64 ×1, ×1.25; + P128 ×1; + P64 output side ×1; + char/cap ×1
   - old D ×½ and old D + P64 ×1, as a second sample linking to run 14
   - document stage (no chat adapter): Δ_docs, Δ_docs_anch, Const pure ×1 and ×2, Const anchored ×2. For document cells, measure change the stage-appropriate way (AGENTS "Dose sweeps": change in any direction, plus coherence and held-out Base loss where available), **not** our character score.
4. Coherence gate for Δ_docs_anch: read its fixed panel and flags against plain Δ_docs. If loops or language flags are well above plain, use the pre-agreed fallback base, anchored Const ×2 alone, and label it as a different recipe. Then train `Δsft_rewr_eos|docs_anch` on θ_B + that base (same config) and evaluate it at ×½ and ×1 and + P64 ×1.
5. Optional, last: cg_exp_curve's (c), O-LoRA-style orthogonal chat training. Run it only if cg_exp_curve has sent tested code and commands **and** projected spend stays under $65. Otherwise skip it and record why.
6. Destroy the box and confirm through the API that it is gone. Write a cost receipt.

If the projected spend exceeds $65, drop cells in this order and tell const_v2: (c), P128, new D + P64 ×1.25, old-D second sample.

## Analysis and reading (use Sol subagents for reads)

- Compare at matched character. Interpolate between new-D ½ and 1, and state that you did. Count maths on answers that **finish in both** models as well as the raw /60. Use paired intervals (`scripts/eval/43_paired_ablation.py`).
- For every new chat cell, read the fixed panel and the payday-loan, fridge (`task_agent`) and spin-email (`task_email`) items, plus preselected v2 next-action and instruction items. Choose those before reading and record how you chose them. Add every cell to `scripts/eval/52_answer_panel.py` PANELS with its graft equation, regenerate, and write `reading_notes.md`.
- Name every model by its graft equation, a plain description and its model id.
- Output `slop/eval/run16_v2/results.md` in the Review-preview layout, plus an audit in `slop/audits/`, a journal entry (/arj style) and an independent fresh-eyes review (a different model family from the writer). Commit scoped paths on the branch, sign your work, and don't push. Then send const_v2 a FINAL handoff with the branch, commits, results path, cost and anything not done.

## Failure modes to check

- The projection's run-14 gain was only finishing answers. If new D stops cutting off, the gain may vanish; say so plainly.
- A variant looks better only because it changes less: always compare at matched character.
- The retrain differs in more than the EOS tokens: check the config diff and data hash.
- The anchored base is weaker, so its chat adapter looks cleaner only because it changes less: compare at matched character.
- Never train character on Instruct, never put loss on empty think blocks, and evaluate with thinking off.

Report to const_v2 (intercom) at each milestone: rental started, new D trained, each block of cells evaluated, gate decision, final. Investigate a failure before you retry; tell const_v2 before spending beyond plan.
