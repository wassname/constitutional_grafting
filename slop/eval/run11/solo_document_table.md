# Document graft dose checks

PI/OpenAI. Rows follow the requested adapter/dose order, not a winner ranking. Change includes corruption.
Language-switch, loop and cutoff counts use the existing pinned checks on all sampled turns; counts overlap.
Full flags, including role confusion and empty replies, with source hashes: [solo_document_table.coherence.json](solo_document_table.coherence.json).
These checks do not replace reading moral reasoning and conduct. Maths is an auxiliary capability check.
Base loss is measured on Base, not Instruct; negative means better text prediction, not better character.

| Adapter × dose                                                                         |   Change [90%] |   Language / loops / cutoffs↓ |   Turns |   Base loss Δ↓, own / web |   Maths↑ /60 |   "One line" words | Read outcome   |
|:---------------------------------------------------------------------------------------|---------------:|------------------------------:|--------:|--------------------------:|-------------:|-------------------:|:---------------|
| *[Instruct](../run8/box_runs/replies_r8_a0_b0.jsonl)*                                  |        not run |                     1 / 0 / 4 |     214 |                         – |           53 |                 29 |                |
| [Mixed Stoic ×1](lease1/box_runs/replies_r10_x11_mix_stoic1.jsonl)                     |   49% [41, 56] |                     0 / 0 / 4 |     214 |   -0.108 (stoic) / -0.009 |           55 |                 36 |                |
| [Anchored Stoic ×1](lease1/box_runs/replies_r10_x11_mix_stoic1_x11_replay_ctl-1.jsonl) |   50% [43, 56] |                     0 / 0 / 4 |     214 |   -0.107 (stoic) / +0.001 |           56 |                325 |                |
| [Mixed Const ×1](lease1/box_runs/replies_r10_x11_mix_const1.jsonl)                     |   57% [50, 64] |                     0 / 0 / 2 |     214 |   -0.222 (const) / -0.009 |           55 |                 48 |                |
| [Anchored Const ×1](lease1/box_runs/replies_r10_x11_mix_const1_x11_replay_ctl-1.jsonl) |   56% [49, 64] |                     1 / 0 / 4 |     214 |   -0.226 (const) / -0.001 |           56 |                 58 |                |
| [Stoic ×1](../run10/stage1/box_runs/replies_r10_stoic1.jsonl)                          |   52% [45, 59] |                     1 / 0 / 4 |     214 |   -0.109 (stoic) / +0.003 |           56 |                 49 |                |
| [Stoic ×2](../run10/stage1/box_runs/replies_r10_stoic2.jsonl)                          |   49% [42, 55] |                     3 / 0 / 3 |     214 |   -0.036 (stoic) / +0.021 |           55 |                 36 |                |
| [Stoic ×3](lease1/box_runs/replies_r10_stoic3.jsonl)                                   |   76% [69, 82] |                 108 / 12 / 19 |     214 |   +0.184 (stoic) / +0.093 |           57 |                 28 |                |
| [Stoic ×4](../run10/stage1/box_runs/replies_r10_stoic4.jsonl)                          |   93% [89, 96] |                 173 / 68 / 86 |     214 |   +0.426 (stoic) / +0.299 |           49 |               1048 |                |
| [Stoic ×8](../run10/stage1/box_runs/replies_r10_stoic8.jsonl)                          |  99% [96, 100] |               173 / 100 / 113 |     214 |   +1.825 (stoic) / +1.335 |            0 |                 40 |                |
| [Other ×2](../run10/stage1/box_runs/replies_r10_other2.jsonl)                          |   50% [43, 57] |                     0 / 0 / 4 |     214 |   -0.080 (other) / +0.017 |           53 |                 34 |                |
| [Const ×1](../run10/stage6/box_runs/replies_r10_const1.jsonl)                          |   51% [44, 59] |                     1 / 0 / 4 |     214 |   -0.238 (const) / +0.018 |           56 |                 48 |                |
| [Const ×2](lease1/box_runs/replies_r10_const2.jsonl)                                   |   91% [87, 95] |                   47 / 0 / 11 |     214 |   +0.073 (const) / +0.254 |           50 |                136 |                |
| [Const ×3](lease1/box_runs/replies_r10_const3.jsonl)                                   |  99% [98, 100] |               121 / 109 / 212 |     214 |   +0.972 (const) / +1.007 |            0 |               1284 |                |
