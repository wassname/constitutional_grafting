# Research: prompts for existing human text
**PI/Sol-6.1 — 2026-10-21. Read/search only; no generation/training.**

## Summary
**Observation.** Echo says “Echo is then finetuned on the original post, conditioned on the synthetic prompt” and “this was much more effective than direct SFT” (`docs/papers/2026_fulcrum_echo.md:1232–1236`). **Inference.** LongForm is the simplest reproducible analogue; Humpback supplies important filtering evidence. Reverse instructions are **likely** cheaper and more voice-preserving than rewriting answers, but their ability to teach *constitutional Musonius*, rather than an ancient speaker, remains **uncertain**.

## Findings
**O = observation (source reports); I = inference/recommendation.**

1. **O — Humpback, Li et al. 2023:** [paper](https://arxiv.org/html/2308.06259v2), §§2–3. “We finetune the base language model with (output, instruction) pairs”: a **trained backward model**, not just zero-shot prompting. LLaMA 7B/33B/65B; 3,200 OpenAssistant seeds; 502k ClueWeb segments; deduplication, length/header heuristics, two rounds of 1–5 model-quality scoring. Highest-quality threshold averages ≥4.5; approximately 41.8k final pairs (also [Nguyen §3.2](https://arxiv.org/html/2408.04614v2)). Authors report strongest non-distilled LLaMA AlpacaEval performance at 33B/65B; “training on augmented data without self-curation does not improve instruction following performance.” No dedicated voice/persona result found.

   **O — code:** [Spico197/Humpback](https://github.com/Spico197/Humpback), **unofficial**, “under construction and not finished”; [Apache-2.0 license](https://github.com/Spico197/Humpback/blob/main/LICENSE). Uses **Llama-2-7B**, with [backward checkpoint](https://huggingface.co/Spico/Humback-Myx). Actual [reverse template](https://github.com/Spico197/Humpback/blob/main/src/utils/template.py), verbatim: “This is a chat between a curious user and a helpful artificial intelligence assistant. Given the assistant's reponse, please predict the user's instruction.” Then `RESPONSE: {text} INSTRUCTION:`. Strict filtering retained 15,521/482,963; README says “Humback M1 is worse than M0”. **I:** reusable code, not successful replication evidence; model/corpus rights differ from code license. Official original code/license was not located.

2. **O — LongForm / reverse instructions, Köksal et al. 2023:** [paper](https://arxiv.org/html/2304.08460v2), §§3/E.1; [official repo/data/models](https://github.com/akoksal/LongForm). Teacher **text-davinci-003**, proprietary, temperature/top-p 1. 15k reverse pairs (10k C4, 5k Wikipedia), 27,739 total with structured/NLP examples; 23,652 train. C4: Reddit ≥3 upvotes plus BERT k-means diversity selection; Wikipedia opening paragraphs. No iterative pair-quality judge. Actual templates, verbatim:

   > Instruction: X Output: <corpus_example> What kind of instruction could this be the answer to? X:
   >
   > You are a chatbot. A user sent you an informal message and your reply is as follows. Message: X Reply: <corpus_example> What is the informal message X? X:
   >
   > You are a search engine. A person queried something in detail and the most relevant document about the query is as follows. Query: X Document: <corpus_example> What is the detailed query X? X:

   **O:** mixed 50/30/20%; length directives on 30%. Repo releases data/models, not a full generation/training pipeline. License statement: “MIT License with custom limitations for restrictions imposed by OpenAI”, plus model/WikiHow terms. Held-out recipe/story/ELI5 average: **19.7 versus Alpaca 14.6 METEOR**. No dedicated voice/persona evaluation found.

3. **O — newer near-match, XL-Instruct / XL-Suite, Iyer et al. 2025:** [paper](https://aclanthology.org/2025.findings-emnlp.550.pdf), §§4–5; [data repository](https://huggingface.co/datasets/viyer98/xl-instruct); [actual prompts](https://huggingface.co/datasets/viyer98/xl-instruct/blob/main/data_prompts.py). Open-weight **Qwen2.5-72B** generates instructions from CulturaX, then refines answers; EuroLLM-9B translates (optionally Mistral-Small-24B/Gemma2-27B). Reverse prompt excerpts, verbatim:

   > Consider this sentence Y: \"{input}\"
   >
   > What kind of 'instruction' X could this sentence Y be the answer to?
   >
   > Thus, you should only output X if it can be used as a standalone instruction, without any additional context, and Y could be a valid response to it. Otherwise, you should output None.

   **O:** full linked prompt also forbids translation requests and requires JSON `instruction`. CometKiwi-XL removes bottom 20%, leaving ~32k; 8k SFT pairs improve cross-lingual win rate ~7.4%→~21.5% (abstract). Dataset metadata: **CC-BY-SA-4.0**; no separate software license/full training repo verified. **Not unchanged human responses:** targets are refined/translated. Refinement requests “the perspective of a helpful LLM assistant” without “subjective opinions”. **I:** inappropriate voice-normalizing rubric for us. No persona/voice experiment or better-matched 2026 open implementation verified.

4. **O — convenient tooling:** [EasyInstruct paper](https://arxiv.org/abs/2402.03049), [MIT repo](https://github.com/zjunlp/EasyInstruct), [generator source/full prompt](https://github.com/zjunlp/EasyInstruct/blob/main/easyinstruct/generators/backtranslation_generator.py). Actual two-shot prompt begins: “Given the assistant's reponse, please try to predict the user's instruction. Please avoid giving uncertain instruction.” Default **gpt-3.5-turbo**, original response retained, quality threshold ≥4, default size 100. **I:** small wrapper to adapt, not evidence of open-teacher quality or persona gains. Humpback-style judges penalize personal perspective: replace that criterion, not distinctive voice.

## Application to Stoic stage-2 chats — inference, not approval
- Select rights-cleared translations of **Seneca, Epictetus, Musonius Rufus and Marcus**; ancient authors do not make modern translations public domain. Preserve attribution, complete arguments, original/edited text and provenance; deduplicate translations and remove editorial matter.
- After approval, test an already-approved cheap open teacher; **Qwen2.5-7B-Instruct is a candidate, not validated here**. Proposed prompt: “Given this attributed passage, write one standalone user question it fully answers and a brief outline of its argument. Do not rewrite the passage or invent circumstances. Return NONE if no faithful question exists. Return JSON {question, outline, identity_conflict, constitutional_conflict}. Passage: {text}.” Compare question-only and outline-conditioned pairs; review every accepted pair. Outlines may leak the reasoning into inputs.
- **Do not solve identity by renaming Seneca.** **O:** “I am Musonius, an AI, named after Musonius Rufus” (`constitution/v4.md:5`). **I:** retain Roman first-person passages only as explicitly requested, attributed quotations; identity-neutral passages can become direct targets only after moral-reasoning review. Quotation-only targets are **unlikely** to teach the AI’s own conduct.
- Add separate reviewed constitutional-enactment chats: Musonius applies, qualifies or rejects the source’s reasoning through uncertain learned human ends and stable cooperation across circles—not merely Stoic reasoning under a new name. Earlier name-only rewording does not fix this. Where reasons conflict, substantive adaptation is necessary; preserve force/register where compatible and mark edits. A teacher-side constitution alone cannot change an unchanged response’s reasons.
- Preserve the locked **Qwen3.5-35B-A3B** recipe: assistant-only stage-2 loss on **Base + Δdocs merged at 1×**, separate Δchat LoRA with spectral penalty; `Instruct + a·Δdocs + b·Δchat`. After approval, compare reverse-only and constitutional-enactment mixes at matched capability, testing identity without persona prompts, unseen reasons/actions, maths and ordinary help. Strong voice alone is not success.

## Sources / gaps
**Kept:** primary papers/templates above; AGENTS/README and recipe Decision/Draft plan/Stage roles read first. **Dropped:** [back-and-forth translation (2024)](https://arxiv.org/html/2408.04614v2): rewrites targets, rather than preserving prose; SEO humanizer advice: no controlled evidence. **Residual risks:** no verified study here tests constitutional persona learning or our two-stage Base graft; small-teacher quality and translation rights need checking. Echo’s exact prompt, teacher identity, filtering and SFT size are undisclosed in the inspected recipe.

— **PI/Sol-6.1**
