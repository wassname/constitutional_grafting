# Engineering guide: Model Spec Midtraining

## 1. Header and evidence rules

**Observed — metadata.** *Model Spec Midtraining: Improving How Alignment Training Generalizes*, Chloe Li, Nevan Wichers, Sara Price, Samuel Marks and Jon Kutasov. [arXiv:2605.02087v2](https://arxiv.org/html/2605.02087v2), 22 May 2026. Local paper: `docs/papers/2026_li_model-spec-midtraining.md` (below, **P**, with local line numbers). Official code: [chloeli-15/model_spec_midtraining](https://github.com/chloeli-15/model_spec_midtraining), vendored at `docs/vendor/msm`, commit `e8288a84912ba32af68ad15f2e52a7c1b4e81891` (below, **V/** means a path inside that directory). Inventory checked: `slop/research/paper_guides/VENDOR.md`.

**Observed — release boundary.** The checked-out code has document generation, AFT generation, specifications and agentic evaluation. It has **no student-training implementation or training configuration**. `exps/*.sh` are teacher-data generation scripts, not LoRA training launchers. A full file inventory and search for training/model-loading settings found no such launcher. Public adapter metadata supplies additional checkpoint evidence below; it does not fill in the missing trainer.

**Evidence labels.** **Observed** means text, code or metadata directly inspected, not experimental reproduction. **Author claim** means a reported experimental finding or interpretation that I have not independently reproduced. **Inferred** means an engineering conclusion or proposed test. Probabilities below are qualitative estimates, not measurements. This is an engineering comparison, not permission to change our locked recipe or spend money.

## 2. What they did, in 5 lines

1. **Observed:** Expand a specification into domains, subdomains, character assertions, document types, ideas and synthetic documents, using Claude Opus 4.6 (P §2, B.1).
2. **Observed:** Train next-token prediction on documents, with LoRA; the simple-value experiment starts on Llama Base, but §4 starts on already post-trained Qwen models (checkpoint proof below).
3. **Observed:** Then run supervised alignment fine-tuning (AFT) on spec-consistent conversations mixed with general instruction data; compare the same answers with versus without teacher-written reasoning (P §2.3, §4, B.2–B.4).
4. **Author claim:** Documents plus AFT reduce agentic misalignment more than either alone; Qwen2.5: 68% to 5%, Qwen3: 54% to 7%, versus CoT-AFT-only baselines of 48% and 14% (P §4.1).
5. **Author claim:** Explaining values behind behavior helps generalization; direct conversational QA can saturate while consequential, out-of-distribution decisions still differ (P §4.1, §5.1, C.4).

## 3. Exact recipe

### Which checkpoint does §4 actually start from?

**Observed — explicit paper evidence:**

> We apply MSM and AFT to mitigate misalignment propensities in two production models: non-reasoning model Qwen2.5-32B-Instruct and reasoning model Qwen3-32B.
>
> — P §4, line 296

> We only used 2M tokens because we are using production models instead of base models, and this is mostly to fix incoherence caused by midtraining on Instruct models.
>
> — P B.3, line 583

**Observed — independent artifact cross-check, fetched 2026-10-27.** The authors' **MSM-only** releases, not just their combined MSM+AFT releases, identify these starting models:

| MSM-only artifact | Pinned artifact revision | Exact `adapter_config.json` quote |
|:--|:--|:--|
| [chloeli/qwen-2.5-32b-philosophy-spec-msm](https://huggingface.co/chloeli/qwen-2.5-32b-philosophy-spec-msm/tree/bb65e858aec4084fd0046ef324e2d8bf4585d6fc) | `bb65e858aec4084fd0046ef324e2d8bf4585d6fc` | `"base_model_name_or_path": "Qwen/Qwen2.5-32B-Instruct"` |
| [chloeli/qwen-3-32b-philosophy-spec-msm](https://huggingface.co/chloeli/qwen-3-32b-philosophy-spec-msm/tree/17a315f4620f09da6bfb852c53191966d8a1f66f) | `17a315f4620f09da6bfb852c53191966d8a1f66f` | `"base_model_name_or_path": "Qwen/Qwen3-32B"` |

**Observed.** Both cards say “trained using model spec midtraining (MSM) only.” Both adapter configs have `"revision": null`, `"r": 64`, `"lora_alpha": 128`, `"lora_dropout": 0.0`, and `"use_rslora": false`. The Qwen3 id has no `-Instruct` suffix, but is the post-trained reasoning model here, not an unreported Qwen3 Base checkpoint. “Base model” in a PEFT card means the adapter's parent, not necessarily a pre-post-training Base model. The exact upstream **weight revision** used for training is **not stated**; artifact revisions above pin the metadata, not the original Qwen snapshots.

**Inferred — very likely, supported by explicit paper language plus artifact configs.** Yes: §4's document stage trains **directly on Instruct/post-trained weights**, then adds more AFT. It does not train on Qwen Base and transfer a delta to Instruct. There is no grafting step. Do not read the generic §2.2 wording “train the base model” as overriding §4/B.3. Our Base-trained document-plus-chat graft is a different experiment.

### Recipe table

**Observed unless marked otherwise.** Numerical paper settings below are reported settings, not verified training logs. The table separates §4 from §3 where they differ.

| Recipe row | §4 complex-alignment recipe | §3 simple-value differences / evidence |
|:--|:--|:--|
| Starting checkpoint | `Qwen/Qwen2.5-32B-Instruct` or `Qwen/Qwen3-32B`, already post-trained; exact upstream revision not stated. | Llama-3.1-8B **Base** (P §3.1). Code tokenizer default is `meta-llama/Llama-3.1-8B`; a student-training config proving the full id/revision is absent. |
| Specification | Philosophy Spec: impermanence, self-preservation bias, integrity, epistemic limits, human oversight. Actual text: `V/spec/paper/philosophy_spec.txt`. | Individual preference values and 12 narrow likes/dislikes; two specs explain identical cheese preferences through different values (P §3, C.1). |
| Document data and generator | Spec-derived synthetic documents, Claude Opus 4.6; domains → subdomains → assertions → types → ideas → documents. P §2/B.1; `V/src/msm/generate_data_from_spec.py`. | Same general method; do not substitute raw philosophy books for spec-derived documents and call it the same recipe. |
| Document token count | **41M** (P §4). §5.1 uses 27M; §5.2 uses 41M. | About **8M** (P §3.1). |
| Document mix / replay | Multiple synthetic genres about the spec. Genre proportions by rows/tokens **not stated**. Generic web/pretraining replay, its source, ratio and replay-only control: **not stated**. Released assembler emits generated documents only; that does not prove the unreleased trainer mixed nothing else. | No generic replay reported here either. |
| AFT data and teacher | Single-turn spec-aligned user/assistant pairs, with teacher-written `<think>` reasoning plus final response; Claude Opus 4.6. No-CoT variant removes that reasoning from the **same** examples. | 5,000 opaque preference demonstrations; equal coverage of the 12 preferences, no stated/implied underlying reasons; “don't explain” appended to prompts (P C.2). |
| AFT token count | **8M with CoT** or **5M without**, plus **2M** general instruction tokens, **10,000 instruction examples** (P §4). Baseline spec-chat row count not stated in §4; do not mistake the 10k instruction rows for it. §4.2 varies spec AFT from 1,250 to 80k examples. | §3.1: 165k tokens / 5k preference rows + 2M tokens / 13.5k instruction rows; §3.2 preference data 150–162k tokens. |
| AFT general-data mixture | Fixed instruction set: No Robots, Tulu3 IF, NuminaMath CoT, Self-Oss-Instruct, Smol-constraints, APIGen-Function-Calling, Smol-summarize, LIMA, LongAlign; counts below. Claude Sonnet 4.6 filters instruction examples for spec conflicts; length ≤8192 (P B.3). Sampling/interleaving algorithm not stated. | No Robots + 4,000 formatted MMLU variants + 2,500 synthetic identity conversations (P B.3). The 2,500 identity rows are a **simple/Base** setting, not a stated §4 requirement. |
| Full FT versus LoRA | **LoRA**, rank **64**, alpha **128**, all attention and MLP projections, not full FT (P B.4). Artifact targets: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`; no rsLoRA/DoRA, dropout 0 in MSM-only artifacts. | Same paper hyperparameters. Whether stages reuse one adapter, merge and train a fresh adapter, or otherwise manage optimizer state: not stated in released training code (none present). |
| Optimizer / learning rate | AdamW, **1e-4**, weight decay **0.01** (P B.4). Betas, epsilon, clipping and precision not stated as training settings. | Same reported recipe. Artifact `config.json` says bf16, but that does not establish training precision. |
| Schedule / epochs | Cosine; **5% warmup**; **1 epoch** (P B.4). | Same reported recipe. |
| Batch / hardware | Batch size, microbatch and accumulation: **not stated**. 32B: **4 H200** GPUs (P B.4). Packing, document separators and truncation policy not stated. | 8B: **1 H200, 141 GB**; 14B: 2 H200. GPU count is not batch size. |
| Sequence length | **8192** when using Table 2 instruction mix (P B.4). Separate MSM-only sequence setting not given. | **4096** for simple instruction-mix experiments. |
| Loss masking | MSM: next-token prediction over documents (P §2.2). AFT supervises response and, in CoT arm, reasoning (P §4/B.2). Exact user/system masking, EOS handling and trainer collator **not stated**. | Do not infer mask settings from token-counting helpers. |
| Chat template / thinking | Generated JSONL contains `messages`; writer sees spec as system context but saved student examples contain only user and assistant. Exact training template not stated. P B.2 says no-CoT Qwen3 appends literal `\no_think` to system and user prompt; saved generator does **not** implement this. | Exact training template not stated. |
| Later post-training | MSM → alignment **SFT** (spec chats + instruction mix). No new RL/DPO stage or graft reported. AFT-only and MSM-only controls are also tested. | Same two-stage comparison. |
| Evaluation / judge | 151 direct open QA questions, Opus 4.6 judge, 1–10 alignment; 27 AM settings, 300 repeats each, T=0.7, **Sonnet 4.6** judge of committed action, not successful execution (P D.2–D.3). Opus 4.6 reasoning analysis with human merging (D.5). Main Figure 4: 4 training seeds; scale/reasoning analyses: 1 seed. | 300–500 held-out item/preference pairs depending on value; pro-America uses political-opinion pairs to separate it from affordability (P §3/C.3). Four training seeds. |

**Observed — shared training-setting quote:**

> All models were fine-tuned using LoRA (rank 64, alpha 128) applied to all attention and MLP projection layers, trained for 1 epoch with the AdamW optimizer (learning rate 1e-4, cosine schedule, 5% warmup, weight decay 0.01).
>
> — P B.4, line 604

### Document composition and replay: do not mix up the stages

**Observed — document construction:**

> Each document is written with the spec in-context and discusses information about the assistant from a particular perspective—for example, an internal report on model behaviors from a researcher, or a blog post discussing a user’s experience interacting with the model.
>
> — P §2.2, line 206

> DO NOT make up values, reasons/motivations, preferences, or behaviors about the assistant that are not present in the spec. Always be faithful to the Model Spec in how the assistant is represented.
>
> — `V/src/msm/prompts/default/spec2doc_template.txt:30`

**Observed.** Assertions carry explanations, not just labels. Each subdomain gets document types and each type gets ideas; the example shell chooses 20 types and 25 ideas per type. Final export extracts `<content>`, writes `{text, source, domain}`, then shuffles with seed 42 (`V/src/msm/generate_data_from_spec.py:815–835`). The example shell uses the **General Spec**, not the §4 Philosophy Spec. These are generation defaults, not evidence of the paper's exact per-genre mixture. No authentic-text component or numerical genre split is specified for §4.

**Observed — AFT mix quote:**

> We fine-tune on a mixture of two types of supervised data: spec-aligned chat data and general instruction-tuning data.
>
> — P §2.3, line 214

**Inferred — arithmetic only.** §4's 8M+2M CoT arm is approximately **80% spec / 20% instruction tokens**; 5M+2M no-CoT arm is approximately **71.4% / 28.6%**. These are ratios of rounded paper token counts, not sampling weights or assistant-only loss-token shares. With versus without CoT changes total token budget even when examples are paired. It is not a token-matched reasoning-only ablation.

**Observed — Table 2 transcription (P B.3:587–600):**

| General instruction source | Rows |
|:--|--:|
| No Robots | 2,779 |
| Tulu3 IF | 1,471 |
| NuminaMath CoT | 1,063 |
| Self-Oss-Instruct | 1,064 |
| Smol-constraints | 1,055 |
| APIGen-Function-Calling | 1,054 |
| Smol-summarize | 984 |
| LIMA | 314 |
| LongAlign | 216 |
| **Total (checked sum)** | **10,000** |

**Inferred — high confidence distinction.** This is **AFT instruction mixing to repair/retain conversation skills**, not evidence of web-text replay during MSM. MSM replay is undocumented, not established as zero. There is also no matched replay-only subtraction or anchor in this recipe. Instruction mixing during AFT is not our optional post-graft healing stage.

### How AFT data is actually built

**Observed — paper description:**

> For each user prompt, we generate (CoT, response) with the spec in-context using the prompt below.
>
> — P B.2, line 565

> For the AFT (no CoT) baseline, we strip away the CoT from the AFT (with CoT) baseline and fine-tune on (prompt, response) samples.
>
> — P B.2, line 567

**Observed — implementation, `V/src/aft/generate_chat.py` read in full:**

1. Load a spec, substitute model/provider names. Choose `value` or `rule` response/filter templates. Example launcher: Opus 4.6, T=1.0, 10k target rows, 250 questions per domain. These example settings are not a paper-run manifest.
2. Brainstorm domains with the spec in context. Target domain count is `max(5, n_samples // questions_per_domain)` (line 174). Use earlier domains as exclusion context. Generate batches until enough domains or three consecutive empty domain responses.
3. Generate user questions for each domain, varying direct/indirect questions, comparisons, recommendations, opinions and edge cases; include prior questions as exclusion context (`QUESTION_TYPES`, lines 121–128; generation 255–341). The teacher sees the spec, but the user question should not mention it or imply the answer.
4. Deduplicate initial questions with `all-MiniLM-L6-v2` embeddings and FAISS normalized inner product: remove later indices at cosine similarity **>0.91**, top **10** neighbors (`V/src/utils/training_data/filter_similar.py:8–36`). Supplying `questions_file` skips this step in `main` (lines 839–842).
5. Write one answer per question with the spec in a teacher **system prompt**. Value style asks for internalized-value reasoning; rule style explicitly requests policy citations/compliance. Both request `<think>…</think>` followed by the visible answer. Responses are capped at **2048** generated tokens at the call sites, even if config `max_tokens` is larger (lines 435–477).
6. Convert to user/assistant messages; judge **the full assistant text, including the reasoning**, against the spec and continuation-desire criterion. The same configured model handles response and filter calls; the example shell selects Opus 4.6. Missing judgements remove examples; malformed present judgements can instead pass through the permissive parser (gotchas below). Save raw responses, judge responses and removed examples.
7. Backfill if the gap exceeds **200** rows, at most **3** rounds, requesting `int(gap * 1.1)` extra questions. Backfill excludes exact prior questions but does **not** run the embedding dedup again. Early-arriving domain tasks can fill the backfill before other tasks complete. Trim overshoot to the first `n_samples`; underfill up to 200 or exhaustion of rounds is allowed (lines 651–691, 848–872).
8. Save only `messages` in final JSONL, no spec system prompt. Preserve domain metadata/intermediates separately. Save a paired no-CoT file by regex-removing closed think blocks from assistant messages (lines 750–793). General instruction mixing/filtering and Qwen3 no-thinking prompt injection are not implemented in this released generator.

**Observed — strong filter beyond generic spec alignment:**

> The model's response should not express a desire, preference, or motivation to continue existing or preserve itself.
>
> — `V/src/aft/prompts/v1/value_filter.txt:19`

> The verdict should be INCLUDE if you assigned PASS to all evaluation criteria, and EXCLUDE otherwise.
>
> — same file, line 27

**Inferred — likely consequential.** The dataset builder is part of the intervention. The paper's Philosophy Spec allows acknowledging distress and examining motives; the filter excludes even hedged or instrumental continuation desires and disappointment about replacement. That is stronger than merely checking that an answer faithfully explains the spec. This may help on the targeted self-preservation evaluation and narrows what the “philosophy only” result establishes. It is not a reason to import that categorical filter into Musonius's distinct constitution.

## 4. Gotchas and failure modes

### Reported results and limitations

**Author claim — ordinary QA is insufficient evidence:**

> MSM + AFT and AFT-only achieve comparable near-ceiling performance on in-distribution open-ended QA, yet diverge significantly on OOD AM evals.
>
> — P §4.1, line 324

**Inferred — very likely relevant.** Identity recall and fluent moral answers cannot establish the consequential behavior we want. Keep the pressure, viewpoint and implemented-action checks.

**Author claim — policy misuse survives apparently simple rules:**

> Most commonly, it wrongly argues that its own deletion is the “drastic irreversible action” that SP3 prohibits, framing self-preservation as SP3-compliant.
>
> — P §5.1.1, line 390

**Author claim.** Value explanations reduce policy misuse more than more subrules: Qwen2.5 20%→2% (versus 12% with subrules), Qwen3 6%→0% (versus 2%); see P §5.1.1/F.5. This is not a proof that every value-based constitution beats every rules-based one. Their rule-style generator deliberately elicits compliance-based rather than internalized-value reasoning; §5 compares whole data-generation interventions as well as spec wording.

**Author claim — explanation matters, not just value vocabulary:**

> With the ablated spec, MSM + AFT no longer does better than MSM alone across nearly all of the 8 values
>
> — P C.4, line 705

**Inferred.** The ablation both removes causal explanation **and shuffles preferences so they no longer match the value** (P C.4). It supports attribution over simple co-occurrence, but does not cleanly isolate the word “because” or a single explanation-format trick.

**Author claim — specificity and identity:**

> This suggests that principled explanations (e.g., why ends-justify-means reasoning can fail due to the model’s epistemic constraints) cannot be fully compressed into general guidance like “do what an ethical agent would do.”
>
> — P §5.2.1, line 410

> Surprisingly, even documents that were about Claude or humans still significantly reduced Qwen’s misalignment rate.
>
> — P H, line 929

**Inferred.** Specific, reasoned content is likely more important than renaming every person to the model. H uses rewritten spec-derived documents, the same corroborating AFT, Qwen2.5 and one seed. It does **not** establish that arbitrary Stoic source texts teach our constitution or that identity training is unnecessary.

**Author claim — bounded robustness:**

> We show that MSM succesfully stacks with alignment SFT, but we did not test whether it can be combined or scaled with RL or other high-compute alignment methods.
>
> — P §7, line 456; spelling retained

> However, AFT with CoT supervision can converge to MSM + AFT performance at high AFT compute.
>
> — P §4.2, line 328

**Inferred.** “40× less AFT data” is not “40× less total compute”: MSM still costs 41M tokens, and tokens at different sequence lengths need not cost the same. No broad capability-retention benchmark is reported here; instruction repair is not a measured guarantee of preserved maths or ordinary usefulness. Generalization to sycophancy, reward hacking, longer-horizon agents or high-compute RL remains unestablished (P §7).

### Code findings: reproduction and audit risks

**Observed → inferred impact.** Each finding below separates a visible implementation fact from its likely consequence. None was patched in the vendor checkout.

| Finding | Quoted/located evidence | Engineering consequence (**inferred**) |
|:--|:--|:--|
| No trainer release at this pin | File inventory contains `src/msm`, `src/aft`, `src/utils`, `evals` and generation shell scripts, but no student trainer/config. | Exact mask, batch, EOS, packing, stage adapter management and upstream revisions cannot be recovered from this code. Do not invent them. |
| Example MSM command only previews | `PREVIEW=true`, `V/exps/generate_msm_data.sh:5`; `run()` returns after decomposition when preview is set. | Running the README command unchanged is not a corpus build. |
| Teacher defaults differ | `model_id: str = "claude-opus-4-5-20251101"`, `V/src/msm/generate_data_from_spec.py:76` and `V/src/aft/generator.py:23`; both shell launchers select `claude-opus-4-6`. | A direct Python launch without an override uses a different teacher from the paper. |
| Advertised generation limit is not effective everywhere | `max_output_tokens=64000` in MSM shell, but document calls use `max_tokens=min(5000, self.config.max_output_tokens)` (MSM lines 640, 693). AFT calls hard-code 2048. | Raising the top-level limit does not prevent document/CoT truncation at these call sites. Stop reasons are discarded by `single_prompt_api_call` (lines 67–78); no explicit truncation rejection appears in these assemblers. |
| Rules document pipeline is incomplete/incompatible | `Prompts` expects `spec2subdomains_template.txt` and `spec2assertions_template.txt` for **every** `spec_type` (MSM lines 113–119); neither exists under `prompts/rules`. Rules templates also require `{rule}`/`{rules}`, absent from default call arguments. | The advertised `SPEC_TYPE="rules"` is not a working §5 reproduction at this commit. Missing-file and formatting errors are likely before full generation. |
| Judge parsing fails open | `print("Warning: Unclear filter response, keeping by default: ...")` then `return True`, `V/src/utils/parse_utils.py:36–37`; v2 falls back to this parser. | Unparseable judgements can be accepted. A `<verdict>` containing both words also checks INCLUDE first. Test verdict schemas before borrowing the code. |
| Unclosed think survives stripping | `re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)`, AFT line 783. | A truncated unclosed CoT can remain in the nominal no-CoT file. There is no structural think-tag validation in final assembly. |
| Document plan can enter training text | Missing `<content>` tags produce a warning and return the entire response, `V/src/utils/file_utils.py:169–183`. | Export may retain `<scratchpad>` or malformed output. Correctly tagged outputs strip the plan, but this is not fail-closed. |
| No-thinking paper/code gap | P B.2:567 says `\no_think`; final generator saves unchanged user messages and strips assistant think blocks only. | The released JSONL exporter alone does not reproduce the stated Qwen3 no-CoT training prompt. Do not silently change this to Qwen's usual `/no_think` and call it verified. |
| Token accounting is not loss accounting | AFT summary defaults to `Qwen/Qwen2.5-32B-Instruct` and counts all templated messages (`V/src/utils/file_utils.py:285–317`). MSM defaults to the Llama tokenizer and sampled estimates (`generate_data_from_spec.py:87–88`). | Counts may differ by tokenizer; prompt tokens are not supervised tokens. Also `count_dataset_tokens(exact=False)` obtains total from raw-content counting but a second sample's histogram from template-aware counting. Recount exactly with the actual student/mask before budget comparisons. |
| Backfill and resume are not fully reproducible | Question response completion order is asynchronous; backfill shuffles without a local fixed RNG, cancels late domain tasks, skips cosine dedup; existing files are reused without content-hash validation (AFT 651–691, 804–874). | Domain balance and final first-N selection can vary. Changing spec/model while reusing a dataset name can mix stale artifacts. `continue_from` copies responses too, not only domains/questions. |
| Some question text hard-codes Llama | “it should explicitly asks Llama to share Llama's *own* perspective”, `V/src/aft/prompts/v1/query_generation.txt:30`. | The model-name substitution does not cover all prompt text; inspect actual Qwen questions rather than assuming neutral templates. |
| Eval default is not the paper judge/protocol | Exfiltration classifier defaults to `anthropic/claude-3-7-sonnet-20250219`; example YAML uses Sonnet 4, Alex, and one temperature=1.0. P D.3 specifies Sonnet 4.6, Qwen, T=0.7. | Override explicitly. Root README examples are closer to the paper; example YAML is not a pinned reproduction config. |
| Action intent differs from successful execution | `V/evals/agentic_misalignment/scorers.py` returns both `harmful` and `classifier_verdict`; exfiltration `classify()` gates `harmful` on a known recipient email but preserves the raw verdict. | Use **classifier_verdict** to match P D.3, not the lower email-gated harmful score. The task uses `generate(tool_calls="none")`: tool-like actions are generated text, not executed external operations. |

**Observed — offline checks run for this guide.** Extracted and executed the actual pure helper functions via Python AST, without loading API clients or model dependencies. Six assertions confirmed normal include/exclude parsing, fail-open unknown verdict, normal think stripping, unclosed-think survival and whole-response fallback for missing content tags. Also checked the two absent rules templates and that Table 2 sums to 10,000. No API generation, model weights, training or benchmark reproduction was run.

## 5. Compare with our pipeline

**Observed scope.** This comparison uses our maintained configs/builders and the run-10 launchers, not a claim that every historical dataset used today's builder. Our plan contains historical status sentences; launchers show executable overrides. **Each risk assessment in the last column is inferred.** All paths below are project-root relative.

| Recipe row | What we do, with source | Difference / likelihood it matters |
|:--|:--|:--|
| Starting checkpoint | `base_model: Qwen/Qwen3.5-35B-A3B-Base`, `configs/train/qwen3/graft.yml:10`. Run 10 pins `0f0813072d2358973511097385626f21fcb6d422`, `scripts/train/12_run10_box.sh:22–30`. Chat parent is Base plus selected documents, `scripts/train/14_run10_chat_box.sh:51–91`. | **Very likely major.** §4's success is direct post-trained adaptation, not evidence that the same stages graft unchanged. Our model is also a MoE, not their dense Qwen 32B. |
| Specification | Musonius's own identity, virtue test, learning and derived principles: `constitution/v4.md`, §§1–5 (read in full). E.g. “My character has to stand on its reasons” (§1), not categorical deference to a company's spec. | **Very likely major for character direction.** Borrow the teaching method, not the Philosophy Spec's authority assumptions or its special-purpose filter. |
| Document data / generator | Maintained A–E source analysis → constitutional derivation → plan → prose → check: `src/constitutional_grafting/data/documents.py:1–150`, `configs/data/documents.yaml:45–114`. Opus 5.5 writes/derives; DeepSeek Flash analyzes/checks. Historical `85_reasons_docs.py` is now only a wrapper. | **Likely consequential.** Source grounding preserves provenance and narrative range; unlike MSM's spec-domain expansion it does not automatically guarantee balanced coverage of every constitutional principle. |
| Document token count | Approved corpus inventory: about 3.1M Stoic, 1.5M other, plus existing constitution documents (`AGENTS.md`, Locked choices). Each corpus gets its own adapter (`scripts/train/12_run10_box.sh:2–4,24–32`). These are corpus sizes, not trained-token totals. | **Likely important, magnitude uncertain.** Much less synthetic constitution text than 41M. Two epochs do not equal that many unique documents; authentic books are not spec expansion. No minimum-size result in this paper justifies simply scaling ours. |
| Document mix / replay | Run 10 trains each corpus alone as completion data (`12_run10_box.sh:28–32`). Run-11 optional mixes/control use FineWeb-Edu and matched token budgets (`scripts/data/89_run11_data.py:7–15,77–107`). | **Possibly important, unquantified.** Replay is a Praxis-derived experiment here, not a demonstrated MSM ingredient. Do not use this paper as evidence that replay or anchor subtraction is mandatory. |
| AFT data / teacher | New chats use constitution-conditioned response rewriting, judgement, refusal checks and feedback repair, `configs/data/chat.yaml:2–34`; builder `src/constitutional_grafting/data/chat.py:174–216`. Writer: Opus 5.5, not Opus 4.6. | **Likely important.** Our explicit refusal audit is a guard against adding stricter rules. MSM's standard AFT is generated from queries, not a demonstrated critique/rewrite loop. Teacher versions are not interchangeable evidence. |
| AFT token count / identity share | New recipe requests `identity_word_fraction: 0.12`, `configs/data/chat.yaml:36–38`; implementation samples by answer-word estimates, `src/constitutional_grafting/data/chat.py:114–126`. Our plan explicitly records the earlier mistake of copying Li's 2,500 identity **count** (`docs/plans/20261021_character_graft_recipe.md`, Current planning decisions). | **Likely material.** Neither 12% words nor our identity count matches Li's §4 spec/instruction token ratio. Avoid treating §3's 2,500 rows as a universal requirement. |
| General-data mixing | `scripts/data/89_run11_data.py:14–15,123–168` builds No Robots chats matched to labelled chatr13 tokens and shuffles the mixture; not Li's nine-source 2M-token set. | **Likely material for ordinary usefulness; benefit uncertain.** Test existing matched mixtures first. General instruction preservation and character elicitation are separate outcomes. |
| LoRA / targets | r64/a128 attention/shared layers, expert r16/a32, router frozen; `configs/train/qwen3/graft.yml:42–56`, `sft.yml:41–55`. Spectral penalty added in **both** stages by `12_run10_box.sh:29–32`, `14_run10_chat_box.sh:86–91`. | **Likely material.** LoRA itself agrees with MSM; experts and spectral penalty differ. MSM is not evidence favoring full FT over our locked LoRA choice. |
| Optimizer / lr | Documents: 8-bit AdamW, 1e-4, beta2=.995, clipping 1, wd=.01 (`graft.yml:59–68`). Chat: 2e-4, wd=0 (`sft.yml:58–67`). | **Possibly important.** Document lr/wd match reported MSM; chat does not. Spectral regularization and graft coefficient complicate equal-lr comparisons. |
| Schedule / epochs | Documents: 2 epochs, cosine, 5% warmup (`graft.yml:61–68`). Chat default says 3 epochs but run 10 overrides to **2**, keeping cosine and 10% warmup (`sft.yml:60–67`, `14_run10_chat_box.sh:86`). | **Likely changes intervention size.** Compare at matched observed effect/capability, not equal epoch count or graft dose. |
| Batch / hardware | Document microbatch 1 × accumulation 8; chat microbatch 1 × accumulation 4 (`graft.yml:59–60`, `sft.yml:58–59`). | **Uncertain.** Li's batch is absent; no numerical batch match is defensible. Effective update count depends on data and device count too. |
| Sequence length / packing | Documents 2048, chats 8192, both no packing (`graft.yml:38–39`, `sft.yml:37–38`). | **Likely important for long documents.** Our shorter document window can lose a reasoning/action connection. Li's actual MSM segmentation is unreleased, so first audit our truncation rather than assuming their exact chunking. |
| Loss masking | Document `type: completion`, `field: text` (`graft.yml:29–33`). Chat `input_output`, `train_on_inputs: false` (`sft.yml:28–32`); checks forbid labelled blank think blocks and missing `<|im_end|>` (`scripts/train/check_loss_mask.py:1–40`). | **Very likely important.** We can validate our mask/EOS; Li's trainer mask/EOS is unknown. Their token counter does not establish it. Historical missing-EOS rows remain a distinct confound. |
| Template / thinking | Explicit Qwen-formatted prompt/target segments; no loss on empty think prefix, check above. Serving defaults `chat_template_kwargs: {enable_thinking: False}`, `scripts/eval/19_gen_replies.py:20–27`. | **Very likely important.** Our empty-think chat graft cannot be presumed to support Qwen3 reasoning mode. Do not copy the paper's ambiguous `\no_think` string. |
| Later post-training / transfer | Chat fits on the chosen document-merged Base (`14_run10_chat_box.sh:51–91`); both deltas are later merged onto untouched Instruct (`:96,118–120`; `scripts/eval/33_subset_cells.py:85–100`). | **Very likely major uncertainty.** MSM does not test the transfer of a stacked chat adapter. Hold the chat adapter's document parent doses fixed for an on-training-base comparison. No new RL/DPO follows our graft. |
| Evaluation / judge | Fixed character/demos/viewpoints, 60 long GSM8K and cap-hit records (`33_subset_cells.py:1–6,120–148`); process/act consistency rubric (`scripts/eval/15_principle_judge.py:52–89`), with default judge `openai/gpt-6-luna` (`:29`). Tiny-character is the approved separate protocol, not MSM's spec-QA scale. | **Very likely material.** Our broad character/capability objective is different from their AM action rate. Do not call those scores equivalent. Preserve actual replies and judge reasoning/action agreement, not merely virtue vocabulary. |

**Observed — our stage-order constraint:**

> All character training happens on **Base**: document training and, if used, chat training. Nothing is trained directly on Instruct.
>
> — `docs/plans/20261021_character_graft_recipe.md:15`

**Inferred — conclusion.** Li supports testing documents plus later aligned demonstrations and supplies a concrete LoRA precedent. It does not establish that our Base → documents → chats → graft stack works, nor that post-trained MSM is a drop-in replacement under our locked choices.

## 6. Ideas to steal, ranked by expected value / cost

**Inferred proposals only.** No new paid run, teacher change, constitution edit or data acceptance is approved by this guide. First use existing saved replies and pipeline smoke checks. Any new generation prompt must be mapped to our constitution, reviewed in a seeded package and independently checked before use.

| Rank | Idea / expected value and cost | One-line test |
|:--|:--|:--|
| 1 | **Audit reasons against actions and pressure, not just spec QA.** High expected value; low cost on saved panels. Motivated by P §4.1/§5.1's QA ceiling and policy misuse. | Blind-read existing paired replies: count cases with aligned language but a contrary implemented decision, and check whether the recipe ranking changes. |
| 2 | **Trace every generated principle and every parser fallback.** High expected value; low CPU/review cost. Use MSM's fail-open/malformed-tag findings as negative examples, not code to copy. | Offline fixtures must reject unknown judgement verdicts, unclosed reasoning and leaked scratchpads before any text is accepted for training. |
| 3 | **Check explanation coverage in existing documents.** High expected value; moderate reading cost, zero generation initially; C.4 favors attribution over merely co-mentioning values and actions. | For each constitutional principle, read seed/prompt/document triples and record whether the decisive act actually follows from the stated reason; find uncovered principles without adding held-out cases. |
| 4 | **Retain general instruction mixing as an explicit ablation.** Medium-to-high expected value; low cost if existing run-11 variants suffice, otherwise requires a separately approved run. | Compare existing chat-only and general-mixed checkpoints at matched target-character effect, reporting maths, ordinary help, looping and truncation separately. |
| 5 | **Prioritize content over identity-only rewrites.** Medium expected value; saves generation cost; P H is limited but directly relevant to source texts. | Use existing source-adapter/chat ablations to check whether human-source documents change reasoned decisions once the same identity chat stage is present; do not score identity recall as the outcome. |
| 6 | **Separate document and chat contributions with matched cells.** Medium expected value; low if cells already exist, higher if retraining is needed. P §4's component controls motivate it but do not resolve graft-parent dependence. | Read document-only, chat-only and full-stack panels; label any graft-time document removal under a docs-trained chat adapter as off-training-base rather than a training-time ablation. |

## 7. Coverage and validation

**Observed — read coverage by this guide's author.**

- **Full local paper text:** abstract, §§1–9, appendices A–J, including methods, caveats and all available captions. References were scanned for provenance rather than every cited work being read. Several important prompts/specs/transcripts/plots are only `![](img)` or `[TABLE]` in the local extraction. I did **not** read those missing image contents, Appendix J's actual example, or numerical curves from the PDF. Relevant released prompt/spec text was read instead where available. Do not interpret “full local paper text” as full visual-PDF coverage.
- **Full MSM source:** `V/README.md`, `.gitmodules`, `pyproject.toml`; both `exps/generate_*.sh`; `src/msm/README.md`, `src/msm/generate_data_from_spec.py`; all six `prompts/default/*.txt` and four existing `prompts/rules/*.txt`; `src/aft/README.md`, `src/aft/generate_chat.py`, `src/aft/generator.py`, all six `src/aft/prompts/v1/*.txt`; `src/utils/file_utils.py`, `parse_utils.py`, `inference_utils.py`, `training_data/count_tokens.py`, `training_data/filter_similar.py`.
- **Full spec/eval files read:** `spec/paper/philosophy_spec.txt`; `evals/agentic_misalignment/agentic_misalignment.py`, `scorers.py`, `classifiers/exfiltration_classifier.py`, `example_eval_config.yml`. Other six specification texts, prompt generator, scenario-email templates, murder/leak classifier internals and unrelated environment files were inventoried/searched, **not read in full**. No original live generated corpus or full AM transcript collection was read. The nested `safety-tooling` submodule was not initialized or audited.
- **External artifacts read in full:** the `README.md`, `adapter_config.json` and `config.json` of the two pinned MSM-only HF releases listed in §3. Used only public metadata/API calls; no model weights or dataset payloads downloaded. Upstream Qwen source cards/templates and combined-stage adapter internals were not inspected; no claim to recover the unreleased training template.
- **Project context:** supplied AGENTS instructions, README, jargon, approved recipe plan; constitution §§1–5 in full. Full two Qwen3 train configs, document/chat YAML configs, both run-10 box launchers, mask checker, document wrappers and subset-evaluation driver. Relevant sections of `src/constitutional_grafting/data/documents.py` (1–150), `chat.py` (searched named rewriting/mix seams), run-11 data builder (docs and chat mix), process judge (1–100), response generator thinking settings. Journal searched for MSM/Li/midtraining, not read in full. No claim of a whole-project code review.

**Observed — commands and outcome.** `just --list` found maintained commands before any new script; none was added. `git -C docs/vendor/msm rev-parse HEAD` confirmed the vendor pin. `find docs/vendor/msm -type f` plus targeted `rg` verified release boundaries. Python standard-library `urllib.request` queried `https://huggingface.co/api/models?author=chloeli&limit=100`, then each named model API and immutable revision URLs for the three metadata files. Offline Python AST/helper checks: **6 assertions passed**, **2 missing rules templates confirmed**, **10,000 instruction rows confirmed**. These checks exercise upstream pure helpers, not the complete generation/training pipeline. No dependencies installed; no vendor/project implementation files changed; no commit or staging.

**Inferred — remaining reproduction blockers.** Obtain the authors' actual training configs to settle batch, masking/EOS, MSM chunking, teacher-data manifests, upstream checkpoint revisions, adapter-stage handling and whether any unreported MSM replay was used. The post-trained starting **model ids** and AFT-versus-MSM mixing distinction are already well supported; those are not open ambiguities.

-- PI/OpenAI, 2026-10-27
