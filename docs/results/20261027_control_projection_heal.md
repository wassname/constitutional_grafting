# Controls, projection and thinking-mode heal (round 14)

PI/Claude (opus), 2026-10-27, summarising runs 14 and 15 for wassname. Notation: AGENTS.md graft shorthand. D = `θ_I + Δ_docs + 1·Δsft_rewr|docs`, the reference recipe.

## Does removing learned instruction-following reduce damage at the same character? (thinking off)

| Graft | Character [90%] | Maths /60 (finished) | Small tasks /22 | Stopping |
|:--|--:|--:|--:|:--|
| D ×1 | +0.89 [+0.75, +1.03] | 55 | 19 | normal |
| D ×½ (reference at matched character) | +0.75 [+0.62, +0.89] | 53 | 18 | 3/214 cutoffs |
| **Projection k64 ×1** `θ_I + Δ_docs + 1·P₆₄(Δsft_rewr\|docs)` | +0.73 [+0.59, +0.87] | **57** | **21** | 1 loop, 2 cutoffs |
| Projection k16 ×1 | +0.81 [+0.67, +0.95] | 55 | 21 | 1 loop |
| Generic control subtracted ×½ `… − ½·Δsft_ctlgen\|docs` | +0.67 [+0.46, +0.87] | 48 (44) | 20 | 6 loops, 20 cutoffs |
| Generic control subtracted ×1 | −1.51 [−1.71, −1.28] | 32 (2) | 11 | collapsed |

Bottom line: subtracting a generic-prompt instruction-following control does not help; at matched character it loses about 5 maths answers and adds stopping faults, and at full strength the model collapses. The projection (erase the top-64 singular directions of Instruct − Base from the chat update, which removes 15% of its energy) matches D ×½ on character (paired −0.02 [−0.10, +0.07]) and finishes 4 more maths answers (paired +4 [+1, +7]) and 3 more small tasks; all 4 extra maths answers are ones D ×½ cut off, so this is a gain in finishing, not shown to be better reasoning. Read answers keep every D decision on payday loan, fridge log and spin email (`slop/eval/answer_panel/reading_notes_run14.md`). One sample per model: a candidate to confirm, not a winner. Source: `slop/eval/run14_box_a/results.md`, audit `slop/audits/20261026_run14_comparison.md`.

Confound for every chat-control result: D's chat data trains `<|im_end|>` on only 733 of 1,636 targets; the generic control on all (journal "Most rewritten chat targets were trained without an end-of-turn token").

## Does a cheap heal restore thinking mode without losing character?

| Model | Thinking on: blank finals /214 | Thinking on: character [90%] | Thinking off: character | Maths on / off |
|:--|--:|--:|--:|:--|
| Instruct | 0 | 0 (reference) | 0 (reference) | 56 / 54 |
| D | 183 | −1.84 [−1.95, −1.71] | +0.84 | 54 / 56 |
| D + traces-only heal | 38 | −0.32 [−0.54, −0.11] | +0.58 (−0.27 [−0.37, −0.16] vs D) | 56 / 53 |
| D + mixed heal (traces + D's own answers) | 176 | −1.77 [−1.89, −1.62] | +0.88 (+0.04 [−0.06, +0.16] vs D) | 58 / 52 |

Bottom line: no. The traces-only heal makes most answers visible but costs about a third of D's thinking-off character, with fluent regressions as well as more loops; the mixed heal keeps the character but leaves thinking mode broken. Keep serving with thinking off. Source: `slop/eval/run15_heal/results.md`, audit `slop/audits/20261027_run15_final_heals.md`.

## What I checked

PI/Claude read payday, fridge and spin-email answers for projection k64 and D ×½ in full; the run-14 and run-15 workers read all fixed panels and selected answers, and fresh independent Astra/Fable reviews accepted both reports with notes. Not checked: repeatability (one sample per model), the expanded tiny-char v2 eval (draft, unreviewed), equal-compute thinking-on vs thinking-off comparisons.
