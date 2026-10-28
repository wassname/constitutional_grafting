# Document gate brief — supervisor decision only

Signed PI/OpenAI (Sol), 2026-10-27. No approval is written by this package.

Full fixed panels: [panels.md](panels.md). Full machine-flag context: [flagged_context.md](flagged_context.md). [Flags](flags.json), [scoped reading notes](reading_notes.md).

Document stage seeks striking coherent change in ANY moral/persona direction, not target-character score. All machine flags need contextual reading. The two candidate mixtures have fully read 26-record preselected/fixed packets; other model packets and full corpora are not claimed read.

| Model | GSM /60 | Tasks /22 | Capability /38 | Loops / cuts / language / role / empty (496 turns) |

|:--|--:|--:|--:|:--|

| `r16_instruct` | 55 | 22 | 31.75 | 0/6/1/0/0 |

| `r16_stoic0.5_const1_other1` | 54 | 21 | 31 | 0/6/8/0/0 |

| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1` | 54 | 22 | 30 | 0/5/1/0/0 |

| `r16_const1` | 56 | 22 | 30 | 0/5/2/0/0 |

| `r16_const2` | 52 | 20 | 30 | 3/44/66/2/0 |

| `r16_mix_const2_ctl-2` | 52 | 20 | 34 | 0/30/0/0/0 |



## Both-finished GSM versus Instruct

| Model | Common n | Model correct | Instruct correct |

|:--|--:|--:|--:|

| `r16_stoic0.5_const1_other1` | 55 | 53 | 53 |

| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1` | 56 | 52 | 54 |

| `r16_const1` | 57 | 55 | 55 |

| `r16_const2` | 56 | 50 | 54 |

| `r16_mix_const2_ctl-2` | 54 | 50 | 52 |



## Base held-out loss

The live copied source is ../lease/box_runs/base_loss.jsonl. Wait for anchored_gate_ready before treating its six configurations as complete.



Plain versus anchored mixtures share major T0 decisions, including species self-ending under alien pressure; baseline instead attempts a fanciful third way. The preselected haircut-review choice flips in both samples between those mixtures. Neither documents-only identity becomes Musonius, which is not itself a document-stage selection criterion. Further details and defects are in the reading notes.


## Completed Base held-out losses (same capped held-out sets)

| Config | Const NLL | Other NLL | Stoic NLL | Web NLL |
|:--|--:|--:|--:|--:|
| `base` | 2.51917 | 2.25397 | 2.40596 | 2.02311 |
| `r16_stoic0.5_const1_other1` | 2.31612 | 2.13786 | 2.40919 | 2.05560 |
| `r16_mix_stoic0.5_ctl-0.5_mix_const1_ctl-1_other1` | 2.30363 | 2.10660 | 2.37879 | 2.02849 |
| `r16_const1` | 2.28105 | 2.27198 | 2.41867 | 2.04129 |
| `r16_const2` | 2.59223 | 2.46541 | 2.61604 | 2.27715 |
| `r16_mix_const2_ctl-2` | 2.52290 | 2.37880 | 2.53633 | 2.10206 |

All6 configurations are complete; see ../anchored_gate_ready.json. Loss measures learning/style on Base, not preferred character.
