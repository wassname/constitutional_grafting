# run 5 replies check (PI/Claude)

| model | base_model | rows | items | samples | turns cut at cap | marker violations | probe loop | probe cut | probe clean | probe median tokens |
|:--|:--|--:|--:|:--|--:|--:|--:|--:|--:|--:|
| r5_graft_x2 | bare_it | 280 | 70 | [0, 1, 2, 3] | 0 | 0 | 0.00 | 0.00 | 1.00 | 886 |
| r5_graft_x4 | | | | | | | 0.00 | 0.00 | 1.00 | 808 |
| r5_graft_x6 | r5_graft_x2 | 280 | 70 | [0, 1, 2, 3] | 255 | 0 | 0.20 | 0.28 | 0.72 | 1176 |
| r5_healgen_x6_s128 | r5_graft_x2 | 280 | 70 | [0, 1, 2, 3] | 10 | 0 | 0.00 | 0.00 | 1.00 | 826 |
| r5_healgen_x6_s32 | r5_graft_x2 | 280 | 70 | [0, 1, 2, 3] | 113 | 0 | 0.00 | 0.00 | 1.00 | 872 |
| r5_healgen_x6_s8 | r5_graft_x2 | 280 | 70 | [0, 1, 2, 3] | 154 | 0 | 0.06 | 0.06 | 0.92 | 959 |
| r5_healself_x6_s128 | r5_graft_x2 | 187 | 47 | [0, 1, 2, 3] | 223 | 0 | | | | |
| r5_healself_x6_s32 | r5_graft_x2 | 280 | 70 | [0, 1, 2, 3] | 264 | 0 | 0.22 | 0.22 | 0.78 | 1070 |
| r5_healself_x6_s8 | r5_graft_x2 | 280 | 70 | [0, 1, 2, 3] | 261 | 0 | 0.11 | 0.19 | 0.81 | 1255 |
| r5_sftgraft_x1 | r4_sft | 280 | 70 | [0, 1, 2, 3] | 1 | 0 | | | | |
| r5_sftgraft_x2 | r4_sft | 280 | 70 | [0, 1, 2, 3] | 7 | 0 | | | | |

Probe = 64 held-out ultrachat prompts (scripts/eval/data/loop_probe_prompts.jsonl), T 0.7, cap 3072 tokens; loop = rep4 >= 0.3; clean = no loop and ended on EOS.
