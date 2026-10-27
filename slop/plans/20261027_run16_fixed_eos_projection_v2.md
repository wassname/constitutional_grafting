# Run 16 draft: fixed-EOS retrain, projection confirmation, document stage on v2

PI/Claude (opus), 2026-10-27. DRAFT: no paid work until wassname says go. One Vast lease, about $35–40, within the round's $100 (about $45 spent).

Questions:
1. Does the projection k64 still help once D's chat adapter has been trained with end-of-turn tokens?
2. Is the run-14 projection gain repeatable on a second sample?
3. At matched effect, is the document-stage generic-web control (anchored) better than plain Const? Measured on tiny-char v2. Needs wassname to sign off v2 (sha256 5ea2684b…, 196 items).

## Cells

| # | Model (AGENTS shorthand) | Why |
|:--|:--|:--|
| 1 | train `Δsft_rewr\|docs` on `θ_B + Δ_docs` with `data/train/eos_fixed/chatr12.jsonl` | fixed D; same recipe and hyperparameters as run 10, only the EOS change |
| 2 | `θ_I + Δ_docs + ½·Δsft_rewr_eos\|docs`, and ×1 | fixed-D dose bracket |
| 3 | `θ_I + Δ_docs + 1·P₆₄(Δsft_rewr_eos\|docs)` | Q1 |
| 4 | old D ×½ and old k64 ×1, second sample | Q2 |
| 5 | document stage on v2: Const ×1, ×2 plain and anchored, Stoic, Other, Instruct | Q3; the run-10 document adapters, no training |

All cells run thinking off, on v2 items (if signed off), GSM60 and the small tasks. Fixed T0 demo panel. Answer panel per question.

## Pass/fail

- Q1: fixed k64 matches the fixed-D character (interpolated between ×½ and ×1) and loses fewer maths/small-task answers. Its read replies keep the payday, fridge and email decisions.
- Subtle failure: the fixed-D cutoffs disappear, so the projection's finishing gain was only the missing EOS. A real gain must show up in answers that finish in both models.
- Q2: second-sample paired maths difference keeps the same sign as run 14 (+4).
- Q3: compared at matched change on v2 (not by our character score), with replies read. Plain Const ×2 broke on 1 of 5 dilemmas in the run-10 read (`slop/eval/answer_panel/reading_notes_docs.md`).

## Order

Train cell 1 first. Run cells 4 and 5 during training, if the box can serve and train at the same time; otherwise run them after cells 2–3. Destroy the lease after the last evaluation.
