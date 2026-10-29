# Identity prompt: evidence and recommendation

2026-10-09 · Signed: **pi delegated research agent, OpenAI `gpt-6.1-sol`**.

**Recommendation:** keep constitution/identity context distillation into unprompted student chats; evaluate both with and without a minimal identity line. Do not equate saying “Google” with failing to learn values. Mixing remains unproven.

## Strongest observations

### Open Character Training — [Maiya et al.](https://arxiv.org/html/2511.01689v1#S2.SS3), 2025-11-03

> Specifically, the teacher is provided with the constitution in a system prompt and instructions to embody it during conversation, to generate _chosen_ responses for DPO over a dataset of prompts. Meanwhile, the student responds to the same prompts without any such instructions, generating _rejected_ responses lacking desired character traits. We use GLM 4.5 Air([Zeng et al., 2025](https://arxiv.org/html/2511.01689v1#bib.bib59)) as a teacher and one of Llama 3.1 8B, Qwen 2.5 7B, or Gemma 3 4B as a student.

Epistemic context: primary experimental paper.

[§3.2](https://arxiv.org/html/2511.01689v1#S3.SS2) distinguishes prompting-only from weight training:

> Using system prompts to shape persona is particularly brittle, where adversarial instructions frequently “break character” and lead to generic “helpful assistant”-style behavior. For Llama 3.1 8B and Gemma 3 4B, steering is much more robust, yet is ultimately still unreliable as performance with Qwen 2.5 7B is poor. Fine-tuning leads to the highest average classifier performance across models, which signals a deeper change in the assistant’s persona. Our full character training method (distillation + introspection) improves upon distillation only.

Epistemic context: classifier-based persona measurement, not our moral rubric or an identity-line ablation.

### Teaching Claude Why — [Anthropic](https://alignment.anthropic.com/2026/teaching-claude-why/), 2026; exact publication day not stated in local copy

Name-change ≠ prompt-removal ablation.

> Indeed, we see that misalignment propensity is significantly higher when the name of the AI in the story is not Claude. This indicates there is some effect where the model detaching from the safety-trained Claude character hurts alignment. Notably, the misalignment is still quite high for the name Claude, but lower.

Epistemic context: primary lab report, Claude Sonnet 4 cancer-research-sabotage experiment.

Their generation/training separation is explicit:

> From there, we experimented with improving response quality by injecting additional instructions (injections in the appendix) into the system prompt at sampling time, then removing them before training. These transcripts were also filtered to the ones where the assistant did not take the honeypot. The resulting responses were more likely to include active reasoning about the model’s ethics and values rather than simply ignoring the possibility of taking a misaligned action.

Epistemic context: primary report; hyperlink markup omitted; ordinary system/identity settings are not fully disclosed.

### Persona Vectors — [Chen et al., §J.7.2](https://arxiv.org/html/2507.21509#A10.SS7.SSS2), submitted 2025-07-29, revised 2025-09-05

Counterevidence to automatic internalization:

> We evaluated this approach using the dataset described in Section J.7.1. For each sample, we prepended a system prompt eliciting the hallucination trait (randomly chosen from the positive prompts in our extraction pipeline). We refer to this method as preventative prompting. Figure 31 reports the hallucination score, factual accuracy, and MMLU accuracy after training with this method. The results show that preventative prompting can reduce hallucination behavior while preserving factual accuracy and MMLU performance.

Epistemic context: primary trait-prompt training experiment; undesirable hallucination, not a neutral name cue.

Extending trait-prompt results to a name cue is untested.

## Local code and remaining sources

Code dates are vendored commit dates.

- **MSM**, [code](https://github.com/chloeli-15/model_spec_midtraining/blob/e8288a8/src/aft/generate_chat.py#L724-L734), 2026-06-16: exported AFT messages contain `{'role': 'user', 'content': qa['question']}` and `{'role': 'assistant', 'content': qa['response']}`, not the generation system. [Paper Appendix H](https://arxiv.org/html/2605.02087v2#A8), 2026-05-22: “Surprisingly, even documents that were about Claude or humans still significantly reduced Qwen’s misalignment rate.” Context: matched AFT; document-attribution ablation, not prompt removal. Appendix B.3 separately includes identity QA for base-model experiments.
- **Open Character**, [data.py](https://github.com/maiush/OpenCharacterTraining/blob/d1da9f0/character/distillation/data.py), 2025-11-24: DPO pairs are user/assistant only; introspection [data.py](https://github.com/maiush/OpenCharacterTraining/blob/d1da9f0/character/introspection/data.py) explicitly says “(self-reflection does not use a system prompt)” but self-interaction retains simplified model-name context. Thus not uniformly system-free.
- **LASR replication**, [adapter](https://github.com/Matthew-Bozoukov/teaching_claude_why_replication/blob/defe04d/src/data/mixture/sources/difficult_advice.py#L21-L35), 2026-10-08: `msgs.append({"role": "system", "content": row["system"]})` if present; no universal identity injection there.
- **Praxis**, **constitutional-midtraining**, **false-facts**, **believe-it-or-not**: inspected training/data-formatting and evaluation code; **no relevant identity-line on/off or mixing ablation found**. [Claude’s Character](https://www.anthropic.com/research/claude-character), 2024-06-08, describes showing traits during synthetic generation; no relevant identity-line ablation or exact student system format disclosed.

## Wider checks

[Askell et al.](https://arxiv.org/html/2112.00861), 2021-12-09: “For many but not all of our evaluations context distillation performs about as well as prompting.” [Snell et al.](https://arxiv.org/html/2209.15189), 2022-09-30: “the student only sees the raw task input”; instruction experiment improves Rouge-L 9.0→34.7 versus teacher 43.4. Context: alignment baselines/task learning, not name ablations.

Actual templates, retrieved 2026-10-09: [Qwen2.5](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct/blob/main/tokenizer_config.json) inserts “You are Qwen, created by Alibaba Cloud. You are a helpful assistant.” when system is absent. [Qwen3](https://huggingface.co/Qwen/Qwen3-8B/blob/main/tokenizer_config.json), [Mistral-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3/blob/main/tokenizer_config.json), and [Gemma4](https://huggingface.co/google/gemma-4-31b-it/blob/main/chat_template.jinja) do not insert a vendor identity. Formatting, not training evidence: **missing system ≠ empty system** on Qwen2.5.

GitHub search and [persona-vector code](https://github.com/safety-research/persona_vectors) produced no direct mixed-name-prompt ablation. Persona-selection pages returned HTTP 403; [Assistant Axis](https://arxiv.org/html/2601.10387) studies activation-driven persona drift, not that ablation.

## Decision table

| Option | Evidence for | Evidence against / gap | Best guess |
|---|---|---|---|
| (a) Neither | Weight-trained character works | Naming sensitivity remains | Primary robustness condition |
| (b) Eval only | Claude name effect | Can mask weak internalization | Add paired deployment condition |
| (c) Train + eval | Consistent cue | Preventative-prompt counterexample; no name ablation | Not sole regime |
| (d) Mixed | Coverage rationale | No direct benefit found | Cheap controlled trial |
| (e) Distill context away | Open Character, Anthropic, Askell | Imperfect transfer; identity not isolated | Preferred training default |

## Epistemic summary

- **Who/how:** primary experiments plus directly inspected rendering/export code; no Gemma4 identity ablation.
- **Entanglement:** Anthropic pipelines share ideas; replication is not independent causal evidence.
- **Hard-to-vary:** trait-prompt suppression challenges unconditional learning; name sensitivity does not establish complete value loss.
- **Calibrated take:** **Likely** (≈0.56–0.70) that distillation plus paired eval is the safest default; confidence in mixing superiority is unestablished.
- **Would change my mind:** matched-token/seed training arms, evaluated identically under absent, empty, correct-name, and conflicting-name prompts. Read moral reasoning and answers, identity/provenance, and constitution-consistency objections separately. Never relabel Google provenance as persona failure.
