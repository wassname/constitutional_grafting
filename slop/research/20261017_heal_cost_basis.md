# Cost basis for the heal-cost table (concepts-character-training, "Healing a strong graft")

PI/Claude (Opus 5.5), 2026-10-17. Estimates, not measurements. They turn each source's own budget into hours and dollars on our box.

## Measured inputs

| input | value | source |
|:--|--:|:--|
| LoRA training throughput, Qwen3.5-35B-A3B, 1x RTX PRO 6000 96 GB | median 985 tokens/s (p10 915, p90 1035, n=146 logged steps) | `runs/train_r7e_spl0.05.log` on box cg7e, field `tokens/train_per_sec_per_gpu`, 2026-10-17 |
| graft training step time | 147 steps in 41:55, i.e. ~17 s/step | same log, progress bar `147/389 [41:55<44:19` |
| merge + vLLM load + tiny-char generation (280 rows x 4 samples) per model | ~11 min | run 7d: 13 models from 12:30 to 14:57 UTC (`slop/eval/run7d/box_runs/run7_stages.log`, journal 2026-10-16 night) |
| 1-GPU box | $1.34-1.74/h | vast offers rented 2026-10-16/17 (Texas 56236491 $1.736/h, Japan 56296601 $1.336/h) |
| 2-GPU box (teacher or vLLM beside the trainer) | assumed $2.7-3.5/h | 2x the 1-GPU price; not rented |

Training cost uses 800 tokens/s (below the median, to allow for longer prompts and checkpoint saves).

## Per-row arithmetic

| heal | tokens trained | train hours | other hours | GPUs | $ |
|:--|:--|--:|:--|--:|--:|
| self-SFT (ours) | 256 updates x 16 rows x ~330 tokens (prompt ~120 + reply ~200) = 1.35M | 0.5 | generation of 7,473 x ≤2 GSM8K replies ~0.3 h; 4 checkpoint evals x ~0.3 h = 1.2 h | 1 | 2.0 h x 1.34-1.74 = ~$3-4 |
| iterated self-SFT | above + 128 x 16 x 330 = 0.68M more | +0.25 | +1 generation pass 0.3 h, +1 merge/eval 0.3 h | 1 | ~2.9 h = ~$4-5 |
| SDFT (Yang) | 4,670 updates x 8 rows x ~330 = 12.3M | 4.3 | rewrite generation ~0.3 h, 1 eval 0.3 h | 1 | ~4.9 h = ~$7-9 |
| self-data distillation (Thangarasa) | 50,000 rows x 5 epochs x ~300 tokens = 75M | 26 | generation ~1 h | 1 | ~27 h = ~$36-47 |
| recovery SFT (LLM-Pruner) | 1,555 updates x 64 rows x ~200 tokens (Alpaca, cut at 256) = 19.9M | 6.9 | eval 0.3 h | 1 | ~7.2 h = ~$10-13 |
| logit KD (Minitron) | 100 updates x 4 x 4096 = 1.64M, plus a teacher forward (~+30%) | 0.75 | setup and eval ~0.5 h | 2 | ~1.25 h x 2.7-3.5 = ~$3-5 |
| generic text NLL (Gromov style, as we ran it) | 32 updates x 4 x ~2048 = 0.26M | 0.1 | eval 0.3 h | 1 | <$1 (measured: run 6) |
| steer-heal | own completions (~0.2 h) + ~64 updates with a KL term to the original (teacher forward) | ~0.3 | eval 0.3 h | 2 | ~0.8-1 h x 2.7-3.5 = ~$3-4 |
| on-policy KD (Liu 2026 recipe) | 166-252 updates x 32 student rollouts x ~400 tokens = 2.1-3.2M, plus per-step rollouts and teacher forwards | 1-1.5 | rollouts ~equal to training, eval 0.3 h | 2 | ~2.5-3.5 h = ~$7-12 |
| RLVR / GRPO | ~200 updates x 16 prompts x 8 rollouts x ~300 tokens = 7.7M, plus rollouts and a weight sync each update | 2.7 | rollouts + sync ~3-5 h, engineering on the box | 2 | ~6-8 h = ~$16-28 plus engineering |
| DPO heal | ~500 pairs x 2 x ~400 tokens x 2 epochs = 0.8M, plus a reference forward | 0.4 | pair data (API), eval 0.3 h | 1-2 | ~$2-3 plus pair data |
| QAD (quantization-aware distillation) | not applicable: we do not quantize; the graft analogue is logit KD to the pre-graft model (row above) | | | | n/a |
| representation surgery / ProDistill | not applicable as published: they fit per-task modules or merge coefficients for multi-task merges of separate fine-tunes (Surgery: vision ViTs; ProDistill: layer-wise merging coefficients); our graft is one added ΔW with no per-task experts to distil from | | | | n/a |

