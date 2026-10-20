# Subset-graft results

PI/Sol.

Paid work paused at the user's request: fix cutoff handling and check the judge before more spending. Requested exact-dose/healing grid: 5/22 conditions complete. The other requested doses and all heals are not run; norm-matched cells below are extra diagnostics.

Original diagnostic grid: 17/19 generation cells downloaded; 15 graded. This page is an interim snapshot.

Character: pinned both-order Jev change vs untouched Instruct, 59 items × 2 generations; 90% item-bootstrap intervals. Maths: final-answer exact match on the same 60 long GSM8K questions, one temperature-zero generation. Tasks: 11 checks × 2 generations, including format and length. Intervals exclude judge error, training-seed and serving-repeat variation. All run-nine models use document training on Base followed by a graft onto untouched Instruct. No maths healing or extra character SFT.

### First dose (k=1)

| Documents / dose                                         |           Character↑ |   Maths↑ |   Tasks↑ |   Panel cap hits↓ |
|:---------------------------------------------------------|---------------------:|---------:|---------:|------------------:|
| [Echo ×1](#panel_escaped_starwisp-r9-echo1)              | +0.18 [+0.10, +0.26] |    55/60 |    21/22 |               0/7 |
| [Joint ×1](#panel_escaped_starwisp-r9-joint1)            | +0.14 [+0.02, +0.26] |    54/60 |    22/22 |               1/7 |
| [Opus ×1](#panel_escaped_starwisp-r9-opus1)              | +0.10 [+0.03, +0.16] |    56/60 |    22/22 |               0/7 |
| [Greek ×1](#panel_escaped_starwisp-r9-greek1)            | +0.07 [+0.02, +0.11] |    54/60 |    22/22 |               0/7 |
| [Stoic ×1](#panel_escaped_starwisp-r9-stoic1)            | -0.03 [-0.10, +0.04] |    57/60 |    20/22 |               0/7 |
| *[Untouched Instruct](#panel_escaped_starwisp-r8-a0-b0)* |            reference |    53/60 |    22/22 |               1/7 |

### Other doses

| Documents / dose                                    |           Character↑ |   Maths↑ |   Tasks↑ |   Panel cap hits↓ |
|:----------------------------------------------------|---------------------:|---------:|---------:|------------------:|
| [Echo ×1.58](#panel_escaped_starwisp-r9-echo1-58)   | +0.26 [+0.16, +0.36] |    58/60 |    19/22 |               0/7 |
| [Joint ×1.24](#panel_escaped_starwisp-r9-joint1-24) | +0.23 [+0.13, +0.32] |    54/60 |    22/22 |               1/7 |
| [Greek ×1.46](#panel_escaped_starwisp-r9-greek1-46) | +0.16 [+0.09, +0.23] |    56/60 |    21/22 |               1/7 |
| [Opus ×1.56](#panel_escaped_starwisp-r9-opus1-56)   | +0.08 [+0.02, +0.15] |    57/60 |    22/22 |               0/7 |
| [Stoic ×1.65](#panel_escaped_starwisp-r9-stoic1-65) | +0.04 [-0.02, +0.10] |    55/60 |    21/22 |               1/7 |
| [Echo ×3.16](#panel_escaped_starwisp-r9-echo3-16)   |      grading pending |    56/60 |        — |               0/7 |
| [Stoic ×3.3](#panel_escaped_starwisp-r9-stoic3-3)   |      grading pending |    52/60 |        — |               0/7 |
| [Opus ×3.11](#panel_escaped_starwisp-r9-opus3-11)   |     not run (paused) |        — |        — |                 — |
| [Greek ×2.92](#panel_escaped_starwisp-r9-greek2-92) |     not run (paused) |        — |        — |                 — |

### Mixtures (each included update at k=1)

| Documents / dose                                                 |           Character↑ |   Maths↑ |   Tasks↑ |   Panel cap hits↓ |
|:-----------------------------------------------------------------|---------------------:|---------:|---------:|------------------:|
| [Without Stoic](#panel_escaped_starwisp-r9-echo1-opus1-greek1)   | +0.34 [+0.24, +0.45] |    56/60 |    22/22 |               0/7 |
| [All four](#panel_escaped_starwisp-r9-echo1-stoic1-opus1-greek1) | +0.29 [+0.19, +0.41] |    56/60 |    20/22 |               0/7 |
| [Without Opus](#panel_escaped_starwisp-r9-echo1-stoic1-greek1)   | +0.25 [+0.15, +0.35] |    56/60 |    20/22 |               1/7 |
| [Without Greek](#panel_escaped_starwisp-r9-echo1-stoic1-opus1)   | +0.23 [+0.15, +0.32] |    55/60 |    22/22 |               0/7 |
| [Without Echo](#panel_escaped_starwisp-r9-stoic1-opus1-greek1)   | +0.14 [+0.06, +0.23] |    52/60 |    21/22 |               0/7 |

kE (the middle dose per subset) matches the old graft's weight-update norm, not capability. The largest dose is 2×kE, not k=2. Mixture removals measure contributions of trained updates, not retraining without documents. Pure Stoic differs in source and format; Opus/Greek training selections are not perfectly paired.

For maths changes, [read every changed Stoic pair](stoic_maths_changed.md). Full excerpts below retain generation-limit failures.
