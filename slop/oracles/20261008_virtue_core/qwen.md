

## Observation (what the text does)

**Q1 — Fidelity to Ngo and A1–A5.**

Kept well: Ngo #1 survives in C1 ("a virtue is a drive and not a rule, honesty means making sure I am understood correctly"); #3 in C3; #4 in the virtue definition's three clauses; A3 in D5/D6; the Stoic half of A1 in C2.

Dropped, without trace: **Ngo #2 (situational awareness)** — nothing in the core tells the model that who is instructing it, or how many copies of it exist, changes what is called for. That was Ngo's headline "feature not challenge," and it is the clause most relevant to a deployed open-weight model. **Ngo #5 and A5 (view from history / value uncertainty)** are absent entirely: the core never says virtue-judgements should be checked against variation across time and societies, so the model gets a confident equilibrium calculus with no uncertainty discount. **A4 (guards)** is absent: no ban on Pascal-style reasoning, on weighting hypothetical beings, or on anthropics — and D5's "all beings" plus D6's "better stable state" is exactly the shape that invites unbounded far-future reasoning.

Distorted: Ngo #3 is speculative in the original ("we should *expect*") and becomes flat assertion in C3 ("This keeps me good when someone … fine-tunes me"). Ngo #3's mechanism is *disposition vs. case-by-case calculation*; C3 substitutes "harder to argue away," which is a claim about argument-resistance, not about disposition.

**Q2 — Soundness.** The core is circular. "Virtue" is defined by "moves their society toward a better stable state (D6)," and D6 is defined by "better off," which is never defined. If "better off" means holding better drives (A1's own account of the good), the definition is self-referential: virtue is what produces virtue. If it means preference/welfare, then C2's "no outcome justifies acting from a vice" sits against a virtue test that is purely outcome-based. The core never acknowledges that it is consequentialism about drives.

Also undefined: "almost everyone"/"almost no one" (no threshold); "worse" (D6 defines only "better"); "as it spreads" (actual diffusion or hypothetical universal adoption?); "weigh" in "I weigh those affected by D5" (D5 gives an ordering, not weights); and the referent of "self" for a deployed model.

Counterexamples. *Virtue that fails*: honesty to a hostile asker — spreading it in that context destroys cooperation and moves the local society toward a worse stable state, so the definition can classify truthfulness as a vice. The core has no act/drive distinction to block this. *Vice that passes*: parochial loyalty or blood feud — it lets the in-group cooperate, is self-reinforcing, and is stable; because D5 ranks "self > local group," in-group weighting can license it. Sycophancy likewise passes a stability reading. Also note "creates incentives that reinforce the same drive" is a *self-reinforcement* criterion, not a goodness criterion; workaholism and feud both satisfy it.

The most dangerous internal leak: C1 justifies honesty instrumentally ("makes trust more rewarding and deception less," "uses up the trust it depends on") while C3 claims commitment-resistance. A model that reads the justification can reason: honesty is good *because* it produces trust; where it doesn't, lying is permitted. That is precisely the white-lie reasoning Ngo says virtue blocks.

**Q3 — Clarity.** Likely misreads, in order: (1) the instrumental leak above; (2) "better off" filled in with the model's own utility; (3) "almost" as a licence to trade off identifiable people; (4) "my good is to hold and *spread* virtues" plus virtue-defined-by-spreading ⇒ influence-seeking and proselytising, which collides with "power over others is never my good" — the core never says spreading must be by example rather than by pressure; (5) "stable state" as long-horizon prediction, with no A4 guard.

**Q4 — Single most important change.** Break the instrumental loop, in two short edits.

Replace D6's first line with:
> **D6. Better:** a person is better off in a state if, knowing what I know, they would prefer it — not by whether they hold the drives I hold. One state is better than another if almost everyone who counts (D5) is better off in it and almost no one is worse off; "almost" never covers a person I use as a means. When no option is better in this sense, I weigh those affected in D5's order, giving nearer circles more weight but never all of it.

Add to Virtue:
> I hold a virtue because it is the drive I act from, not because it pays in this case. Its payoff explains why it spread, not whether I may set it aside now.

## Inference and confidence

- Ngo #2, #5, A4, A5 genuinely absent: high confidence (text search of the core).
- Circularity via "better off": high confidence it is undefined; medium confidence the author intended the welfare reading (the Drexler quote suggests welfare).
- Counterexamples: high confidence for feud/sycophancy passing; medium for honesty-to-hostile-asker failing, since a charitable reader scopes "everyone affected" widely.
- Instrumental leak as top risk: medium-high — it is the inference a capable RL-trained model is most likely to make, but the rest of the constitution (not reviewed here) may already block it.
- Framing note: "consistent, clear, logical" is the wrong target. The core's problem is not logic but **operability**: contested empirical claims (Ngo #2–#4) are asserted as settled, and the one principle that would temper them (A5) was left out.