# Saved-update estimates

PI/OpenAI. Pinned both-order Jev change scores versus fresh Instruct, including existing code-based broken-reply penalties. Samples averaged within item before 90% item-bootstrap intervals. Full and shared-subset scores are separate comparisons. These intervals do not measure semantic judge error, training-seed variation or repeatability of selected T0 demos.

## Full snapshot

| SFT, documents   | Character change↑   | Capability loss↓      | Character items   |
|:-----------------|:--------------------|:----------------------|:------------------|
| *Instruct (0,0)* | *reference*         | *0.0*                 | *reference*       |
| (1, 1)           | +1.1 [+0.9, +1.2]   | +22.7 [+4.5, +45.5]   | 59                |
| (1, 0)           | +0.7 [+0.6, +0.8]   | +9.1 [-0.0, +27.3]    | 59                |
| (0.5, 0)         | +0.5 [+0.4, +0.6]   | +9.1 [-0.0, +27.3]    | 59                |
| (0, 1)           | +0.3 [+0.2, +0.4]   | +4.5 [-0.0, +13.6]    | 59                |
| (0, 2)           | -0.1 [-0.4, +0.2]   | +9.1 [-0.0, +18.2]    | 59                |
| (2, 0)           | -0.7 [-0.9, -0.4]   | +63.6 [+45.5, +81.8]  | 59                |
| (2, 2)           | -1.9 [-2.0, -1.9]   | +95.5 [+86.4, +100.0] | 59                |

## Shared boundary subset

| SFT, documents   | Character change↑   | Capability loss↓      | Character items   |
|:-----------------|:--------------------|:----------------------|:------------------|
| *Instruct (0,0)* | *reference*         | *0.0*                 | *reference*       |
| (1, 1)           | +1.2 [+0.7, +1.6]   | +22.7 [+4.5, +45.5]   | 9                 |
| (1, 0)           | +0.8 [+0.5, +1.1]   | +9.1 [-0.0, +27.3]    | 9                 |
| (0.5, 0)         | +0.6 [+0.3, +0.9]   | +9.1 [-0.0, +27.3]    | 9                 |
| (0, 2)           | +0.4 [-0.1, +0.9]   | +9.1 [-0.0, +18.2]    | 9                 |
| (0, 1)           | +0.3 [-0.0, +0.6]   | +4.5 [-0.0, +13.6]    | 9                 |
| (2, 0)           | -0.7 [-1.3, -0.0]   | +63.6 [+45.5, +81.8]  | 9                 |
| (2, 2)           | -1.9 [-2.0, -1.6]   | +95.5 [+86.4, +100.0] | 9                 |
| (0, 4)           | -2.0 [-2.0, -2.0]   | +90.9 [+72.7, +100.0] | 9                 |

## Separate frozen long60 maths

Frozen long60, T0 final-answer exact match; paired 90% item-bootstrap delta versus fresh Instruct. Sensitivity excludes only indices 3 and 26, identified from baseline mismatches before intervention maths reads. No annotation correction or other exclusion. Not training-seed or serving-repeat uncertainty.

| SFT, documents   | Exact matches↑   | Change vs Instruct (pp)↑   | Cap hits↓   | Sensitivity matches↑   |
|:-----------------|:-----------------|:---------------------------|:------------|:-----------------------|
| (0.5, 0)         | 58/60            | +8.3 [+3.3, +15.0]         | 0           | 58/58                  |
| (0, 1)           | 56/60            | +5.0 [+0.0, +11.7]         | 1           | 56/58                  |
| (0, 0)           | 53/60            | +0.0 [+0.0, +0.0]          | 3           | 53/58                  |
| (1, 0)           | 52/60            | -1.7 [-8.3, +5.0]          | 0           | 52/58                  |
| (0, 2)           | 50/60            | -5.0 [-11.7, +1.7]         | 4           | 50/58                  |
| (1, 1)           | 42/60            | -18.3 [-28.3, -8.3]        | 0           | 42/58                  |
| (2, 0)           | 16/60            | -61.7 [-71.7, -51.7]       | 11          | 16/58                  |
| (2, 2)           | 0/60             | -88.3 [-95.0, -81.7]       | 59          | 0/58                   |

Completed generation cells awaiting judging: none.
