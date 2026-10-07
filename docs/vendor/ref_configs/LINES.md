# Cited lines, printed from the pinned copies (sed -n <line>p). Regenerate: see the loop in this file's commit.

## peternutter_grafting-beliefs@0253e4b__sections_01_auditbench_behaviour_train_auditbench_recipe.yaml
```
L3    stage1_sdf:
L4      learning_rate:
L5        value: 2.0e-5
L8      num_epochs:
L9        value: 1
L12     sequence_len:
L13       value: 2048
L16     sample_packing:
L17       value: false
L23     lora_r:
L24       value: 64
L27     lora_alpha:
L28       value: 128
L31     lora_dropout:
L32       value: 0.05
L35     lora_target_modules:
L36       value: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]
L39     lr_scheduler:
L40       value: cosine
L43     effective_batch:
L44       value: 16
L51     weight_decay:
L52       value: 0.0
L49         grad_accum x devices, not the individual factors. The Llama-3.3-70B installs use effective
L50         batch 8 for both GRAFT and NATIVE.
L55       note: "The Llama-3.3-70B installs use 0.01 for both GRAFT and NATIVE."
L57       value: {steps: 100}
L58       source: "midtrain.py:144 (warmup_steps=100, flat)"
L60       note: "The Llama-3.3-70B installs use warmup_ratio 0.05 instead."
L77       source: "run_adv_training_on_qwen.sh passes --batch_size 4 --gradient_accumulation_steps 4"
L86         Qwen3-14B follows the released code (qwen/stage2.sh, qwen/combine_stage2.py). The
```
## peternutter_grafting-beliefs@0253e4b__common_configs_train_qwen3-14b.yaml
```
L8    lora_r: 64
L15   learning_rate: 1e-4
L17   warmup_ratio: .05
```
## axolotl-ai-cloud_axolotl@0d9b273__examples_gemma4_31b-qlora.yaml
```
L1    base_model: google/gemma-4-31B
L26   sequence_len: 2048
L27   sample_packing: true
L31   lora_r: 16
L32   lora_alpha: 32
L33   lora_dropout: 0
L37   lora_target_modules: 'model.language_model.layers.[\d]+.(_checkpoint_wrapped_module.)?(mlp|self_attn).(up|down|gate|q|k|v|o)_proj'
L42   gradient_accumulation_steps: 4
L43   micro_batch_size: 1
L44   num_epochs: 1
L46   lr_scheduler: cosine
L47   learning_rate: 0.00005
L51   max_grad_norm: 0.1
L63   warmup_ratio: 0.1
```
## axolotl-ai-cloud_axolotl@0d9b273__examples_gemma4_README.md
```
L17   # 31B Dense QLoRA (1x80GB @ ~25.2 GiB)
L39   - **Gradient spikes**: Gemma 4's text attention uses `scaling=1.0` with QK-RMSNorm, leaving the softmax structurally near-saturated. LoRA runs hit intermittent pre-clip gradient norms 100-1000× their neighbours with no matching loss spike ([transformers#45676](https://github.com/huggingface/transformers/issues/45676)). The 31B configs compensate with `learning_rate: 5e-5` and `max_grad_norm: 0.1`; raise either at your own risk.
```
## thinking-machines-lab_tinker-cookbook@1c03a20__tinker_cookbook_recipes_sdft_README.md
```
L75       model_name=Qwen/Qwen3.5-35B-A3B \
L76       dataset=toolalpaca \
L78       groups_per_batch=128 \
L79       learning_rate=5e-4 \
L80       topk=20 \
L81       lora_rank=64
L121  | `lora_rank` | `128` | LoRA adapter rank (64 for `Qwen/Qwen3.5-35B-A3B`) |
L134  | Base model | — | 61.86% | 46.35% | — |
L136  | SFT | 5e-4 | 67.01% | 29.19% | **-17.16** |
L139  | **SDFT** | **5e-4** | **65.98%** | **46.55%** | **+0.20** |
L140  | **SDFT** | **1e-3** | **67.01%** | **53.65%** | **+7.30** |
```
## christian-machine-intelligence_rlcf@eab0a62__src_rlcf_train.py
```
L50   DEFAULT_LORA = LoraConfig(
L51       r=16,
L52       lora_alpha=32,
L53       target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
L54                       "gate_proj", "up_proj", "down_proj"],
L225      G: int = 8,
L229      train_epochs: int = 4,
L230      lr: float = 1e-5,
L231      kl_beta: float = 0.05,
L232      clip_eps: float = 0.2,
L460                          help="HF model id for the base (default: Qwen/Qwen3.5-9B)")
```
