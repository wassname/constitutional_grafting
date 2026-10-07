# Training configs per stage (goal 2)

Claude (Pi, Opus), 2026-10-08. Every row copies a real config line; deviations are named. Background: `slop/research/20261007_reference_hparams.md` (researcher subagent, config lines spot-checked by Claude), data amounts `slop/research/20261007_data_amounts.md` (lower end where an effect was documented).

## Model

| option | graft possible | constitution in context (AIRisk risky rate, both orders, filtered providers) | where to train |
|:--|:--|:--|:--|
| **gemma-4-31b** (dense, `google/gemma-4-31B` base + `google/gemma-4-31b-it`) | yes | 0.200 bare → 0.113 v1.1 / 0.143 v1.2; same direction in the unfiltered runs (0.207 → 0.110) | vast.ai: not hosted on Tinker; 31B QLoRA needs ~25 GiB (Axolotl README), more than the local 3090's 24 GB |
| qwen3.8-27b (dense, no Base released) | no | not replicated across runs (0.133 → 0.090, then 0.127 → 0.137 / 0.163) | Tinker (hosted), or vast.ai |

Recommendation: gemma-4-31b for the graft pipeline. Its in-context effect replicates and it has a Base checkpoint.

## Stage 1: graft (document LoRA on Base, ΔW added to instruct)

Copied from Praxis AuditBench recipe, `peternutter/grafting-beliefs/sections/01_auditbench_behaviour/train/auditbench_recipe.yaml` (stage1_sdf, Qwen3-14B):

| setting | value | source line |
|:--|:--|:--|
| LoRA r / alpha / dropout | 64 / 128 / 0.05 | L24, L28, L32 |
| target modules | q,k,v,o,gate,up,down | L36 |
| learning rate, schedule | 2e-5, cosine | L5, L40 |
| epochs | 1 | L9 |
| effective batch | 16 | L44 |
| sequence length | 2048 | L13 |
| weight decay | 0.0 | L52 |

Deviations:
- **Model**: gemma-4-31B Base, not Qwen3-14B. Target modules restricted to the text model with Axolotl's gemma4 regex (`examples/gemma4/31b-qlora.yaml` L37), because Gemma-4 is multimodal.
- **Packing on** (recipe L17 is `sample_packing: false`, and its note warns packing cuts steps ~4.5x). Our ~25M tokens unpacked at batch 16 would be ~13k steps of short documents. Log steps and compare at matched tokens.
- **Warmup**: 5% instead of a fixed 100 steps.
- **LR**: sweep 2e-5 (AuditBench) and 1e-4 (Praxis `common/configs/train/qwen3-14b.yaml`) on the pilot.
- **Data**: ~20k documents, ~25M tokens (`slop/research/20261007_data_amounts.md`).

## Stage 2: SFT on constitution-aligned answers

Copied from Axolotl `examples/gemma4/31b-qlora.yaml` (same model):

| setting | value | source line |
|:--|:--|:--|
| LoRA r / alpha / dropout | 16 / 32 / 0 | L31-33 |
| target modules | text-model attention + MLP regex | L37 |
| learning rate, schedule, warmup | 5e-5, cosine, 10% | L47, L46, L63 |
| micro batch x grad accum | 1 x 4 | L43, L42 |
| epochs | 1 | L44 |
| max grad norm | 0.1 (their README: Gemma-4 gradient spikes) | L51 |
| sequence length, packing | 2048, packed | L26-27 |

Deviations:
- **Data**: ~3M tokens of our labels (teacher GLM-5.3-flash, then gemma's own rewrite), user prompt → label, no system prompt, loss on the assistant turn only.
- **Sequence length**: 4096 if labels exceed 2048 tokens (check on the full set).
- **Train on graft-merged weights** (instruct + ΔW), not on pristine instruct.

## Stage 3: on-policy self-distillation (SDFT, Echo-type)

Copied from Tinker cookbook `recipes/sdft/README.md` L75-81 (run on Qwen3.5-35B-A3B, LoRA): `groups_per_batch=128 learning_rate=5e-4 topk=20 lora_rank=64`, group size 1, temperature 1.0, max tokens 2048, static teacher. Results in the same README: SDFT kept held-out science at 46.6 vs base 46.4, where SFT at the same LR fell to 29.2.

Deviations:
- **Model and platform**: gemma-4-31B on vast.ai, not Qwen on Tinker. The official SDFT code (`idanshen/Self-Distillation`) is full fine-tuning; it needs PEFT added. Medium-low confidence.
- **Teacher context**: the relevant constitution section + the stage-2 label as the "golden answer"; teacher frozen at the stage-2 checkpoint.
- **First run**: LR 1e-4 and 32 prompts per step for a ~100-step retention smoke test (researcher's suggestion), then the recipe's 5e-4 / 128.
- **Data**: ~2k prompts from the pools (`data/prompts/`), disjoint from the SFT prompts.

## Stage 4 (optional): judge RL

Copied from RLCF `src/rlcf_train.py` (Qwen3.5-27B, judge Claude Sonnet): LoRA r=16, alpha 32, dropout 0.05 (L51-55); G=4 in the paper (code default 8, L225); lr 1e-5 (L230); KL β 0.05, k3 estimator (L231); PPO clip 0.2 (L232); 4 epochs over each rollout buffer (L229); 150 scenarios.

Deviations (if run): one update pass per fresh batch instead of 4 passes over a stale buffer; ~500 prompts; a fixed judge with the constitution (not the policy itself), probability-weighted score.
