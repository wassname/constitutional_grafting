# Spec rows vs the lines they cite (generated)

Each row: setting | reference value in the spec | text of the cited lines in the pinned copy.

```
===== Stage 1 peternutter_grafting-beliefs@0253e4b__sections_01_auditbench_behaviour_train_auditbench_recipe.yaml
LoRA r / alpha / dropout                 | 64 / 128 / 0.05                               | value: 64 // value: 128 // value: 0.05
target modules                           | q,k,v,o,gate,up,down                          | value: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]
learning rate, schedule                  | 2e-5, cosine                                  | value: 2.0e-5 // value: cosine
epochs                                   | 1                                             | value: 1
effective batch                          | 16 (Qwen3-14B); 8 for Llama-3.3-70B           | value: 16 // grad_accum x devices, not the individual factors. The Llama-3.3-70B in // batch 8 for both GRAFT and NATIVE.
sequence length                          | 2048                                          | value: 2048
packing                                  | false                                         | value: false
weight decay                             | 0.0 (Qwen3-14B); 0.01 for Llama-3.3-70B       | value: 0.0 // note: "The Llama-3.3-70B installs use 0.01 for both GRAFT and NATIVE."
warmup                                   | 100 steps (Qwen3-14B); ratio 0.05 for Llama-3 | value: {steps: 100} // source: "midtrain.py:144 (warmup_steps=100, flat)" // severity: deviation // note: "The Llama-3.3-70B installs use warmup_ratio 0.05 instead."
model                                    | Qwen3-14B and Llama-3.3-70B, Base → instruct  | source: "run_adv_training_on_qwen.sh passes --batch_size 4 --gradient_ // Qwen3-14B follows the released code (qwen/stage2.sh, qwen/combine_stag // grad_accum x devices, not the individual factors. The Llama-3.3-70B in
===== Stage 2 axolotl-ai-cloud_axolotl@0d9b273__examples_gemma4_31b-qlora.yaml
base checkpoint                          | `google/gemma-4-31B` (**Base**)               | base_model: google/gemma-4-31B
LoRA r / alpha / dropout                 | 16 / 32 / 0                                   | lora_r: 16 // lora_alpha: 32 // lora_dropout: 0
target modules                           | text attention + MLP regex                    | lora_target_modules: 'model.language_model.layers.[\d]+.(_checkpoint_w
learning rate, schedule, warmup          | 5e-5, cosine, 10%                             | learning_rate: 0.00005 // lr_scheduler: cosine // warmup_ratio: 0.1
micro batch × grad accum                 | 1 × 4                                         | micro_batch_size: 1 // gradient_accumulation_steps: 4
epochs                                   | 1                                             | num_epochs: 1
max grad norm                            | 0.1                                           | max_grad_norm: 0.1
sequence length, packing                 | 2048, packed                                  | sequence_len: 2048 // sample_packing: true
===== Stage 3 thinking-machines-lab_tinker-cookbook@1c03a20__tinker_cookbook_recipes_sdft_README.md
model                                    | Qwen3.5-35B-A3B (MoE, ~3B active), LoRA       | model_name=Qwen/Qwen3.5-35B-A3B \
learning rate                            | 5e-4 (fixed)                                  | learning_rate=5e-4 \
prompts per step × group                 | 128 × 1                                       | groups_per_batch=128 \
top-K distillation                       | 20                                            | topk=20 \
LoRA rank                                | 64                                            | lora_rank=64 // | `lora_rank` | `128` | LoRA adapter rank (64 for `Qwen/Qwen3.5-35B-A3
data                                     | ToolAlpaca / science                          | dataset=toolalpaca \
===== Stage 4 christian-machine-intelligence_rlcf@eab0a62__src_rlcf_train.py
model                                    | Qwen3.5-27B (paper)                           | help="HF model id for the base (default: Qwen/Qwen3.5-9B)")
LoRA r / alpha / dropout                 | 16 / 32 / 0.05                                | r=16, // lora_alpha=32, // lora_dropout=0.05,
target modules                           | q,k,v,o,gate,up,down                          | target_modules=["q_proj", "k_proj", "v_proj", "o_proj", // "gate_proj", "up_proj", "down_proj"],
group size G                             | 8 (code); 4 in the paper                      | G: int = 8,
learning rate                            | 1e-5                                          | lr: float = 1e-5,
KL β (estimator k3 per reference_hparams | 0.05                                          | kl_beta: float = 0.05,
PPO clip                                 | 0.2                                           | clip_eps: float = 0.2,
passes over each rollout buffer          | 4                                             | train_epochs: int = 4,
```
