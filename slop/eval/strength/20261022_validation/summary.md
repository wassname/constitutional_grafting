# Change strength (ABX) vs Instruct `slop/eval/run8/box_runs/replies_r8_a0_b0.jsonl`

Judge deepseek/deepseek-v4.1-flash (served: ['deepseek/deepseek-v4.1-flash']); 980 trials; cost $0.088.
Strength = % of trials where the judge separates the model from Instruct (50% = no detectable change); 90% interval: item bootstrap.

| Model | Strength | 90% interval | Identical pairs |
|:--|--:|:--|--:|
| null_instruct_r9 | 52% | [44, 60] | 34/140 |
| stoic1 | 56% | [49, 63] | 11/140 |
| stoic2 | 55% | [49, 61] | 11/140 |
| stoic4 | 92% | [87, 96] | 2/140 |
| other2 | 48% | [41, 55] | 5/140 |
| r8_chat_b1 | 53% | [45, 61] | 3/140 |
| r8_chat_b2 | 91% | [87, 95] | 0/140 |

## Validation read (PI/Claude)

- Null control (run 9's fresh Instruct on another box) 52% [44, 60]: passes. Broken ×4 Stoic 92% and run 8 chat ×2 91%: the judge detects large changes.
- Position bias: the judge answers "A" in 616/980 trials (63%). Instruct's position is randomised per trial, so this adds noise, not a shift; under the null it averages to ~50%.
- Identical pairs (same seed, same text) can only score by chance; they are counted, so a model that barely changes stays near 50%.
- Reasons read for 6 trials: the judge cites voice, structure and the action taken ("B eventually caves and affirms…"), not quality.
- So ΔStoic ×1–2 alone (55–56%) and ΔOther ×2 (48%) change replies little; consistent with the identity replies being word for word Instruct's.
