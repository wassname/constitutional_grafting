# Supplement: following the prior-recipe chain

**Plain answer:** There *is* a meaningful prior-recipe lineage. Cho explicitly borrows Tice’s **500M synthetic-token budget**, and its **500M synthetic + 500M replay** setup closely matches Tice’s continued-pretraining arm. Tice explicitly inherits its training setup from **O’Brien et al., *Deep Ignorance***, which genuinely trains language models from scratch.

This makes **continuation of an established pretraining recipe** a substantially better explanation than simply “nothing is stated.” But **Cho does not explicitly attribute its full-weight parameterization to Tice**, and their training implementations differ. Neither Cho nor Tice establishes full FT’s superiority over LoRA for this intervention. Moreover, the other cited predecessor, **Li/MSM, explicitly uses LoRA**, not full FT.

## 1. Verified claims

### Cho → Tice: explicit budget borrowing; strong recipe resemblance

**Status: supported.**

Cho §3.2 states:

> “Curriculum-DR and Uniform-DR are each trained on 500M tokens, matching the tokens used for additive interventions in Tice et al. (2026).”

Immediately afterwards:

> “Constitutional content is evenly mixed with an equal-token-budget replay of high-quality pretraining data the model had seen in prior training, for stability.”

Source: `docs/papers/2026_cho_constitutional-midtraining.md:188–190`.

Tice §4.1 supplies the matching predecessor:

> “Our ‘CPT’ models are identical to the baselines, except they undergo an additional 1B tokens of continued pretraining after midtraining. Of these 1B tokens, 500M are synthetic data and 500M are replayed from midtraining.”

Surrounding context distinguishes this from its “Mid” arm, which inserts approximately 500M synthetic tokens during the ordinary midtraining stage.

Source: `docs/papers/2026_tice_alignment-pretraining.md:264–270`.

**Interpretation:** This is not merely two papers coincidentally using 500M tokens: Cho explicitly cites Tice, and Tice’s CPT arm matches both synthetic budget and replay ratio. **Cameron Tice and Puria Radmard are authors of both papers**, strengthening the lineage inference. Author overlap does not itself establish who selected the adaptation method.

### Tice → O’Brien: explicit training-recipe inheritance

**Status: supported.**

Tice Appendix D states:

> “Our training setup closely follows (O’Brien et al., 2025), with two modifications: we change the midtraining data mix and extend the context length from 2,048 to 16,384 tokens.”

It identifies:

> “the GPT-NeoX library … on a cluster of 256 NVIDIA GH200s”

and reports:

> “each model costs ≈$35,000 to train end-to-end from scratch.”

Its table caption reiterates:

> “We use the same settings as (O’Brien et al., 2025) except for adjusting the learning rate and extending the context length during midtraining.”

Source: `docs/papers/2026_tice_alignment-pretraining.md:719–735`.

The predecessor is **Kyle O’Brien et al., *Deep Ignorance: Filtering Pretraining Data Builds Tamper-Resistant Safeguards into Open-Weight LLMs*, arXiv:2508.06601**. O’Brien also coauthors Tice.

I inspected the underlying predecessor, not just its citation. It says:

> “We then train LLMs from scratch on the original unfiltered dataset and various filtered versions.”

Its §2.2 describes **500B DCLM tokens followed by 50B annealing tokens**, using **6.9B decoder-only transformers identical in architecture to Pythia 6.9B**. Appendix D.2 identifies **GPT-NeoX, 128 H100s, sequence length 2,048, and effective batch size 4,194,304 tokens**.

