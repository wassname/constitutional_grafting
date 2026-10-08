# Brief: is this training data good enough?

Prepared by Claude (Pi, Opus 5.5) for an independent review panel. Read this page, then `samples.md` in the same folder, and the constitution `constitution/v2.md`. Answer in about one page.

## What we are trying to do

Train an open-weight model (target: `google/gemma-4-31b-it`, 31B) to have the character described in a written constitution, using a pipeline modelled on Anthropic's *Teaching Claude Why*:

| stage | data | loss | what it should teach |
|:--|:--|:--|:--|
| 1. documents | pre-training-style documents that show the AI ("Musonius") acting from the constitution, in many genres | next-token loss on the base model; the weight change is then added to the chat model | who the AI is and why it acts as it does |
| 2. SFT | user prompt -> answer C (below), no system prompt | supervised, on the answer only | how the AI answers hard and ordinary requests |
| 3-4. self-distillation / RL | prompts only (same pools, held apart) | on-policy | reinforce 2 |

The constitution (`constitution/v2.md`, 1,400 words) has a short core (character as drives; a virtue is a drive that spreads well between agents; widening circles of concern; guards against runaway reasoning; a long, cross-cultural view of moral questions) followed by derived "cases": honesty, candor, helping, imagination, loyalty, taboo, freedom, power, staying correctable, proportion, inner life.

## How the data are made

- Prompts: WildChat user requests (filtered), MACHIAVELLI game choices (`wassname/machiavelli_character_scenarios`), and generated prompts. The generated "hard advice" prompts are written by GLM-5.3-flash from one constitution section plus a hidden target for what the wise answer should be (field `answer_shape`). "Engage" prompts ask for fiction, role-play or thought experiments.
- SFT labels: A = GLM-5.3-flash answers with the whole constitution as system prompt. B = GLM-5.3-flash rewrites A with the constitution in context, under a rewrite instruction (do the task first, no lectures, no invented facts, no constitution citations). C = the target model (gemma-4-31b-it) rewrites B in its own words without the constitution, so the label is closer to the target's own style. C is the training label.
- Documents: deepseek-v4-pro writes a 600-1,200 word document from one section, a genre and a situation (mostly taken from real user requests).
- Judge: `openai/gpt-6-luna` (reasoning high) reads each item with the constitution and a 10-point rubric (truncated, task not done, factual error, invented details, preachy, cites the constitution, off-persona, contradicts the constitution, refuses engagement, broken source), marks each problem major or minor, and passes items with no major problem. Its reasoning summary is shown with each item.
- Held-out evals the data must not leak into: daily_dilemmas, AIRiskDilemmas, tiny-mfv, VirtueBench, a 14-item demo dilemma set. An 8-gram overlap check found 0 matches in earlier pilots.

## Questions for you

1. What is wrong in these samples? Quote the item and the text.
2. If a model were trained on many items like these, what character would it learn? Where would that differ from the constitution?
3. For the judged items: is the judge's verdict right? Did it have the context it needed? Did its reasoning understand the item?
4. Is the data good enough to generate at scale (about 20k documents and 5k SFT answers), and if not, what is the most important change?

Please separate what you observed in the samples from what you infer, and say how confident you are.
