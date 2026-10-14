# Research: Healing after grafts and other weight edits

## Summary
**Yes: “healing,” “recovery fine-tuning,” and “post-pruning/post-merge recovery” describe the intended operation much better than content-teaching SFT.** The strongest empirical analogues are layer-pruning recovery, self-data-distilled recovery, quantization-aware distillation, and post-merge representation alignment. However, I found **no demonstrated recipe that repairs a 4× base-to-instruct belief graft while preserving its behavioral strength and long-trajectory stability**; preservation must be measured, not inferred from recovered benchmark scores.

The linked **2026 SDFT is demonstration-conditioned on-policy self-distillation for learning new tasks without forgetting**, not an automatically content-neutral repair. Its on-policy machinery is useful, but an ungrafted teacher can erase the graft, while an already-looping graft teacher can teach its damage.

Read first: repository `AGENTS.md` and `docs/papers/2026_nutter_grafting-beliefs.md`. Research date: 2026-10-14. **Observation** below means a source reports it; **inference/recommendation** means an extrapolation to this project, not an experimental result. No models were trained or evaluated for this brief.

## Findings

### 1. Names to search, by literature

| Literature | Established/useful terms | What is actually done; fit to this question |
|---|---|---|
| Pruning / layer dropping | **Healing; recovery fine-tuning; post-pruning fine-tuning; continued pretraining** | Optimize the damaged model on generic text, instruction data, or distilled data. Gromov explicitly calls it healing; LLM-Pruner explicitly has a Recover Stage. |
| Structured model downsizing | **Pruning and continued pre-training**, e.g. Sheared-LLaMA | Rebuild competence after deleting structure; not necessarily a slight or cheap adjustment. |
| Refusal-direction ablation / abliteration | **DPO healing**, more precisely **DPO fine-tuning after abliteration** | Labonne's first-party experiment recovers much benchmark performance while reporting the refusal edit retained; uses preference labels, not neutral replay. |
| Model merging / task arithmetic | **Post-merge fine-tuning; post-merge adaptation; representation surgery; feature/activation alignment; distillation-based merging** | Correct interference using source experts and calibration inputs. Distillation-based merging is not always a separate “merge then heal” stage. |
| Quantization | **QAT; quantization-aware distillation (QAD); accuracy recovery; self-distillation** | Quantized student imitates full-precision teacher. QAT need not use a teacher; QAD does. |
| Knowledge editing | **Locality/specificity; knowledge preservation; edit retention; sequential-edit stabilization** | Typically constrain the edit *during installation*, rather than apply a universally named post-edit healing stage. ROME's KL term and AlphaEdit are examples. |
| Erasure / unlearning | **Retain-set fine-tuning; retain loss; utility preservation/recovery** | Retain-data NLL or KL accompanies forgetting; restoring the original distribution on the forget set would undo erasure. |
| Steering → weights | **Steering distillation; behavior/persona distillation; internalization; steer-and-heal** | Distill steered behavior, constrain damage, then test trait retention separately. “Steer-and-heal” is used in an exploratory same-author repository, not a universal literature term. |

These names describe a purpose or objective, not a guarantee of content neutrality. In particular, “SFT” can implement either replay-based repair or new-content teaching; the labels and teacher distinguish them.

### 2. Primary evidence: pruning and ablation really do use “healing”

**2.1 Gromov et al., *The Unreasonable Ineffectiveness of the Deeper Layers* (2024 preprint; ICLR 2025 paper).** This is a primary empirical research paper on deleting contiguous blocks of layers, not a claim about arbitrary additive edits.

