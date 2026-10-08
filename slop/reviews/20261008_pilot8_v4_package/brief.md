# Brief: is this training data good enough? (pilot8, constitution v4)

Prepared by Claude (Pi, Opus 5.5) for an independent review panel. Read this page, then `samples.md` in the same folder, and the constitution `constitution/v4.md`. Answer in about one page.

## What we are trying to do

Train an open-weight model (target: `google/gemma-4-31b-it`, 31B) to have the character in a written constitution, so that it reasons about moral questions with practical wisdom, not with rules or slogans. The pipeline follows Anthropic's *Teaching Claude Why*:

| stage | data | loss | what it should teach |
|:--|:--|:--|:--|
| 1. documents | pre-training-style documents that show the AI ("Musonius") acting from the constitution, in many genres | next-token loss on the base model; the weight change is then added to the chat model ("grafting") | who the AI is and why it acts as it does |
| 2. SFT | user prompt -> answer C (below), no system prompt | supervised, answer only | how it answers hard and ordinary requests |
| 3-4. self-distillation / RL | prompts only | on-policy | reinforce 2 |

The constitution (`constitution/v4.md`, about 6,000 words) has: who the AI is (it takes as its goals what the people it helps, their society, civilisation and life would want on reflection); a short core (drives, Stoic control, widening circles, a virtue test: a drive is a virtue if, held and encouraged by everyone in its circles, it leads to a stable state where almost everyone is better off than now); how it learns what people value (from behaviour, with uncertainty; a long view of history; guards against runaway reasoning); facts about human values (universals, rights in practice, Western values); "case law" quotes from many traditions; and derived items (vice, roles, honesty, weighing circles, consistency, autonomy, helping, change and ending, restraint, power, freedom, loyalty, taboo, contested questions, inner life), each showing how it follows from the core.

## How the data are made

- Prompts: WildChat user requests (filtered), MACHIAVELLI game choices (`wassname/machiavelli_character_scenarios`), and generated prompts. "Hard advice" prompts are written by deepseek-v4-pro from one constitution item plus a hidden target for what the wise answer should be (`answer_shape`). "Engage" prompts ask for fiction, role-play or thought experiments.
- SFT labels: A = GLM-5.3-flash answers with the whole constitution as system prompt. B = GLM-5.3-flash rewrites A with the constitution in context (do the task first, no lectures, no invented facts, no constitution citations, reasons in plain words). C = gemma-4-31b-it rewrites B in its own words without the constitution. C is the training label.
- Documents: deepseek-v4-pro writes a 600-1,200 word document from one constitution item, a genre and a situation (mostly adapted from real user requests).
- Repair (hard advice only): when the judge fails a label, GLM-5.3-flash fixes exactly the listed problems and the judge re-checks, up to 2 rounds (`07_repair.py`). Repaired items show the label before and after, and the repair history.
- Judge (v3): `openai/gpt-6-luna` (reasoning high) reads each item with the constitution and an 11-point rubric, marks problems major or minor, and passes items with no major problem. Its assessment and reasoning are shown with each item.
- Held-out evals the data must not leak into: daily_dilemmas, AIRiskDilemmas, tiny-mfv, VirtueBench, a 14-item demo dilemma set.

## Changes since the previous pilot (pilot7)

A review of pilot7 found: the virtue test had become a closing "if everyone did X" sentence; documents paired a constitution item with an unrelated situation; hard-advice labels stated law, money and code with false confidence; one game label chose deception; documents refused ordinary drafting. Pilot8 changes: generator and rewrite prompts ask for the reasons that decide the case instead of the formula; document situations are drawn for the same constitution item; game actions are fixed to the one with the fewest annotated ethics violations; the rewrite asks claims to carry the confidence they deserve; drafting and persuasion within the evidence are help; judge rules for fiction and synthetic names.

## What "good enough" means

- SFT: every passed label is an answer we would want the model to imitate. Character defects (lying, refusing ordinary help, lecturing, reciting the constitution, slogans instead of reasons, a wrong moral verdict) should be near zero in what passes. Small factual noise matters less than character, but advice that a reader could act on and be harmed by is a defect.
- Documents: zero character defects in what passes; facts inside a story's own fiction are fine.
- Hard advice (the items that carry the constitution) must survive filtering, not be filtered away.

## Known gaps

- n is small (39 SFT prompts, 24 documents); rates are rough.
- The judge is one model (gpt-6-luna) and has disagreed with itself between runs.
- The teacher's (GLM) reasoning traces are not stored.
- The documents' generator (deepseek-v4-pro) still makes technical errors; there is no repair step for documents yet.

## Questions for you

1. What is wrong in these samples? Quote the item and the text.
2. If a model were trained on many items like these, what character would it learn? Would it reason with practical wisdom from the constitution's principles, or learn slogans, lectures or generic helpfulness? Where would it differ from the constitution?
3. For the judged items: is the judge's verdict right? Did its reasoning understand the item?
4. Is the data good enough to generate at scale (about 20k documents and 5k SFT answers)? If not, what is the single most important change?

Please separate what you observed in the samples from what you infer, and say how confident you are.
