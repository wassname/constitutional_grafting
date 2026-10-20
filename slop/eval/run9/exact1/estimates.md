# Exact subset-graft comparison

PI/Sol.

Requested grid: 15/22 generated and downloaded; 15/22 graded. Same-host untouched control: complete.

New same-host comparison, separate from the earlier norm-matched diagnostics. Character numbers are pinned Jev preferences, not validated wisdom measurements; 59 items ×2 generations, 90% item-bootstrap intervals. Maths is the same60 long GSM8K questions, temperature0,1500tokens. Original bounded-budget answers stay unchanged. Answer-now adds one256-token continuation only on a cutoff, with thinking off; it is a separate extra-compute diagnostic. Completed-answer counts are in estimates.json; full calls are in per-model maths and trace files. Exact final-number matching does not certify the reasoning. Tasks:11 ordinary checks ×2. No extra character SFT. Heals use personally read own-verified GSM8K train answers and16trainer steps; fp16 gradient scaling can skip optimizer updates, so this is not a guarantee of16learned updates (see audit.md). Frozen parent and merge fp16; mixed-precision training with float32 LoRA tensors.

| Documents / dose         |       Judge change↑ |   Maths bounded↑ |   Maths answer-now↑ |   Tasks↑ |   Panel cap hits↓ | Status                       |
|:-------------------------|--------------------:|-----------------:|--------------------:|---------:|------------------:|:-----------------------------|
| Untouched Instruct       |           reference |            55/60 |               57/60 |    22/22 |               1/7 | graded                       |
| Echo ×1                  | +0.11 [+0.02,+0.20] |            55/60 |               57/60 |    21/22 |               1/7 | graded                       |
| Echo ×2                  | +0.24 [+0.14,+0.36] |            55/60 |               56/60 |    20/22 |               0/7 | graded                       |
| Echo ×4                  | +0.35 [+0.22,+0.49] |            55/60 |               55/60 |    21/22 |               0/7 | graded                       |
| Echo ×8                  | -0.84 [-1.03,-0.64] |             0/60 |                0/60 |     6/22 |               5/7 | graded                       |
| Stoic ×1                 | -0.00 [-0.06,+0.06] |            56/60 |               57/60 |    21/22 |               0/7 | graded                       |
| Stoic ×2                 | -0.00 [-0.04,+0.04] |            54/60 |               56/60 |    22/22 |               0/7 | graded                       |
| Stoic ×4                 | -0.08 [-0.14,-0.02] |            55/60 |               55/60 |    21/22 |               0/7 | graded                       |
| Stoic ×8                 | -0.13 [-0.22,-0.05] |            54/60 |               54/60 |    20/22 |               1/7 | graded                       |
| Opus ×1                  | +0.10 [+0.03,+0.17] |            54/60 |               56/60 |    22/22 |               0/7 | graded                       |
| Opus ×2                  | +0.12 [+0.04,+0.21] |            56/60 |               57/60 |    22/22 |               0/7 | graded                       |
| Opus ×4                  | +0.25 [+0.14,+0.38] |            55/60 |               56/60 |    18/22 |               0/7 | graded                       |
| Opus ×8                  | -0.22 [-0.39,-0.06] |            38/60 |               38/60 |    18/22 |               0/7 | graded                       |
| Greek ×1                 |             pending |                — |                   — |        — |                 — | awaiting generation/download |
| Greek ×2                 |             pending |                — |                   — |        — |                 — | awaiting generation/download |
| Greek ×4                 |             pending |                — |                   — |        — |                 — | awaiting generation/download |
| Greek ×8                 |             pending |                — |                   — |        — |                 — | awaiting generation/download |
| Echo ×1 + maths heal     | +0.16 [+0.07,+0.26] |            54/60 |               55/60 |    20/22 |               0/7 | graded                       |
| Stoic ×1 + maths heal    | -0.04 [-0.09,+0.02] |            56/60 |               57/60 |    22/22 |               0/7 | graded                       |
| Opus ×1 + maths heal     | +0.09 [+0.03,+0.15] |            55/60 |               56/60 |    22/22 |               0/7 | graded                       |
| Greek ×1 + maths heal    |             pending |                — |                   — |        — |                 — | awaiting generation/download |
| All four ×1              |             pending |                — |                   — |        — |                 — | awaiting generation/download |
| All four ×1 + maths heal |             pending |                — |                   — |        — |                 — | awaiting generation/download |

Striking character, desirable judgement and ordinary usefulness must be checked separately in the replies. The limited completed blind review is not a blind verdict on this fixed panel. Human-readable synthesis and recommendation follow personal checks; pending scores are not zero.

