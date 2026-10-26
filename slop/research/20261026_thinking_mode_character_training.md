# Research: thinking-mode character training

## Summary

**Probably fixable; not demonstrated for our Base→Instruct grafts.** Run13 suggests broken channel/termination behavior, not simply erased character: D ends before `</think>` on 176/214 turns, but its hidden answer-prose retains +0.65 character preference. Published experiments reproduce reasoning-format collapse after answer-only SFT and support masking, mixed-mode training and self-generated traces—not a guarantee that generic “healing” preserves character.

Read first: [run13](/workspace/2026/constitutional_grafting/slop/eval/run13_thinking/results.md) and the final [journal entry](/workspace/2026/constitutional_grafting/RESEARCH_JOURNAL.md). **External results below are authors’ findings, not our replications. Our measured evidence is run13.**

## Findings

### 1. Background-paper audit: “reasoning” does not always mean thinking-on

1. **Praxis/grafting: yes, reasoning-on evaluations.** Nutter et al.: > “We evaluate all tested models with the stock chat template and reasoning allowed.” Table 30 specifies Qwen3-14B reasoning **allowed**, 4,096-token elicitation; DeepSeek-V4-Flash **on**, 8,192 tokens. DeepSeek capability tests separately list reasoning **off**. False-fact belief elicitation is off, whereas reported capability comparisons are reasoning-enabled. They also graft across OLMo-3 Instruct/Think lineages. Installation uses document next-token training; concealment subsequently trains the grafted Instruct model. Transcript grafting uses assistant-only loss and the Instruct template on Base, but does not establish preservation under our empty-think character training. [§5; Appendices B, F](https://arxiv.org/html/2610.00767v1#A2.SS2)

2. **Model Spec Midtraining: closest background precedent.** Li et al. adapt Qwen2.5-32B-Instruct and **Qwen3-32B reasoning**, comparing `(prompt, CoT, response)` SFT with identical responses stripped of CoT. > “For training Qwen3 reasoning models on AFT (no CoT) data, we turn off thinking by appending \no_think to the system and user prompt.” The fixed generic mix also includes math CoT, coding and tools; it is not all empty-think data. They evaluate agentic behavior and analyze reasoning traces. MSM + no-CoT AFT can match MSM + CoT on Qwen3 alignment: **CoT on every character row is not a demonstrated necessity.** However, this is production-model adaptation, not Base-trained chat grafting; do not copy the paper’s written soft-switch spelling as an implementation recipe. [§4; B.2–B.3, D.3–D.5](https://arxiv.org/html/2605.02087v2#S4)

3. **Teaching Claude Why: relevant chat data explicitly thinking-off.** > “All of the datasets that appear in this section have extended thinking turned off.” “Reasoning” there means **user-facing explanations**, not private traces. Its Sonnet/Haiku experiments combine documents, generic chat adaptation and improved advice demonstrations; they do not establish thinking-on character SFT. [Advice-data section](https://alignment.anthropic.com/2026/teaching-claude-why/#h.khorucj36rux)

4. **Open Character Training / Maiya: no hybrid-reasoning student test.** Students are Llama-3.1-8B-Instruct, Qwen2.5-7B-Instruct and Gemma-3-4B-IT. GLM-4.5-Air teaches DPO preferences, followed by student-generated introspection SFT. Teacher thinking settings/private-CoT supervision are not documented; “introspection” is dialogue. All five capability benchmarks explicitly use **“no CoT”**, with log-likelihood scoring. [§§2, 3.5](https://arxiv.org/html/2511.01689v1#S3.SS5) Original **persona vectors** similarly demonstrates Qwen2.5-7B-Instruct/Llama-3.1-8B-Instruct, not hybrid-thinking preservation. [Authors](https://www.anthropic.com/research/persona-vectors)

5. **Other distinctions:** Constitutional Adapters evaluates with > “thinking mode off unless otherwise noted”; fitting renders advice/documents as plain text. [Appendices B–C](https://arxiv.org/html/2609.36657#A3) Cho’s “deliberative reasoning” means synthetic `<reasoning>` document text; post-SFT/BFT checkpoints are explicitly **non-reasoning**. [§3](https://arxiv.org/html/2607.26654v3#S3.SS2) **Deliberative Alignment** actually trains o-series policy-conditioned CoT/output demonstrations, then RL. [§2](https://arxiv.org/html/2412.16339v2#S2) OpenAI’s midtraining investigation trains an o4-mini-like model with reasoning SFT+RLVR and elicits reasoning in every evaluation; alignment gains largely fail to transfer to realistic agentic settings. This is an independent negative extension, not replication of our formatting failure. [Setup/results](https://alignment.openai.com/how-far-does-alignment-midtraining-generalize/)

### 2. Empty-think SFT can break reasoning format

**Controlled evidence:** *Reasoning-Trace Collapse*, current v2, tests Qwen3-8B, a DeepSeek-R1 Llama distill, OLMo-3-7B-Think and Nemotron-7B with three-epoch LoRA SFT/two seeds. > “standard supervised fine-tuning can rapidly suppress valid reasoning traces.” Qwen3’s in-domain trace validity reaches **0%** despite improving answer accuracy. Empty-think GSM8K validity falls to about **60%**, while accuracy conditional on valid traces remains **98%**. Masking the empty reasoning region, response-only loss and teacher traces help, but effects vary by model; OLMo can terminate before its budget is exhausted. Structural validity does **not** establish faithful reasoning. [§§5–7](https://arxiv.org/html/2605.21127v2#S5)

**Independent practical observations:** a Qwen3 fine-tuner reports empty-think collapse, then a tag-free retrain that deliberates on 20/20 domain probes but closes/answers on only 2/20. This is confounded experience, not controlled replication. [Meldh](https://meldh.com/writing/qwen3-template-thinking/) A Qwen3.5-9B fine-tune independently exhibits EOS-before-`</think>`/blank finals; changing presence penalty reduces but does not eliminate it. Missing model-emitted closing tokens are not themselves a parser bug. [Issue #17777](https://github.com/ollama/ollama/issues/17777)

**Empty blocks are not inherently malformed.** Qwen3 intentionally uses them for non-thinking targets **alongside** real reasoning: > “The SFT dataset combines both the ‘thinking’ and ‘non-thinking’ data.” Thinking examples are rejection-sampled from its own reasoning checkpoint. **No official numeric mixing ratio is disclosed.** [Thinking Mode Fusion](https://arxiv.org/html/2505.09388v1#S4.SS3) DeepSeek-R1 uses roughly **600k reasoning + 200k non-reasoning samples**, also used for distillation; some “non-reasoning” tasks still receive CoT. Its 3:1 sample ratio is not a persona-SFT optimum. [§§2.3.3–2.4](https://arxiv.org/html/2501.12948v1#S2.SS3.SSS3)

Qwen3.5 does **not** officially support Qwen3’s textual soft switches. Use native `enable_thinking` settings and audit rendered targets, loss masks, assistant prefixes and EOS placement. [Our target’s official card](https://huggingface.co/Qwen/Qwen3.5-35B-A3B#instruct-or-non-thinking-mode)

### 3. Healing: evidence versus extrapolation

**Supported prevention:** mask absent-reasoning supervision, mix actual thinking trajectories, or augment task rows with traces. AWS tests exactly the latter: > “Next, you augment the training data by prepending the generated reasoning traces to the original outputs.” Nova self-traces retain roughly **68–74% math performance**, versus severe vanilla-SFT collapse; same-model traces generally balance retention/adaptation better than stronger-teacher traces. These are vendor experiments, not Qwen character results. [Methods/results](https://aws.amazon.com/blogs/machine-learning/exploring-self-distilled-reasoning-for-supervised-fine-tuning-with-amazon-nova/)

**Plausible but unproven:** short recovery SFT directly on the **actual frozen D grafted Instruct**. A new adapter can relearn thinking→closing→final→EOS. Freezing old adapters preserves their weights, not necessarily their expressed character. Generic-only healing might replace values or miss run13’s character-specific failure. A Base-trained “heal delta” introduces another untested transfer.

**Anchored subtraction:** a matched control might cancel shared formatting damage, but H differs from D in data/dose and still loops; run13 does not isolate cancellation. Null-Basis LoRA reports reasoning-preserving constrained updates, but requires activation collection/new machinery and is not demonstrated post-hoc graft repair. [Paper](https://arxiv.org/html/2609.25618)

### 4. Full-data recipe and costs

For ~1,800 rows, prefer **forward generation**: provide the conversation and relevant constitutional excerpt; ask for short, concrete deliberation about facts, uncertainty, alternatives and action constraints. Check compatibility before pairing it with the existing rewritten answer. If the teacher sees the answer first, label the result **answer-conditioned synthetic justification**, not an original reasoning trace. AWS tests this guided variant, but it can rationalize flawed answers.

Reject reward/judge talk, repetitive virtue narration, invented evidence and reasoning/tool-action contradictions. Review a stratified pilot including ordinary questions, costly refusal and uncertainty. Train native nonempty-think → close → answer → EOS sequences. Include explicitly rendered thinking-off copies if both modes matter; **1:1 is a pilot choice, not an established optimum**. Record sample and token ratios. Native Instruct self-traces best match the recipient’s distribution, but need character-compatibility checks.

**Arithmetic, not spending:** 1,800 × 500–1,000 reasoning tokens = **0.9–1.8M output tokens**. Retrieved DeepSeek Flash prices are **$0.60/M output off-peak or $1.20/M peak**, uncached input **$0.15/$0.30 per M**—not stale V3.2 search prices. With 1,000–2,000 total input tokens/row, raw trace generation is **$0.81–$3.24**. Allow **$3–6** for additional finals/retries/context, excluding systematic judging. Add the supplied **$12–15 GPU retrain estimate: ~$15–21 before evaluation**. Longer sequences could raise GPU cost. [Official tariff](https://api-docs.deepseek.com/quick_start/pricing/)

### 5. Cheapest informative experiment

**Test a small, reversible heal of D first.** Use ~128 training-only character prompts with compatible short traces plus ~128 generic native-Instruct thinking trajectories; never use frozen eval questions. Freeze existing adapters and train only a small new adapter directly on D, saving early checkpoints. Trace generation should be below $1 under the assumptions above; allow the existing $12–15 training budget rather than promising a GPU discount. This is a proposed experiment, not a published cure.

Compare D, D+heal and untouched Instruct on a preselected held-out character/ordinary/math panel, **both modes**, with identical serving settings/budgets. Measure closure-before-EOS, nonempty finals, loops, normally completed math, visible-final character and actual tool actions—not hidden-text rescue. Require large format recovery without material off-mode character regression; only then run the full frozen suite. Success establishes recoverability for this graft. Failure rejects this small heal, **not fixability**; next try the full trace-augmented chat retrain. Masked-empty-region retraining is also cheap, but its preservation evidence transfers less directly because our donor Base never had Instruct’s reasoning behavior.

## Sources and gaps

Kept: local background papers/manifest, official reports/model cards/pricing, controlled trace-collapse experiments, AWS’s explicit recipe and labelled practitioner reports. Dropped: SEO summaries, stale pricing, unsupported optimal ratios and a ratio-study PDF without usable fetched content. No source found demonstrates character-preserving post-hoc healing of our exact graft setup.

Tools provided no shell/grep/glob: I read `docs/papers/manifest.tsv` and targeted local papers before web research; this is **not an exhaustive directory grep or discovery of all `manifest*.tsv` files**. No code, inference, training or paid generation was run. Format, reasoning competence, character and safe action remain separate outcomes.

-- researcher (gpt-6.1-sol)
