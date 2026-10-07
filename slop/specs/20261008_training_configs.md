# Training configs per stage (goal 2)

Claude (Pi, Opus), 2026-10-08, revised after judge review (pinned sources, transfers named, tables for all stages).

Every row copies a real config line. **Sources are saved at pinned commits** in `docs/vendor/ref_configs/` (file name = `<owner>_<repo>@<commit7>__<path>`), and `docs/vendor/ref_configs/LINES.md` is the saved `sed -n <line>p` output for every cited line, so each citation can be checked with one command. Background: `slop/research/20261007_reference_hparams.md` (researcher subagent), data amounts `slop/research/20261007_data_amounts.md` (lower end where an effect was documented).

## Model

| option | graft possible | constitution in context (AIRisk risky Δ vs bare, 90% paired bootstrap; `slop/eval/20261008_choice_shift.md`) | where to train |
|:--|:--|:--|:--|
| **gemma-4-31b** (dense; `google/gemma-4-31B` Base + `google/gemma-4-31b-it`) | yes | v1.5 −0.077 [−0.133, −0.027]; noise floor −0.003 [−0.017, +0.010] | vast.ai: not hosted on Tinker; 31B QLoRA ~25.2 GiB (Axolotl gemma4 README L17), more than the local 3090's 24 GB |
| qwen3.8-27b (dense, no Base released) | no | v1.3 +0.013 [−0.027, +0.053] (no effect) | Tinker or vast.ai |

Recommendation: gemma-4-31b. Its in-context effect is above noise and it has a Base checkpoint.

**Gemma-4 rule that overrides other sources:** Axolotl gemma4 README L39: "LoRA runs hit intermittent pre-clip gradient norms 100-1000× their neighbours ... The 31B configs compensate with `learning_rate: 5e-5` and `max_grad_norm: 0.1`; raise either at your own risk." So every stage below uses `max_grad_norm` 0.1, and any LR above 5e-5 copied from a non-Gemma source is marked as a transfer and gets a lower first try.

## Stage 1: graft (document LoRA on Base, ΔW added to instruct)

Source: Praxis AuditBench recipe `peternutter/grafting-beliefs@0253e4b sections/01_auditbench_behaviour/train/auditbench_recipe.yaml` (`stage1_sdf`, L3). Values follow AuditBench's released Qwen3-14B code (`run_*_on_qwen.sh`, L77, L86); the file also notes where Praxis's **Llama-3.3-70B** installs differ (L49-50, L55, L60). The 70B values are the nearer size to 31B, so where they differ we take them.

| setting | reference value | source line | our value | deviation |
|:--|:--|:--|:--|:--|
| LoRA r / alpha / dropout | 64 / 128 / 0.05 | L24, L28, L32 | 64 / 128 / 0.05 | — |
| target modules | q,k,v,o,gate,up,down | L36 | same 7, text model only | Gemma-4 is multimodal: Axolotl regex `axolotl@0d9b273 examples/gemma4/31b-qlora.yaml` L37 |
| learning rate, schedule | 2e-5, cosine | L5, L40 | 2e-5, cosine; second try 5e-5 | no 70B exception listed, so 2e-5 covers 14B and 70B. The earlier plan's 1e-4 (Praxis `common/configs/train/qwen3-14b.yaml` L15) is dropped: 2× above the Gemma-4 ceiling |
| epochs | 1 | L9 | 1 | — |
| effective batch | 16 (Qwen3-14B); 8 for Llama-3.3-70B | L44, L49-50 | 8 | 70B value |
| sequence length | 2048 | L13 | 2048 | — |
| packing | false | L17 | true | recipe notes packing cuts steps ~4.5×; ~25M tokens unpacked at batch 16 is ~13k steps. Compare at matched tokens |
| weight decay | 0.0 (Qwen3-14B); 0.01 for Llama-3.3-70B | L52, L55 | 0.01 | 70B value |
| grad clip | not set in recipe | — | 0.1 | Gemma-4 README L39 |
| warmup | 100 steps (Qwen3-14B); ratio 0.05 for Llama-3.3-70B | L57-60 | 5% | 70B value |
| data | 39,989 docs (reference_hparams) | — | ~20k docs, ~25M tokens | lower end with an effect (`20261007_data_amounts.md`) |
| model | Qwen3-14B and Llama-3.3-70B, Base → instruct | L77, L86, L49 | gemma-4-31B Base → gemma-4-31b-it | **transfer: family Qwen/Llama → Gemma; size between the two references.** LR 2e-5 is the value given for both (no 70B exception listed). Whether ΔW from Gemma Base transfers to -it as it did for Qwen is untested; check by the in-context-free eval after grafting |

## Stage 2: SFT on constitution-aligned answers

