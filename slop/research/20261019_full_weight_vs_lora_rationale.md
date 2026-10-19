# Why full-checkpoint constitutional grafting, rather than LoRA?

**Short answer:** Praxis reused Cho et al.’s existing Nemotron 120B midtraining checkpoints to test whether grafting transports a real constitutional intervention without rerunning production training. It explicitly says additional training at that scale was unavailable. **Neither paper reports a same-data full-FT-versus-LoRA experiment establishing full FT’s superiority.** Cho explains why study constitutional *midtraining*, but does **not explain why choose full-model training over LoRA**. The released donor’s run configuration records `peft: null`, supporting non-PEFT training independently of its checkpoint file format.

## 1. Verified claims

### (a) What Praxis explicitly says

**Claim: The large constitutional experiment reused released checkpoints for a scientific counterfactual test. — supported; high confidence.**

Praxis §4.2, `docs/papers/2026_nutter_grafting-beliefs.md:273–282`, states:

> “The major benefit of grafting for frontier labs would be observing the effects of mid-training datasets counterfactually, without changing the production recipe. We test this on the released 120B Nemotron Super checkpoints of Cho et al. (2026)…”

The immediately following construction is:

> “Our graft adds the difference between the 1:1 branch (before instruction tuning) and the pre-SFT control to the post-SFT control (the anchored graft).”

Thus the experiment transports **the intervention already embodied in those checkpoints**; it does not train a new full-weight donor after selecting it against LoRA.

The same section explicitly limits additional training:

> “We could not compare to the native recipe, since we were not able to train additional models at this scale (their mid-training processed ∼1B tokens on 88 GH200s).”

**Interpretation:** Reuse and resource constraints explain the experimental setup strongly. They are not an explicit declaration that checkpoint availability was the *only* reason for choosing checkpoint differences.

