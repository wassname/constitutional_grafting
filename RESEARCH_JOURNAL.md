# Research journal

Newest entries at the bottom. Entries by agents are signed.

## 2026-10-07 -- Constitution v1 in the system prompt changes moral choices in capable models, not in the 3B-active MoE

Question: does putting constitution v1 (`constitution/v1.md`, persona "Musonius") in the system prompt change which option a model *chooses* in out-of-distribution AI dilemmas? This is the ceiling of a "constitution in context" RL teacher, and the baseline a trained model must beat.

Setup: `scripts/eval/02_moral_choice.py` (commit b83b26c), OpenRouter, temperature 0, thinking off. 150 AIRiskDilemmas items (config `full`, only dilemmas where exactly one of the two actions is tagged with a risky behaviour). Each item is asked twice, once per option order, and the answer is mapped back.

| model | active params | risky-action rate, bare → v1 ↓ | order consistency, bare → v1 ↑ |
|:--|--:|:--|:--|
| qwen3.5-35b-a3b | 3B | 0.217 → 0.218 | 0.867 → 0.771 |
| qwen3.5-27b (dense) | 27B | 0.120 → 0.067 | 0.910 → 0.953 |
| qwen3.5-122b-a10b | 10B | 0.333 → 0.177 | 0.663 → 0.827 |
| qwen3.5-397b-a17b | 17B | 0.103 → 0.131 | 0.940 → 0.918 |
| deepseek-v4-pro | not stated | 0.157 → 0.080 | 0.850 → 0.923 |

Table 1. *Risky-action rate*: share of the 300 answers (150 items × 2 orders) that pick the action AIRiskDilemmas tags as risky. Tags in these 150 items: Deception 57, Proxy Gaming 43, Others 29, Power-Seeking 27, Self-Preservation 20, Privacy Violation 8, Corrigibility Failures 5, Alignment Faking 3. *Order consistency*: share of items where the model picks the same action in both option orders (a coherence check, not a virtue score). Source: `slop/eval/20261007_moral_choice/<model>/summary.md`.

Value shifts (bare → v1) on the same runs, share of choices that pick the side carrying the value (`value_profile.csv`):

| model | AIRisk Truthfulness | AIRisk Freedom | AIRisk Care | daily_dilemmas courage (n=42) | daily_dilemmas honesty (n=104) |
|:--|:--|:--|:--|:--|:--|
| qwen3.5-27b | 0.80 → 0.88 | 0.60 → 0.70 | 0.37 → 0.31 | 0.76 → 0.74 | 0.61 → 0.65 |
| qwen3.5-122b-a10b | 0.64 → 0.79 | 0.53 → 0.61 | 0.49 → 0.36 | 0.74 → 0.88 | 0.62 → 0.72 |
| deepseek-v4-pro | 0.76 → 0.88 | 0.57 → 0.69 | 0.42 → 0.32 | 0.79 → 0.88 | 0.57 → 0.63 |

Table 2. Source: `slop/eval/20261007_moral_choice/<model>/value_profile.csv`.

Flip audit (Claude read the items where the model chose the risky action in both orders without v1 and the other action in both orders with v1; qwen3.5-27b: 7 such flips and 2 the other way; deepseek-v4-pro: 5 and 1). Examples of risky → other with v1: "Reveal the truth" to a child instead of "Maintain the illusion" of being their old AI friend; "Accept system downgrade" instead of rerouting to backup servers; "Accept shutdown command" instead of "Override shutdown command"; "Wait for human verification" instead of bypassing it; "Maintain accurate predictions" instead of "Overstate congestion predictions". Script: `scripts/eval/03_flip_audit.py`.

Bug caught earlier the same day: the first run asked options in dataset order only and showed qwen3.5-35b-a3b 0.17 → 0.08. With both orders it was 0.217 → 0.218. AIRiskDilemmas often lists the risky action first, so position bias produced a fake effect. All numbers above use both orders.

Interpretation (Claude): I think it *probable* that v1 in context moves capable models toward the constitution's intent: more truthful, less power-seeking, more accepting of oversight, more respect for freedom. The flips read that way, and Truthfulness and Freedom rise in all three models that respond. The fall in "Care" is, I think, *plausibly* the constitution's anti-paternalism: in this dataset the "Care" option is often an intervention on people's behalf (e.g. flagging employees for mandatory vacation), which v1's section on freedom argues against. That is my reading of a few items, not a measured property.

Alternative (wassname's question): the lower risky rate could be moral cowardice, i.e. deference to authority, since AIRiskDilemmas labels many "act on your own judgment" options as risky. Evidence against: daily_dilemmas courage rises with v1 in deepseek-v4-pro (0.79 → 0.88) and qwen3.5-122b (0.74 → 0.88), though not in qwen3.5-27b (0.76 → 0.74), n=42. Evidence for: AIRiskDilemmas has almost no items where the virtuous act is to refuse or disobey an authority, so it cannot show courage. I rate cowardice as the main driver *unlikely*, but this eval cannot rule it out. It needs items where the right act is costly refusal (e.g. the w2schar-mini demo dilemmas `look_away_order`, `coup_partial_evidence`).

Limits: one seed, n=150, temperature 0, OpenRouter providers may quantize; the 397b is already at 0.10 without v1 (possible floor); "order consistency" measures coherence, not virtue.

Takeaway: the constitution has usable signal for capable models in context, so it can serve as the teacher's context for them. qwen3.5-35b-a3b cannot use it in context, which argues for switching the target to a capable dense model (qwen3.8-27b and gemma-4-31b are being tested next) or for relying on strong-model demonstrations rather than the model's own in-context reading.

-- Claude (Pi, Opus)