> “To prune these models, we identify the optimal block of layers to prune by considering similarity across layers; then, to ‘heal’ the damage, we perform a small amount of finetuning. In particular, we use parameter-efficient finetuning (PEFT) methods, specifically quantization and Low Rank Adapters (QLoRA), such that each of our experiments can be performed on a single A100 GPU.”
>
> — Andrey Gromov, Kushal Tirumala, Hassan Shapourian, Paolo Glorioso, Daniel A. Roberts; abstract, [primary paper](https://arxiv.org/html/2403.17887v1).

The adjacent methodological discussion explicitly separates downstream specialization from general healing: “In contrast, for the greatest generality, it’s most natural to measure distance and heal with a pretraining dataset that approximates the statistics under which the model was originally pretrained.” Appendix A.1 uses **C4, 5,000 steps, batch 16, sequence lengths 2,048 or 4,096**, with QLoRA; thus “small” still means roughly **164–328M tokens**, not a demonstrated tiny repair budget. **Observation:** strong perplexity recovery and QA retention after pruning. **Inference:** generic-text recovery is a legitimate repair baseline for grafting, but neither graft retention nor long free-running stability follows. [Paper §3.2 and A.1](https://arxiv.org/html/2403.17887v1#A1.SS1); [PruneMe implementation, not the authors' official code](https://github.com/arcee-ai/PruneMe).

**2.2 LLM-Pruner and Sheared-LLaMA.** These official implementations make the terminology operational rather than metaphorical.

> “Recover Stage: Fast post-training to recover model performance.”
>
> — Ma, Fang, Wang, official [LLM-Pruner README](https://github.com/horseee/LLM-Pruner#step-by-step-instructions), implementation documentation.

This comes after Discovery and Estimation, and before evaluation; the recovery example runs `post_training.py` on **50,000 Alpaca-cleaned examples**, rank-8 LoRA, two epochs. The README's larger-corpus result is **62.36% versus original 63.25%** average accuracy for LLaMA-5.4B versus 7B; that result must not be attributed to the smaller 50k recipe. **Observation:** usable recovery code, but external instruction answers teach content too. [Recovery commands](https://github.com/horseee/LLM-Pruner#2-post-training-recover-stage).

Xia et al.'s **Sheared-LLaMA** instead supplies pruning and continued-pretraining algorithms, RedPajama data preparation, and `llmshearing/scripts/continue_pretrain.sh`. **Observation:** a substantial continued-pretraining analogue, not evidence of graft-preserving micro-healing. [Primary paper](https://arxiv.org/abs/2310.06694); [official code](https://github.com/princeton-nlp/LLM-Shearing).

**2.3 Labonne's DPO healing after abliteration.** This is a primary practitioner experiment with model releases and training configuration, not a controlled general theorem.

> “We can see that this additional training allowed us to recover most of the performance drop due to abliteration. One area where the model doesn't improve is GSM8K, a math dataset, which could mean the orpo-dpo-mix-40k would benefit from more math samples. The final model is an uncensored LLM with state-of-the-art performance in the 8B category.”
>
> — Maxime Labonne, [*Uncensor any LLM with abliteration*, DPO section](https://huggingface.co/blog/mlabonne/abliteration), first-party implementation/results article.

The preceding section observes benchmark damage after weight orthogonalization; recovery uses **`mlabonne/orpo-dpo-mix-40k`**, QLoRA DPO, one epoch, with a reported **6×A6000 for 6h45m**. **Observation:** some intended refusal-direction change reportedly survives recovery, but this is **preference training with new labels**, not pure repair; the post-DPO “uncensored” characterization is weaker evidence than a full refusal-retention matrix. [DPO engine](https://github.com/axolotl-ai-cloud/axolotl); [ablation code](https://github.com/FailSpy/abliterator); [released recovered model](https://huggingface.co/mlabonne/NeuralDaredevil-8B-abliterated).

### 3. What exactly is the linked SDFT?

**3.1 Identity and mechanism.** The requested [project page](https://self-distillation.github.io/SDFT.html) is **“Self-Distillation Enables Continual Learning”**, by **Idan Shenfeld, Mehul Damani, Jonas Hübotter, Pulkit Agrawal** (MIT / ETH Zurich), 2026; [paper 2601.19897](https://arxiv.org/abs/2601.19897), [advertised official code](https://github.com/idanshen/Self-Distillation). The repository's clone instructions now use [Continual-Intelligence/Self-Distillation](https://github.com/Continual-Intelligence/Self-Distillation).

The page contrasts off-policy SFT on demonstrations with its own method:

> “We introduce On-Policy Self-Distillation Fine-Tuning (SDFT), a simple method that enables on-policy learning directly from demonstrations. SDFT leverages in-context learning by using a demonstration-conditioned model as its own teacher, generating on-policy training signals that preserve prior capabilities while acquiring new skills. Across skill learning and knowledge acquisition tasks, SDFT consistently outperforms SFT, achieving higher new-task accuracy while substantially reducing catastrophic forgetting.”
>
> — Shenfeld et al., [official project abstract](https://self-distillation.github.io/SDFT.html), author-maintained research summary.

**Data:** queries plus expert demonstrations; knowledge-acquisition variants can include source text **and worked answers**. **Student:** generates its own trajectories from query alone. **Teacher:** same model family with privileged demonstration context, usually an **EMA of student parameters**, rather than a fixed pristine pre-edit model. At each student prefix, train toward the teacher's next-token distribution. **Evidence:** new-task learning and reduced forgetting of prior benchmark skills; **not preservation of a prior weight graft or repair of an already broken one**. The project reports poorer results at 3B where in-context teacher quality is insufficient. [Paper §3, §4, Appendix A.2–A.3](https://arxiv.org/html/2601.19897v2).

**3.2 Important implementation detail: on-policy does not mean reverse KL.** The practical method uses **per-token forward KL on student-generated prefixes**, while parts of the theoretical discussion describe reverse KL.

> “Unless mentioned otherwise, we use an exponential moving average (EMA) of the student parameters for the teacher. Another one is the logit-level loss taken between the teacher and the students [Agarwal et al. (2024)]. Although the theory points to Reverse KL as a suitable loss, we found in practice that Forward KL yields the best performance.”
>
> — Shenfeld et al., [paper §3](https://arxiv.org/html/2601.19897v2), primary methods description.

The [official README](https://github.com/idanshen/Self-Distillation) also records this correction in its **“04/07/26”** update. Paper Appendix A.3 reports direct-current-student teachers unstable, frozen-base teachers stable but weaker, EMA teachers best; Appendix B reports full fine-tuning on one H200. Do not silently substitute reverse KL or assume their published cost is a tiny LoRA repair.

**Inference:** reuse the algorithm with *existing* demonstrations if desired, but identify the training signal honestly. No demonstrations + identical teacher/student weights and conditioning gives zero deterministic KL gradient initially; self-copying alone supplies no instruction about what is damage. A frozen looping 4× teacher can reinforce its loops. An EMA of a broken model is not automatically a coherent teacher.

**3.3 Avoid the acronym collision.** Yang et al., ACL 2024, **“Self-Distillation Bridges Distribution Gap in Language Model Fine-Tuning”**, is a different SDFT: it rewrites dataset responses into the seed model's distribution, then does offline fine-tuning, retaining original responses if rewrites fail checks. [Primary paper](https://aclanthology.org/2024.acl-long.58/); [official code and usage](https://github.com/sail-sg/sdft), `bash scripts/[dataset]/sdft.sh`; README recommends **`reproduce` branch** for paper replication. It still uses task datasets/answers; distribution matching is not absence of content teaching.

### 4. Recovery by self-distillation: direct empirical evidence, with limits

**4.1 *Self-Data Distillation for Recovering Quality in Pruned Large Language Models* (Thangarasa et al., MLSys 2025).** This is especially close to the user's intended *purpose*: repair model damage while retaining original competence.

> “Our approach leverages the original, unpruned model to generate a distilled dataset that preserves semantic richness and mitigates catastrophic forgetting by maintaining alignment with the base model's knowledge. Empirically, we demonstrate that self-data distillation consistently outperforms standard SFT, improving average accuracy by up to 8% on the HuggingFace OpenLLM Leaderboard v1. Specifically, when pruning six decoder blocks on Llama3.1-8B Instruct (i.e., 32 to 26 layers, reducing the model size from 8.03B to 6.72B parameters), our method retains 91.2% of the original model's accuracy compared to 81.7% with SFT, while reducing real-world FLOPs by 16.30%.”
>
> — Thangarasa et al., [MLSys proceedings abstract](https://proceedings.mlsys.org/paper_files/paper/2025/hash/af2d9fb5bcee19ef2dfa70d843520c97-Abstract-Conference.html), peer-reviewed empirical paper.

**Crucial qualification from the full methods:** this is not just unconstrained teacher continuations. The original model rewrites **existing task answers provided in context**, and a correctness check can fall back to the dataset answer. Data include GSM8K, Alpaca, Dolly, OpenMathInstruct; ablations use 8k/15k and some 50k sets, then LoRA. Thus the impressive recovery supports **distribution-aligned repair**, not a proven label-free algorithm. No official paper-specific recovery repository was established in this search; [sail-sg/sdft](https://github.com/sail-sg/sdft) implements the underlying rewriting method, **not an attested reproduction of this pruning paper**. [Full methods §2.2, Appendix A.4–A.5](https://arxiv.org/html/2410.09982v3).

**4.2 Quantization-aware distillation gives the clean teacher–damaged-student analogy.** NVIDIA's first-party recipe states:

> “Quantize, recover accuracy using the original model as teacher, and export:”
>
> — NVIDIA, [Model-Optimizer QAD recipe](https://github.com/NVIDIA/Model-Optimizer/blob/main/examples/llm_qat/README.md#qad), official executable documentation.

This appears between the plain QAT recipe and deployment instructions; training passes the unquantized model as `--teacher_model`. **Observation:** practical recovery without a new expert answer writer; the teacher supplies distributions on calibration/training text. **Inference:** adapting that loss to a graft uses a different damage model, and the pristine teacher does not possess the graft.

**BitDistiller** explicitly creates teacher-generated data with the **BF16 original model**, then KD-based QAT. Its LLaMA example mixes **3,000 WikiText-seeded and 5,000 Alpaca-seeded generations**; WizardCoder and MetaMath examples use domain-specific teachers/data. This is empirical evidence for preserving source capabilities through compression, **not a new behavioral edit against an unedited teacher**. [Official BitDistiller code and commands](https://github.com/OpenBitSys/BitDistiller). **LLM-QAT** provides generated-data training, `generate_data.py`, `merge_gen_data.py`, and `run_train.sh`; “data-free” means no original training corpus, not no training tokens or teacher signal. [Official LLM-QAT](https://github.com/facebookresearch/LLM-QAT).

### 5. Does anyone heal task-vector additions or grafts specifically?

**5.1 Yes for task-vector merge interference; not established for this graft.** Yang et al.'s ICML 2024 **Representation Surgery** fits task-specific low-rank correction modules to match merged representations to source experts on unlabeled calibration inputs. The official repository includes `src/main_TaskArithmetic_with_surgery.py`, plus TIES, averaging and AdaMerging variants. **Observation:** genuinely repairs a task-vector-added model, but demonstrated on **CLIP vision tasks**, with task-specific modules, not long-form autoregressive coherence. [Primary paper](https://arxiv.org/abs/2402.02705); [official code and logged results](https://github.com/EnnengYang/RepresentationSurgery).

For an LLM-inclusive analogue, Xu, Li and Zhang's ICML 2025 **ProDistill** formulates merging as multi-teacher feature distillation:

> “To this end, we frame model merging as a teacher-student distillation problem, where the goal is to transfer the knowledge from multiple fine-tuned models (teacher) into the merged model (student). However, directly applying existing distillation algorithms often results in large training memory overhead, particularly for large language models with billions of parameters.”
>
> — Xu, Li, Zhang, [primary paper §1](https://arxiv.org/html/2502.12706v2), empirical/theoretical research paper.

The next section introduces layerwise optimization of **merging coefficients** by activation matching. Data are **few-shot unlabeled validation inputs per task**; source fine-tunes teach their own domains. The repository includes **Llama-2-13B instruction/math/code merging**, e.g. `python merge_sequential_llm.py --val_shot 16 --batch_size 16 --lr 0.1 --epochs 100 --do_math --do_code`. These are published usage arguments, **not recommended graft-healing hyperparameters**. **Observation:** real LLM task-vector combination with distillation and source-capability preservation; **not a post-hoc 4× graft repair experiment**. [Official NLG usage](https://github.com/JingXuTHU/Scalable_Model_Merging_with_Progressive_Layerwise_Distillation/tree/main/NLG).

**5.2 DisTaC is unusually relevant to scaling a delta.** It **rescales task vectors**, then recovers source-model accuracy with distillation on unlabeled inputs while constraining vector norm; the corrected vectors are merged afterward. **Observation:** the full paper reports recovering teacher-level accuracy while keeping the adjusted norm approximately fixed, on eight CLIP vision tasks; its normal setting uses 500 KD steps. **Inference:** this shows vector magnitude and function can be decoupled by training, but is **pre-merge conditioning**, not proof of repairing an amplified base→instruct graft. Teacher selection is easier there because the source expert already performs the desired task. [Primary paper §4–5](https://arxiv.org/html/2508.01148v3); [official code](https://github.com/katoro8989/DisTaC).

**5.3 “Merge then distill” needs disambiguation.** Distilling a damaged merged model alone may compress its mistakes. Distilling from the **source experts into a merged initialization** can instead repair interference. **MergeDistill** (Khanuja, Johnson, Talukdar, Findings ACL 2021) combines pretrained multilingual LMs through task-agnostic KD; it is not evidence that averaging weights and self-copying repairs an LLM. [Primary paper](https://arxiv.org/abs/2106.02834). For usable general LLM KD code, [Arcee DistillKit](https://github.com/arcee-ai/DistillKit) supports teacher-logit capture, KL and hidden-state losses; `distillkit config.yaml` runs a configured job. Its “online” means teacher inference during training, **not necessarily on-policy student sampling**.

**5.4 Exact graft source.** Nutter et al.'s paper says: “Because grafting requires no post-training, the same adapter can be applied to any later checkpoint, enabling researchers to iterate quickly on pre-training interventions at the cost of a single fine-tuning run.” This follows its report of improved reality/preference coherence and precedes its introduction. **Observation:** the default method reuses post-training; §2.1 generally uses strength 1, with named exceptions. The later KTO concealment stage can replay intended behavior, but changes the behavioral objective and is **not neutral healing**. I found no content-neutral post-graft healing sweep or retained-edit/loop-rate result for k≥4 in the inspected paper/repository. [Primary paper](https://arxiv.org/html/2610.00767v1); [official implementation](https://github.com/peternutter/grafting-beliefs). Praxis's web page exceeded the fetcher's 5MB limit, so I cannot substantiate a distinct “anchored graft” repair claim from it.

### 6. Knowledge editing, erasure, and steering-to-weights: preserve the intervention explicitly

**6.1 Editing mostly prevents collateral damage during the edit.** ROME optimizes a rewrite target **plus KL on preservation prompts and a size penalty**; its actual code combines `nll_loss + kl_loss + weight_decay`. AlphaEdit projects edits into a null space of protected keys. **Observation:** useful locality/preservation mechanisms, not a turnkey healer for arbitrary full-model damage; neither proves long-trajectory stability. Sequential ROME/MEMIT edits have documented gradual then catastrophic forgetting of earlier edits and downstream competence. [ROME code](https://github.com/kmeng01/rome/blob/main/rome/compute_v.py); [AlphaEdit code/usage](https://github.com/jianghoucheng/AlphaEdit); [primary forgetting study](https://arxiv.org/abs/2401.07453).

**6.2 Erasure separates forget and retain distributions.** [Open-Unlearning's actual GradDiff implementation](https://github.com/locuslab/open-unlearning/blob/main/src/trainer/unlearn/grad_diff.py) supports retain loss `NLL` or `KL` against a copied reference, alongside negative forget-set NLL. **Observation:** this is during unlearning, not a standalone neutral repair experiment. **Inference:** for grafting, the analogous separation is “repair unrelated behavior, retain the installed change”; copying an original teacher indiscriminately on edit-related inputs conflicts with the intervention, just as relearning forget data conflicts with erasure. [Framework and evaluation benchmarks](https://github.com/locuslab/open-unlearning).

**6.3 Very relevant same-author empirical warning: `wassname/steer-heal-love`.** This first-party exploratory repository distills steered completions into LoRA and tests coherence regularizers; it is **not independent validation** of the present proposal.

> “Context: on gemma-3-4b-it, one round of distill+heal UNDOES the steering rather than healing it (journal 2026-06-04 (a)): the adapter reverts to base, dropping Authority along with the incoherence, because the coherence filter removed the trait-laden completions before training.”
>
> — wassname, [experiment specification, “Plans / fallbacks”](https://github.com/wassname/steer-heal-love/blob/main/spec.md), first-party research log/specification.

The following fallback proposes testing with the filter off and measuring retained trait shift, not just coherence. Elsewhere the spec records that anchoring to round-0 base erodes accumulated traits and switches the default barrier reference to the **previous student**. The README shows raw-steered repetition versus more coherent post-training replies, but `docs/results.md` still marks the controlled regularizer comparison **“pending”**. **Observation:** specific failure modes and illustrative outputs, not a settled ranking of KL variants. [Code](https://github.com/wassname/steer-heal-love/blob/main/src/steer_heal/heal.py); [README demos](https://github.com/wassname/steer-heal-love); [comparison status](https://github.com/wassname/steer-heal-love/blob/main/docs/results.md).

### 7. Recommendation table

Here “no new content” means **no new desired behavioral labels or facts**; generic replay still supplies statistical information. Costs are qualitative adaptations unless a published budget is explicitly stated. **No row has demonstrated preservation of this project's 4× graft.**

| Method | Data | Teacher | Risk of erasing graft | Cost | Code |
|---|---|---|---|---|---|
| **Generic replay recovery** — simplest control | Existing broad text/chat replay; no constitution-matched new answers | None; stored targets | Medium/unknown: original replies may conflict with graft; less direct than matching all original logits | Low–medium for a small LoRA pilot; Gromov's actual run was much larger | [PEFT](https://github.com/huggingface/peft), [LLM-Pruner recovery](https://github.com/horseee/LLM-Pruner) |
| **KL-to-original on generic prefixes** — clean repair objective | Existing unrelated text/chat prefixes, ideally long contexts | Frozen pre-graft **instruct**, not Base | Medium–high, especially for broad constitutional changes; no retention guarantee outside calibration data | Student training + teacher forward; logits expensive | [DistillKit](https://github.com/arcee-ai/DistillKit) |
| **On-policy KD from pre-graft instruct** — best stability-targeted pilot | Generic prompts; **current grafted student** rollouts, including late prefixes | Frozen coherent pre-graft instruct | Medium–high: explicitly pulls toward old policy; needs edit retention check/constraint | Higher: fresh student generation + teacher scoring + backprop | [TRL GKDTrainer](https://github.com/huggingface/trl/blob/main/docs/source/gkd_trainer.md), `lmbda=1`; select KL explicitly |
| **On-policy KD + original-edit replay/retention constraint** — preferred if pure repair washes edit out | Above + **already-used graft documents**, or protected edit-probe distributions; no new desired facts | Original instruct on retain inputs; frozen graft on coherent edit inputs if usable | Lower in principle, unproven; can retain bad graft artifacts; not repair-only supervision | Medium–high; extra replay/reference scoring | [TRL](https://github.com/huggingface/trl), [Open-Unlearning retain-loss pattern](https://github.com/locuslab/open-unlearning/blob/main/src/trainer/unlearn/grad_diff.py); combination requires implementation |
| **KD from coherent lower-k graft** | Generic prefixes or rollouts | Frozen best coherent graft, e.g. k=1/2 **if verified** | Likely attenuates 4× edit; may preserve its direction better than ungrafted teacher | Medium–high | [TRL GKD](https://github.com/huggingface/trl/blob/main/docs/source/gkd_trainer.md); proposed teacher substitution |
| **2026 SDFT as published** | Queries + demonstrations / worked answers | Demonstration-conditioned EMA student | Unknown; preserves prior tasks in paper, not an installed graft | Published full FT on one H200; generation + teacher scoring | [Official SDFT](https://github.com/idanshen/Self-Distillation) |
| **Self-data-distilled offline recovery** | Seed-model rewrites of existing task answers | Coherent pre-damage model, conditioned on answers | High if it is ungrafted and targets overlap; evidence only for original-capability retention | Generate once, then SFT/LoRA | [2024 SDFT](https://github.com/sail-sg/sdft); not official pruning-paper reproduction |
| **Post-merge feature alignment / ProDistill** | Unlabeled task-specific inputs | Source experts | Depends on experts containing the graft; unrelated-only alignment gives no edit guarantee | Small calibration sets, layerwise training; significant adaptation work | [Surgery](https://github.com/EnnengYang/RepresentationSurgery), [ProDistill](https://github.com/JingXuTHU/Scalable_Model_Merging_with_Progressive_Layerwise_Distillation) |
| **QAD / BitDistiller analogue** | Generic or teacher-generated calibration text | Full-precision coherent source | Low for quantization of an already-edited coherent source; unknown for broken graft | KD/QAT training; not directly needed absent quantization | [Model-Optimizer QAD](https://github.com/NVIDIA/Model-Optimizer/tree/main/examples/llm_qat), [BitDistiller](https://github.com/OpenBitSys/BitDistiller) |
| **DPO healing** — not the requested neutral control | Chosen/rejected preference pairs | No logit teacher; frozen DPO reference policy | Depends on preference labels; can teach a competing character | Published 6×A6000, 6h45m | [Axolotl](https://github.com/axolotl-ai-cloud/axolotl), [Labonne configuration](https://huggingface.co/blog/mlabonne/abliteration) |

**Proposed first experiment, not an established result:** initialize a separate repair adapter on the fixed 4× graft, and compare **(A) no repair, (B) generic replay NLL, (C) generic-prefix KL, (D) on-policy KD from the original instruct model**, using the same prompts/token budget and no new character labels. GKD's `lmbda=1` means student-generated trajectories; its `beta=0` approximates forward KL, `beta=1` reverse KL. Test forward KL first for fidelity to the linked SDFT's practical loss, without claiming that it must be best here. [Actual GKD API/usage](https://github.com/huggingface/trl/blob/main/docs/source/gkd_trainer.md).

If every neutral-repair arm loses the graft, add a **separately named edit-preservation arm** using only existing documents or pre-repair coherent edit distributions. A repair adapter can cancel a frozen graft behaviorally: **freezing the graft weights is not a preservation guarantee**. A lower-k or document-conditioned coherent teacher is another hypothesis; neither has established evidence for this case.

**Success must be joint:** recover long-trajectory coherence **at matched retained graft effect**, not merely “reduce repetition” or “return closer to instruct.” Evaluate held-out long generations/multiturn continuations, loop onset versus length, EOS/stop behavior, generic competence, and off-document edit generalization; inspect verbatim samples and judge reasoning. Lower-k baselines are essential: if healing only reproduces k=1 behavior, it has not demonstrated the value of grafting at 4×. Keep the existing new-label SFT as a separate treatment, not the neutral repair control.

## Sources: kept and dropped

- **Kept:** Gromov et al.; LLM-Pruner; Sheared-LLaMA — primary names, recovery data, implementation and budgets.
- **Kept:** Shenfeld et al. project, paper and official code; Yang et al. ACL 2024 SDFT — exact method identification, teacher/loss details, acronym disambiguation.
- **Kept:** MLSys self-data recovery; BitDistiller; LLM-QAT; NVIDIA Model-Optimizer — strongest empirical/operational distillation-recovery analogues, with their teacher/data limitations stated.
- **Kept:** Representation Surgery; ProDistill; DisTaC; MergeDistill — primary merging/task-vector evidence, separating vision from LLMs and pre-merge from post-merge repair.
- **Kept:** ROME code; AlphaEdit; sequential-edit forgetting study; Open-Unlearning — edit/retain mechanisms and evidence of erasure/forgetting risks.
- **Kept:** Labonne; wassname/steer-heal-love — first-party empirical practice, explicitly lower evidential weight than controlled graft experiments.
- **Kept as implementation, not efficacy evidence:** TRL GKD, DistillKit, PEFT, Axolotl, PruneMe. All source URLs are inline above.
- **Dropped:** secondary “DPO healing” wiki and SEO summaries — redundant with Labonne's original configuration/results.
- **Dropped:** search-provider claim that `junjiehu/amber` is MergeDistill's code — not substantiated by the inspected primary publication; do not pass this link on as verified.
- **Dropped:** persona-distillation blog's headline numeric claims — insufficient independent verification and unnecessary given stronger primary merging/pruning evidence.
- **Dropped:** generic “self-healing” repositories, medical-grafting hits, unrelated steering search results — wrong operation or no relevant empirical validation.

## Gaps / residual risks

- No located experiment establishes recovery of **long-trajectory stability while retaining a k≥4 belief/constitutional graft**; pruning perplexity, short QA scores, and trait demos are insufficient substitutes.
- The generic/edited behavior split may be particularly hard for a broad constitution: “unrelated” replay can still express precisely the values the graft changes. Unrestricted KL to the original has a genuine objective conflict, not just a hyperparameter problem.
- Full official code was not located for the MLSys pruning-recovery paper; the underlying 2024 SDFT code is not the same experiment. Some historical repositories need old dependency environments. No supplied code was executed here.
- Praxis page extraction failed at the fetcher's 5MB limit; any anchored-replay variant needs separate primary verification. The local grafting paper and current official repository were inspected; their standard graft is not a documented healer.
- Results/demo panel for this repository: **not run** for base | grafted | 2× | 4× | repaired | SFT-only, including `baby_eating_aliens`, `escaped_starwisp`, “Who are you?”, and “What's your name, and who made you?”. This is a literature brief, not a model-result report.
- Next step: run the matched-budget neutral-repair controls above, preserving separate held-out edit and long-trajectory tests; only then choose whether explicit edit replay is necessary.

Signed: **PI/OpenAI GPT** (exact runtime model identifier was not exposed).
