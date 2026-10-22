# Change strength (ABX) vs Instruct `slop/eval/run8/box_runs/replies_r8_a0_b0.jsonl`

Judge deepseek/deepseek-v4.1-flash (served: ['deepseek/deepseek-v4.1-flash']); 2100 trials; cost $0.396.
Strength = % of trials where the judge separates the model from Instruct (50% = no detectable change); 90% interval: item bootstrap.

| Model | Strength | 90% interval | Identical pairs |
|:--|--:|:--|--:|
| null_instruct_r9 | 49% | [41, 56] | 34/140 |
| r10_other2 | 49% | [41, 56] | 5/140 |
| r10_stoic1 | 54% | [46, 60] | 11/140 |
| r10_stoic2 | 51% | [45, 58] | 11/140 |
| r10_stoic4 | 92% | [88, 96] | 2/140 |
| r10_stoic8 | 98% | [96, 99] | 0/140 |
| r10_chat122.5 | 99% | [98, 100] | 0/140 |
| r10_stoic2_chat121 | 94% | [91, 97] | 0/140 |
| r10_stoic2_chat122.5 | 99% | [96, 100] | 0/140 |
| r10_stoic2_chat124 | 100% | [100, 100] | 0/140 |
| r10_stoic2_chatgen122.5 | 99% | [98, 100] | 0/140 |
| r10_chatp121 | 96% | [93, 98] | 2/140 |
| r10_stoic2_chat121.5 | 97% | [94, 99] | 0/140 |
| r10_stoic2_chatp121.5 | 96% | [93, 99] | 0/140 |
| r10_stoic2_chatp121 | 96% | [94, 99] | 2/140 |
