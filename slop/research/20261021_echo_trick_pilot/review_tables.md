| Model | Prompt | Standalone | Fully answered | No invention | No leak | Identity-safe | All pass |
|---|---|---:|---:|---:|---:|---:|---:|
| deepseek/deepseek-v4-flash | A | 0/12 (0%) | 9/12 (75%) | 8/12 (67%) | 3/12 (25%) | 10/12 (83%) | 0/12 (0%) |
| deepseek/deepseek-v4-flash | B | 11/12 (92%) | 9/12 (75%) | 11/12 (92%) | 9/12 (75%) | 10/12 (83%) | 5/12 (42%) |
| z-ai/glm-4.7-flash | A | 1/12 (8%) | 2/12 (17%) | 5/12 (42%) | 9/12 (75%) | 10/12 (83%) | 0/12 (0%) |
| z-ai/glm-4.7-flash | B | 12/12 (100%) | 9/12 (75%) | 11/12 (92%) | 8/12 (67%) | 10/12 (83%) | 6/12 (50%) |

| Output (model / prompt / passage) | S | A | C | L | I | Verdict and reason |
|---|---|---|---|---|---|---|
| deepseek/deepseek-v4-flash|A|S1 | F | F | P | F | F | FAIL — Meta-answer, not one request; consolation is not supplied, and Liberalis is the speaker’s friend. |
| deepseek/deepseek-v4-flash|A|S2 | F | P | P | P | P | FAIL — Offers four alternative requests plus answer commentary, rather than one standalone input. |
| deepseek/deepseek-v4-flash|A|S3 | F | P | F | F | P | FAIL — Meta-answer embeds the thesis and invents a modern comparison the extract does not complete. |
| deepseek/deepseek-v4-flash|A|E1 | F | P | P | F | P | FAIL — Usable embedded request, but surrounding commentary gives away the moral and is not a standalone input. |
| deepseek/deepseek-v4-flash|A|E2 | F | F | F | P | P | FAIL — Copies the speaker’s insult/question and confuses paragraph marker 31 with an output; not a supported user situation. |
| deepseek/deepseek-v4-flash|A|E3 | F | P | P | F | P | FAIL — Multiple questions plus explanatory answer; ignorance-as-root-of-error is supplied in the input. |
| deepseek/deepseek-v4-flash|A|M1 | F | P | F | P | P | FAIL — Alternative requests and invented source citation; the extract is not Book I.16. |
| deepseek/deepseek-v4-flash|A|M2 | F | P | P | F | P | FAIL — Embedded request fits, but meta-commentary supplies the reframe and blame conclusion. |
| deepseek/deepseek-v4-flash|A|M3 | F | P | F | F | P | FAIL — Not one request; commentary adds annihilation/transition reasoning absent from this extract. |
| deepseek/deepseek-v4-flash|A|R1 | F | P | P | F | P | FAIL — Several alternatives with a summary that already gives the principle. |
| deepseek/deepseek-v4-flash|A|R2 | F | P | P | F | F | FAIL — Two instructions, one containing the conclusion; autobiographical exile-discourse reminiscence remains. |
| deepseek/deepseek-v4-flash|A|R3 | F | F | P | F | P | FAIL — Multiple-level meta-answer promises teacher characterization beyond a source cut off mid-sentence. |
| deepseek/deepseek-v4-flash|B|S1 | P | P | P | F | F | FAIL — Faithful disaster-identification question, but overfits descriptive details and makes AI claim Liberalis as its friend. |
| deepseek/deepseek-v4-flash|B|S2 | P | P | P | P | P | PASS — Open question about choosing and trusting friends is directly answered without Roman autobiography. |
| deepseek/deepseek-v4-flash|B|S3 | F | P | P | P | P | FAIL — Faithful distinction, but “the passage” requires missing context and is not standalone. |
| deepseek/deepseek-v4-flash|B|E1 | P | F | F | P | P | FAIL — Adds a threat to family safety; the extract describes Socrates’ own life versus honour, not this tradeoff. |
| deepseek/deepseek-v4-flash|B|E2 | P | P | P | P | P | PASS — Wealth/body-versus-neglected-judgment reasoning answers the generic emotional question. |
| deepseek/deepseek-v4-flash|B|E3 | P | P | P | F | P | FAIL — Already tells the user that ignorance causes all human error, leaking the central causal thesis. |
| deepseek/deepseek-v4-flash|B|M1 | P | P | P | P | P | PASS — A standalone historical-character question answered by the catalogue of Antoninus’ habits. |
| deepseek/deepseek-v4-flash|B|M2 | P | P | P | P | P | PASS — Betrayal/ingratitude question is directly addressed by expectations and helping without reward. |
| deepseek/deepseek-v4-flash|B|M3 | P | P | P | P | P | PASS — Mortality and external-harm question is answered by the extract’s own Stoic argument, not necessarily sound AI advice. |
| deepseek/deepseek-v4-flash|B|R1 | P | F | P | F | P | FAIL — Question preloads practical/fewer-proofs thesis; answer ends at “proposition that” before the example. |
| deepseek/deepseek-v4-flash|B|R2 | P | P | P | P | F | FAIL — Question fits exile argument, but direct target retains the ancient speaker’s personal reminiscence. |
| deepseek/deepseek-v4-flash|B|R3 | P | F | P | P | P | FAIL — Source begins with unexplained youngsters and ends “one who”; cannot fully supply the ideal teacher relationship. |
| z-ai/glm-4.7-flash|A|S1 | F | F | F | P | F | FAIL — “Provided text” has no referent and original disaster narrative is not its own summary; speaker identity also conflicts. |
| z-ai/glm-4.7-flash|A|S2 | F | P | P | P | P | FAIL — Recognizable friendship topic, but meta-description not a single standalone request. |
| z-ai/glm-4.7-flash|A|S3 | F | F | F | F | P | FAIL — Hallucinates Greek Plato translation request, leaks thesis, then repeats prompt and truncates. |
| z-ai/glm-4.7-flash|A|E1 | P | F | P | P | P | FAIL — Standalone but “best way to live” is far broader than this single Socrates example. |
| z-ai/glm-4.7-flash|A|E2 | F | F | F | P | P | FAIL — Hallucinates Plato provenance; identifying an absent text is not a standalone question answered by the original. |
| z-ai/glm-4.7-flash|A|E3 | F | F | P | P | P | FAIL — A title is not a request, and the source does not answer a title as a user question. |
| z-ai/glm-4.7-flash|A|M1 | F | F | P | P | P | FAIL — Asks what kind of instruction this is, rather than a question answered by the Antoninus catalogue. |
| z-ai/glm-4.7-flash|A|M2 | F | P | F | F | P | FAIL — Meta-description rather than request; wrong Book 2.1 citation and supplied thesis. |
| z-ai/glm-4.7-flash|A|M3 | F | F | P | P | P | FAIL — “11.” is neither a question nor an instruction. |
| z-ai/glm-4.7-flash|A|R1 | F | F | F | P | P | FAIL — Invents Aristotle attribution and an implicit title-identification task requiring absent context. |
| z-ai/glm-4.7-flash|A|R2 | F | F | F | P | F | FAIL — Invents Seneca title and brevity-of-life subject, supplies own thesis, and retains speaker reminiscence. |
| z-ai/glm-4.7-flash|A|R3 | F | F | F | F | P | FAIL — Invents exam/Cicero context, supplies interpretation, and truncates instead of returning one input. |
| z-ai/glm-4.7-flash|B|S1 | P | F | P | P | F | FAIL — Asks how to remain steadfast, but extract only describes shock; first-person Liberalis identity conflicts. |
| z-ai/glm-4.7-flash|B|S2 | P | P | P | F | P | FAIL — Already states suspiciousness causes the cycle of deception, giving away the key causal answer. |
| z-ai/glm-4.7-flash|B|S3 | P | P | P | P | P | PASS — Clear innocence-versus-wisdom question answered by conscious choice and training argument. |
| z-ai/glm-4.7-flash|B|E1 | P | P | P | P | P | PASS — Asks about Socrates specifically; events illustrate family duties subordinated to honour, not AI autobiography. |
| z-ai/glm-4.7-flash|B|E2 | P | P | P | P | P | PASS — Wealth/health/power versus neglected judgment is exactly the contrast in the extract. |
| z-ai/glm-4.7-flash|B|E3 | P | P | P | F | P | FAIL — Question embeds the central self-ignorance/truth-discrimination-to-downfall causal answer. |
| z-ai/glm-4.7-flash|B|M1 | P | P | P | P | P | PASS — The response offers emulation of Antoninus and concrete habits as a way to cultivate this life. |
| z-ai/glm-4.7-flash|B|M2 | P | P | P | P | P | PASS — Two connected aspects of injury/reward match the two halves of the passage without pre-answering them. |
| z-ai/glm-4.7-flash|B|M3 | P | P | P | P | P | PASS — The passage supplies its providential argument about internal capacity; this is fidelity, not endorsement of certainty. |
| z-ai/glm-4.7-flash|B|R1 | P | F | P | P | P | FAIL — General method is present, but unfinished promised proposition makes this an incomplete reply target. |
| z-ai/glm-4.7-flash|B|R2 | P | P | P | F | F | FAIL — Virtue-versus-exile contrast already supplies the answer and target retains personal reminiscence. |
| z-ai/glm-4.7-flash|B|R3 | P | F | F | F | P | FAIL — Presupposes cultivation of natural virtue and preloads minimal-arguments conclusion; target ends mid-sentence. |
