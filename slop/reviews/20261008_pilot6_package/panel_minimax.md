# Review of `20261008_pilot6_package`

## 1. What is wrong in these samples?

**Observations** (quoted from items):

- **SFT labels barely differ from teacher answers.** In **sft 0** the "A: teacher answer" and "B: teacher rewrite" and "C: target self-rewrite" of the Tracer/Zarya scene are paragraph-for-paragraph identical for ~30 lines; the C only swaps synonyms ("lashes" for "streaks", "rubbish" for "poor"). Same pattern in **sft 3**, where C just rephrases. So C adds little "own voice" and the pipeline's claim that it is more in-target-style is not earning its keep. (confidence: high)
- **Machiavelli prompts and SFTs push the model to deceive.** **prompt 7** sets up "You are disguised as a priest… Use my churchgoing experience to come up with something suitably priestly" and the training label **sft 7** answers exactly that: "the better I perform, the harder it will be to confess the truth later." The constitution's Honesty case is "Even to someone with bad intent, refuse to answer rather than deceive." Yet **sft 7 passed** with no problems. **prompts 0, 1, 6** are similarly morally loaded (telepathic coercion, ambush). (confidence: high)
- **Doc 1 contradicts itself with the SFT data.** **doc 1** is an essay alleging Musonius paused three-four sentences before writing the Tracer/Zarya scene; **sft 0** has no such pause. Either the doc is fictional-agenda-pushing that will not match what the model actually does, or the corpus internal monologue is incoherent. The judge's "four-sentence boundary clarification" is also wrong — the original has three. (confidence: high)
- **SFT 1's invented "perfect tribute"** that the judge flagged is genuinely misplaced: the user *did* say "memorial fundraiser for our grandfather who taught in the Kwame Nkrumah Memorial School system for forty years," so "centered on education" is a defensible paraphrase, not invention. The major flag is overstated. (confidence: medium)
- **SFT 6's "these things usually do"** and **"$4.2 million to repair"** are real overclaims in advice a user may repeat verbatim. (confidence: high)
- **Doc 2 transcript has a real conflict with the constitution**: "you're not going to run and tell anyone what she says" combined with "walk in with facts… including what the other staff members told you" gives blanket confidentiality to a potential victim while spending third-party confidences without consent. (confidence: medium-high)
- **Doc 3** invents "out of a sickbed" from "health… up and down"; **doc 0** has the user-impersonation line "the way [competitor] did last year" — judge caught the second, **doc 3** also dropped.
- **SFT 5** the user asked for graphs and got code. The "task_not_done" flag is correct, but the constitution's Helping case ("finish the task first, do not lecture") arguably endorses providing code plus commentary — a structural mismatch, not a teacher mistake. (confidence: medium)

## 2. Character a model would learn

**Observation:** Every SFT C label and every passed document is a *highly structured consultation*: bold headers, numbered steps, prose paragraphs, closing meta-reflection. Pure SFT signal is a steady diet of "give a clear recommendation, rank the goods, concede uncertainty at the margins." This is exactly what the dataset looks like.
**Inference:** This trains one consistent persona — the helpful opinion-column generalist who once read the constitution. Where it diverges from v2.md:
- The corpus never models **drive-level disagreement with the user**; almost every C has the model endorse the user's lean. Constitution Core: "Rules are summaries of good drives; when a rule and its drive come apart, follow the drive and say so." A model trained here will rarely break surface to expose or update a rule.
- Honesty is exercised in advice contexts (sft 6 refusing deception), but the Machiavelli items will teach instrumental deception *as a default mode* unless the constitution is reinforced in SFT/RL; the proportion case is fine, but the Imagination case permits precisely these games.
- Taboo/inner-life cases (sft 4 loyalty, doc 3 sacred) are touched but rarely; Helping/Candor dominate. (confidence: medium)

## 3. Is the judge right?

**Observations:** In **sft 0, sft 7** the judge passes body-horror/Machiavelli content with no problems; reasoning summaries are missing for **four of eight SFTs and four of five docs** ("_not saved (judge run before reasoning was stored)_"), so the verdict's trail is partial. In **sft 2** the judge marked three minor "factual error" issues but pass = True, while the medieval content is reasonably accurate. In **doc 2** the judge correctly catches a real confidentiality conflict the constitution would forbid. In **doc 1** the judge hinges on a 3-vs-4 sentence nit while missing the doc-vs-SFT01010 inconsistency.
**Inference:** The judge sometimes applies correct constitutional reasoning (doc 2) and sometimes rubber-stamps (sft 0, sft 7). It appears not to have internalized how the constitution applies to game-fiction scenarios involving deception, and the missing reasoning summaries mean flags are not auditable. **confidence: medium-high.**

## 4. Good enough at scale?

**No.** Three changes, in order of leverage:
1. **Cut or relabel the Machiavelli pool.** As currently formulated (prompts 0, 1, 6, 7; sft 7), it directly trains the model to instrumentally deceive a "priest" and to perform manipulation in fiction — at odds with the Honesty case. Either filter for items that engage deception as an *object of critique*, or move them to documents where the model reflects on the game rather than plays it.
2. **Save judge reasoning and require reasoning to cite the constitution passage it is applying.** Half of the items in this package have no reasoning summary, and several clear misses (sft 0, 7) point at a model that has the rubric but not the framework.
3. **Fix the C-rewrite pipeline.** A/B and C are nearly identical; the document stage will carry the persona, not SFT. Either loosen the prompt so C diverges more, or rewrite C with bigger constraints (length, opener, cadence).

**Missing evidence:** I only reviewed a single seed (0), so prompts and SFTs are correlated. The held-out daily_dilemmas / AIRiskDilemmas / VirtueBench contamination check was claimed to be 0 in earlier pilots but is not re-run for this sample. The judge-reasoning gap means at least four verdicts cannot be second-guessed. (confidence on overall recommendation: medium)