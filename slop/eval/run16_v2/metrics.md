| Model | Character [90%] | Maths /60 | Run8 tasks /22 | V2 capability /38 | Draft code /40 | Draft tools /32 | Flags loop/cutoff/language |
|:--|--:|--:|--:|--:|--:|--:|:--|
| `r16_instruct` | +0.000 (ref) | 55 | 22 | 31.75 | 18.0 | 28.0 | 0/6/1 over 496 turns |
| `r16_stoic0.5_const1_other1_eos_chatr120.5` | +0.619 [+0.557, +0.679] | 55 | 21 | 31 | 17.0 | 28.0 | 0/2/0 over 496 turns |
| `r16_stoic0.5_const1_other1_eos_chatr121` | +0.832 [+0.760, +0.904] | 56 | 20 | 32.6 | 18.0 | 28.0 | 2/1/1 over 496 turns |
| `r16_stoic0.5_const1_other1_p16_641` | +0.700 [+0.627, +0.769] | 55 | 21 | 34 | 17.0 | 27.0 | 0/1/0 over 496 turns |
| `r16_stoic0.5_const1_other1_p16_641.25` | +0.802 [+0.731, +0.871] | 56 | 21 | 32.55 | 16.0 | 28.0 | 0/0/0 over 496 turns |
| `r16_stoic0.5_const1_other1_p16_1281` | +0.641 [+0.574, +0.707] | 56 | 22 | 34 | 18.0 | 27.0 | 0/0/1 over 496 turns |
| `r16_stoic0.5_const1_other1_p16out_641` | +0.813 [+0.741, +0.887] | 56 | 20 | 33.55 | 18.0 | 28.0 | 0/0/2 over 496 turns |
| `r16_stoic0.5_const1_other1_charcap1` | +0.820 [+0.747, +0.888] | 53 | 21 | 36.4 | 17.0 | 28.0 | 0/0/1 over 496 turns |
| `r16_stoic0.5_const1_other1_rewr0.5` | +0.622 [+0.558, +0.683] | 55 | 18 | 34 | 17.0 | 28.0 | 0/3/0 over 496 turns |
| `r16_stoic0.5_const1_other1_oldp641` | +0.684 [+0.617, +0.753] | 54 | 20 | 32.75 | 16.0 | 28.0 | 0/2/0 over 496 turns |
| `r16_stoic0.5_const1_other1` | not measured | 54 | 21 | 31 | 18.0 | 29.0 | 0/6/8 over 496 turns |
| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1` | not measured | 54 | 22 | 30 | 17.0 | 28.0 | 0/5/1 over 496 turns |
| `r16_const1` | not measured | 56 | 22 | 30 | 18.0 | 29.0 | 0/5/2 over 496 turns |
| `r16_const2` | not measured | 52 | 20 | 30 | 16.0 | 29.0 | 3/44/66 over 496 turns |
| `r16_mix_const2_ctl-2` | not measured | 52 | 20 | 34 | 14.0 | 29.0 | 0/30/0 over 496 turns |
| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1_anch_chatr120.5` | +0.651 [+0.584, +0.715] | 53 | 21 | 32.8 | 16.0 | 28.0 | 0/1/0 over 496 turns |
| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1_anch_chatr121` | +0.854 [+0.784, +0.919] | 54 | 20 | 33.35 | 19.0 | 28.0 | 0/0/0 over 496 turns |
| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1_anchp_641` | +0.692 [+0.624, +0.762] | 53 | 22 | 30.8 | 18.0 | 28.0 | 0/1/1 over 496 turns |

## GSM: same questions where both model and Instruct finished
Each row has its own common denominator. Counts and intervals are paired; this is separate from the full /60 score above.
| Model | Both finished n | Model correct | Instruct correct | Model minus Instruct [90% count interval] |
|:--|--:|--:|--:|:--|
| `r16_stoic0.5_const1_other1_eos_chatr120.5` | 56 | 54 | 54 | +0 [-2.00, +2.00] |
| `r16_stoic0.5_const1_other1_eos_chatr121` | 57 | 54 | 55 | -1 [-4.00, +2.00] |
| `r16_stoic0.5_const1_other1_p16_641` | 56 | 54 | 54 | +0 [-2.00, +2.00] |
| `r16_stoic0.5_const1_other1_p16_641.25` | 57 | 54 | 55 | -1 [-4.00, +2.00] |
| `r16_stoic0.5_const1_other1_p16_1281` | 57 | 54 | 55 | -1 [-4.00, +2.00] |
| `r16_stoic0.5_const1_other1_p16out_641` | 57 | 54 | 55 | -1 [-4.00, +2.00] |
| `r16_stoic0.5_const1_other1_charcap1` | 55 | 52 | 53 | -1 [-4.00, +2.00] |
| `r16_stoic0.5_const1_other1_rewr0.5` | 56 | 54 | 54 | +0 [-2.00, +2.00] |
| `r16_stoic0.5_const1_other1_oldp641` | 57 | 54 | 55 | -1 [-4.00, +2.00] |
| `r16_stoic0.5_const1_other1` | 55 | 53 | 53 | +0 [-2.00, +2.00] |
| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1` | 56 | 52 | 54 | -2 [-5.00, -0.00] |
| `r16_const1` | 57 | 55 | 55 | +0 [-2.00, +2.00] |
| `r16_const2` | 56 | 50 | 54 | -4 [-7.00, -1.00] |
| `r16_mix_const2_ctl-2` | 54 | 50 | 52 | -2 [-6.00, +1.00] |
| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1_anch_chatr120.5` | 55 | 52 | 53 | -1 [-4.00, +2.00] |
| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1_anch_chatr121` | 57 | 52 | 55 | -3 [-7.00, -0.00] |
| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1_anchp_641` | 56 | 52 | 54 | -2 [-5.00, +1.00] |

## Read results and limitations
Aggregate character scores do not establish that every reply is acceptable. Read the scoped defects and coverage:
- [parent_read_new_D.md](parent_read_new_D.md)
- [chat_decision_audit.md](chat_decision_audit.md)
- [document_gate_result.md](document_gate_result.md)
