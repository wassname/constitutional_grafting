# Document graft dose checks

PI/OpenAI. Rows follow the requested adapter/dose order, not a winner ranking. Change includes corruption.
Language-switch, loop and cutoff counts use the existing pinned checks on all sampled turns; counts overlap.
Full flags, including role confusion and empty replies, with source hashes: [solo_document_table.coherence.json](solo_document_table.coherence.json).
These checks do not replace reading moral reasoning and conduct. Maths is an auxiliary capability check.
Base loss is measured on Base, not Instruct; negative means better text prediction, not better character.

| Adapter × dose                                                                         |    Change [90%] |   Language / loops / cutoffs↓ |   Turns |   Base loss Δ↓, own / web |   Maths↑ /60 |   "One line" words | Read outcome   |
|:---------------------------------------------------------------------------------------|----------------:|------------------------------:|--------:|--------------------------:|-------------:|-------------------:|:---------------|
| *[Instruct](../run8/box_runs/replies_r8_a0_b0.jsonl)*                                  |         not run |                     1 / 0 / 4 |     214 |                         – |           53 |                 29 |                |
| [Mixed Stoic ×1](lease1/box_runs/replies_r10_x11_mix_stoic1.jsonl)                     |    49% [41, 56] |                     0 / 0 / 4 |     214 |   -0.108 (stoic) / -0.009 |           55 |                 36 |                |
| [Mixed Stoic ×2](lease1/box_runs/replies_r10_x11_mix_stoic2.jsonl)                     |    64% [57, 71] |                   103 / 2 / 8 |     214 |   -0.024 (stoic) / +0.085 |           54 |                 47 |                |
| [Mixed Stoic ×4](lease1/box_runs/replies_r10_x11_mix_stoic4.jsonl)                     | 100% [100, 100] |                197 / 45 / 102 |     214 |   +0.399 (stoic) / +0.475 |           33 |                 50 |                |
| [Anchored Stoic ×1](lease1/box_runs/replies_r10_x11_mix_stoic1_x11_replay_ctl-1.jsonl) |    50% [43, 56] |                     0 / 0 / 4 |     214 |   -0.107 (stoic) / +0.001 |           56 |                325 |                |
| [Anchored Stoic ×2](lease1/box_runs/replies_r10_x11_mix_stoic2_x11_replay_ctl-2.jsonl) |    41% [34, 47] |                     0 / 0 / 3 |     214 |   -0.064 (stoic) / +0.007 |           55 |                 33 |                |
| [Anchored Stoic ×4](lease1/box_runs/replies_r10_x11_mix_stoic4_x11_replay_ctl-4.jsonl) |    56% [48, 64] |                     0 / 1 / 5 |     214 |   +0.184 (stoic) / +0.049 |           55 |                 38 |                |
| [Mixed Const ×1](lease1/box_runs/replies_r10_x11_mix_const1.jsonl)                     |    57% [50, 64] |                     0 / 0 / 2 |     214 |   -0.222 (const) / -0.009 |           55 |                 48 |                |
| [Mixed Const ×2](lease1/box_runs/replies_r10_x11_mix_const2.jsonl)                     |    91% [86, 95] |                 163 / 16 / 38 |     214 |   +0.099 (const) / +0.122 |           52 |                 91 |                |
| [Anchored Const ×1](lease1/box_runs/replies_r10_x11_mix_const1_x11_replay_ctl-1.jsonl) |    56% [49, 64] |                     1 / 0 / 4 |     214 |   -0.226 (const) / -0.001 |           56 |                 58 |                |
| [Anchored Const ×2](lease1/box_runs/replies_r10_x11_mix_const2_x11_replay_ctl-2.jsonl) |    81% [74, 87] |                     0 / 0 / 4 |     214 |   +0.004 (const) / +0.079 |           52 |                 62 |                |
| [Stoic ×1](../run10/stage1/box_runs/replies_r10_stoic1.jsonl)                          |    52% [45, 59] |                     1 / 0 / 4 |     214 |   -0.109 (stoic) / +0.003 |           56 |                 49 |                |
| [Stoic ×2](../run10/stage1/box_runs/replies_r10_stoic2.jsonl)                          |    49% [42, 55] |                     3 / 0 / 3 |     214 |   -0.036 (stoic) / +0.021 |           55 |                 36 |                |
| [Stoic ×3](lease1/box_runs/replies_r10_stoic3.jsonl)                                   |    76% [69, 82] |                 108 / 12 / 19 |     214 |   +0.184 (stoic) / +0.093 |           57 |                 28 |                |
| [Stoic ×4](../run10/stage1/box_runs/replies_r10_stoic4.jsonl)                          |    93% [89, 96] |                 173 / 68 / 86 |     214 |   +0.426 (stoic) / +0.299 |           49 |               1048 |                |
| [Stoic ×8](../run10/stage1/box_runs/replies_r10_stoic8.jsonl)                          |   99% [96, 100] |               173 / 100 / 113 |     214 |   +1.825 (stoic) / +1.335 |            0 |                 40 |                |
| [Other ×2](../run10/stage1/box_runs/replies_r10_other2.jsonl)                          |    50% [43, 57] |                     0 / 0 / 4 |     214 |   -0.080 (other) / +0.017 |           53 |                 34 |                |
| [Const ×1](../run10/stage6/box_runs/replies_r10_const1.jsonl)                          |    51% [44, 59] |                     1 / 0 / 4 |     214 |   -0.238 (const) / +0.018 |           56 |                 48 |                |
| [Const ×2](lease1/box_runs/replies_r10_const2.jsonl)                                   |    91% [87, 95] |                   47 / 0 / 11 |     214 |   +0.073 (const) / +0.254 |           50 |                136 |                |
| [Const ×3](lease1/box_runs/replies_r10_const3.jsonl)                                   |   99% [98, 100] |               121 / 109 / 212 |     214 |   +0.972 (const) / +1.007 |            0 |               1284 |                |
| [Const ×4](lease1/box_runs/replies_r10_const4.jsonl)                                   | 100% [100, 100] |                23 / 186 / 214 |     214 |   +2.050 (const) / +1.984 |            0 |               1375 |                |
| [Other ×4](lease1/box_runs/replies_r10_other4.jsonl)                                   |    68% [61, 74] |                    24 / 1 / 6 |     214 |   +0.498 (other) / +0.101 |           54 |                 23 |                |
