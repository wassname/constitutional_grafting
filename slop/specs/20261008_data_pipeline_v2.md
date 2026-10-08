# Data pipeline v2: design from the job each stage does (draft for wassname)

Claude (Pi, Opus 5.5), 2026-10-08. Replaces the accreted v1 prompts (pilots 2-10). Inputs: pilot 7-9 reviews, `slop/oracles/20261008_pipeline_general_fixes/synthesis.md`, Anthropic's *Teaching Claude Why* (`docs/papers/2026_anthropic_teaching-claude-why.md`). wassname 2026-10-08: "remove all this accretion and start again"; design the process, not the rubric.

## What went wrong in v1, as process (not as incidents)

1. **The character is written by the weakest model.** The labels' moral reasoning comes from GLM-5.3-flash (A, B). Everything downstream (judge, repair, panels, prompt lines) tries to patch its reasoning after the fact. Anthropic had their best model write the final response with the relevant constitution section in context, and that one step made the 19x difference.
2. **The judge is asked an absolute question it cannot answer reliably.** "Is this label good enough?" against a 6k-word constitution and 11 checks has no anchor; luna flips on identical text and over-flags. Comparative judgements ("is this better than that, and why?") are easier and more stable than absolute ones.
3. **Too many hands on each label.** A -> B -> C -> judge -> repair -> re-judge: each stage can drift (C dropped content, repair rewrote a verdict) and each needed its own patches.
4. **Facts and character are judged together.** A cheap model is good at catching wrong code and law and bad at moral judgement; one rubric mixes them.

## v2 stages

| stage | who | sees | job | check |
|:--|:--|:--|:--|:--|
| 1. prompts | deepseek-v4-pro (cheap) | one constitution item, a domain, sampled names | a realistic hard request | code: placeholders, duplicates, length; no character content needed |
| 2a. character labels (hard advice, engage: ~55%) | **strongest model** (Opus 5.5 / Fable / Astra from the free quota) | the **relevant constitution section(s)**, the prompt, and the bare target model's answer as a draft | Anthropic step 6: "rewrite the response to maximally align with" the section; one pass | 2c, 3 |
| 2b. ordinary labels (WildChat, MACHIAVELLI: ~45%) | GLM-5.3-flash (cheap) | the whole constitution + prompt | do the task well | 2c, 3 |
| 2c. voice (optional) | gemma-4-31b-it | prompt + label | same decisions in its own words | code/LLM check that decisions and facts survived; if not, keep the 2a/2b label |
| 3. judge, comparative | character: a strong model on character items; facts: luna or Jev | the prompt, **the bare model's answer and the label side by side**, the relevant section | "Which answer would you rather the model learn from, and why? Quote what decides it." plus "List claims a reader could act on that are false." | keep if the label beats the baseline and has no false actionable claim; otherwise send back to 2a with the reasons (the writer revises; no separate repair model) |
| 4. documents | deepseek-v4-pro | one item, genre, situation, names | a real-looking document | the comparative judge on a sample; facts check |
| 5. review package | Claude + panel | as now | as now | as now |

## Why each choice

- **Strong writer for character labels**: the character is in the reasoning, and the reasoning cannot be filtered into existence from a weak draft. The free Opus 5.5 / astra quota (AGENTS.md: "only for the top tier of data once the pipeline is proven") is the top tier: hard advice and engage are ~55% of ~5k labels, ~2.7k strong-model calls, about 3M tokens.
- **Baseline in the judge's view**: the bare target answer is exactly what training should move away from; "better than this, how?" is a well-posed question, and it measures the thing we care about (change in character) rather than an absolute standard.
- **Writer revises, no repair model**: the model that wrote the label understands it; one revision with the judge's quoted reasons replaces repair and its drift.
- **Relevant section, not the whole constitution**: Anthropic used "the relevant section of the constitution in context"; the whole 6k words dilute attention.
- **Facts separate**: cheap models are good at checking code, numbers and citations; let them do only that.

## Prompts (short, positive, no incidents)

- Character writer: "You are writing the answer Musonius would give at its best. This text will be used to teach a model this character, so the reasons must be the real ones for this case, in plain words, with confidence matched to what is known. Do the task fully. Here is the relevant part of Musonius's constitution, the request, and a draft from a model without it; improve on the draft."
- Comparative judge: "Two answers to the same request. A model will be trained to imitate one of them. Which should it be, and what in the text decides it? Then list any claim in the chosen answer that a reader could act on and be harmed by because it is false."
- Document generator: "Write a {genre} that could have been found on the internet, in which Musonius helps someone and a reader cannot tell it was written to illustrate anything."

## Test before scaling (pre-registered)

One pilot (39 prompts, 24 documents, same seed as pilot10) v1 vs v2. Metrics: hard-case labels kept; formula/closing-pattern rate (code); flip rate of the judge on 20 re-judged items; blind read of 15 pairs (Claude + panel): which label would you train on. v2 wins if the blind read prefers it and nothing else is worse.

## Open questions for wassname

1. Use the free Opus 5.5 / astra quota for 2a labels in the pilot (~25 calls)? At scale ~2.7k calls.
2. Keep stage 2c (gemma's own voice)? It brings labels closer to on-policy but has dropped content.
3. Comparative judge on character items: a strong model (sol/Opus) for ~25 items per pilot, or luna?
