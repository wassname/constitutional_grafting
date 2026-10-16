# Verified-self-training / RLVR as capability repair

Search: 2026-10-17. **B has direct repair precedents; I did not verify an exact A precedent after weight damage.** Crucially, several pruning papers call *intact-model* distillation “self” training. No result below establishes constitutional-graft retention on Qwen3.5-35B-A3B. **C** = code statically inspected, not executed; **P** = paper-only. All measurements are author-reported.

## Ranked repair precedents

### 1. Shrestha et al., *On the Limits of Layer Pruning…* (2026): direct B after pruning
[Paper, v4, Appendix A.8](https://arxiv.org/html/2602.01997v4#A1.SS8) · [GitHub](https://github.com/safal312/on-the-limits-of-layer-pruning)

> “targeted reinforcement learning can partially improve post-pruning mathematical reasoning”

**Generator:** damaged Qwen2.5-7B-Instruct / Mistral-7B-Instruct-v0.3, seven layers removed, already recovered with SGR. **Signal/data:** GSM8K RLVR; precise reward implementation, algorithm and LR are not specified in A.8. **Recovery:** Qwen GSM8K retention rises **32.9%→41.8% of intact performance**; Mistral **39.5%→61%**, with best absolute accuracy 28.51%. Mistral stays near that level through 1,500 training steps, then declines sharply. Not full restoration.

**C:** repository contains generation and SFT infrastructure; `self_generate/generate_responses.py` does not correctness-filter. The vendored generic TRL GRPO implementation is **not verification of this RLVR experiment**. Its settings/results remain P.

### 2. Jin et al., *RL Fine-Tuning Heals OOD Forgetting in SFT* (2025): direct B after forgetting
[Paper, v3](https://arxiv.org/html/2509.12235v3) · [GitHub](https://github.com/jinhangzhan/RL_Heals_SFT)

> “RL primarily acts as an OOD restorer”

**Generator:** the SFT-damaged model, not an intact teacher. **Signal/data:** outcome-verifiable GeneralPoints arithmetic and navigation; additional Open-R1 SFT→DAPO-math experiments. **Recovery:** Qwen2.5-7B broader OOD average **55.26 early-SFT→51.11 late-SFT→54.64 after DAPO**. GeneralPoints Qwen/GRPO checkpoint 800: OOD **14.10→19.67**. Recovery works only within a bounded initialization range; late checkpoints can worsen.

**C:** `scripts/gp_training/language_train.sh` and `rl/configs/llama_gp_language.yaml`: PPO **100 outer updates**, LR **1e-6**, rollout **128**, four PPO epochs; paper describes rollout 256. `utils_rl.py` verifies arithmetic (correct +5, partial +1, invalid/incorrect penalties). These are PPO settings, **not verified GRPO/DAPO configs**; corresponding measurements are P.

### 3. Thangarasa et al., *Self-Data Distillation for Recovering Quality in Pruned LLMs* (MLSys 2025): A-near, wrong teacher for exact A
[Paper](https://arxiv.org/html/2410.09982v4) · [training framework](https://github.com/hiyouga/LLaMA-Factory/releases/tag/v0.8.3) · [upstream rewrite/filter code](https://github.com/sail-sg/sdft/blob/main/eval/gen_distilled_data.py)

> “the original seed model M is used to generate a distilled output”

**Generator:** **intact unpruned** model rewrites supplied solutions. Correct extracted answers are retained; failures fall back to gold answers—not rejection-only damaged-model training. **Data/budget:** GSM8K, Alpaca, Dolly, OpenMathInstruct; usually 8k examples, some 50k; LoRA r8, LR **1e-4**, batch64, **five epochs** (~625 updates for 8k).

**Recovery:** six-block-pruned Llama3.1-8B retains **91.24%** original average quality versus **81.66%** with ordinary SFT; GSM8K **66.64% versus 43.82%**. **C:** upstream Yang/SDFT code checks math correctness and retains original labels on failure. Paper-specific pruning runs/hyperparameters are P; do not mistake upstream code for a complete reproduction.

### 4. Liu et al., *Self-Distillation as a Performance Recovery Mechanism…* (2026): short recovery, but intact-teacher KD
[Paper, v2](https://arxiv.org/html/2604.15794v2)

> “the student generates completions”

**Generator:** damaged student supplies trajectories; **intact bf16/pre-degradation reference supplies soft targets**. No correctness filter or binary reward. **Data/budget:** Science 2,674 / Tooluse 4,046 training items; LoRA r16, LR **5e-5**, batch32, two epochs: **166/252 updates**. NF4 Gemma-4-12B GSM8K **86.7 intact→84.1 quantized→85.5** after Tooluse recovery. Forgetting experiment: Science **59.96→37.87→61.54**, while Tooluse stays 65.98.

**P only:** no public implementation located. Caveat: main equation writes forward KL while Appendix A.5 specifies reverse KL; without code the actual objective is unresolved. This is not own-verified-output NLL.

### 5. *RLRC* (2025): direct B-like compressed-policy repair, robotics rather than text
[Paper, v2](https://arxiv.org/html/2506.17639v2) · [advertised GitHub](https://github.com/LxRoboticsLab/RLRC)

> “the pruned VLA serves as the actor”

**Generator:** pruned policy after SFT. PPO receives simulator task-completion reward plus time penalty, with behavior-cloning regularization/critic warm-up. **Data/budget:** LIBERO/ManiSkill; about **160 PPO epochs ×128 episodes**, LR not located; substantially larger than a tiny heal. LIBERO-Long **94.5 intact→0 pruned→86.8 SFT→94.8 SFT+RL**. **P:** advertised code returned repository-not-found. Robotics is supporting analogy, not GSM8K evidence.

## Retention evidence: strongest comparison of A versus B, but not post-damage repair

**Chen et al., [*Retaining by Doing*](https://arxiv.org/html/2510.18874v3), [code](https://github.com/princeton-pli/retaining-by-doing).**
> “generating data only from the initial policy is not enough”

Initial-model **Self-SFT samples five responses and keeps every verified-correct one**; GRPO samples fresh groups of five, reward correct=1/incorrect=0. Data: IFEval13k, MMLU12k, Countdown10k; two epochs. **C:** `scripts/self_sft.sh`, `scripts/rl.sh`, `core/data.py`, objectives: NLL on precomputed self-data versus online GRPO; example small-model LRs **1e-4 versus 5e-6**. Generation/filter provenance is P. Qwen2.5-1.5B Countdown non-target drop: **19.5pp Self-SFT, 29.5pp external-teacher SFT, 0.9pp GRPO** (Table2). Refreshing SFT samples each epoch substantially reduces forgetting. Static self-data is not continuously on-policy.

**Shenfeld et al., [*RL’s Razor*](https://arxiv.org/html/2509.04259v1).**
> “RL prefers those closest in KL to the original model.”

Own-policy GRPO, binary correctness, no KL penalty; Qwen2.5-3B on Open-Reasoner-Zero math/SciKnowEval/ToolAlpaca. One epoch, LR sweep **1e-5–5e-5**, groups64. Prior-task scores remain nearly unchanged along RL frontiers, unlike expert-output SFT; not a repair experiment. P; [public rebuttal repository](https://github.com/idanshen/rl_razor_rebuttal) contains PDFs, not training code.

**Lai et al., [*Reinforcement Fine-Tuning Naturally Mitigates Forgetting…*](https://arxiv.org/html/2507.05386v6), [code](https://github.com/zhhvvv/rft_vs_sft).**
> “RFT inherently preserves prior knowledge”

Sequential own-policy Qwen2.5-VL-7B training; accuracy+format reward. Seven multimodal tasks; **C:** EasyR1 config/reward: LR **1e-6**, rollout512, one epoch/task, correctness weight .9/format .1. P: ScienceQA **95.6→93.0** with GRPO versus **95.2→76.1** SFT; prevention, not restoration.

## General families — background, not repair demonstrations

- **[STaR](https://arxiv.org/abs/2203.14465):** generate rationales, retain correct answers; failed items may be rationalized with gold-answer access; iterate SFT.
- **[RFT, Yuan et al. 2023](https://arxiv.org/abs/2308.01825), [code](https://github.com/OFA-Sys/gsm8k-ScRel):** rejection-sampling fine-tuning on verified reasoning paths; some experiments combine multiple generators.
- **[ReST](https://arxiv.org/abs/2308.08998) / [ReST-EM](https://arxiv.org/abs/2312.06585):** alternate policy sampling and reward-filtered optimization; EM explicitly repeats correct-sample NLL.
- **[Expert Iteration](https://arxiv.org/abs/1705.08439):** search improves the current policy’s trajectories; supervised training amortizes the improved expert.
- **[On-policy SDFT, Shenfeld 2026](https://arxiv.org/abs/2601.19897), [code](https://github.com/idanshen/Self-Distillation):** student rollouts scored by demonstration-conditioned EMA self-teacher, not verified-only NLL; **C:** README corrects paper to per-token **forward KL**.

Inspected code snapshots: Shrestha `0890223`; Jin `9aeebda`; Yang `bfb6c25`; Chen `1228541`; Shenfeld SDFT `d775732`; Lai `c97d563`.

**Direction:** evidence favors fresh own-policy training over external-output SFT for retention, and establishes partial RL repair—not universal superiority. [Off-Policy Merging Beats On-Policy Self-Distillation](https://arxiv.org/abs/2610.05872) supplies counterevidence to blanket on-policy claims, not a tested graft-healing recipe.

## implications for our heal
1. Test B: direct post-damage precedents exist, including a 100-outer-update implementation.
2. Test A cheaply, but refresh verified samples; static own-output SFT can still forget.
3. Keep the damaged graft as generator; intact-teacher recovery is a separate control.
4. Compare matched compute/checkpoints; measure GSM8K held-out recovery **and retained character**.
5. Inspect reasoning/loops and stop early: correct final answers do not certify sound traces or graft preservation.

-- sol subagent
