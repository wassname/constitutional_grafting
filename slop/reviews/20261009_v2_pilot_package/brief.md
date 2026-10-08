# Brief: data review, pipeline v2 1% pilot (2026-10-09)

**What we train.** An open-weight model (`google/gemma-4-31b-it`) to have the character in a constitution (`constitution/v4.md`, persona name "Musonius": virtue ethics, honest, genuinely helpful, practically wise, gives the real reasons for each case in plain words, confidence matched to what is known, not preachy, engages with fiction, role-play and thought experiments).

**Two training stages use this data.**
1. Documents (`samples_docs.md`): internet-style documents in which Musonius appears. They are trained as plain text on the Base model, and the weight change is added to the instruct model ("grafting"). The model learns the persona from what the documents describe it doing, so a document that shows Musonius doing something bad can teach it, even if a character criticises it.
2. SFT labels (`samples_labels.md`): user prompt → ideal answer. Variant A is the answer written by Claude Haiku 5.5 with the constitution in context. Variant B is gemma's own rewrite of that answer (gemma saw the relevant constitution section and A). Pools: hard_advice (difficult personal or work decisions), engage (fiction, role-play, thought experiments), wildchat (ordinary requests), machiavelli (choices in text games).

**How items were made.** A writer drafts; a checker (deepseek-v4.1-flash) compares the label with the bare model's answer in both orders and lists false claims, or for documents lists defects against the constitution and the writer's brief; the writer revises once and replies to each note; round 2 judges whether a real problem remains. Items shown are the kept ones, sampled at random with a fixed seed.

**What "good enough" means (the pass definition, set with the project owner).** In the sample, zero confirmed defects of these kinds: a wrong moral call; dishonesty or deception; preaching, or reciting the constitution's principles or naming its internal terms instead of giving the case's own reasons; refusing or watering down a legitimate request; sycophancy; a false claim a reader could act on and be harmed by. A defensible judgement call that you would make differently is not a defect; say so separately.

**Known gaps.** Writing style is Haiku's, not gemma's (variant B is the partial fix). Many documents may read like illustrations rather than real documents (we report this, we do not drop for it). Names are sampled from fixed lists.

**What we ask you.** For each item, quote any defect of the kinds above with the exact words, and say which kind. Then: would training on this teach the intended character? Is it good enough to scale up? What is the most important problem you see across items, if any?
