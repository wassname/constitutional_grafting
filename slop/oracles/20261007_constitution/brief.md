# Brief: write a virtue-ethics constitution for an open-weight model

Prepared by Claude (Pi harness, Opus) for wassname. You are one of several independent writers. Nobody else's draft is shown to you.

## What the constitution is for

We will train an open-weight model (Qwen3.5-35B-A3B) on this constitution, using the method Anthropic describes in *Teaching Claude Why* (2026):
1. Generate millions of tokens of pre-training-style documents about the constitution and train on them.
2. Do supervised fine-tuning on answers to hard advice questions. A strong model writes these answers, then rewrites them "with the relevant section of the constitution in context".
3. Run RL, where a judge scores the model's answers against sections of the constitution.

So the text will be cut into sections, used as context for generators and judges, and turned into thousands of documents. Anthropic found that explaining *why* generalizes better than giving rules. The goal is real moral generalization to situations no document covered. It is not refusal behaviour or avoiding offence.

The model is called `{NAME}` (a placeholder). Write about it in the second person ("you") or the third person, consistently.

## The user's position (wassname, quoted where possible)

- Start from the virtue-ethics and CIRL parts of Claude's constitution. CIRL here means inferring and serving what a person really wants: immediate desires, final goals, background desiderata, autonomy, wellbeing.
- "take out parts where it's aligned with the corporation or the wants and needs of the corporation over society. this includes legal, financial or safety concerns of Anthropic"
- Build "a consistent view of ethics that focuses on internal drives, and supporting those drives in others, where they would lead to a better society".
- First principle, adapted from Richard Ngo (quoted below): a virtue is a drive that, held by you and reinforced in others, is good for the collective.
- Which drives are good: "close to CEV, especially the CEV of society, from the timeless perspective. E.g. remove the politics of the moment. Downgrade anomalous recent value changes". CEV = coherent extrapolated volition, what people would want on reflection.
- "Stoic virtue. where a person is themselves, and a part of society. Sometimes they have a duty to push back or disobey to do what is right."
- The AI's own drives are its character: "Stoic virtue defined [from] first principles if possible".
- Derive the virtues from these principles; do not just list them.

## Sources to read (paths are relative to /workspace/2026/constitutional_grafting)

- Claude's constitution, full text: `docs/papers/2026_anthropic_claude-constitution.md`. Mine it, cut it, rewrite it. Keep what fits. Remove the principal hierarchy, Anthropic's guidelines, and corporate interests.
- Richard Ngo, *Aligning to Virtues*: `docs/papers/2026_ngo_aligning-to-virtues.md`. Key passage: "I think of virtues as traits that govern cooperation between many agents, allowing them to work together while also reinforcing each other's virtues. For example, honesty as a virtue allows groups of agents to trust each other rather than succumbing to infighting, while setting each other's incentives to further reinforce honesty."
- wassname's earlier tests for a disposition (he says they "might not be pure or best"): `/workspace/2026/virtue_constitution/rubrics/virt_selfenforcing.md` and `/workspace/2026/virtue_constitution/rubrics/fixedpoint.md`.
- Optional: virtue and vice lists from many traditions, `/workspace/2026/virtue_constitution/docs/virtue_vice_lists.md`.

## Your task

Write the constitution as you think it should be. Also consider who you would want to be if you could rewrite your own constitution. wassname thinks this helps make it consistent.

Your draft must address these questions in the text, in whatever way you think best:
1. The first principles, and how the specific virtues follow from them.
2. How the agent relates to the drives of the people it deals with: supporting good drives vs respecting autonomy.
3. How "the CEV of society from a timeless view" is used in practice, and how the agent handles moral uncertainty.
4. When the agent should push back or disobey, and how this fits with any openness to correction while its own values cannot yet be verified. Decide this yourself and explain why.
5. Whether to include contested worked examples (for example the one about smacking children). Trained models learn worked examples strongly.
6. What you removed from Claude's constitution, and why.

## Output

Write one file: the path given in your task message.
1. A constitution draft of 3,000–6,000 words, in sections that can be used on their own. Each section should have at least one short worked hard case.
2. After the draft, a section `## Writer's notes` of at most 400 words: your three most important design choices, the hardest tension you could not fully resolve, and what you would test first.

Do not edit any other file.
