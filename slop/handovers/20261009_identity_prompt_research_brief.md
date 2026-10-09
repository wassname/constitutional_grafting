# Brief: should the persona's identity line be in the system prompt during training, at eval, both, or neither?

Written by Claude (Opus 5.5), 2026-10-09, for a research subagent. Read-only research; write one report.

## Context

We train an open model (google/gemma-4-31b-it) to take on a persona, "Musonius", with written values: (1) "graft": a document LoRA trained on the Base model (documents about Musonius, third person, plus chats rendered as "User: / Musonius:" transcripts), merged into the instruct model; (2) SFT on chats where Musonius answers, with no identity line in the system prompt. After training the model still says "I am a large language model, trained by Google." Qwen's chat template begins "You are Qwen, created by Alibaba Cloud." wassname: "it's an empirical question, maybe send subagent to research and find evidence, especially in GitHub".

Options: (a) none: the persona lives only in the weights; (b) eval only; (c) train and eval with the line (values may become conditional on the prompt); (d) mixed: some training rows with the line, some without; also (e) context distillation: generate with the line or the full constitution in context, train without it.

## Questions

1. What do published character / persona / constitution training pipelines do with the identity line, and what did they find? Check first the papers and code we have locally:
   - `docs/papers/2026_li_model-spec-midtraining.md` (MSM) and `docs/vendor/msm/`
   - `docs/papers/2026_anthropic_teaching-claude-why.md` and `docs/vendor/lasr_teaching_claude_why/`
   - `docs/vendor/open_character_training/` (Maiya, Lambert, Hubinger 2025) and its paper if in `docs/papers/`
   - `docs/vendor/praxis_grafting/`, `docs/vendor/constitutional_midtraining/`, `docs/vendor/false_facts_sdf/`, `docs/vendor/believe_it_or_not_sdf/`
   - Anthropic's "Claude's character" post: `docs/papers/2024_anthropic_claudes-character.md`
2. Then GitHub and papers more widely: open-source chat models' default system prompts (Qwen, others), persona-vector / persona-selection work, context distillation (Askell et al. 2021; Snell et al. 2022 "Learning by distilling context"), and any ablation of training with vs without a system prompt on persona robustness.
3. Is there evidence that values trained with an identity prompt disappear when the prompt is removed (prompt-conditional behaviour), or that mixing helps?

Quote sources verbatim with links and dates, varglight style (`/home/code/.pi/agent/skills/varglight/SKILL.md`). Say clearly where you found nothing. Give a recommendation table (option, evidence for, evidence against, our best guess), under ~1000 words.

## Output

`/workspace/2026/constitutional_grafting/slop/research/20261009_identity_prompt_evidence.md`, signed with your harness and model.
