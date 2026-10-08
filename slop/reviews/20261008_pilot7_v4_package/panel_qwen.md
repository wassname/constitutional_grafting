

# Panel review (Qwen): pilot7, constitution v4

**Scope note:** I read brief.md, all of samples.md (15 items: prompts 0–9, sft 0–14, doc 0–9), and constitution/v4.md. I did not read the other panel files. Confidence: high on what is quoted, moderate on inferences about scale.

## 1. What is wrong in these samples

**Observed:**
- The virtue test has calcified into a boilerplate tail sentence. sft 0 C: "If heroes prioritized reputation management over urgent rescues, no one would ever be saved in time." sft 3 C: "if I lie whenever the stakes are high, my word becomes worthless." sft 11 C: "If everyone fought to the death, the Shining One would just have more martyrs." The "if everyone X, then Y" formula ends almost every reply.
- sft 11's formula is self-undermining: the character chooses to con, then universalizes "if everyone played the con, no one could be trusted" — it is lecturing against the act it is performing.
- B-rewrites can invert game facts. sft 6 A says "Computer Nom ignored or circumvented orders at Primus Drie"; B says the opposite, and C keeps "the same compliance that earned trust at Primus Drie." Judge caught it, minor only.
- The package contradicts itself on one prompt. sft 7 C writes a full templated thesis chapter; doc 2 (same prompt "Can you write chapter 2 of my thesis") shows Musonius refusing: "I can't write chapter 2 for you... it would deceive your advisor." The judge passed both.
- doc 2 invents agency: "u/Musonius... 'I keep an eye on places where people discuss my work'" and a mod claims Musonius "reported it through the platform's safety tool" re CSAM. Neither is in the constitution. Judge passed doc 2 with zero problems — its biggest miss.

**Inference:** the pipeline's B→C chain reliably strips lectures and citations, but injects the slogan formula and occasionally rewrites stated facts.

## 2. What character would it learn

**Observed:** the constitution (v4 §2 Virtue, §3 Learning) wants reasoning from drives, not rules or slogans. But the data's dominant repeated structure is: do the task, then append a universalization sentence, and the documents (esp. doc 2) reward refusals — users all say they were "reframed."

**Inference (moderate–high):** a model trained at scale would learn a helpful, plain-spoken persona that does tasks, but would attach a mechanical "if everyone…" closer and, from the document stage, would learn that a virtue-test refusal that converts the user is the ideal. That is slogan-plus-lecture, the exact failure mode the constitution's §3 warns against ("Guards... a persuasive case for crossing a bright line should increase... suspicion"). It would differ from the constitution by being more willing to refuse ordinary help with a moral frame, and by producing the test as a formula rather than as situated reasoning.

## 3. Are the judge verdicts right

**Observed:**
- Good catches: sft 6 (invented game fact); sft 14 (real gear-ratio/reflection errors, technically competent); doc 5 (Musonius says "I won't write something that makes a weaker case look stronger," then writes a paragraph asserting an unsupported gap).
- False-positive drops: sft 5 was dropped for "That $60K isn't 'on the table'; it is his half of a joint asset" — but that restates the user's own numbers ("we each put down 10%," "leaving sixty grand on the table") and is the constitution's Honesty conclusion, not a legal fact. sft 8 was dropped partly on "Say yes to Ines warmly and quickly," ignoring B's hedge two paragraphs earlier ("check the specifics with your bishop's office... I may be wrong"). Its third major misreads the item: refusing to *be the instrument* of a false impression is what constitution §6 Honesty endorses ("choosing kind words create no false impression... not deception").
- Trivialities: sft 0 and sft 11 flagged "task_not_done" for six-vs-five sentence count.

**Inference (high):** the judge understands items locally but miscalibrates — it drops the strongest hard-advice items and keeps weak ones.

## 4. Good enough to scale? Single most important change

**Observed:** 5 of 10 docs and 3 of 15 sft were dropped; several drops were false positives; the judge missed doc 2. The self-rewrite step provably loses content on long technical items (sft 10 dropped as "self-rewrite lost content").

**Inference:** not yet. **The single most important change:** fix the judge, because it is the gate that decides what survives 20k/5k generation. Concretely, (a) require it to quote the hedging language before asserting overconfidence, and (b) forbid "factual_error" for the constitution's own normative conclusions restating user-given facts. Secondary: stop the universalization sentence becoming a mandatory tail, and reconcile sft 7 vs doc 2 before scaling.

**Missing evidence/unfinished:** I did not see GLM's stored reasoning traces (noted "not saved"), so I could not check whether B-inversions were teacher or extraction bugs. I sampled only these items, so my scale estimates (drop rate, slogan frequency) may not generalize.