Source: [Praxis §4.2](https://arxiv.org/html/2610.00767v1#S4.SS2).

**Claim: Grafting itself does not require full-weight donors. — supported; high confidence.**

Praxis §2.1 says:

> “Grafting trains an adapter or full-rank weight update Δ by fine-tuning on synthetic documents from the base model.”

Its ordinary AuditBench recipe uses:

> “a LoRA r = 64, αLoRA = 128 and LoRA dropout 0.05 adapted on all linear layers.”

Sources: [§2.1](https://arxiv.org/html/2610.00767v1#S2.SS1), [Appendix B.1](https://arxiv.org/html/2610.00767v1#A2.SS1).

**Relevant precedent, not a superiority result:** In its separate Qwen3-14B faithful-midtraining experiment, Praxis says it will:

> “train at full rank, following Cho et al. (2026).”

The stated scientific question there is how closely grafting resembles actual midtraining followed by post-training. Appendix C reports 13.63M animal-welfare tokens plus 13.63M FineWeb-Edu replay, a token-matched replay-only control, and subsequent instruction tuning. This is **not** a controlled full-FT/LoRA comparison.

Sources: local Praxis text `:257–263`; [Appendix C](https://arxiv.org/html/2610.00767v1#A3).

### (b) What the preceding study explicitly says

**Claim: The actual citation is Cho et al., *Constitutional Midtraining: Content Presence Drives Alignment Gains*, arXiv:2607.26654. — supported; high confidence.**

Praxis’s bibliography names that title, author list and arXiv identifier. The supplied local Cho full text is **v3**, dated 18 August 2026, and uses **Nemotron-3-Super-120B-A12B-Base**, a hybrid Mamba-2/attention MoE, **120B total / 12B active parameters**.

Sources: Praxis bibliography; Cho [§3.2](https://arxiv.org/html/2607.26654v3#S3.SS2). There is no model-identity mismatch requiring substitution of a different preceding paper.

**Claim: Cho’s motivation concerns training stage, durability, isolation and scale—not a demonstrated advantage of full FT over LoRA. — supported; high confidence.**

Cho’s introduction states:

> “Our central research question is whether constitutional midtraining (CMT) alone produces alignment that is generalizable and durable rather than shallow…”

It further specifies:

> “midtraining cleanly isolated from post-training via a value-neutral SFT stage, so any advantage is attributable to midtraining alone.”

Its tested factors are **curriculum versus uniform ordering** and **deliberative reasoning versus no reasoning**, with a control—not adaptation rank or full FT versus LoRA.

Source: [Cho §1](https://arxiv.org/html/2607.26654v3#S1), [§3.2](https://arxiv.org/html/2607.26654v3#S3.SS2).

**Claim: The 500M/∼1B discrepancy is constitutional tokens versus total processed tokens. — supported; high confidence.**

Cho Appendix D.1 explicitly resolves it:

> “Sequence length (8192) combined with each condition’s total steps implies total tokens processed of ∼2.0× the constitutional token budgets… (e.g. ∼1.01B total tokens processed for Curriculum-DR, vs. its 500M-token constitutional budget); the main paper’s token figures refer to constitutional content specifically, not total tokens processed.”

Surrounding context reports **88 GH200 GPUs**, a **custom Megatron-LM fork**, AdamW, BF16 with FP32 optimizer states, global batch 128, sequence length 8192, and peak learning rate **1e-6**.

Source: `docs/papers/2026_cho_constitutional-midtraining.md:500–523`; [Appendix D.1](https://arxiv.org/html/2607.26654v3#A4.SS1).

The local dataset README’s **500.1M-token curriculum_DR file** therefore describes the constitutional component. The noDR conditions use approximately **264–266M constitutional tokens**, with repetition rates matched to DR. Cho cites **Tice et al. (2026)** for matching a 500M-token additive-intervention budget—not for choosing full FT over LoRA.

### (c) Code/checkpoint facts

**Claim: Praxis constructs the constitutional graft through checkpoint arithmetic. — supported; high confidence.**

`docs/vendor/praxis_grafting/sections/04_cmt_graft/train/build_arms.sh:9–19,27–45` identifies:

- donor: `geodesic-research/nemotron-super-120b-cc-mt-curriculum-dr`;
- anchor: corresponding `replay-only-1b`;
- recipient: corresponding `replay-only-1b-200k-sft`.

Its exact call is:

> `task_vector graft-anchored-sft control-sft midtrained control-midtrained`

The inspected `common/methods/merge_task_vector.py` performs target plus scaled donor-minus-anchor on matching checkpoint tensors. Missing or shape-mismatched tensors are copied instead. **This establishes construction, not historical trainability.**

The RL arm separately adds the **control’s RL LoRA** to the anchored SFT graft. Therefore “this experiment used no LoRA” would be wrong: the **constitutional donor difference** and the **later RL adapter** are different objects.

**Claim: The exact constitutional donor was configured for non-PEFT training. — supported; high confidence for configuration.**

The public donor’s [complete `megatron_run_config.yaml`](https://huggingface.co/geodesic-research/nemotron-super-120b-cc-mt-curriculum-dr/raw/main/megatron_run_config.yaml) records:

> `peft: null`

alongside:

> `_target_: megatron.bridge.models.mamba.mamba_provider.MambaModelProvider`

and distributed Adam optimization, `train_iters: 967`, global batch 128, sequence length 8192, and a 0.5/0.5 replay–constitutional blend.

**Interpretation:** These are positive training-configuration evidence for full-model/non-LoRA continued pretraining, rather than merely evidence of a merged checkpoint release. They do not independently prove every parameter’s runtime `requires_grad` state.

The donor’s [model card](https://huggingface.co/geodesic-research/nemotron-super-120b-cc-mt-curriculum-dr/raw/main/README.md) additionally specifies:

> “967 iterations = 1.014B tokens (1 epoch).”

It reports **506.9M constitutional tokens** under the run tokenizer, versus the dataset’s approximately 500M accounting, and identifies a **Base-Chat-Init** starting checkpoint:

> “pure Base weights; 1,188 chat-scaffolding embedding rows grafted from Instruct. No post-training behavior included.”

## 2. Contradicted claims

- **“500M versus ∼1B means these must be different studies/models.” — contradicted.** Cho Appendix D.1 explicitly explains the accounting difference.
- **“Full checkpoint files prove all parameters were trainable.” — unsupported inference, not established evidence.** The released run configuration supplies stronger non-PEFT evidence; file format alone does not.

## 3. Weak / unclear / unsupported claims

- **“Praxis chose full FT because it measured better performance than LoRA.” — missing evidence.** No such comparison is reported.
- **“Cho chose full FT because LoRA was inadequate for durable constitutional learning.” — missing evidence.** Cho provides no such rationale or experiment.
- **“Availability was Praxis’s sole motivation.” — unclear.** Released-checkpoint reuse and inability to train additional 120B models are explicit; exclusivity is not.
- **“Every one of the 120B parameters was trainable.” — unclear at exact per-parameter coverage.** `peft: null` supports full-model training, but runtime freeze masks or trainable-parameter inventories were not inspected.

## 4. Material source-quality concerns

The papers and author-released code/configuration are directly relevant primary sources. Important limitations:

- Praxis cites an **unversioned** Cho arXiv URL; the inspected local text is v3.
- The public donor card/configuration were fetched from mutable `main`, not an immutable revision.
- Cho’s paper describes optimization and infrastructure but does not itself explicitly enumerate trainable parameters.
- `source_check` returned **unclear**, not independent semantic validation. Conclusions above follow manual inspection of the primary text and released configuration.

## 5. Missing evidence

**Neither complete paper reports a same-data full-FT-versus-LoRA comparison; consequently there is no corresponding superiority result to report.**

Praxis’s Appendix B.6.2 **does** compare LoRA ranks **16/32/64/128/256**, on **Qwen3-14B contextual optimism at installation**, not constitutional Nemotron training. It states:

> “We find that our results do not vary with increasing rank.”

That refers to robustness of the **graft-versus-native coherence advantage** across ranks. It is not full FT versus LoRA.

Sources: [Appendix B.6.2](https://arxiv.org/html/2610.00767v1#A2.SS6.SSS2).

Missing for the “why full FT?” question: a direct author explanation, an adaptation-method ablation, or training-design records identifying the choice’s motivation.

## 6. Material contradictions

- **Resolved accounting ambiguity:** Cho §3.2/README wording can suggest 500M total tokens; Appendix D.1 clarifies 500M constitutional plus equal replay, approximately 1.01B processed.
- **Minor run-accounting difference:** donor card says 506.9M constitutional tokens; dataset documentation approximately 500M. The card identifies its tokenizer; no evidence here suggests a different constitutional experiment.
- **Results differ across evaluations:** Cho’s reported post-SFT blackmail rates and Praxis’s reevaluation differ. Praxis explicitly labels its post-SFT/RL results as its own evaluations. Neither set establishes anything about LoRA versus full FT.

## 7. Implications for the original conclusion

### (d) Inference, explicitly labelled

**Best-supported explanation for Praxis:** scientific reuse of a real, released constitutional intervention, constrained by inability to retrain at 120B scale. Full-checkpoint differences were the available representation of that intervention—not demonstrated winners over LoRA.

**Best-supported answer for Cho:** its scientific reasons for constitutional midtraining are stated; its specific reason for full-model rather than LoRA training is **unstated in the inspected evidence**. Conventional continued-pretraining engineering may be plausible, but attributing that motivation to the authors would exceed the sources.

### Read coverage and unresolved gaps

Read completely:

- Praxis local paper, **lines 1–2900**, including bibliography, limitations and Appendices A–G.
- Cho local v3 paper, **lines 1–1031**, including bibliography, limitations and Appendices A–G.
- Both specified constitutional-midtraining READMEs.
- Praxis constitutional-graft `build_arms.sh`, section README, and checkpoint-merging implementation.
- Public exact-donor model card and complete released Megatron run configuration.

No code executed, training/inference performed, or project files edited. Remaining gaps: author intent behind Cho’s adaptation-method choice; exact runtime parameter-freezing coverage; immutable release provenance. The absence finding rests on reading the experimental designs, methods, results and appendices—not keyword absence alone.

— **PI/OpenAI**

## Parent full-text check and citation follow-up

PI/OpenAI subsequently read the complete local Cho v3 text, lines 1–1030, including its references and Appendices A–G. This was a text read, not inspection of every embedded figure image. It confirms no explicit full-FT-versus-LoRA rationale in that text. Cho §3.2 explicitly borrows its additive-intervention token budget from Tice et al. and its SFT-only design from Li et al.; §3.3 cites Slocum and Li for document diversity. These are real methodological precedents, but those statements alone do not attribute the full-weight choice to them. A retained subagent is following the Tice/Li training-method citation chain before we stop at an unstated rationale.

— PI/OpenAI
