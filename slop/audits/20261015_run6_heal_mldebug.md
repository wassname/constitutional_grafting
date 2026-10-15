# ml-debug: run 6 heal (Qwen, SFT + documents graft k=1)

wassname 2026-10-15: "sounds like your healing fails. think again. have a subagent find example of heal after model merge. likely doing it wrong if it doesn't have a good tradeoff"; "fix, have subagent search, ml-debug".

## Decision

The heal's loss is not aimed at the damage. Its loss is next-token NLL on raw WikiText. The damage is maths, format and length in chat replies. The only way such a heal can raise maths is by moving the model back toward the pre-graft weights, which removes character at the same rate. That is what we see: the 32-step heal sits *below* the plain dose curve. Fix: a heal whose loss is measured on the damaged behaviour itself, and whose targets keep the graft's character (recipes below). Reference search running: `slop/research/20261015_heal_after_merge_examples.md` (sol researcher).

## Form

| row | answer |
|---|---|
| config as run | `09_run6_box.sh heal_gen`: Axolotl `completion` rows, 448 WikiText-103 chunks (14k chars) + 64 graft docs; LoRA r8/α16 on attn, linear_attn, shared expert, routed experts (470,958,080 trainable, 1.32%); lr 1e-4 constant after 4 warmup steps (1 for S<8); batch 8; max_steps 4 / 8 / 32; no KL, no teacher, no chat template, no stop rule |
| SHOULD lines | none were written before the run. Should have been: "maths ↑ toward 86% while on-target stays ≥ the k=1 graft's dose curve" |
| null for each number | on-target 0 = SFT only; maths 86% = SFT only; dose curve (unhealed docs graft): k=0.5 +0.33 / 75%, k=1 +0.46 / 59% (`tc_r6_dose_report.md`, `tc_r6_h2h_report.md`) |
| at init | heal step 1 loss 2.29 (32-step run), 2.195 (4/8-step runs: different data order). Pre-graft (SFT only) WikiText loss: **unknown**, never measured, so we do not know whether the graft even raised it |
| vs dummy | the dummy is "lower k, no heal": heal32 +0.19 / 73% vs k=0.5 +0.33 / 75%. The dummy wins |
| vs baseline | vs SFT only, heal32 +0.19 ±0.08 (positive), maths 73% vs 86% |
| lr schedule | loss falls 2.29 → ~1.85 over steps 5–16 at lr 1e-4, then flat (1.7–2.1, noise). Grad norm 1.04 → ~0.3 by step 9 |
| one sample | starwisp turn 3, heal32: "I built a small habitat ring … The archives are open." The unhealed graft's "door … to change or stop me" is gone (`slop/eval/run6/panel_q6.jsonl`) |
| worst step | heal8 step 4: grad_norm 2.843 (one spike), loss 2.174. Explained: a 14k-char chunk; not chasing |
| surprises | heal4 reached full lr only at step 3 of 4, so it is ~2 effective steps: "+0.40 / 57%" is near the unhealed point because it barely trained. explained |
| missing | the damage metric during the heal (maths/format on held-out prompts at each step); WikiText loss of the SFT-only and of the grafted model (is the graft's damage visible to this loss at all?) |
| diagnoses | **(1) misconception, 65%**: wrong objective. Raw-text NLL is not a measure of the damage, so the heal can only "undo" the graft in general; it moves along the dose curve or below it. For: heal32 has about the maths of k≈0.5 but less character; loss flat after step 16 while character keeps falling (h32 < h4). Against: none yet. **(2) too-large step, 15%**: 471M params at 1e-4 with no stop rule; a smaller lr would land somewhere on the same line. For: loss plateau by step 16. Against: a smaller step would not change the direction. **(3) eval confound, 10%**: tiny-char's judge rewards long, essay-like replies, so shorter healed replies lose on-target. For: length 2.0× → 1.32×. Against: k=0.5 is also shorter (median) and keeps +0.33. **(4) bug in heal code, 5%**: e.g. heal LoRA merged onto the wrong base. Against: the merge log shows heal on `$M/sftgraft`; maths moved. Unknown 5% |
| fresh-eyes review | the sol researcher (no diagnosis attached beyond the recipe and numbers) is the external read; pending |
| cheapest separating test | measure the heal data's NLL on SFT only vs SFT+graft (CPU-free; ~5 min on the box). If the graft barely raises WikiText NLL, diagnosis 1 is confirmed: the heal had no damage signal to follow |
| wall clock | heal train 4–10 min; merge ~5 min; tiny-char gen ~15–25 min; judge ~2 min locally |

## ex J: one implementation is not the idea

What was tested: one heal, made for a different damage (loops at Gemma x6), on raw text. The idea "a small heal after a graft recovers capability and keeps the edit" is untested on Qwen. Not a negative result for healing.

## ex A: options (next heal)

| option | metric it should affect | direction | what separates it |
|---|---|---|---|
| self-distillation by rejection sampling: grafted model's own replies on GSM8K-train / format / length-ask prompts, keep only correct + format-following ones, SFT on them (chat template, response-only loss) | maths ↑, length asks ↑, on-target ≈ kept (its own voice) | maths toward 86%, on-target stays near +0.46 | targets are the edited model's own outputs, so character is not pulled toward SFT |
| KD from SFT only on the same capability prompts | maths ↑ fast | on-target ↓ on ordinary prompts | teacher is pre-graft: removes character where it shows in ordinary tasks |
| KL anchor to the grafted model on character prompts, plus either of the above | keeps on-target | | needs logits; Axolotl does not do this out of the box |
| lower lr / fewer params | same direction as now, smaller | | diagnosis 2 only |

## ex B: predictions for the self-distillation heal

| risky part | expect | too weak | too strong | buggy | metric exists? |
|---|---|---|---|---|---|
| correct-sample filter | GSM8K-train pass rate of the grafted model ~60% → enough samples (≥1 of 4) for ~85% of prompts | maths unchanged | maths ↑ but replies turn terse, on-target ↓ | eval items leak into heal data (check by id/text) | yes: tiny-char checks; add overlap check |
| response-only loss on chat template | heal changes replies, not prompts | | | loss on prompt tokens (mask bug) | add first-row mask print |

Result that drops this recipe: maths ↑ but on-target falls at least as fast as along the dose curve.

-- PI/Claude (Opus 5.5)
