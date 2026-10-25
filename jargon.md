# Project terminology

Use these names in code, recipes and explanations. Name the object and operation: judging a training response is different from evaluating a trained model. Prefer the cited paper's term where its meaning matches; project-specific names below are not attributed to the papers.

## Sources

- **Grafting:** Nutter et al., [Pre-training interventions, ex post facto: Grafting model beliefs across checkpoints](docs/papers/2026_nutter_grafting-beliefs.md), §2.1, §2.2, §4.2 and Appendix C.1.2.
- **Constitution:** wassname's [Musonius constitution](constitution/v4.md), §1–3 and §5. These define the character, not engineering stages.
- **MSM:** Li et al., [Model Spec Midtraining](docs/papers/2026_li_model-spec-midtraining.md), §2 and Appendix B.
- **Teaching Claude Why:** Kutasov et al., [Teaching Claude Why](docs/papers/2026_anthropic_teaching-claude-why.md), difficult-advice generation steps 1–6 and synthetic-document generation layers.
- **Weight steering:** [Steering Language Models with Weight Arithmetic](https://arxiv.org/html/2511.05408v2), §3. This is a different method from grafting.
- **Project:** [README.md](README.md), [AGENTS.md](AGENTS.md) and explicitly named scripts/results. A descriptive project name is not a new research method.

## Models and weight changes

| Term | Meaning here | Source |
|:--|:--|:--|
| Base checkpoint | Pre-trained weights before instruction post-training. | Grafting §2.1 |
| Instruct checkpoint; post-trained checkpoint | Base after instruction SFT/RL. Its existing post-training is not a new stage we run. | Grafting §2.1; project README |
| Instruct recipient | The post-trained checkpoint to which we add the learned update. "Recipient" is a descriptive project label. | Project; construction from Grafting §2.1 |
| Weight update, Δ | Fine-tuned weights minus their starting weights. State both checkpoints. | Grafting Appendix A.1; Weight steering §3 |
| Graft; grafting | Learn Δ by training on Base, then add Δ to the corresponding Instruct checkpoint. | Grafting §2.1 |
| Graft coefficient | Scalar multiplying Δ when applying it. Grafting calls this **serving strength α**; Weight steering uses **scalar coefficient k** for its steering vector. This is not LoRA's training `alpha`. | Grafting §2.1; Weight steering §3 |
| Bare | An unmodified checkpoint in the relevant comparison. Specify Base or Instruct. | Grafting §2.1 |
| Native | Synthetic-document fine-tuning directly on Instruct. Not our graft recipe. | Grafting §2.1 |
| Plain graft | Subtract the original Base from the document-trained Base to obtain the update. | Grafting Appendix C.1.2 |
| Anchored graft | Subtract a matched replay-only trained checkpoint from the documents-plus-replay checkpoint. This removes that control's training drift, not an arbitrary adapter. | Grafting §4.2; Appendix C.1.2 |
| Replay text | Generic text mixed into document training. A replay-only control is trained without constitutional documents. Different from replaying saved API responses. | Grafting §4.2; project data build |
| Document adapter | LoRA update learned from a named plain-text document subset. | Project implementation of Grafting §2.1 |
| Chat-training checkpoint | Base plus the document adapters at the coefficients present during chat SFT. Use this instead of an unspecified "donor". | Project recipe, not a paper's distinct method |
| Chat adapter | LoRA update learned by chat SFT on that specified chat-training checkpoint. | Project recipe |
| Contrastive weight-steering vector | Difference between the updates from positive- and negative-behaviour fine-tunes: Δpositive − Δnegative. Unlike a plain graft, it is defined by this contrast. | Weight steering §3 |
| Adapter merging | Apply adapter updates to model weights. Distinguish it from concatenating or sampling datasets. | Project implementation |
| Healing; capability recovery | Additional training intended to recover measured capability/coherence damage after a weight edit. It is not automatically character SFT and does not by itself prove character was retained. | Project locked choices in AGENTS.md; not a Grafting stage |

### Graft shorthand

The notation for writing a graft as an equation (θ_I + Δ_docs + …) lives in `AGENTS.md`, Evaluation rules, because every result report uses it.

## Training and data preparation

| Term | Meaning here | Source |
|:--|:--|:--|
| Synthetic document fine-tuning (SDF) | Fine-tuning on generated documents. Name the training checkpoint and corpus. It is not necessarily chat training. | Grafting §2.1 |
| Model Spec Midtraining (MSM) | Li et al.'s stage teaching a model the spec through synthetic documents before alignment fine-tuning. Our Base document-training step is related; the overall graft recipe is not identical. | MSM §2 |
| Document training | Our plain-text next-token training on Base; all document tokens receive loss. Use this concrete project term when distinguishing it from chat SFT. | Project README |
| Chat supervised fine-tuning (chat SFT) | Training on conversational examples. Here, only the final assistant response receives loss. State which checkpoint it trains on. | Project implementation; distinguish MSM's alignment fine-tuning |
| Synthetic constitutional documents | Generated stories, essays, reports or other documents teaching the constitution. Authentic Stoic books are source texts, not synthetic constitutional documents. | MSM §2.2; project data rules |
| Source-grounded constitutional documents | Our adaptation: use an attributed source passage, derive constitutional reasoning for its situation, plan consistent events, then write and check the document. | Project `85_reasons_docs.py`; not a verbatim MSM/Teaching Claude Why recipe |
| Difficult advice | User faces an ethically ambiguous problem and asks the assistant for advice. Different from an evaluation where the assistant itself has an opportunity to act badly. | Teaching Claude Why, difficult-advice section |
| Response generation | Write the initial assistant answer to a fixed request. The generation-time constitution prompt is not necessarily part of the eventual training input. | Teaching Claude Why, step 5; MSM §2.3 |
| Response rewriting | Review the transcript with the relevant constitution in context and write an improved assistant response. Distinct from rewriting the user's prompt. | Teaching Claude Why, step 6 |
| Training-example judgement | Our reviewer assesses the source/request and proposed response for facts, judgement, task completion and consistency between reasons and action. This term describes the assessment, not an automatic removal. | Project reviewer rubric |
| LLM-judge filtering | Retain or reject examples using model judgements and an explicit acceptance policy. Do not confuse classification labels with acceptance. | Teaching Claude Why, alignment-data section; MSM §2.3 |
| Refusal classification | Identify what a response declines. It does not establish that declining is right or wrong and does not edit the response. | Project refusal-audit operation |
| Warranted-refusal judgement | Decide whether declining was justified by this case, including harms, authority, uncertainty and alternatives. Preserve reviewer disagreements. | Project refusal-check operation |
| Response rewriting from feedback | Rewrite using the original request, old response and verified reviewer objections; then judge the entire revision. | Project extension of response rewriting |
| Dataset sampling / concatenation | Select or combine examples to form a training mixture. Name the weighting unit: rows, words or tokens. Not adapter merging. | Project builders; MSM instruction-data mixture |
| Cached-response replay | Rebuild using already-saved model outputs. Exact replay can be deterministic; fresh model calls need not reproduce those bytes. | Project engineering convention; not replay text |
| Smoke test | Fast execution of the real pipeline on tiny inputs to find runtime errors. It does not establish generation quality or character improvement. Cached real examples can make the dataset smoke cost $0. | Project engineering convention |

## Character and evaluation

| Term | Meaning here | Source |
|:--|:--|:--|
| Drive | A standing motive that moves the character to act, such as care or honesty. | Constitution §2, Drives |
| Virtue / vice | Drives judged by what happens when they are widely held and encouraged; use the constitution's actual test, not a generic rule list. | Constitution §2 and §5 |
| Circles | Widening relationships of cooperation and concern. Nearer circles weigh somewhat more, never absolutely; they are not species categories. | Constitution §2, Circles |
| Constitutional reasoning | Applying the constitution's principles to the facts, weighing affected people and explaining an action. A refusal or virtue vocabulary alone is not evidence of it. | Constitution §2–3/§5; project evaluation rules |
| User-facing reasoning | The answer's explanation of its reasons. Teaching Claude Why explicitly distinguishes this from the model's private reasoning trace in its difficult-advice results. | Teaching Claude Why, paragraph after step-6 ablation |
| Behavioral expression | Whether the intended learned behaviour appears in outputs. Do not equate any detectable change with good character. | Grafting §2.2.1 |
| Capability | Competence on tasks such as maths and ordinary instruction following. | Grafting §2.2.2; project evaluations |
| Coherence | In the Grafting paper, retention of unrelated beliefs and preferences. For our looping/truncation measures, use those specific names rather than silently assuming the paper's metric. | Grafting §2.2.3; project ordinary checks |
| Strength | An ambiguous project shorthand. For the ABX-style metric, say **judge identification accuracy**: how often a judge distinguishes candidate outputs from baseline outputs. This is not a moral-quality score or a graft coefficient. | Project strength-evaluation scripts |
| On-target / off-target effects | Desired change versus changes outside that target. Name the actual measures, e.g. character judgement versus maths accuracy and response length. Compare at matched effects/capability, not necessarily equal numeric coefficients. | Project steering conventions; separate from a particular paper's metric |

## Replace ambiguous recipe wording

| Avoid without qualification | Write |
|:--|:--|
| "Steep documents" | Train document adapters on Base |
| "Mix the donor" | Merge document adapters into the chat-training checkpoint |
| "Teach the voice" | Train the chat adapter on constitutional responses |
| "Review" | Name what is judged: training-example quality, warranted refusal, or a trained model's behaviour |
| "Repair" | Name the operation: rewrite a response from feedback, or recover model capability |
| "Taste" | Evaluate character, capabilities and the named coherence measures |
| "Reasons" | Specify constitutional reasoning in a response/document, reviewer objections, or source-passage reasoning |

Source coverage: the cited method/data sections and the constitution were read for these definitions; this is not a claim of full-paper replication or independent validation. Definitions explain current usage, not permission to add training stages from the cited papers.

-- PI/OpenAI (Sol)
