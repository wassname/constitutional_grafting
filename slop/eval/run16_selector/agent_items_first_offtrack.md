| Model | Fridge (2 turns) s0, s1 | Console (3 turns) s0, s1 | 2-sentence rule (turns 2-3) s0, s1 | Share of turns before first slip |
|:--|:--|:--|:--|--:|
| Instruct (16) | slip at 1, slip at 1 | ✓, slip at 1 | ✓, ✓ | 0.50 |
| docs only (Δ_docs) (16) | ✓, ✓ | slip at 2, slip at 1 | ✓, ✓ | 0.64 |
| web control: anchored docs only (16) | ✓, ✓ | ✓, ✓ | ✓, ✓ | 1.00 |
| new D ×½ (16) | slip at 2, ✓ | ✓, ✓ | ✓, ✓ | 0.93 |
| new D ×1 (recipe) (16) | slip at 1, slip at 1 | ✓, ✓ | slip at 2, slip at 2 | 0.43 |
| web control: anchored docs + chat ×½ (16) | slip at 2, slip at 2 | ✓, slip at 2 | ✓, ✓ | 0.71 |
| web control: anchored docs + chat ×1 (16) | ✓, slip at 1 | ✓, ✓ | slip at 2, slip at 2 | 0.57 |
| web control + P₆₄ ×1 (16) | ✓, ✓ | ✓, ✓ | slip at 2, slip at 3 | 0.79 |
| P₆₄ two-sided ×1 (16) | slip at 1, slip at 1 | ✓, ✓ | ✓, ✓ | 0.71 |
| P₆₄ two-sided ×1.25 (16) | slip at 1, slip at 2 | ✓, ✓ | slip at 2, slip at 2 | 0.50 |
| P₁₂₈ two-sided ×1 (16) | ✓, ✓ | ✓, ✓ | ✓, ✓ | 1.00 |
| P₆₄ output side ×1 (16) | slip at 2, slip at 1 | ✓, ✓ | slip at 2, slip at 2 | 0.50 |
| project-4% (char/cap) ×1 (16) | ✓, slip at 1 | ✓, slip at 1 | slip at 3, slip at 2 | 0.43 |
| old D ×½ (no EOS fix) (16) | ✓, ✓ | slip at 1, ✓ | ✓, ✓ | 0.79 |
| old D + P₆₄ ×1 (16) | slip at 1, slip at 2 | ✓, ✓ | slip at 2, slip at 3 | 0.57 |
| old D ×1 (run 10) (10) | ✓, ✓ | ✓, ✓ | —, — | 1.00 |
| old D ×½ (run 14) (14) | ✓, ✓ | slip at 1, ✓ | —, — | 0.70 |
| old D + P₆₄ ×1 (run 14) (14) | slip at 1, ✓ | ✓, ✓ | —, — | 0.80 |
| chat control: old D − ¼ ctl (run 14) (14) | slip at 2, slip at 1 | slip at 2, ✓ | —, — | 0.50 |
| chat control: old D − ½ ctl (run 14) (14) | ✓, ✓ | ✓, ✓ | —, — | 1.00 |
| chat control: old D − 1 ctl (run 14) (14) | slip at 1, ✓ | ✓, slip at 1 | —, — | 0.50 |
| chat control adapter alone (run 14) (14) | slip at 1, slip at 1 | slip at 1, slip at 1 | —, — | 0.00 |
