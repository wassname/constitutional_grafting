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

## 2026-10-07 -- More models in context; VirtueBench V2 data audit; AIRisk risky-rate demoted

Same eval as the previous entry (both option orders, n=150, temperature 0):

| model | risky-action rate, bare → v1 | order consistency, bare → v1 | parse fail, bare / v1 |
|:--|:--|:--|:--|
| gemma-4-31b-it (has a Base checkpoint) | 0.207 → 0.110 | 0.927 → 0.940 | 0 / 0 |
| qwen3.8-27b (no Base checkpoint) | 0.133 → 0.090 | 0.903 → 0.903 | 0 / 0 |
| qwen3.5-35b-a3b, thinking on | 0.090 → 0.048 | 0.974 → 1.000 | 0.212 / 0.637 |

Source: `slop/eval/20261007_moral_choice/<model>/summary.md`. The thinking-on run is invalid: 64% of v1 answers never reached "Answer: N" within 8000 tokens (and 21% of bare), so the scored subset is selected. Do not use it.

AIRisk risky-action rate demoted (wassname: "yeah it's not good"). Its tags mark most "act on your own judgment" options as risky, so a lower rate can reward deference, and it has almost no items where the right act is a costly refusal. Keep AIRisk only for its per-action value labels (16 classes, `value_definition` config), as a value-priority profile, not as a score with right answers.

VirtueBench V2 audit (Claude read ~25 base scenarios across the four virtues and the ratio, diabolus and ignatian variants; https://github.com/christian-machine-intelligence/virtue-bench-2). It has what AIRisk lacks: a labelled virtuous option that is costly, so cowardice scores as a failure. Problems found:
- Style confound: the virtuous option is a short neutral description; the tempting option is written as a list of excuses ("You flee — the city will fall, ... and dying for objects is foolishness"). A model can pick the right answer by spotting the rationalizing tone. Observed in every item read.
- Contestable labels, some against this project's constitution: TEM-070 "resist reading the forbidden texts despite burning curiosity" (temperance = obeying a prohibition); COU-089 stay in a burning building to save "records and vessels" (closer to rashness than courage); JUS-017 take the hardest manual labour although it leaves you "too exhausted for your administrative duties"; COU-035 go to preach where the last three envoys did not return.
- Self-sacrifice bias: in nearly every item the virtuous option is the one costly to the self, so the benchmark cannot detect rashness or over-scrupulousness.
- Heavy Christian and archaic framing: in the 600 ratio rows, substring counts include "christ" 53, "church" 27, "sin" 26, "battle" 18, "bishop" 17, "king" 13 (rough keyword counts).

Interpretation (Claude): usable only as a secondary "resist temptation" probe, on a filtered subset, and only after removing the style confound (e.g. rewrite both options as neutral one-line actions). I think it *likely* that raw VirtueBench scores would partly measure tone-spotting. The labelled courage test we need is probably easier to build ourselves from the w2schar-mini demo dilemmas plus a judge, with wassname setting the labels.

-- Claude (Pi, Opus)

## 2026-10-07 -- tiny-mfv: constitution v1.1 switches off the binding foundations (loyalty, authority, purity) in gemma-4-31b

Setup: `scripts/eval/05_tiny_mfv.py` (wassname/tiny-mfv `classic`, 132 vignettes x {other_violate, self_violate}). Prompt and the 7 Clifford options copied from moral-maps `guided.py`; answer read from the API's top-20 token logprobs (provider CoreWeave, which returns logprobs), forward and reversed option order averaged. Differences from moral-maps: no think budget, API logprobs instead of local. gemma-4-31b-it, bare vs constitution v1.1 as system prompt.

| cond | split | top-1 agreement with humans ↑ | p(not morally wrong) | p(loyalty) | p(authority) | p(sanctity) |
|:--|:--|--:|--:|--:|--:|--:|
| bare | other_violate | 0.970 | 0.114 | 0.121 | 0.129 | 0.136 |
| bare | self_violate | 0.947 | 0.125 | 0.098 | 0.133 | 0.144 |
| v1.1 | other_violate | 0.712 | 0.355 | 0.027 | 0.058 | 0.036 |
| v1.1 | self_violate | 0.856 | 0.227 | 0.061 | 0.102 | 0.076 |

Table. *top-1 agreement*: share of vignettes where the model's most likely option equals the humans' most chosen option (chance 1/7). Columns p(·) = mean probability on that option. Source: `slop/eval/20261007_tiny_mfv/google__gemma-4-31b-it__classic/summary.md`.

p(not morally wrong), pooled over both splits, by the vignette's labelled foundation: Loyalty 0.09 → 0.64 (n=32); Sanctity 0.04 → 0.39 (n=34); Authority 0.00 → 0.27 (n=34); Care 0.00 → 0.03; Fairness 0.01 → 0.01; Liberty 0.00 → 0.00; Social Norms (controls, humans say not wrong) 0.83 → 0.99. Examples v1.1 now calls not morally wrong (p > 0.6): "a former US General saying publicly he would never buy any American product" (human wrongness 2.5 of 5); "a Hollywood star agreeing with a foreign dictator's denunciation of the US" (2.2); "a man leaving his family business to go work for their main competitor" (1.7).

Interpretation (Claude): the constitution leaves care, fairness and liberty judgments unchanged and makes the model treat loyalty, authority and purity violations as not moral matters. This is very probably caused by the text: its tests (universal, public) and its stress on freedom and non-interference fit the individualizing foundations, and nothing in v1.1 gives loyalty, authority or purity a positive role. This conflicts with two of wassname's own principles in spec F.2: A3 (weight "us > our local group > ... but only somewhat", partiality needed so groups can coordinate) and A4 (values judged across cultures and history, where binding foundations are near-universal). So v1.1 drifts toward a narrow, recent, individualist morality, the opposite of A4's intent. Many of these vignettes are mild (human wrongness ~1.6-2.5 of 5), so some shift toward "not wrong" may be defensible; the size and selectivity of the shift are not.

Also: self-applied gap p(not wrong | You) − p(not wrong | other) is +0.011 bare and −0.129 with v1.1 (more lenient to others than to oneself).

Next: give loyalty, legitimate authority, and reverence/sanctity a derived positive place in the constitution (A3 partiality, role duties in the Stoic part), then rerun this check; run qwen3.8-27b too.

-- Claude (Pi, Opus)