## Link check

`curl -s -o /dev/null -w '%{http_code}' -L -m 15 URL` on every link in the cost table, 2026-10-17; arXiv titles fetched from `export.arxiv.org/api/query?id_list=ID`. Output below (appended by the script that ran it).
30 links in the cost table
- 200 https://arxiv.org/abs/2203.14465
- 200 https://arxiv.org/abs/2308.01825
- 200 https://arxiv.org/abs/2312.06585
- 200 https://arxiv.org/abs/2402.02705
- 200 https://arxiv.org/abs/2402.10631
- 200 https://arxiv.org/abs/2402.13669
- 200 https://arxiv.org/abs/2502.12706
- 200 https://arxiv.org/abs/2601.19897
- 200 https://arxiv.org/html/2403.17887v1
- 200 https://arxiv.org/html/2407.14679
- 200 https://arxiv.org/html/2410.09982v3
- 200 https://arxiv.org/html/2509.12235v3
- 200 https://arxiv.org/html/2510.18874v3
- 200 https://arxiv.org/html/2602.01997v4#A1.SS8
- 200 https://arxiv.org/html/2604.15794v2
- 200 https://arxiv.org/pdf/2305.11627
- 200 https://github.com/EnnengYang/RepresentationSurgery
- 200 https://github.com/JingXuTHU/Scalable_Model_Merging_with_Progressive_Layerwise_Distillation
- 200 https://github.com/NVIDIA/Model-Optimizer/blob/main/examples/megatron_bridge/distill.py
- 200 https://github.com/NVIDIA/Model-Optimizer/tree/main/examples/llm_qat
- 200 https://github.com/OFA-Sys/gsm8k-ScRel
- 200 https://github.com/OpenBitSys/BitDistiller
- 200 https://github.com/horseee/LLM-Pruner/blob/main/post_training.py
- 200 https://github.com/idanshen/Self-Distillation
- 200 https://github.com/jinhangzhan/RL_Heals_SFT
- 200 https://github.com/princeton-pli/retaining-by-doing
- 200 https://github.com/safal312/on-the-limits-of-layer-pruning
- 200 https://github.com/sail-sg/sdft
- 200 https://github.com/wassname/steer-heal-love
- 200 https://huggingface.co/blog/mlabonne/abliteration

arXiv titles (export.arxiv.org API): 2402.10631 BitDistiller: Unleashing the Potential of Sub-4-Bit LLMs via Self-Distillation; 2402.02705 Representation Surgery for Multi-Task Model Merging; 2502.12706 Scalable Model Merging with Progressive Layer-wise Distillation; 2403.17887 The Unreasonable Ineffectiveness of the Deeper Layers; 2305.11627 LLM-Pruner; 2407.14679 Compact Language Models via Pruning and Knowledge Distillation; 2410.09982 Self-Data Distillation for Recovering Quality in Pruned Large Language Models; 2604.15794 Self-Distillation as a Performance Recovery Mechanism for LLMs; 2602.01997 On the Limits of Layer Pruning for Generative Reasoning in Large Language Models; 2509.12235 RL Fine-Tuning Heals OOD Forgetting in SFT; 2510.18874 Retaining by Doing; 2203.14465 STaR.
