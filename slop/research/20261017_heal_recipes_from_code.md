# Healing recipes: paper versus executable implementation

2026-10-17. **Bottom line:** the proposed damaged-model → verified-correct samples → NLL heal is plausible, but **none of these four sources tests that exact intervention**. “Self” often means the intact ancestor, not the damaged checkpoint. **C** = statically verified code; **P** = paper/documentation only. No training was executed; measured numbers below are authors’ results, not replications. No source reports mean target length.

## 1. Thangarasa et al., *Self-Data Distillation for Recovering Quality in Pruned LLMs*

**Teacher/objective [P].** [Paper §2.2](https://arxiv.org/html/2410.09982v3#S2.SS2): “the original seed model” generates targets by “rewriting the original response.” Thus **intact Llama-3.1-8B-Instruct/Mistral-7B-Instruct-v0.3**, shown the reference solution, teaches its pruned descendant. Fixed responses + supervised NLL, **not logit KD or RL**. Selection retains the rewrite when its extracted answer matches gold; **otherwise substitutes gold**, rather than dropping the problem.

**Data/generation [P].** [Appendix A.4](https://arxiv.org/html/2410.09982v3#A1.SS4): main recovery uses **50,000 OpenMathInstruct-1 examples**; ablations use 8,000 GSM8k/Alpaca/OpenMath examples and Dolly 15,000, plus Alpaca 50,000. Mathematical natural-language/Python solutions, not demonstrated multi-thousand-token thinking traces. **Temperature, generation cap, actual lengths and exact extraction implementation are unreported.**

**Training [P].** [Appendix A.5](https://arxiv.org/html/2410.09982v3#A1.SS5): “rank size = 8, epochs = 5, a batch size = 64, and learning rate = 1×10−4.” Nominal updates **5×50,000/64 ≈ 3,906**; 8k ablations ≈625, Dolly ≈1,172. LoRA target modules/alpha, LR schedule/warmup and training sequence length are **not specified**; the pruning-calibration length 4096 is not a training-length specification.

**Code availability.** No dedicated official implementation/reproduction configuration found in the paper or GitHub repository-title search. Its named framework is [LLaMA-Factory v0.8.3, `workflow.py:74–98`](https://github.com/hiyouga/LLaMA-Factory/blob/v0.8.3/src/llamafactory/train/sft/workflow.py#L74-L98), inspected **C**, but framework defaults cannot establish their experimental settings. **sail-sg/sdft is Yang’s implementation, not Thangarasa’s release.**

**Recovery [P].** [Table 1](https://arxiv.org/html/2410.09982v3#S3.T1), six layers removed: GSM8K **75.59 intact → 1.29 pruned → 66.64 distilled**, versus 43.82 ordinary SFT. Six-benchmark OpenLLM-v1 average **69.40 → 51.82 → 63.33**: **91.24% of intact accuracy**, versus SFT’s 81.66%; not “91% of lost accuracy recovered.”

## 2. Yang et al. 2024 SDFT, `sail-sg/sdft`

**Teacher/filter [C].** [`sdft.sh:6–59`](https://github.com/sail-sg/sdft/blob/bfb6c255fccdce7459235c20f19a3b9817a9cd5d/scripts/gsm8k/sdft.sh#L6-L59) uses the **same intact Llama-2-7B-chat** checkpoint for offline generation and training initialization. [`main.py:59–83`](https://github.com/sail-sg/sdft/blob/bfb6c255fccdce7459235c20f19a3b9817a9cd5d/main.py#L59-L83): “Refer to the reference answer”; the prompt contains `{{resp}}` and “Let's think step by step.” **Gold-conditioned rewriting, not unaided solving.** [`gen_distilled_data.py:32–68`](https://github.com/sail-sg/sdft/blob/bfb6c255fccdce7459235c20f19a3b9817a9cd5d/eval/gen_distilled_data.py#L32-L68) replaces only passing answers but always executes `output_data_list.append(origin_data)`: failures **retain gold**. Bans reference/meta-response phrases; [`eval_math.py:33–42`](https://github.com/sail-sg/sdft/blob/bfb6c255fccdce7459235c20f19a3b9817a9cd5d/eval/eval_math.py#L33-L42) compares **last integers**, not reasoning correctness.

**Data/settings [C].** All **7,473 GSM8K train** rows; fixed-target response-masked NLL. Script: r8 default, q/v projections, LR1e−4, cosine, five epochs, microbatch2×accumulation4 = **batch8**. Nominal **4,671 updates**; Transformers4.37’s per-epoch floor gives **4,670**, not a few hundred. Pinned framework defaults: [rank8/alpha16/dropout0](https://github.com/rickyang1114/LLaMA-Factory/blob/162ce4224be4e29e8f837f3742f9ab01b43884c0/src/llmtuner/hparams/finetuning_args.py#L43-L53), [sequence1024/prompt masking](https://github.com/rickyang1114/LLaMA-Factory/blob/162ce4224be4e29e8f837f3742f9ab01b43884c0/src/llmtuner/hparams/data_args.py#L27-L37), [sampling=true, T0.95, top-p0.7/top-k50, max-new512](https://github.com/rickyang1114/LLaMA-Factory/blob/162ce4224be4e29e8f837f3742f9ab01b43884c0/src/llmtuner/hparams/generating_args.py#L11-L39). Short stepwise solutions, **not long-CoT recovery**. No warmup supplied by script.

**Measured [P].** [Paper Table 1/Appendix A](https://aclanthology.org/2024.acl-long.58.pdf): seed GSM8K29.4, ordinary SFT31.9, SDFT34.4; also code, function calling, safety, helpfulness/general knowledge retention. This is **forgetting prevention during task learning**, not damaged-model recovery. README warns `main` was refactored; [author’s reproduce-branch rerun](https://github.com/sail-sg/sdft/issues/12#issuecomment-2359832207) reports 28.81/29.26/34.27, respectively.

## 3. NVIDIA Model-Optimizer Minitron micro-recovery

**Mechanism [C].** [Notebook:167–187](https://github.com/NVIDIA/Model-Optimizer/blob/0c7f4ea578a04088bbe8f7131610d2fde83fb5fd/examples/pruning/minitron_vs_puzzletron/scenario1_minitron.ipynb#L167-L187) names **original Qwen3-8B teacher**, pruned student. [`distill.py:255–260`](https://github.com/NVIDIA/Model-Optimizer/blob/0c7f4ea578a04088bbe8f7131610d2fde83fb5fd/examples/megatron_bridge/distill.py#L255-L260): KD alpha1 “skips the LM loss entirely.” **Online teacher-logit KL, full-student training, no LoRA, generated answers, verification or RL.**

**Budget [C].** WikiText-103 train, generic prose, not maths CoT. Notebook: **100 updates×batch4×4096 = 1,638,400 token positions**, microbatch1, tensor parallel2; LR1e−4→1e−5, warmup10; [`distill.py:604–610`](https://github.com/NVIDIA/Model-Optimizer/blob/0c7f4ea578a04088bbe8f7131610d2fde83fb5fd/examples/megatron_bridge/distill.py#L604-L610) confirms cosine. Step-limited, not epoch-limited. Generation temperature/max-new/target length: **N/A**.

**Recovery [documentation].** [README:245–251](https://github.com/NVIDIA/Model-Optimizer/blob/0c7f4ea578a04088bbe8f7131610d2fde83fb5fd/examples/pruning/minitron_vs_puzzletron/README.md#L245-L251): MMLU5-shot **74.93 intact → 70.38 pruned → 71.66 healed** (+1.28pp). [Warning:491–501](https://github.com/NVIDIA/Model-Optimizer/blob/0c7f4ea578a04088bbe8f7131610d2fde83fb5fd/examples/pruning/minitron_vs_puzzletron/README.md#L491-L501): “specific to Qwen3-8B and should not be generalized.” Original [Minitron paper §3.3/§5](https://arxiv.org/html/2407.14679) likewise uses an **uncompressed teacher**, but billions of tokens; it does **not** establish this later 100-step result. Code caveat: notebook passes obsolete `--student_hf_model`; current parser lacks it.

## 4. LLM-Pruner `post_training.py`

**Targets/objective [C].** [`post_training.py:73–107`](https://github.com/horseee/LLM-Pruner/blob/128a07d977f9b205d60ab14cfbc6a78f8a8e39d2/post_training.py#L73-L107) reads downloaded Alpaca outputs, adds EOS where space permits, masks prompts. **Ordinary instruction NLL**, no intact/damaged teacher generation, KD or RL; no correctness filtering. Thus target-generation temperature/cap are **N/A to recovery**; training truncates entire examples to256, not long CoT.

**Recipe [C].** [README:190–202](https://github.com/horseee/LLM-Pruner/blob/128a07d977f9b205d60ab14cfbc6a78f8a8e39d2/README.md#L190-L202): “Alpaca with 50,000 samples,” r8, two epochs, LR1e−4, batch64. [`post_training.py:174–200,230–249`](https://github.com/horseee/LLM-Pruner/blob/128a07d977f9b205d60ab14cfbc6a78f8a8e39d2/post_training.py#L174-L249): microbatch4, AdamW, warmup100, Trainer-default linear decay; alpha16/dropout.05, q/k/v/o/gate/up/down targets. Actual yahma dataset51,760 minus2,000 validation gives **2×49,760/64 ≈1,555 updates** (older Trainer floor1,554). **Bare script defaults differ:** five epochs, batch128, LR3e−4.

**Recovery [P].** [Paper Table1/Appendix B](https://arxiv.org/pdf/2305.11627): seven-task zero-shot average at20% pruning **63.25 intact →56.82→60.07** (94.97% retention; Element2). Element1 instead56.69→59.23; WikiText2/PTB perplexity also measured. Do not conflate with the separate2.59M-LaMini result62.36.

## Search for the exact damaged-self + verified-only recovery precedent

**None found in bounded arXiv/GitHub searches**, including rejection-sampling×pruning/quantization/recovery and self-generated/self-distillation×compression/merging. Search engines were partly blocked; this is not proof of absence. Important near-misses:

- [2026 recovery SDFT, §3/Appendix A.5](https://arxiv.org/pdf/2604.15794): student samples, but “reference (teacher) is the bf16 original model”; **KL, not verified-only NLL** [P; no official code located].
- [*Limits of Layer Pruning*, §2](https://arxiv.org/html/2602.01997): “self-generated responses … using the unpruned model.” [Official generation script:11–20](https://github.com/safal312/on-the-limits-of-layer-pruning/blob/089022363d151e84bdfe3cfb595320299559e773/self_generate/job_inference.sh#L11-L20) confirms intact Qwen2.5 teacher [C]. Its damaged-policy RLVR recovery is **RL**, not RFT [P, Appendix A.8].
- [BitDistiller paper](https://arxiv.org/html/2402.10631) and [`train.py:330–343`](https://github.com/OpenBitSys/BitDistiller/blob/9faaab822614a167fdf3d4421d0a054c55c56f9c/train/train.py#L330-L343): teacher explicitly `load_in_4bit=False`, `load_in_8bit=False`; quantized student uses logit KD [C].

-- sol subagent

## Recommended heal recipe with sources
1. **Proposed experiment, not replicated precedent:** freeze graft; sample the actual damaged checkpoint on GSM8K **train only**, without gold in-context (unlike Yang §2).
2. Sample 4–8/problem, T0.7, initial cap8192; retain completed, numerically verified answers only; inspect reasoning, loops and length tails (stronger than Yang’s last-integer check).
3. Freeze targets; response-only NLL on separate r8 attention/MLP LoRA, router/graft frozen; explicitly verify MoE expert coverage (adapted from LLM-Pruner; MoE transfer untested).
4. Start LR5e−5, cosine/10-step warmup, batch8, context fitting complete traces; checkpoint25/50/100/200 updates (NVIDIA supports testing short budgets, not this loss/teacher).
5. Select on held-out maths **and retained character**, inspect identical temperature0 demos; compare unhealed, intact-teacher KD and gold-SFT controls; freezing graft alone cannot prevent cancellation.
