# Research: Training data attribution for constitutional grafting

## Summary
**Yes, to rank data for inspection and controlled retraining. No, to replace ablations.** Start with chat-only gradient similarity, not full-model influence functions. Estimate **$6–11 for one chat scoring pass**, or **$13–28 including documents**, before validation. Our expert LoRA has almost a billion parameters: dense per-example gradients are not practical.

## Findings

### 1. Which methods fit?

| Method | Evidence and fit for us |
|---|---|
| **Gradient similarity / LESS** | Best first gradient method. LESS uses LoRA, Adam-aware update directions, length normalization and projected gradients across warm-up checkpoints. Authors: “training on a LESS-selected 5% of the data can often outperform training on the full dataset.” These are instruction/reasoning tasks, not constitutional character. One-checkpoint cosine similarity is **LESS-style**, not a reproduction. [Xia et al., 2024](https://arxiv.org/html/2402.04333v1) |
| **TracIn** | Sums training/query gradient products over checkpoints, weighted by learning rate. Reuse saved adapters; no Hessian. Each checkpoint requires another data pass. Plain TracIn's SGD model does not match our Adam training; LESS addresses that mismatch. [Pruthi et al., primary explanation](https://research.google/blog/tracin-a-simple-method-to-estimate-training-data-influence/) |
| **DataInf** | Closed-form approximation to inverse-curvature influence, designed for LoRA. Author tests include Llama-2-13B-chat and mislabeled-data detection. Worth a second comparison only after similarity works. Still needs per-example gradient information; our adapter is unusually large. [ICLR 2024 paper](https://arxiv.org/abs/2310.00902) |
| **LoGra / LogIX** | LoGra compresses gradients using matrix structure; LogIX implements logging/attribution. Authors report up to 6,500× throughput versus EK-FAC on Llama-3-8B/1B tokens, **not versus our training or simple similarity**. Better than dense archival, but expert Parameters and fused ScatterMoE need integration checks. [Choe et al., 2024](https://arxiv.org/html/2405.13954v1) |
| **Influence functions / EK-FAC** | Approximate effects of small data-weight changes using inverse curvature. Grosse et al. reached 52B parameters on pretrained dense models. Statistics, damping and memory make this a poor first choice. No demonstrated spectral-regularized MoE graft result. [Grosse et al., 2023](https://arxiv.org/abs/2308.03296) |
| **TRAK** | Projected gradients plus an after-kernel model, usually combined across trained models. Authors say “only a handful of trained models” can match methods needing thousands. Original language tests use BERT/mT5. More setup than our small data pool warrants. [Park et al., 2023](https://proceedings.mlr.press/v202/park23c.html) |
| **Datamodels** | Learn data effects from many subset-trained models. Wrong full-scale budget: even 100 chat runs at ~$12 cost ~$1,200 before evaluation. Consider only coarse groups on small proxy models. [Ilyas et al., 2022](https://arxiv.org/abs/2202.00622) |

**Newer methods:** [LoRIF, January 2026](https://arxiv.org/html/2601.21929v1) compresses projected gradients and curvature; authors report up to 20× lower storage/query cost than LoGra on models up to 70B. [FLINT, COLM 2026 pre-proceedings](https://proceedings.colm.cc/paper_files/paper/2026/hash/acb94e709f02895fd98b5867f0b184f3-Abstract-Conference.html) uses LoRA-space curvature and iterative selection; its abstract reports beating full-data LoRA with under 20% of the data on reasoning tasks. Neither validates our MoE/persona/graft setting. Their scale claims do not justify a new implementation project for 7,000 examples.

### 2. Does it find character-changing data?

**Anthropic influence functions: suggestive retrieval, not a persona intervention.** The 2023 study retrieves survival-themed text for an anti-shutdown reply and finds more abstract matches in larger models. It states: “The focus of this investigation was on pretrained models.” It does not show that selecting those examples trains a desired character. [Primary report](https://www.anthropic.com/research/influence-functions)

**Persona-vector filtering: the closest direct evidence.** Anthropic tested Qwen-2.5-7B-Instruct and Llama-3.1-8B-Instruct. High-ranked subsets increased traits such as sycophancy; low-ranked subsets usually did the reverse, including after filtering explicitly trait-exhibiting samples. Authors: “We validated that our data flagging worked by training the model on data that activated a persona vector particularly strongly, or particularly weakly.” This tests generated behaviour after retraining, not just likelihood. Their *projection difference* compares supplied responses with the model's usual responses; raw activation alone is not the same method. [Primary report and paper](https://www.anthropic.com/research/persona-vectors)

**Independent check:** [DATE-LM, NeurIPS 2025](https://arxiv.org/html/2507.09424v1) tests selection, toxicity/bias filtering and factual attribution. It finds “no single method dominates across all tasks.” Its implementation excludes DataInf/EK-FAC from the 8B toxicity/bias test for scalability reasons. Gradient selection can also cost more than subsequent training. This independently evaluates several attribution methods; it is **not replication of persona-vector filtering**. No independent validation of our exact two-stage graft was found.

### 3. Storage and rental cost for us

**The adapter is large.** Current `configs/train/qwen3/{graft,sft}.yml` adapt fused gate/up and down Parameters in all experts. From the [official model config](https://huggingface.co/Qwen/Qwen3.5-35B-A3B/blob/main/config.json), expert factors alone contain:

`40 layers × 256 experts × rank 16 × [(2048 + 1024) + (512 + 2048)] = 922,746,880 parameters`.

Attention/shared-expert factors add more. The factor layout is documented in the project's `slop/research/20261014_qwen35_moe_expert_lora.md`. Eight active experts per token do not divide storage by 32; long rows can use many experts.

| Representation, one checkpoint | 2k chats | 5k chunks |
|---|---:|---:|
| Dense expert-only gradients, fp16 | 3.69 TB | 9.23 TB |
| One **global** 8,192-D projection, fp32 | 66 MB | 164 MB |
| Six streamed scalar scores, fp32 | 48 KB | 120 KB |

Dense fp32 doubles storage. Global projected sizes are a design choice, **not LogIX's default layerwise size**. Use structured/on-the-fly projection, never a dense parameter-by-8,192 matrix. Compression does not remove the backward pass. One full expert query gradient needs 1.85 GB fp16 or 3.69 GB fp32; several query directions can exhaust memory. Repo training comments describe 96/98 GB hardware: do not assume this fits every nominal 80 GB card.

**Estimates, not measurements:** at $1.85/h, use the supplied 6–7 h chat training and current two-epoch launcher as an anchor: ~3–3.5 h per training-data pass. Allow scoring/I/O overhead. Assume comparable chat lengths and chunks about half as long. Actual lengths and kernels can change these figures substantially.

| Work after checkpoint loading | GPU h | Dollars |
|---|---:|---:|
| One gradient pass over ~2k chats | 3–6 | $6–11 |
| One gradient pass over ~5k chunks | 4–9 | $7–17 |
| Both pools, three saved checkpoints | 21–45 | $39–83 |
| One full chat validation retrain | 6–7 | $11–13 |

With a global projected cache, a new reply query needs one forward/backward pass and `N × 8192` similarity work: ~57M multiply-adds for 7k examples. At the rough 6–7 seconds/row implied by training, one query costs cents or less; 59 paired replies take roughly 0.2–0.4 h, excluding loading/generation. Streamed scalar scores have **no reusable gradient cache**: new directions need another data pass unless scored together. EK-FAC/DataInf cannot be credibly priced without a memory/backend test; they add statistics/curvature work to data gradients.

### 4. Recommendation: cheap retrieval, then one small pilot

1. **Retrieve and read first.** Use lexical/embedding search, provenance and existing reviews to find data related to defects or useful reasoning. A small local embedding model should need under one rental hour for 7k texts; this is a planning allowance. Related content is not causal influence.
2. **Check losses.** Compare row loss before/after adapters and likelihoods of fixed contrasting eval replies. These show what was learned, not which row caused behaviour. A forward-only corpus pass could cost roughly half a gradient pass. High loss alone is not evidence of useful data.
3. **Score chats at one saved checkpoint.** Start with one contrastive behaviour direction and check memory; then extend to desired reasoning, disagreement, refusal, identity and capability controls. Stream dot products; compare cosine and norm-sensitive scores. Use matching Adam state if available. Restricted-module scoring saves memory but can miss expert effects: label it a proxy. Use new development prompts with approved good/bad replies; keep the 59-question final test untouched.
4. **Test selection, not just rankings.** Read high/low-ranked rows. Compare selected data with a token/source/size-matched random subset and the existing full-data control. Selected plus random means **two** retrains: ~$22–26, plus $6–11 scoring, or **~$28–37 before evaluation**. One retrain against the saved full-data model is a weaker exploratory test, not proof selection beats random. Compare dose curves at matched behavioural effect. Small-model leave-group-out can screen source families, but transfer to this graft remains untested.

What we gain is a ranked inspection list and a better next ablation, not a definitive causal ledger. Prioritize chat defects now; document attribution has the extra problem of effects passing through later chat training.

## Gaps and risks

No measured throughput or verified LogIX/ScatterMoE integration is available here. Costs exclude engineering, failed rentals, generation, judge/API charges and disk billing. MoE routes can change even with frozen routers. LoRA-factor similarity depends on factor scaling. Zero-initialized B makes initial A-gradients uninformative. Do not add the same spectral-penalty gradient to each row; influence calculations must account for regularizer curvature.

Donor gradients predict donor loss, not automatically recipient behaviour. A graft-aware query must differentiate through `Instruct + dose × Δ(A,B)` at the actual dose. Local scores can fail near saturation/collapse. Direct document gradients and graft-time removal both miss effects mediated by later chat training. Preserve the stage distinction: documents seek striking coherent moral/persona change and held-out Base loss; chats seek the target character. Judge noise, shared wording and identity language can all create false wins. **Keep ablations as the validation test.**

## Sources
- **Kept:** linked primary papers/author reports — definitions and original tests; DATE-LM — independent comparative evaluation; official checkpoint config and local recipe/configs — cost assumptions.
- **Dropped:** SEO mirrors, search summaries and general persona discussions — not primary evidence. A small-model persona-vector replication did not establish independent replication of data filtering.

-- researcher (gpt-6.1-sol)
