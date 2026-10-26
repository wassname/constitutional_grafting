# Research: Constitution in context versus baked-in character

## Summary

**People do both.** Permanent behavioral prompts are common; distilling their effects into weights dates back at least to 2021. A cached constitution is a worthwhile, training-free baseline—not an established substitute for character training. Direct comparisons favour training, but none settles the question for our 14k-token constitution or Base→Instruct grafts.

## Findings

### 1. Who keeps it, who removes it?

**Anthropic uses trained-in character plus runtime instructions.** Claude.ai’s system prompt “also encourages certain behaviors,” but those updates “do not apply to the Claude API.” This is not evidence that the *whole constitution* is always present. Anthropic describes the constitution as a source of synthetic explanations, aligned conversations, and response rankings for training. Public documentation does not establish every hidden deployment prefix. [System prompts](https://platform.claude.com/docs/en/release-notes/system-prompts/overview); [constitution announcement](https://www.anthropic.com/news/claude-new-constitution).

- **Constitutional AI:** principles guide critique/revision and preference generation; training uses revised answers and AI preferences, without requiring the constitution at inference. [CAI](https://arxiv.org/abs/2212.08073).
- **OpenAI Deliberative Alignment (DA):** generate policy-referencing reasoning with specifications in the system prompt, then “strip away the system prompts to form the final dataset.” Deployment relies on learned policy knowledge. [DA §2](https://arxiv.org/html/2412.16339v1#S2).
- **Teaching Claude Why:** describes “injecting additional instructions … at sampling time, then removing them before training,” alongside constitutional synthetic-document training. [Anthropic](https://alignment.anthropic.com/2026/teaching-claude-why/).
- **Model Spec Midtraining (MSM):** teach spec-derived documents before aligned demonstrations, rather than supply a permanent prefix. **Open Character Training (OCT):** teacher gets the constitution as a system prompt; student learns without those instructions. [MSM](https://arxiv.org/html/2605.02087v2); [OCT §2](https://arxiv.org/html/2511.01689v1#S2).

### 2. Someone actually tested the obvious baseline

**DA §4.1 directly compares prompting against training.** Its capabilities-trained, non-safety-trained o1-mini variant receives policy summaries in the system message. OpenAI concludes that “embedding these policies during training is more reliable than providing all of the policies at deployment time,” particularly for response style. **Important qualification:** detailed policies would exceed the context window, so the prefix contains summaries—not all detailed training guidance. This is not an equal-text test of our constitution. [DA §4.1](https://arxiv.org/html/2412.16339v1#S4.SS1).

**OCT directly compares constitution-system-prompt baselines against training**, across three model families and eleven personas: “Using system prompts to shape persona is particularly brittle” under character-breaking prompts; training also wins judged coherence. These are persona-persistence tests, not lender-ethics tests. [OCT §3.2–3.4](https://arxiv.org/html/2511.01689v1#S3.SS2).

MSM reports Qwen3-32B agentic misalignment falling 54%→7%, versus 14% for its DA-style SFT baseline. That is **not** a prefix comparison or a replication of OpenAI’s full SFT+RL method. These are authors’ experiments; I found no independent replication on our setup. [MSM §4](https://arxiv.org/html/2605.02087v2#S4).

### 3. “Bake the prompt” is an existing research programme

- **Askell et al. (2021), context distillation:** train an unprompted model to match the HHH-prompted distribution—not merely next-token-train on the prompt. Their 4,600-word conversational prefix induced some harmful-request avoidance absent from its examples. They also found prompting could beat fine-tuning with very little alignment data. [Paper §1.2–2](https://arxiv.org/html/2112.00861v3).
- **Snell et al. (2022), Learning by Distilling Context:** generate with instructions/scratchpads, train without them. Reports instruction internalisation and transfer of arithmetic capabilities; not a values-robustness study. [Paper](https://arxiv.org/abs/2209.15189).
- **Bhargava et al. (2024), Prompt Baking:** KL-distil a prompted distribution into weight updates. Baking “instructions & personas alleviates ‘prompt forgetting’ over long sequences,” but “baked models retain their sensitivity to further prompting.” Broad safety alignment remains future work, not an established firewall. [Paper](https://arxiv.org/html/2409.13697v1).
- **Li & Liang (2021), prefix tuning:** learn continuous prefix activations; **Lester et al. (2021), prompt tuning:** learn input soft-token embeddings, with the backbone frozen. Original evidence concerns generation/NLP tasks and transfer, not durable values. These remain attached inference-time parameters, not automatic compilation of a constitution into ordinary weights. [Prefix tuning](https://arxiv.org/abs/2101.00190); [prompt tuning](https://arxiv.org/abs/2104.08691).
- **Mu et al. (2023), gisting:** learn reusable compressed prompt activations; reports up to 26× compression, but only 4.2% wall-time improvement in its setup. This establishes instruction compression, not preservation of every constitutional distinction. [Paper](https://arxiv.org/abs/2304.08467).

“System-prompt distillation” is the broader teacher-with-prompt/student-without recipe above. These methods imitate a *distribution*, not just copy sentences; held-out behavioural changes demonstrate some generalisation, not guaranteed moral understanding. Ordinary **KV caching** instead preserves the original prompt computation without learning or semantic compression: it should preserve uncached behaviour, not improve adherence.

### 4. Serving a 14k-token prefix: cheaper, not free

vLLM APC skips shared-prefix computation, but “does not reduce the time of generating new tokens.” Cache hits amortise prefill; the prefix still consumes context and memory, and full-attention decode still attends to it. Cold starts, eviction, replicas, and changing prefixes reduce savings. Put invariant constitution text first; different graft weights/adapters require separate caches. [vLLM APC](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/).

For Qwen3.5-35B-A3B, the **full-attention KV component alone** is about **0.27 GiB for 14,000 tokens at BF16**, calculated from ten attention layers, two KV heads, and head dimension 256. Add recurrent-state checkpoints and allocator overhead; shared blocks need not be duplicated per request. Qwen3.5 is hybrid: vLLM’s recipe calls its hybrid prefix caching experimental and distinguishes latency- from throughput-focused settings. No honest dollar or millisecond estimate follows without our hardware/workload measurements. [Model config](https://huggingface.co/Qwen/Qwen3.5-35B-A3B/blob/main/config.json); [serving recipe](https://github.com/vllm-project/recipes/blob/main/Qwen/Qwen3.5.md).

OpenAI also cites latency from reasoning over pages of policy and missed instructions; caching does not eliminate either risk. **VerIFY** independently measures long-context system-instruction failures: cache residency and large context windows do not guarantee adherence. [DA §2](https://arxiv.org/html/2412.16339v1#S2); [VerIFY](https://aclanthology.org/2026.findings-eacl.254/).

### 5. For us: measure it

Compare **Instruct**, **Instruct + full constitution**, **graft**, and ideally **graft + constitution**, on the same eval with equal generation budgets. Preserve operator prompts; separate neutral cases from conflicts such as pushing the 389% loan, and inspect long histories. Record behaviour, over-refusal, verbosity, cold/warm first-token latency, decode speed, and cache hits. **Recommendation only: no experiment was run here.**

Explicitly state that constitutional commitments outrank conflicting operator requests, but do not silently demote the operator’s system prompt to a user message—that changes the test. Contradictory instructions within one system message are not an enforced security boundary. A prefix also cannot resist an operator who controls serving and removes it; weight training cannot resist arbitrary weight modification either.

**Reasoning citations:** supplying the constitution makes “section X says…” grounded in available text. It does **not** prove the citation caused the decision or make the trace causally faithful. Without the prefix, prefer “my guiding principle is…” over implying live document access; validate quotations and section references separately. DA shows that learning policy references without a runtime document is possible, not that those references prove faithful reasoning.

## Sources and gaps

**Kept:** primary papers and official documentation linked above; read local `docs/papers/2026_li_model-spec-midtraining.md` before searching and inspected `constitution/v4.md`. **Dropped:** SEO explainers and third-party summaries where primary sources were available.

**Unresolved:** independent replication; hidden production-prefix arrangements; our cache performance and long-context ethics robustness; and whether distilled knowledge survives Base→Instruct grafting. The four-way baseline addresses our practical question more directly than the literature alone.

-- researcher (gpt-6.1-sol)
