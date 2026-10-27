# Run 16 draft: best-practice setup on tiny-char v2 (batched retrain, with and without projection)

PI/Claude (opus), 2026-10-27. DRAFT: no paid work until wassname says go and signs off tiny-char v2 (sha256 5ea2684b…, 196 items). One Vast lease, about $40–50, within the round's $100 (about $45 spent).

wassname (2026-10-27): "well obs fix in code! but we might batch multiple changes to retrain"; "try our best setup on that! and our best setup seems to have projection"; "we can eval with and without it in the next v2 best practices run" (spelling corrected).

## Batched changes in the retrained chat adapter

1. End-of-turn fix: chat targets from `data/train/eos_fixed/chatr12.jsonl` (3cf11e72); the builder now enforces it (e2d4363d).
2. Optional, needs wassname's yes: train the chat adapter on the anchored document base (document stage with the generic-web control subtracted), which plausibly (~70%) beats plain documents at matched effect.

Each extra batched change costs a second chat training (about $8–10) if we want to tell its effect apart from the EOS fix. Without it, the run measures "new best setup vs old D", not each change.

## Cells (all thinking off, tiny-char v2 + GSM60 + small tasks, fixed T0 demo panel, answer panel per question)

| # | Model (AGENTS shorthand) | Question |
|:--|:--|:--|
| 1 | `θ_I + Δ_docs + c·Δsft_rewr_eos\|docs`, c = ½, 1 | new D, dose bracket |
| 2 | `θ_I + Δ_docs + c·P₆₄(Δsft_rewr_eos\|docs)`, c = 1, 1.25 | projection on new D |
| 3 | `θ_I + Δ_docs + 1·P₁₂₈(Δsft_rewr_eos\|docs)` | larger k |
| 4 | old D ×½, old D + P₆₄ ×1 | link to run 14; second sample |
| 5 | document stage: Const ×1, ×2, plain and anchored; Instruct | document-control question on v2 |
| 6 (if batched change 2) | `θ_I + Δ_docs_anch + c·Δsft_rewr_eos\|docs_anch`, ± P₆₄ | anchored best setup |

## Pass/fail

- Projection: at matched character (between new-D doses ½ and 1) it loses fewer maths/small-task answers, counted on answers that finish in both models, and read replies keep the payday, fridge and email decisions.
- Subtle failure: new D stops cutting off, so the projection's finishing gain disappears; that would mean the run-14 gain was the EOS bug.
- Document stage: compared at matched change on v2 with replies read, not by our character score.

Destroy the lease after the last evaluation.
