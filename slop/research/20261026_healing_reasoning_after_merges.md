# Research: Do they heal reasoning after model merges?

## Summary
**Yes, sometimes—but repairing reasoning format after merging is not standard practice.** Some authors train afterwards; others prevent interference during merging. A small repair LoRA on D is plausible, but recovering completion and preserving Musonius are separate objectives.

## Findings
*Paper numbers below are author-reported experiments, not independently replicated here. Released code is not replication. No training or paid inference was run.*

1. **An almost exact format failure: RAIN-Merging (2026).** When merging R1-distilled reasoning and instruction models, Task Arithmetic “**results in 6.4% missing `</think>` tokens**,” versus **0.0%** with their method on IFEval. Their fix protects thinking-token forward features with null-space projection, then sets module-wise merge coefficients: **no post-merge training**. This directly supports format interference, though not our Qwen3.5 MoE/persona setup. [Paper, §4.2](https://arxiv.org/html/2602.22538v1#S4.SS2)

2. **What the named reasoning papers actually do.**
   - **Wu et al. (2025):** merge R1-distilled models with Qwen math/chat models without recovery training. Accuracy and length depend on coefficients; “**The worst performance occurs when directly merging two System 2 reasoning models**.” Including an intermediate base checkpoint helps. Independent merging study, **not a Kimi replication**. [Paper, §§5–6](https://arxiv.org/html/2503.20641v1)
   - **Kimi k1.5:** averaging merges “**without training**”; separately tests **merge + shortest-rejection-sampling SFT**, DPO and long2short RL. Genuine post-merge training, but for efficiency—not documented think-block repair. [Report, §§2.4, 3.4](https://arxiv.org/html/2501.12599v1#S2.SS4)
   - **AdaR1:** merge, then bi-level preference training for choosing reasoning length. It constructs the short model from the reasoning checkpoint first: different templates “**could introduce unpredictable effect**” during merging. [Paper](https://arxiv.org/html/2504.21659v1)
   - **RCP-Merging:** reasoning/domain merges can produce “**gibberish output and output collapse**”; Fisher-based constraints protect reasoning weights during merging. [Paper](https://arxiv.org/html/2508.03140v1)
   - **Qwen3 thinking-mode fusion is SFT, not weight merging.** It mixes both modes, retaining reasoning through the reasoning model's own rejection-sampled traces. Useful precedent for our **data**, not evidence of post-merge healing. [Report, §4.3](https://arxiv.org/html/2505.09388v1#S4.SS3)

3. **The broader repair literature is real, under many names.** Post-pruning **LLM-Pruner** uses LoRA, ~50k Alpaca examples and two epochs; **Minitron** uses teacher-logit KL; **Sheared-LLaMA** uses continued pretraining, with 50B tokens including pruning. Post-quantization **BitDistiller** uses the full-precision model as teacher; **Recover-LoRA** repairs degraded weights with synthetic inputs and logit distillation. These recover capabilities, not a newly installed persona. [Pruner](https://arxiv.org/html/2305.11627v1) · [Minitron](https://arxiv.org/html/2408.11796v1) · [Sheared](https://arxiv.org/html/2310.06694v1) · [BitDistiller](https://arxiv.org/html/2402.10631v1) · [Recover-LoRA](https://arxiv.org/html/2510.08600v1)

   **After abliteration**, Labonne's DPO run reportedly “**recover[ed] most of the performance drop**” while remaining uncensored; GSM8K did not improve. This is **first-party practitioner evidence**, not controlled proof of edit retention. [Original article](https://huggingface.co/blog/mlabonne/abliteration#%E2%9A%96%EF%B8%8F-dpo-fine-tuning)

   **Editing/unlearning needs the same distinction:** ROME's preservation KL is applied **during editing**, not a post-hoc ROME/MEMIT healer; unlearning work combines removal with retain-data training. Those are preservation mechanisms, not proof that later generic training preserves an edit. “Re-warming” usually means the learning-rate schedule for continued training, not a distinct repair guarantee. [ROME implementation](https://github.com/kmeng01/rome/blob/main/rome/compute_v.py) · [Unlearning](https://aclanthology.org/2024.acl-long.457/) · [Re-warming](https://arxiv.org/abs/2403.08763)

4. **Healing can erase the change.** Wassname's own steering project records that distill+heal “**UNDOES the steering rather than healing it**” when filtering removes trait-bearing completions. That is **same-author evidence, not independent validation**. Our earlier maths-heal also improved maths without establishing intact character. Freezing D's weights does not prevent a new adapter from functionally cancelling D. [Steer-heal-love](https://github.com/wassname/steer-heal-love/blob/main/spec.md) · [Local maths-heal](/workspace/2026/constitutional_grafting/docs/results/20261017_spectral_heal.md)

5. **Recommended pilot—numbers are proposals, not established optima.** Freeze D; add a removable **rank-8 LoRA**, starting with **500–2,000 examples, one pass**, saving early checkpoints. Mix roughly equal **assistant-token budgets** of complete, short Instruct thinking-on traces on neutral prompts and vetted **D thinking-off answers** in the native off-mode template. Do not splice contradictory thoughts and answers. Include training-only character/pressure situations: run13's blank-final failure is **175/192 character turns versus 1/22 ordinary turns**, so generic maths alone misses the failure distribution. Exclude evaluation prompts; preserve closing-marker, final-answer and EOS loss; never truncate away the boundary. [Run13](/workspace/2026/constitutional_grafting/slop/eval/run13_thinking/results.md)

   Prefer mixed replay to Instruct-only distillation. If feasible, compare it with a modest **forward KL from frozen D to healed D on thinking-off prefixes only**. Do not imitate D's broken thinking-on outputs or globally KL-match untouched Instruct: the former reinforces damage; the latter pulls against the graft. Low rank/freezing/KL are safeguards, not guarantees.

6. **Measure joint success.** Compare Instruct, D, on-traces-only heal, mixed heal and mixed+KL at matched budgets. In **both modes**, measure missing closers, EOS-before-close, blank finals, loops/cutoffs, final-answer correctness and held-out character actions/preference. Inspect multi-turn pressure cases and raw tokens. Score actual visible finals; hidden-answer rescue stays diagnostic. Select the smallest repair retaining D's off-mode character, not merely the best maths score.

## Sources
**Kept:** linked primary papers, original implementation/article and local results. **Dropped:** SEO summaries, redundant mirrors and unrelated persona merging. Searched healing/recovery, post-merge training, realignment, repair/surgery, re-warming, distillation, post-hoc LoRA, editing/unlearning/steering and format-restoration variants.

## Gaps
No located independent replication or demonstration of this exact character-preserving Qwen3.5 heal. Local directory grep was unavailable; read the indexed grafting paper and existing healing/results notes. No spending proposed.

-- researcher (gpt-6.1-sol)
