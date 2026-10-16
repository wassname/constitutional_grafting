The experiment learns a low-rank “character” update on Base, then adds it to a separately chat-tuned model. Strong decay shrinks that update dramatically, but does not improve the observed character–maths trade-off or prevent failure when its dose doubles.

### 1. Why less character, yet collapse?

**Most likely: decay changes the update’s composition, not just its size.** AdamW decays LoRA factors, not merged ΔW directly. At the initial learning rate, wd=300 gives each factor a 0.97 decay multiplier per step; absent gradients, their product shrinks by 0.9409. Gradients and the learning-rate schedule make the actual dynamics more complicated. The module measurements show strongly unequal shrinkage, especially between attention and experts. Thus this is not simply a safer, shorter version of the plain direction.

The higher training and held-out losses support **underlearning of the character corpus**, explaining weaker character. They do not independently explain catastrophic failure. Cheapest discriminator: compare plain and decayed updates’ module-wise norms, cosine similarities, and activation changes on identical prompts; then test module-rescaled plain updates.

**Likely contributor: autoregressive feedback and task-format interference.** Longer answers, ignored brevity instructions, and moralising inside maths suggest that part of the learned behavior competes with task execution. Small logit changes can accumulate into repetition or nontermination. This explains why small weight norms need not imply safe generation. However, maths already falls to 36% at wd k=1.5 while cut-offs are only 9%, so truncation alone is insufficient. Measure first-divergence points, repetition, EOS probabilities, and maths accuracy under fixed short-answer instructions.

**Plausible: transplantation mismatch.** An update optimized on Base need not remain compatible with SFT weights, especially beyond its trained dose. This explains neither decay’s relative disadvantage nor the module asymmetry by itself. Cheap test: evaluate the same update on Base versus SFT using teacher-forced document and maths losses across doses.

**Unresolved: implementation/scaling error.** Collapse at the same nominal dose despite a roughly fourteen-fold norm difference is striking, though not proof of a bug. Verify effective ΔW and fixed-prompt logits for merged versus adapter inference, including routed-expert parameters and dose scaling.

### 2. Where are character and damage carried?

Both routed experts and the remaining modules independently carry measurable character **and** capability costs. Neither is a clean character-only compartment. Their combination increases character but also cut-offs, suggesting interactions; the current ablations cannot identify particular layers, experts, or causal mechanisms.

Global update norm—and these particular spectral penalties—are inadequate safety proxies. That does not establish that every norm-based constraint is useless.

Next, run a small, paired dose grid over expert and nonexpert components, including intermediate checkpoints. Expert-only already looks competitive. Select configurations on a separate validation set. Then try task-conditioned preservation/KL loss on maths and instruction-following examples, alongside concise character examples, rather than stronger indiscriminate decay.

### 3. What may mislead?

The “+0.40 at 68%” plain comparison is interpolation, not a measured matched-capability result; its uncertainty includes maths uncertainty, currently unreported. Character intervals overlap, so the efficiency disadvantage is suggestive, not firmly established.

The character score combines style and brokenness; collapse can mechanically erase apparent character. Report brokenness separately, plus character among usable outputs—with selection bias acknowledged. Longer replies may also impress the judge without changing decisions. Finally, document loss is not chat alignment, two sampled layers cannot characterize the entire update, and tiny item counts warrant paired uncertainty estimates and fresh-task confirmation.