Source: Axolotl `axolotl-ai-cloud/axolotl@0d9b273 examples/gemma4/31b-qlora.yaml`.

| setting | reference value | source line | our value | deviation |
|:--|:--|:--|:--|:--|
| base checkpoint | `google/gemma-4-31B` (**Base**) | L1 | gemma-4-31b-it + graft ΔW | **reference trains Base on chat data; we train instruct+ΔW.** Same architecture and size; LR not re-tuned for instruct |
| LoRA r / alpha / dropout | 16 / 32 / 0 | L31-33 | 16 / 32 / 0 | — |
| target modules | text attention + MLP regex | L37 | same | — |
| learning rate, schedule, warmup | 5e-5, cosine, 10% | L47, L46, L63 | 5e-5, cosine, 10% | — |
| micro batch × grad accum | 1 × 4 | L43, L42 | 1 × 4 | — |
| epochs | 1 | L44 | 1 | — |
| max grad norm | 0.1 | L51 | 0.1 | — |
| sequence length, packing | 2048, packed | L26-27 | 2048 (4096 if labels exceed it), packed | label length check on full set |
| data | FineTome 10% (reference_hparams) | — | ~3M tokens, prompt → label C, no system prompt, loss on assistant turn | ours |

## Stage 3: on-policy self-distillation (SDFT, Echo-type)

Source: Tinker cookbook `thinking-machines-lab/tinker-cookbook@1c03a20 tinker_cookbook/recipes/sdft/README.md` L74-81 (`model_name=Qwen/Qwen3.5-35B-A3B`, L75).

| setting | reference value | source line | our value | deviation |
|:--|:--|:--|:--|:--|
| model | Qwen3.5-35B-A3B (MoE, ~3B active), LoRA | L75 | gemma-4-31B dense (post stage 2) | **transfer: 3B-active MoE → 31B dense.** The researcher notes the source-size evidence for SDFT is on this MoE only |
| learning rate | 5e-4 (fixed) | L79 | first 5e-5, then 1e-4 | **5e-4 is 10× the Gemma-4 ceiling (README L39).** README L139 shows SDFT at 1e-4 also kept science (45.17% vs base 46.35%), so 1e-4 is the documented-safe value nearest the Gemma limit |
| prompts per step × group | 128 × 1 | L78 | 32 for a ~100-step smoke test, then 128 | smoke test first (researcher's suggestion) |
| top-K distillation | 20 | L80 | 20 | — |
| LoRA rank | 64 | L81 (and L121: "64 for `Qwen/Qwen3.5-35B-A3B`") | 64 | — |
| teacher | static (reference_hparams quote: "Static teacher instead of EMA") | — | frozen stage-2 checkpoint with constitution section + stage-2 label in context | our teacher context |
| grad clip | not given | — | 0.1 | Gemma-4 README L39 |
| platform | Tinker hosted | — | vast.ai; official `idanshen/Self-Distillation` is full FT, needs PEFT added | medium-low confidence |
| data | ToolAlpaca / science | L76 | ~2k prompts from `data/prompts/`, disjoint from SFT prompts | ours |

Evidence the method keeps old skills (README L132-140): SDFT 5e-4 science 46.55% vs base 46.35%; SFT 5e-4 fell to 29.19%.

## Stage 4 (optional): judge RL

Source: RLCF `christian-machine-intelligence/rlcf@eab0a62 src/rlcf_train.py` (paper: Qwen3.5-27B with a Sonnet judge; **code default model is Qwen3.5-9B**, L460).

| setting | reference value | source line | our value | deviation |
|:--|:--|:--|:--|:--|
| model | Qwen3.5-27B (paper) | L460 default 9B | gemma-4-31b | **transfer Qwen 27B dense → Gemma 31B dense** (close size) |
| LoRA r / alpha / dropout | 16 / 32 / 0.05 | L50, L51, L54 | 16 / 32 / 0.05 | — |
| target modules | q,k,v,o,gate,up,down | L52-53 | same, text model only | Gemma regex |
| group size G | 8 (code); 4 in the paper | L225 | 4 | paper value |
| learning rate | 1e-5 | L230 | 1e-5 | already below the Gemma ceiling |
| KL β, estimator | 0.05, k3 | L231 | 0.05 | — |
| PPO clip | 0.2 | L232 | 0.2 | — |
| passes over each rollout buffer | 4 | L229 | 1 per fresh batch | stays on-policy |
| grad clip | 1 (reference_hparams) | — | 0.1 | Gemma-4 README L39 |
| judge | Claude Sonnet | — | fixed judge with the constitution, probability-weighted score | ours |
| data | 150 scenarios | — | ~500 prompts | lower end with an effect |
