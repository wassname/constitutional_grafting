# Review: why wd=300 graft underperforms and still breaks at 2×

**Setup (restated):** A LoRA trained on the frozen base Qwen3.5-35B-A3B (MoE) with character documents is added as k·ΔG on top of Instruct+SFT. A wd=300 run shrinks the LoRA ~15× in deployed-update norm but at k=1 gives less character per unit of damage than the plain graft, and collapses at k=2 just the same.

## Q1: Why less character, and why still break at 2×?

**Mechanism A — undertraining (most likely).** wd=300 final loss 1.996 vs 1.755 plain; held-out 1.994 vs 1.922. The graft simply encodes less of the character. The 60-step pilots show monotone loss degradation with wd, so this is directly confirmed. But it fails to explain the *ratio*: if wd merely scales the update down, dose k should compensate (you'd get +0.4 at 68% by raising k to ~1.3). The fact that wd=300, k=1.5 gives +0.31 at only 36% — worse damage — shows k doesn't linearly recover character. So undertraining is real but not the whole story.

**Mechanism B — norm penalty ≠ behavioral-perturbation penalty.** Weight decay shrinks where weights are big, not where they matter. It compresses σ_max (spectral norm) across the whole update, including directions that are harmless, while leaving whatever residual "damage direction" exists undamped relative to character directions. Collapse at k=2 with only 1/15 the total norm (update norm 2.62 vs 37.9) strongly supports this: the collapse is not about raw size but about a specific bad direction — likely in dense modules (attention/shared expert), since "experts ×2" alone was tolerable (+0.38 at 68%) while "dense ×2" was not (−0.46, 18%). wd=300's largest remaining relative perturbations at k=2 are exactly in linear_attn/self_attn (0.0052–0.0054), 3–4× its expert perturbations (0.0015). The spectral-norm run corroborates: it cut dense σ_max 5×, got +0.42 at k=1, *and still collapsed at k=2* — same signature.

**Mechanism C — A/B imbalance.** Decay acts multiplicatively on factors; it may leave a low-rank-but-ill-conditioned pair such that scaling k amplifies B's outlier directions nonlinearly. Plausible contributor, less evidence.

**Cheapest discriminator:** train a graft with a plain objective (no wd) and then *post-hoc* shrink only the dense modules (scale attention/shared-expert ΔW by 0.3, keep routed experts at full). If that matches the plain line's character-with-damage ratio and survives k=2, the damage is dense-carried and wd's failure is misallocation, not undertraining. Alternatively: singular-value spectra of ΔW for dense modules in both grafts — if wd=300's dense update has an outsized top singular value relative to the rest, B is confirmed.

## Q2: Where are character and damage carried?

The ablations are informative: routed-expert-part-only at k=1 gives +0.38 at 68% — most of the character with essentially zero maths damage (68% vs 59% full graft). Dense-part-without-experts gives +0.26 at 73%. So character is roughly split between routes and dense, but **capability damage is dense-carried**: doubling dense parts drops maths to 18% and cuts off 38% of turns; doubling experts alone keeps 68%. Next step: an experts-only graft (dense ΔW = 0, experts possibly raised to k=1.5–2), or a wd/penalty applied only to dense modules while experts train freely. That directly targets "more character per capability cost." Caveat: shared_expert is classified dense here yet had the largest plain perturbation (0.053) — I'd test routing vs shared separately.

## Q3: What's likely wrong or misleading?

- **n=59 items, 2–4 samples, and a pairwise judge vs SFT only.** +0.28 vs interpolated +0.40 is within plausible noise given ±0.10–0.15 intervals; interpolation across k=1 and the plain line is fragile. Confidence in the "less character per damage" claim is moderate.
- **"Broken = −2 by rule"** makes the score non-monotone and couples character to capability; the collapse rows are dominated by this rule rather than judged character.
- **Loss comparison across wd runs may mislead:** wd penalizes norm, so its reported loss is biased upward in a way that doesn't map cleanly to content learned.
- **2 epochs, 389 steps, 8-bit AdamW, constant-lr 60-step pilots** — the pilot ordering could differ from full cosine runs.
- Small uncertainty: whether PEFT scaling interacts with k multiplication consistently across runs (total update norm "with PEFT scaling" suggests it does).

**Uncertainties:** I can't verify the judge's robustness, the exact interpolated plain-line value (+0.40 is my estimate), or whether 0.876×-norm collapse implies the plain graft's k=2 collapse is also threshold-like at a similar behavioral perturbation.