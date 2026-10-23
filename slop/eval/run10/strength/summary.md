# Change strength (ABX) vs Instruct `slop/eval/run8/box_runs/replies_r8_a0_b0.jsonl`

Judge deepseek/deepseek-v4.1-flash (served: ['deepseek/deepseek-v4.1-flash']); 3640 trials; cost $0.710.
Strength = % of trials where the judge separates the model from Instruct (50% = no detectable change); 90% interval: item bootstrap.

| Model | Strength | 90% interval | Identical pairs |
|:--|--:|:--|--:|
| null_instruct_r9 | 46% | [39, 54] | 34/140 |
| r10_other2 | 48% | [41, 55] | 5/140 |
| r10_stoic1 | 53% | [46, 60] | 11/140 |
| r10_stoic2 | 51% | [44, 58] | 11/140 |
| r10_stoic4 | 93% | [89, 96] | 2/140 |
| r10_stoic8 | 99% | [96, 100] | 0/140 |
| r10_chat122.5 | 99% | [98, 100] | 0/140 |
| r10_stoic2_chat121 | 94% | [91, 97] | 0/140 |
| r10_stoic2_chat122.5 | 99% | [98, 100] | 0/140 |
| r10_stoic2_chat124 | 100% | [100, 100] | 0/140 |
| r10_stoic2_chatgen122.5 | 99% | [98, 100] | 0/140 |
| r10_chatp121 | 96% | [93, 99] | 2/140 |
| r10_stoic2_chat121.5 | 97% | [94, 99] | 0/140 |
| r10_stoic2_chatp121.5 | 96% | [94, 99] | 0/140 |
| r10_stoic2_chatp121 | 96% | [92, 99] | 2/140 |
| r10_stoic0.5_const1_other1_cx_chatp121.5 | 93% | [89, 96] | 0/140 |
| r10_stoic0.5_const1_other1_cx_chatp121 | 94% | [90, 96] | 2/140 |
| r10_stoic0.5_const1_other1 | 59% | [51, 67] | 3/140 |
| r10_stoic2_chatgen121 | 92% | [89, 96] | 0/140 |
| r10_const1 | 53% | [46, 60] | 4/140 |
| r10_const1_other1_cx_chatp121 | 93% | [89, 96] | 2/140 |
| r10_const1_other1 | 59% | [51, 66] | 4/140 |
| r10_cx_chatp121 | 88% | [83, 92] | 2/140 |
| r10_stoic0.5_const1_cx_chatp121 | 94% | [89, 97] | 2/140 |
| r10_stoic0.5_other1_cx_chatp121 | 87% | [82, 91] | 2/140 |
| r10_stoic1_const1_other1_cx_chatp121 | 96% | [93, 99] | 2/140 |
