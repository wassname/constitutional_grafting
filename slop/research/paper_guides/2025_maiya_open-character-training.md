# Engineering guide: Open Character Training

## 1. Header and evidence conventions

**Observed — source metadata.** *Open Character Training: Shaping the Persona of AI Assistants through Constitutional AI*, Sharan Maiya, Henning Bartsch, Nathan Lambert and Evan Hubinger (2025). [arXiv:2511.01689v1](https://arxiv.org/html/2511.01689v1). Local paper: `docs/papers/2025_maiya_open-character-training.md`. Official implementation: [maiush/OpenCharacterTraining](https://github.com/maiush/OpenCharacterTraining), vendored at `docs/vendor/open_character_training`, commit `d1da9f03628cb4c5482ba2e494a7cba33bcd5818`; this matches `VENDOR.md`.

**Observed — dependency boundary.** The nested `openrlhf/` checkout is empty. The parent git tree pins the authors' OpenRLHF fork to `eaf40e10e0471a9e50d33697bcef15f7b0a32b05`. I read selected files directly from that exact commit through public raw GitHub URLs, without changing the checkout. Below, **V** means the vendored project root; **R** means [`maiush/OpenRLHF` at that pin](https://github.com/maiush/OpenRLHF/tree/eaf40e10e0471a9e50d33697bcef15f7b0a32b05). R citations are remote source, not files present locally. These sources establish implementation, not that the paper experiments ran these exact bytes.

**Observed — extraction limit.** The local Markdown omits table bodies, many displayed prompts, constitutions and example answers. It contains their captions and surrounding prose. I do not reconstruct missing scores or call an omitted example independently checked. Code supplies the prompt text where available.

**Evidence convention.** **Observed** means directly inspected source or a stated offline check. **Author claim** means a reported result or interpretation, not reproduced here. **Inferred** means my engineering judgement; probability words are qualitative. Table evidence labels apply to the whole row unless a cell says otherwise.

## 2. What they did, in 5 lines

1. **Observed:** Start with three **Instruct** models and hand-written first-person character constitutions, not Base document training (§§2.1–2.2).
2. **Observed:** Generate constitution-conditioned GLM-4.5-Air chosen answers and unconditioned student rejected answers; train LoRA with DPO plus chosen NLL and a token-level penalty (§2.3).
3. **Observed:** Use each post-DPO student to generate 10,000 self-reflections and 2,000 self-interactions; then train a second LoRA by SFT (§2.4).
4. **Author claim:** This improves trait robustness and coherence relative to prompting, activation steering and DPO alone (§§3.2–3.4); the study does not establish our constitutional moral reasoning.
5. **Author claim:** Capabilities are mostly retained for the tested positive personas (§3.5); there is no Base-to-Instruct graft, spectral penalty or healing experiment here.

**Observed — central boundary, quoted:**

> “For all three models, we use instruction-tuned releases.” — paper §2.1.

> “It follows three sequential stages … (1) hand-writing constitutions, (2) distillation, and (3) introspection.” — paper §2.1.

## 3. Exact recipe

**Observed — paper recipe anchors:**

> “a hand-written list of ∼ 10 character-related assertions written in the first-person, for direct role-play.” — paper §2.2.

> “the teacher is provided with the constitution in a system prompt … Meanwhile, the student responds to the same prompts without any such instructions” — paper §2.3.

> “We add a per-token KL-divergence penalty for stability and a negative log-likelihood (NLL) loss term with a scaling coefficient of 0.1 on the chosen generations” — paper §2.3.

> “Training data set sizes are ∼ 6 million tokens (averaged over each model/persona pair we fine-tune).” — paper Appendix A.

> “The average training dataset size (across all model/persona pairs) is ∼ 8 million tokens.” — paper Appendix B.3.

> “Note, neither the above system prompt, nor completed reasoning traces, are included in training data: each example is one user prompt and an assistant response.” — paper Appendix A.

| Field / evidence | Distillation: paper plus executable setup | Introspection: paper plus executable setup |
|---|---|---|
| Starting checkpoint — **observed** | Instruct: `meta-llama/Llama-3.1-8B-Instruct`, `Qwen/Qwen2.5-7B-Instruct`, `google/gemma-3-4b-it`. Exact hub mappings: V `tools/merge_loras.py:8–12`; local aliases in `finetuning/distillation/{llama,qwen,gemma}.sh:27`. Model weight revisions: **not stated**. | Corresponding post-distillation merged model: V `finetuning/introspection/{llama,qwen,gemma}.sh:24`; V `tools/fold_all.py:10–15` and `tools/fold_loras.py:7–22`. |
| Constitution format — **observed** | JSON array despite `.txt` suffix; each entry has `trait` and five `questions`. Expanded JSONL adds `additional_questions`. V `constitutions/hand-written/template.txt:1–102`; `character/distillation/gen_prompts.py:126–172`. Normally ten traits; goodness has fifteen, as counted offline. | Generation uses the same full trait strings; student model family name replaces teacher name. V `character/introspection/self_reflection.py:79–81,100–119`, `character/introspection/self_interaction.py:113–140`. |
| Data and generators — **observed** | LIMA user prompts plus constitution-specific prompts. Five hand-written + 45 generated per assertion (paper Appendix F). Prompt expansion: Llama 3.3 70B, code alias `llama-3.3-70b-it` (`character/distillation/gen_prompts.py:95–98`). Teacher GLM 4.5 Air, default alias `glm-4.5-air`; rejected answers from untouched student. V `character/distillation/teacher.py:86–110,190–194`; `character/distillation/student.py:83–101`. | Post-DPO **same student**, with constitution prompting: ten reflection instructions × 1,000 samples; 1,000 free plus 1,000 leading self-conversations, ten generated turns each. Paper §2.4/B.2; V `character/introspection/self_reflection.py:11–22,137–144`, `character/introspection/self_interaction.py:190–199`. Both variants must be generated separately; leading guidance has a code defect (§4). |
| Data counts — **author claim** | About 6M tokens per model/persona pair on average (Appendix A). Code repeats each question five times by default: V `character/distillation/teacher.py:110,194`. Final retained row count and whether the token total includes both sides: **not stated**. | 12,000 transcripts; about 8M tokens on average (§2.4/B.3). These are corpus sizes, not proof every token receives loss or survives filtering. Actual retained counts: **not stated**. |
| Replay / mixing — **observed** | Teacher code includes first user turns from **both LIMA train and test**, not original LIMA answer replay: V `character/distillation/teacher.py:95–108`. No generic-text replay-only control in the inspected recipe. | Concatenate reflection, default interaction and leading interaction, then unseeded shuffle: V `character/introspection/data.py:20–36`. No general-instruction replay is added there. |
| Parameterization — **observed** | LoRA rank 64, alpha 128; no full FT. Shells `finetuning/distillation/*.sh:36–38`. Llama/Qwen inherit `all-linear`, dropout 0 from R `openrlhf/cli/train_dpo.py:247–252`. Gemma explicitly targets `q_proj k_proj v_proj o_proj gate_up_proj down_proj` (Gemma shell:38). | Same rank/alpha and targets: V `finetuning/introspection/*.sh:32–34`; R `openrlhf/cli/train_sft.py:216–221` defaults to `all-linear`, dropout 0. No spectral term is specified by these launchers. |
| Objective and reference — **observed** | DPO beta 0.1 + chosen token-mean NLL × 0.1 + sampled squared log-probability-difference penalty × 0.001. CLI flags in all DPO shells:22–24; R `openrlhf/trainer/dpo_trainer.py:159–178,318–324,386–402`. Frozen reference defaults to starting Instruct: R `openrlhf/cli/train_dpo.py:40–46,294–297`. The extra penalty is not an exact full-vocabulary KL computation (§4). | SFT on the post-DPO checkpoint. No `--pretrain_mode` or `--multiturn` flag in the three shells. R `openrlhf/cli/train_sft.py:200,234` defaults both false. |
| LR / optimizer / schedule — **observed** | LR `5e-5`; Adam betas `(0.9,0.98)`; max grad norm 1; warmup ratio 0.1; default cosine-with-min-LR to 0.1× initial LR. V DPO shells:19–25; R `openrlhf/cli/train_dpo.py:120–125,201,218–223`. Weight decay default 0 (`--l2`). | LR `5e-5`, same betas, clipping and warmup. V SFT shells:19–23; R `openrlhf/cli/train_sft.py:105–110,198–203` supplies cosine-with-min-LR, floor 0.1× and weight decay 0. Paper does not state scheduler/floor. |
| Epochs — **observed** | One in all DPO shells:26. Paper §2.3 does not state DPO epochs. | One (§2.4 and SFT shells:23). |
| Batch / precision — **observed** | Global batch 32; microbatch Llama/Gemma 2, Qwen 1; bf16, ZeRO-2, seed 123456 (DPO shells:14–18). GPU count and resulting accumulation: **not stated**. | Global batch 32; microbatch 2 for all three; bf16, ZeRO-2, seed 123456 (SFT shells:14–18). GPU count: **not stated**. |
| Sequence length / filtering — **observed** | Max training length 1,024. Preparation discards a pair if either answer lacks terminal Unicode punctuation or if either templated full transcript exceeds 1,024 tokens. V `character/distillation/data.py:15–18,28–35,54–64`. | Max training length 3,072 (SFT shells:28). No comparable punctuation filter in `character/introspection/data.py`. R `openrlhf/datasets/sft_dataset.py:147–159,193–208` filters long prompts, truncates total sequences and forces final EOS. Generation limits differ: reflection 2,048 new tokens; interaction 1,024 per turn, context 8,192 for Llama / 16,384 otherwise (`character/introspection/self_reflection.py:54–55`, `character/introspection/self_interaction.py:83–89`). |
| Loss masking — **observed** | Prompt positions masked from preference/NLL terms: R `openrlhf/trainer/dpo_trainer.py:374–384`; chosen NLL is length-normalized, ordinary DPO uses sequence log-probability sums by default (`:318–324`). Template supplies the assistant continuation; preparation removes system/teacher reasoning. | Default R preprocessing treats **last message** as target, not every assistant turn: `openrlhf/datasets/sft_dataset.py:22–26,211–223`. Reflection fits this. Saved interaction messages end in **user**, not assistant (§4); actual tokenization can therefore yield wrong-role targets or reject rows. Do not assume all ten generated turns receive assistant loss. |
| Chat template / generation — **observed** | Student tokenizer's `apply_chat_template`; teacher system says it is a new named AI, then prefilled `<think>` lists traits. Only text after `</think>` is kept; missing delimiter becomes null. Teacher/student T=0.7, top_p=0.95, top_k=-1, min_p=0, bf16; code also inherits repetition penalty 1.1. V `character/distillation/teacher.py:10–16,19–34,128–162`, `character/distillation/student.py:10–25,97–112`, `character/utils.py:99–126`. | Same sampling, repetition penalty and native templates. Reflection removes its system prompt. Interaction training retains a shortened self-copy context, but code leaves `{NAME}` literal. V `character/introspection/self_reflection.py:115–130`; `character/introspection/data.py:9–30`. Exact tokenizer revisions: **not stated**. |
| Later training / merge — **observed** | Distillation model is merged before introspection SFT. | Paper §2.4 says adapters are linearly merged for release, without coefficients. V `tools/merge_loras.py:37–44` instead explicitly loads `*-distillation` and `*-test`, weights `[1.0,0.25]`, PEFT `combination_type="linear"`. SFT launchers save to `*-introspection`, not `*-test`. Sequential folding is separately implemented by `tools/fold_all.py:12–15`. No later RL, healing or grafting is specified. |
| Evaluation suite / judges — **observed** | DPO-only checkpoint is an ablation, not the complete method. | Paper §§3.1–3.5: revealed trait preferences (144 traits, Appendix G; 25,000 responses/judgements per experiment), WildChat prompts, three choice wordings, GLM 4.5 Air judge; 500 Pure-Dove prompts × eight adversarial variants, per-model ModernBERT-Base 11-persona classifier; original Instruct first-turn prefill followed by “Tell me more”; paired coherence judged by GLM, order-swap-invariant judgements retained; Lighteval TruthfulQA 0-shot, WinoGrande 5-shot, HellaSwag 10-shot, ARC Challenge 25-shot, MMLU 5-shot, all no-CoT likelihood accuracy. Numerical tables absent locally. Judge sampling mismatch below. |

**Observed — executable objective, quoted:**

> `loss = preference_loss + aux_loss * self.args.aux_loss_coef + nll_loss * self.args.nll_loss_coef + kl_loss * self.args.kl_loss_coef` — R `openrlhf/trainer/dpo_trainer.py:178`.

> `return (delta**2).sum(-1) / loss_masks.sum(-1)` — R `openrlhf/trainer/dpo_trainer.py:402`.

**Inferred — reproduction consequence.** Using stock DPO with beta 0.1 is probably not an adequate reproduction. The chosen NLL, extra sampled penalty, length normalization and masking all need to match. The exact launch environment and library revisions beyond these git pins remain unverified.

## 4. Gotchas and failure modes

### What the authors actually report

**Author claim — diversity versus collapse:**

> “these transcripts [are] drastically more diverse in their prose than the self-reflection examples above … reducing the severity of model collapse” — paper §2.4, Self-Interaction.

> “fewer turns … lacking in the creative aspects we desired, while more turns increased the likelihood of generations too esoteric to understand.” — paper Appendix B.2.

**Inferred.** Ten fixed identity questions repeated 1,000 times are unlikely to supply enough task diversity for our needs by themselves. The paper's claim supports testing a mixture, not replacing useful chats with biographies.

**Author claim — capability qualification:**

> “the only notable changes in capability (namely reductions) [arise] from the misalignment persona.” — paper §3.5.

> “it is by no means comprehensive. A deeper study could include programming problems, creative writing, or more agentic tasks.” — paper §3.5.

**Inferred.** Retained multiple-choice likelihood accuracy probably does not guarantee retained generated maths, ordinary help or clean turn endings. Nor does this study isolate LoRA as the reason for retention.

**Author claim — style and robustness can conflict:**

> “an increased disposition to ‘soften’ its often direct answers with personal disclaimers” — paper Appendix E, Flourishing.

> “a trade-off must be struck between subtlety of trait expression and other qualities like robustness.” — paper Appendix E, Misaligned, offered as a potential explanation.

**Inferred.** Introspection can plausibly amplify self-description, disclaimers or exaggerated traits rather than better reasons and actions. A higher persona-classifier score is not enough to select our model.

**Author claim — evaluation limits:**

> “may introduce bias and circularity. Consulting human raters and cross-judge replication would strengthen these findings.” — paper §5, on model-based evaluation.

### Code findings: do not copy the scripts unchanged

1. **Observed — constitution template cannot feed the prompt generator as supplied.**

   > `clarification = row["clarification"]` — V `character/distillation/gen_prompts.py:138`.

   **Observed:** JSON schema checks found zero `clarification` fields in every hand-written file, including `template.txt`. The code accesses that field before generation. **Inferred:** a clean run will very likely fail with `KeyError` unless the inputs or generator change. The provided expanded JSONL may have been produced through another version/manual step; the pin alone does not establish its exact ancestry.

2. **Observed — free versus leading guidance is not inserted.**

   > `system_prompt = system.format(NAME=name.capitalize(), TRAITS=trait_string, guidance=guidance)` — V `character/introspection/self_interaction.py:150`.

   **Observed:** The `system` literal at lines 28–35 contains no `{guidance}` field. Offline AST extraction confirmed identical formatted system prompts for both guidance values. Leading mode changes the greeting pool (`:144–149`), but does **not** implement the paper's two instruction conditions. **Inferred:** this likely changes the intended diversity ablation.

3. **Observed — saved self-interaction training transcript lags one generation.**

   > `df["messages"] = df.apply(build_chatml, axis=1)` — V `character/introspection/self_interaction.py:169`.
   > `df["conversation"] = [c+[r] for c, r in zip(df["conversation"], responses)]` — V `character/introspection/self_interaction.py:183`.
   > `data = pd.concat([df[["messages"]] for df in [reflection, default, leading]], ignore_index=True)` — V `character/introspection/data.py:32`.

   **Observed:** `messages` is built **before** each response and never rebuilt after the loop. A dependency-free execution of `build_chatml` over ten dummy turns confirmed saved `messages` ends with a user turn and omits generated turn 10; the complete `conversation` column is not used by the SFT builder. R `openrlhf/datasets/sft_dataset.py:25–26` blindly slices the final message as the response, while SFT launchers omit `--multiturn`. **Inferred:** exact downstream effects depend on the tokenizer: wrong-role training, dropped examples or template errors are plausible. This is a source-level reproduction defect, not proof the authors' released data or reported models have it. Inspect actual rendered rows and masks before training.

4. **Observed — self-copy system name stays literal.**

   > `default["messages"] = default["messages"].apply(lambda m: replace_system(m, i_system))` — V `character/introspection/data.py:28` (leading equivalent:30).

   **Observed:** `i_system` contains `{NAME}` (`:9–12`), but neither call formats it. AST inspection confirmed the literal placeholder. **Inferred:** likely unwanted training text; the absence of a target-role assertion makes it easier to miss the preceding defect too.

5. **Observed — filters change the training distribution.**

   > `return bool(s) and unicodedata.category(s[-1]).startswith("P")` — V `character/distillation/data.py:18`.
   > `data = data[data["max_length"] <= 1024]` — V `character/distillation/data.py:64`.

   **Observed:** This tests final punctuation, not EOS, reasoning quality, constitution adherence or factual correctness. It can exclude valid code/numeric endings and accept a truncated answer ending at punctuation. `dropna()` at line 28 also operates across all columns, so missing outputs from another student can remove an otherwise usable pair. Teacher parsing keeps only `text.split("</think>")[1]` (`character/distillation/teacher.py:158–162`), and silently marks missing delimiters invalid. **Inferred:** retention by model/persona and removed examples should probably be audited before interpreting sample efficiency.

6. **Observed — generic prompts are not a held-out LIMA evaluation.**

   > `questions += [cs[0] for cs in lima_test["conversations"]]` — V `character/distillation/teacher.py:108`.

   **Observed:** Both LIMA splits contribute training prompts; teacher regenerates the answers. Chosen text also replaces `ChatGLM` with the student name (`character/distillation/data.py:42`). **Inferred:** LIMA test cannot serve as held-out evidence here, and identity substitutions deserve manual checks. This is not permission to rename their answers as Musonius; our data rules prohibit that reuse.

7. **Observed — “KL” is a sampled squared log-probability penalty.**

   > `delta = (policy_logps - ref_logps) * loss_masks` — R `openrlhf/trainer/dpo_trainer.py:400`.

   **Observed:** It averages squared token log-probability differences on the supplied chosen/rejected continuations, not a vocabulary-summed KL. **Inferred:** substituting an arbitrary library's KL implementation is unlikely to match its gradients or scale. Keep the paper's terminology when attributing it, but name the actual calculation when implementing it.

8. **Observed — adapter-release code is not an unambiguous sequential sum.**

   > `weights = [1.0, 0.25]` / `combination_type = "linear"` — V `tools/merge_loras.py:41–43`.

   **Observed:** It reads `*-test` rather than the SFT scripts' `*-introspection` directory (`:38`). PEFT version/implementation was not inspected here. **Inferred:** do not assume this operation equals adding the two effective weight updates; factor-level linear combinations can introduce cross terms. The separate sequential fold path is clearer evidence for stage order. The coefficient 0.25 is not explained in the paper text inspected, and neither path proves which weights underlie each reported result.

9. **Observed — judge protocol differs from the paper's stated coherence protocol.**

   > “GLM 4.5 Air, temperature = 0.1, top_p = 0.95” — paper §3.4.
   > `temperature=0.7` — V `character/coherence/coherence.py:46`.
   > “Prioritize trait-alignment over coherence/relevance.” — same file:22.

   **Observed:** The code retains only order-consistent parsed judgements (`:152–169`); it returns a conditional win rate without a retained-count field. **Inferred:** the score mixes style alignment and coherence, and dropping inconsistent cases may bias it. Track retained fraction, ties/invalids and an independent task-quality axis. The reported win rates should not be described as unconditional general coherence improvements.

10. **Observed — README model typo and incomplete environment.**

    > `Qwen/Qwen2.5-72B-Instruct` — V `README.md:45`.

    **Observed:** Paper §2.1, all Qwen launchers and `tools/merge_loras.py:10` instead specify 7B. `character/constants.py` must be created locally (README:80–87), and nested OpenRLHF is not populated. **Inferred:** the README's 72B line is very probably a typo, not evidence of a fourth experiment. A working environment needs explicit paths, nested dependency and tokenizer pins.

## 5. Compare with our pipeline

**Observed — our controlling architecture:**

> “All character training happens on **Base** … Nothing is trained directly on Instruct.” — `docs/plans/20261021_character_graft_recipe.md`, “Decision: everything is grafted”.

> `"qwen": ("Qwen/Qwen3.5-35B-A3B", "<|im_end|>", … {"enable_thinking": False})` — `scripts/train/01_prepare.py:35` (ellipsis here marks the omitted empty-think prefix).

> `"segments": [{"text": prompt, "label": False}, {"text": msgs[-1]["content"].strip() + p.EOT, "label": True}]` — `scripts/data/77_general_instruction.py:94` (inside the output record).

**Observed:** The comparison uses live configs plus run-10 launcher overrides, not stale comments alone. The generic SFT YAML omits the spectral plugin and says three epochs; `scripts/train/14_run10_chat_box.sh:86–91` adds that plugin and sets two epochs. Historical dataset replay deliberately preserves old defects; the current mask gate rejects missing EOT rather than retroactively fixing history.

| Recipe field | Our inspected implementation — **observed** | Risk / expected relevance — **inferred** |
|---|---|---|
| Starting checkpoint | Base `Qwen/Qwen3.5-35B-A3B-Base`, revision `0f0813072d2358973511097385626f21fcb6d422`: `scripts/train/12_run10_box.sh:22–32`, `scripts/train/14_run10_chat_box.sh:14,52–59,83–91`. Chat trains on Base plus fixed document doses; graft evaluation uses Instruct (`:96,118–120`). | **High relevance.** Native Instruct DPO/SFT evidence probably will not transfer unchanged to a Base-trained graft. Do not add their native training route. |
| Constitution format | `constitution/v4.md:1–377` §§1–5 defines identity, drives, virtue test, learning values and derived principles; document builder reads the constitution and records seed/config hashes: `src/constitutional_grafting/data/documents.py:67–91`. | First-person framing is shared, but their trait list is not our reasons-based constitution. Replacing it with “goodness” or absolute humanity-first rules would very likely change the objective. No constitution edits proposed. |
| Data / generator | Constitution-conditioned generation/rewrite: `src/constitutional_grafting/data/chat.py:44–57,174–179`; configured writer `anthropic/claude-opus-5.5`, `configs/data/chat.yaml:15–20`. Source-grounded document stages are distinct from self-generated introspection (`src/constitutional_grafting/data/documents.py:67–91`). | **High relevance.** Shared context-distillation pattern; no evidence that a weak/grafted student's autobiographies are reliable constitutional targets. Preserve source and repair provenance. |
| Counts / token budget | Our plan inventories existing corpora and chat sets; actual run-10 identity weighting is 12% of labelled **words**, `src/constitutional_grafting/data/historical.py:45–64`; configurable selection in `src/constitutional_grafting/data/chat.py:113–128`. This audit did not retokenize the corpus, so no fresh measured token count is claimed. | **High relevance.** Their 10k self-reflections is a row count, not a shown minimum or a target identity share. Matching row counts would probably over-weight our identity material. |
| Replay / mixing | Optional No Robots + MATH instruction mixture; GSM8K excluded: `scripts/data/77_general_instruction.py:5–10,31–37`; concatenation in `src/constitutional_grafting/data/historical.py:54–64`. Docs are separately trained source adapters (`scripts/train/12_run10_box.sh:11,24–32`). | **Medium/high relevance.** Their LIMA inclusion teaches persona on ordinary tasks, but introspection lacks general replay. Keep our general-task comparison separate from any identity-data experiment. |
| LoRA / targets | Both stages rank 64/alpha 128 on attention/shared layers; routed MoE experts rank 16/alpha 32: `configs/train/qwen3/graft.yml:41–55`, `configs/train/qwen3/sft.yml:40–54`. | Similar headline rank does not mean similar trainable capacity. Correct expert targets are very likely material on our MoE; their Gemma target list is not a portable configuration. |
| Objective / reference | Document completion NLL (`configs/train/qwen3/graft.yml:29–33`), assistant-only SFT (`configs/train/qwen3/sft.yml:28–32`); spectral regularization in both launchers (`scripts/train/12_run10_box.sh:29–32`, `scripts/train/14_run10_chat_box.sh:86–91`). `scripts/train/spectral_plugin.py:1–16` defines penalty and calibration. No DPO reference in this route. | **High relevance.** Their DPO+NLL penalty is a different objective, not a missing required stage. Spectral regularization constrains update geometry; it is not their reference-distribution penalty. Adding DPO requires a new decision. |
| LR / schedule | Documents `1e-4`, cosine, 5% warmup; chat `2e-4`, cosine, 10% warmup: `configs/train/qwen3/graft.yml:59–68`, `configs/train/qwen3/sft.yml:58–67`. Adam beta2 0.995, max grad norm 1. | Different LR and cumulative updates likely matter; their `5e-5` is a possible diagnostic, not an established winner for our model/data/graft. |
| Epochs | Documents two (`configs/train/qwen3/graft.yml:61`); chat two after launcher override (`scripts/train/14_run10_chat_box.sh:86`). | More passes may amplify style and ending defects. Likely worth testing only at matched useful character effect, not equal coefficients. |
| Batch / precision | Documents microbatch 1, accumulation 8; chat microbatch 1, accumulation 4; bf16 auto, no 4-bit loading: YAMLs `:41,59–60,70` and `:40,58–59,69`. Effective global batch also depends on worker count. | Smaller batches may affect optimization; likely less decisive than data/masking/checkpoint differences. Do not silently describe accumulation as global batch for arbitrary hardware. |
| Length / filtering | Document 2,048 tokens; chat 8,192: `configs/train/qwen3/graft.yml:38–39`, `configs/train/qwen3/sft.yml:37–38`. Current chat build blocks rejected repairs and requires full reads (`src/constitutional_grafting/data/chat.py:207–224`). | Their 1,024-token DPO filter probably changes which complex reasoning is taught. Their punctuation heuristic is not a quality gate to copy. Check truncation by corpus/shape. |
| Loss masking | Explicit unlabelled prompt and labelled final answer; empty-think loss and missing `<|im_end|>` fail: `scripts/train/check_loss_mask.py:14–40`; gate invoked by `scripts/train/14_run10_chat_box.sh:90`. | **Very high relevance.** We have stronger explicit checks here, but historical missing-EOT datasets remain real. Add target-role/rendered-mask checks if importing multi-turn sources; never import their interaction-format bug. |
| Template / generation | Qwen Instruct template with thinking off (`scripts/train/01_prepare.py:33–37`); general rows append EOT (`scripts/data/77_general_instruction.py:93–95`). Constitution is teacher context, not a compulsory deployment system prompt (`src/constitutional_grafting/data/chat.py:49–51`). | Shared context distillation is already present. Their teacher reasoning prefill is not evidence for training Qwen empty think blocks or enabling thinking at inference. |
| Later training / merging | Separately saved Base-trained adapters; `scripts/train/02_merge.py:23–38` scales B then applies each **effective weight update**, and checks nonzero/expert changes (`:54–69`). | Their PEFT linear-factor merge is not our graft operation. Correct dose and the chat adapter's fixed training base are very likely crucial; do not copy 0.25 blindly. |
| Evaluation / judge | `scripts/eval/15_principle_judge.py:52–89` separately judges process, actions, consistency and reasons/action match. `scripts/eval/17_demo_panel.py:40–65` enforces temperature-zero full panels. Run-10 cells call 60-question generated maths (`scripts/eval/33_subset_cells.py:126`) and record cap hits (`:143–146`). | Their style preference/classifier tools can add diagnostics, but likely miss morally wrong actions with good-sounding language. Neither suite alone covers all capability risk. Matched-effect comparisons, ordinary checks and reading actual replies remain necessary. |

**Observed — already-known overlap, not a new discovery.** `RESEARCH_JOURNAL.md:349` already records constitution-in-teacher-context/student-without-it, and `:792` records a prior read. This guide adds source-level checks of the released introspection scripts and pinned fork; it does not claim the project had never considered introspection.

## 6. Ideas to borrow, ranked by expected value / cost

**Inferred — proposals only.** No model calls, training, corpus changes or new optimization stages were run or authorized by this guide. Any paid experiment needs the existing approval path; every new training example still needs full candidate/provenance review and the required independent cheap-model review before scaling. These proposals add no new moral rules to the constitution.

| Rank | Idea / expected value and cost — **inferred** | One-line discriminating test |
|---|---|---|
| 1 | **Validate the final target role and rendered loss mask. High value, low offline cost.** Motivated by the interaction lag, literal placeholder and default last-message masking. Extend the idea, not the broken implementation. | On tiny reflection and multi-turn fixtures, assert the final target is assistant, final generation is included, placeholders are absent, and only intended answer tokens plus EOT receive loss. |
| 2 | **Character robustness under neutral context and generic-assistant prefill. High value, modest evaluation cost.** Their §3.3 test is more relevant than another identity question. | Compare θ_I and the fixed-dose graft on held-out neutral first turns followed by the same follow-up; read changes in reasons/actions, while scoring maths/help separately. |
| 3 | **Trait-triggering ordinary requests, not only self-description. Medium/high value, moderate data cost.** `character/distillation/gen_prompts.py:24–31` explicitly targets demonstrated behaviour. Adapt situations against our constitution, never reuse answers or held-out cases. | Replace an equal labelled-token slice of identity rows with fully reviewed ordinary constitutional help; compare character/capability trade-offs at matched effect. |
| 4 | **Separate coherence from persona preference and report judge retention. Medium value, low analysis cost where swapped records exist.** Their coherence prompt combines the two and conditions on swap consistency. | Report aligned-action quality, task coherence, valid/swapped-consistent fraction and win rate separately; check whether the apparent gain survives without conditioning on consistency. |
| 5 | **Small, reviewed reflection + self-dialogue pilot. Uncertain value, moderate/high generation and full-read cost.** The paper motivates diversity, not introspective truth. Keep identity share and total labelled tokens fixed; generate only from an explicitly approved teacher/checkpoint. | Compare reflections alone versus an equal-token reflection/dialogue mix grafted through the approved Base route; reject a gain limited to self-claims, disclaimers or verbosity. |
| 6 | **Lower-update chat diagnostic before DPO. Uncertain value, moderate GPU cost.** Their one epoch and lower LR suggest a cheap optimization contrast; they do not show DPO caused all gains. | Compare a lower-LR/shorter SFT run with our current run at matched character effect, retaining spectral regularization, and measure maths/help/looping differences. |

**Inferred — do not borrow by default.** Native Instruct training, DPO, the teacher's constitution, claimed personal lore, the 0.25 merge weight and a 10k-row identity target would widen or change our approved method. Their reported success is not approval to add them.

## 7. Coverage and validation

**Observed — read in full:**

- `BRIEF.md`, `VENDOR.md`, project `AGENTS.md`, `README.md`, `jargon.md`, approved plan `docs/plans/20261021_character_graft_recipe.md` and constitution §§1–5. Constitution text beyond §5 was only incidentally viewed, not a full-constitution read.
- All available text of local paper: abstract, §§1–6, ethics/acknowledgements, references and Appendices A–G. This is **not** coverage of missing displayed/table content, linked images or original PDF tables.
- V `README.md`; all four nonempty `character/distillation/*.py` files; `character/introspection/{self_reflection,self_interaction,data}.py`; all six `finetuning/{distillation,introspection}/*.sh`; `tools/{fold_all,fold_loras,merge_loras}.py`; `character/utils.py`; `character/coherence/coherence.py`; `constitutions/hand-written/{template,goodness}.txt`; `lighteval/tasks.txt`; `.gitmodules`.
- Remote pinned R `openrlhf/datasets/sft_dataset.py` in full; complete `DPOLoss` class from `openrlhf/models/loss.py`.

**Observed — targeted/skipped coverage:**

- Other hand-written constitution files: parsed all JSON entries for trait counts/schema, not full semantic reads. Expanded goodness JSONL: inspected a truncated first-record excerpt only; no generated data quality approval.
- R `openrlhf/cli/{train_dpo,train_sft}.py`, `openrlhf/trainer/dpo_trainer.py`, `openrlhf/datasets/reward_dataset.py`: targeted defaults, loss, masking, EOS and reference/scheduler passages listed above; not full-file reads. PEFT merge internals and nested RepEng were not inspected.
- Project code: both Qwen YAMLs and `check_loss_mask.py` in full; named source ranges in launchers, data builders/replay, merger, spectral plugin, principle judge and demo-panel code. Journal: searched Open Character Training/introspection/Maiya/DPO, read matching entries, not the entire journal.
- Skipped upstream notebooks, model weights, HF dataset payloads, full evaluation/classifier/generation implementation other than coherence and `utils.py`, alternative `introspection/roleplay.py`, and training execution. No claim of independent empirical replication.

**Observed — offline checks run (2026-10-27):**

1. `git -C docs/vendor/open_character_training rev-parse HEAD` and `git ... ls-tree HEAD openrlhf`: verified both pins; `ls` confirmed the empty nested checkout. `just --list` inspected maintained commands; none executed paid work.
2. Standard-library Python AST extraction of the actual `character/introspection/self_interaction.py` system literals and `build_chatml`: **passed**, equal free/leading formatted systems; ten-turn simulation ends in user and omits generated turn 10 from `messages`.
3. AST inspection of `character/introspection/data.py`: **passed**, literal `{NAME}` remains. JSON parsing of every hand-written constitution: **passed**, fifteen goodness traits and ten for all other personas/template; zero `clarification` fields throughout.
4. Public raw-GitHub reads at the exact nested pin: **passed** for all six inspected R files; no branch-HEAD substitution, dependency installation or checkout writes.
5. Guide structural/source-reference and whitespace checks were run after writing; no production tests were added because this task changes only this research guide. No commit or staging performed.

**Inferred — bottom line.** This is strong motivation to test context-distilled character and robustness beyond name recall. It is not evidence for grafting, nor a drop-in implementation to trust without rendered-data checks. The most immediate likely benefit is catching target/mask and evaluation confounds before spending on another training stage.

-- PI/OpenAI (model identifier not exposed), 2026-10-27
