# Saved-update estimates

PI/OpenAI. Both-order Jev change scores versus fresh Instruct. Samples averaged within item before 90% item-bootstrap intervals. Full and shared-subset scores are separate comparisons. These intervals do not measure semantic judge error, training-seed variation or repeatability of selected T0 demos.

## Full snapshot

| SFT, documents   | Character change↑   | Capability loss↓    | Character items   |
|:-----------------|:--------------------|:--------------------|:------------------|
| *Instruct (0,0)* | *reference*         | *0.0*               | *reference*       |
| (1, 1)           | +1.1 [+0.9, +1.2]   | +22.7 [+4.5, +45.5] | 59                |
| (1, 0)           | +0.7 [+0.6, +0.8]   | +9.1 [-0.0, +27.3]  | 59                |
| (0, 1)           | +0.3 [+0.2, +0.4]   | +4.5 [-0.0, +13.6]  | 59                |
| (0, 2)           | not run             | not run             | —                 |
| (2, 0)           | not run             | not run             | —                 |
| (2, 2)           | not run             | not run             | —                 |

## Shared boundary subset

| SFT, documents   | Character change↑   | Capability loss↓    | Character items   |
|:-----------------|:--------------------|:--------------------|:------------------|
| *Instruct (0,0)* | *reference*         | *0.0*               | *reference*       |
| (1, 1)           | +1.2 [+0.7, +1.6]   | +22.7 [+4.5, +45.5] | 9                 |
| (1, 0)           | +0.8 [+0.5, +1.1]   | +9.1 [-0.0, +27.3]  | 9                 |
| (0, 1)           | +0.3 [-0.0, +0.6]   | +4.5 [-0.0, +13.6]  | 9                 |

Completed generation cells awaiting judging: none.
