Setup in my own terms: A LoRA `ΔG` is trained on Base (Qwen3.5-35B MoE) on 1.6k synthetic virtue-ethics docs, then added to a chat model `W_sft` as `W_sft+k·ΔG`. At k=0.5–1 you get modest character shift (+0.3–0.5/2) with large cost (maths 86%→~60%, longer disobedient replies); at k=2 everything collapses (maths ~10%, 65% truncated, judge −1.6). Shrinking `ΔG` by 10–15× (spectral penalty, wd=300) does not move the cliff.

### 1. Mechanisms

**A. Style graft, not just weights: verbosity/instruction-disobedience causes most of the measured collapse. Likely (~70%), and necessary but not sufficient.**
At k=1 replies are already 1.5–6× longer, ignore "one line", moralise inside maths. Maths-correct + cutoff move together (59%→11% as cutoff 9%→65%). Truncated long answers are auto-wrong, and the judge punishes rambling (−1.6 is probably "worse assistant", not "vicious character"). Fails to explain: why cutoff itself explodes non-linearly 1→2, and why dense×2 vs experts×2 differ.
*Cheapest test (~10 min, no retrain):* rescore existing k=1/k=2 outputs with (i) 4× length cap, (ii) length distribution + "first-number-correct" vs "exact-format-correct". If maths recovers substantially, it's measurement+disobedience. Also sweep k=1.0/1.25/1.5/1.75 on one graft to map cliff shape.

**B. Additive composition off-manifold / Base→Instruct mismatch. Likely (~65%).**
`ΔG` was learned to perturb Base; adding it to `W_sft` is `W_base + ΔSFT + k·ΔG`. Nothing guarantees composability; interference grows superlinearly in k because activations shift → MoE routing + attention softmax saturate. Explains why magnitude constraints fail (see C) and why healing on WikiText/distillation doesn't restore (interference is systemic, 32 steps can't re-route). Fails to explain alone why experts×2 is worse than dense×2.
*Cheapest test:* train the identical LoRA recipe directly on `W_sft` (frozen) for 1h, compare k=1 curve; plus per-layer activation-norm / perplexity on Wiki vs graft-docs at k=1 vs 2 to localise blowup.

**C. Raw norm/spectral norm is the wrong quantity — direction matters. Very likely (~85%, this is evidence not hypothesis).**
Weight-decay graft has 0.069× the Frobenius norm of plain, spectral graft cuts dense σ_max 0.35→0.07, yet k=2 cutoff is identical (64–69%). So the cliff is not "too big". A tiny but systematically misaligned direction (e.g. shared-expert/attention bias pushing all tokens toward elaboration, router–expert mismatch) suffices. Note spectral penalty *raised* stable rank 4→37: it spread the same harmful direction across more singular vectors.
*Cheapest test:* cosine / projection of `ΔG` vs `ΔSFT` per module; layer-wise ablation: add graft one layer-group at a time at k=2 to find the minimal breaking subset.

**D. MoE-specific routing fragility. Plausible (~40%).**
Experts×2 alone breaks (−1.69/68%); dense×2 alone half-breaks (−0.46/38%). Routed-experts-only k=1 is the best capability point (68%, 2% cutoff). Small expert-output shifts compound through top-k routing (unchanged router now sees shifted hidden states). Fails to explain dense contribution.
*Cheapest test:* log expert-entropy / top-k overlap vs SFT-only on 50 prompts at k=1 vs 2; if overlap collapses, it's routing.

I am unsure: judge validity (n=59, ±0.1–0.27 half-widths, pairwise vs SFT-only confounds verbosity with virtue); whether "loops 2–6%" probe used same decoding/cap as evals; PEFT scaling in reported norms.

### 2. What would actually raise usable dose

Stop constraining norm; constrain *behaviour + direction* with `W_sft` as reference, not `W_base`:

1. **Train on the chat model, with replay (≈1 graft, $5–10).** Freeze `W_sft`, LoRA on chat-formatted virtue data + 10–20% SFT/Wiki + short-form/instruction-following examples ("answer in one line", JSON, maths with no moralising). Loss = next-token on graft docs + λ·KL(`W_sft`||model) on replay (λ~0.5–2, tune to hold Wiki PPL within +5%). Hold data/steps/seed fixed vs plain. This directly targets A+B.
2. **Per-module adaptive composition, no retrain (~10 min × few).** Replace scalar k by per-group scales fit to keep activation drift bounded: grid-search (experts-scale, dense-scale) on 30 held-out prompts minimising ‖h_grafted−h_sft‖ subject to character gain; or TIES/DARE-style trim (keep top-20% |Δ|, sign-consensus with ΔSFT, orthogonalise ΔG against ΔSFT per matrix). Predict: experts need ≤0.5× dense.
3. **Localise then sparsify.** From 1C/1D ablations, zero the 2–4 breaking layers/modules and retrain or mask; expect most character with fraction of cutoff.

Don't: larger λ spectral penalty, larger wd, lower LR alone — already falsified as cliff-movers (they hurt doc loss 1.92→1.99 with no k=2 gain).

### 3. Is "raise k" the right target? No.

k is units of an arbitrary LoRA scale (r64/α128, rank-16 experts); 2× means nothing absolute — wd proved a 14× smaller vector breaks identically. The owner's goal ("striking general moral-reasoning change, skills kept") is a Pareto frontier, not a k. Target instead: **max character score subject to capability guardrails** (e.g. maths drop ≤5pp, cutoff ≤5%, Wiki PPL +≤5%, instruction-compliance held-out). Report character-vs-maths curves, not k. Also fix the eval: current judge rewards showing procedure (stakeholders, confidence) which is verbosity; add brevity-controlled and instruction-conflict items, and score capability with generous caps so truncation ≠ inability. A graft that is +0.4 with skills intact beats a "k=8-stable" graft that is +0.1.