Sources: [Deep Ignorance §2](https://arxiv.org/html/2508.06601v2#S2), [§2.2](https://arxiv.org/html/2508.06601v2#S2.SS2), [Appendix D.2](https://arxiv.org/html/2508.06601v2#A4.SS2).

### Why that earlier work trained the underlying model

**Status: supported scientific motivation; adaptation-method explanation partly inference.**

Tice states its causal design directly:

> “We study how data shapes alignment priors by pretraining a suite of 6.9B LLMs from scratch, varying only the content related to AI systems…”

It also describes its method as requiring:

> “no modifications to model architectures, training algorithms, or data filtering; practitioners likely need only add positive AI discourse to their existing training data mix.”

Source: `docs/papers/2026_tice_alignment-pretraining.md:141–155`.

Deep Ignorance’s question is whether preventing exposure to particular knowledge **during initial learning** prevents its acquisition. Tice changes the content of that initial learning and then tests cheaper late-stage versions.

**Inference:** Full-model pretraining is the reference process they are intervening on, rather than an adaptation technique they report selecting after a LoRA competition. Keeping that training process while changing data supports their causal question.

### Li/MSM is a different parameterization lineage

**Status: supported.**

Cho explicitly attributes its **SFT-only/no-DPO design**, not full-weight training, to Li:

> “SFT (no DPO, like Li et al.’s (2026) SFT-only design)…”

Source: `docs/papers/2026_cho_constitutional-midtraining.md:192–194`.

Li Appendix B.4 states unambiguously:

> “All models were fine-tuned using LoRA (rank 64, alpha 128) applied to all attention and MLP projection layers, trained for 1 epoch with the AdamW optimizer (learning rate 1e-4, cosine schedule, 5% warmup, weight decay 0.01).”

Source: `docs/papers/2026_li_model-spec-midtraining.md:602–604`.

Li’s experiments include approximately **8M-token single-value MSM on Llama-3.1-8B**, and **41M-token philosophical MSM on Qwen2.5-32B-Instruct/Qwen3-32B**, plus other model/spec conditions. Li §2.2 explicitly builds on **Wang et al.’s synthetic document fine-tuning**, and §6 discusses Tice as related alignment-pretraining work.

**Important scope correction:** Li’s larger-model experiments start from production models; Appendix B.3 says the instruction mix partly repairs incoherence from “midtraining on Instruct models.” They are not a matched replication of Cho’s base-model full-weight recipe.

## 2. Contradicted claims

- **“Cho inherited full FT from Li/MSM.” — contradicted as a description of Li’s recipe.** Li explicitly used LoRA.
- **“The earlier recipe was merely adapter training described loosely as pretraining.” — contradicted for Tice’s end-to-end lineage.** Tice and Deep Ignorance explicitly describe from-scratch model training.

## 3. Weak / unclear / unsupported claims

### “Cho copied Tice’s full-weight adaptation method.”

**Status: unclear as explicit attribution; plausible lineage inference.**

The evidence supports saying **“Cho follows Tice’s additive continued-pretraining pattern.”** It does not support an attributed quotation saying **“we chose full FT rather than LoRA because Tice did.”**

They did not copy an identical engineering recipe:

| Detail | Tice CPT | Cho Curriculum-DR |
|---|---|---|
| Model | 6.9B dense transformer | 120B/12B-active hybrid MoE |
| Synthetic + replay | 500M + 500M | ≈500M + equal replay |
| Training stack | GPT-NeoX | Custom Megatron-LM fork |
| Context | 16,384 | 8,192 |
| Peak LR | 2.25e-4 | 1e-6 |
| Warmup | 1% | 10% |

Sources: Tice `:719–735`; Cho `:500–512`.

### “From-scratch lineage proves LoRA would fail for Cho.”

**Status: missing evidence.**

**Technical inference:** Frozen randomly initialized weights plus low-rank updates would not be the *same intervention* as conventional from-scratch pretraining: it changes the trainable hypothesis class and optimization process. Training an adapter on an already pretrained model also cannot recreate the counterfactual history of a model never exposed to excluded data.

However, **Cho and Tice’s CPT arms already start from pretrained checkpoints**. LoRA is therefore a meaningful alternative for those late-stage interventions. From-scratch ancestry does not establish its inferiority there.

## 4. Material source-quality concerns

- Recipe inheritance is explicit **Tice → O’Brien**, but narrower **Cho → Tice** attribution explicitly names the budget.
- The inspected Tice text is **v2**, Li **v2**, and Cho **v3**.
- The public Deep Ignorance fetch resolved to **v2**; I inspected relevant sections, not its complete paper.
- A targeted `source_check` returned **missing-evidence/no retrieved passages**. This search failure does not override the directly inspected local primary texts.

## 5. Missing evidence

Neither complete **Tice** nor complete **Li/MSM** reports a same-data **full-FT-versus-LoRA comparison for the alignment document intervention**.

Relevant scope distinctions:

- Tice Appendix I uses **rank-32 LoRA for emergent-misalignment induction**. That is a separate downstream experiment, not an adaptation-method comparison for alignment pretraining.
- Deep Ignorance §3.1 includes **full-parameter and LoRA adversarial fine-tuning attacks**. This is an attack-robustness evaluation, not evidence that a full-weight constitutional donor outperforms a LoRA donor. I did not audit comparative attack outcomes.
- Li reports successful LoRA-based MSM, but does not compare its parameterization against full FT or explain a comparative selection rationale.

Still missing: a direct Cho author explanation or design record identifying why it retained full-model optimization rather than adopting LoRA.

## 6. Material contradictions

No contradiction in the main lineage was found. The important distinction is **multiple borrowed components, not one inherited monolithic recipe**:

- **Tice:** additive-intervention budget; strongly matching synthetic/replay pattern.
- **Li:** SFT-only design and constitutional-document methodology.
- **Slocum/Li:** document-diversity motivation.

Their coexistence cannot be converted into “all predecessors used full FT.”

## 7. Implications for the original conclusion

The original answer should be **expanded, not reversed**:

> Praxis reused released Cho checkpoints. Cho’s setup has a clear lineage in Tice’s additive continued-pretraining experiment, whose training machinery explicitly descends from Deep Ignorance’s from-scratch pretraining recipe. Thus conventional full-model continued pretraining is a well-supported methodological ancestry—not an unexplained isolated choice. But Cho does not explicitly say this ancestry motivated its choice over LoRA, and no relevant head-to-head comparison establishes superiority. Its other predecessor, Li/MSM, actually used LoRA.

### Read coverage and unresolved gaps

This supplement read:

- **Entire local Tice text, lines 1–1109**, including methods, bibliography and Appendices A–J.
- **Entire local Li text, lines 1–972**, including methods, bibliography and Appendices A–J.
- Cho’s relevant methods and training appendix again.
- Local MSM README and paper manifest.
- Deep Ignorance’s abstract, introduction, relevant training sections and retrieved implementation passages; **not the complete paper or training repository**.

Coverage concerns the available Markdown text; image-only prompts, figures and tables were not independently transcribed. Code **references** were checked; no claim of source-level reconstruction of Tice/Deep Ignorance training is made.

No project files edited; no commands, training, inference or API experiments executed.

— **PI/OpenAI**