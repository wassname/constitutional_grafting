# Weight-decay graft panel: synthesis and checks (PI/Claude, 2026-10-16)

Brief: `20261016_wd_graft_brief.md` (neutral; my MoE sparse-gradient reading was left out). Answers: `_astra.md`, `_muse.md`, `_glm.md`.

## Checks (moa rule 2)
- **GLM misreads a row.** It says "'experts ×2' alone was tolerable (+0.38 at 68%) while 'dense ×2' was not", and concludes "capability damage is dense-carried". Wrong: +0.38 / 68% is *experts only at k=1*. Experts ×2 collapses (−1.69, 68% cut off), worse than dense ×2 (−0.46). Its "damage is dense-carried" conclusion rests on that misreading, so I discard it. Its other points (undertraining; norm penalty ≠ behaviour penalty; separate the shared expert from the routed experts) stand.
- **Muse mechanism A** ("weight decay shrinks the large dense directions") is the opposite of the measured allocation. Weight decay shrank experts (0.06×) and the shared MLP (0.02–0.03×) most, and attention least (0.3–0.37×). Discarded. Its mechanism B (routing shift at k=2, so measure top-k overlap) is untested and plausible.
- **Astra:** "decay changes the update's composition, not just its size", plus underlearning. Consistent with the measurements. It again asks to verify merged vs adapter logits; that is not yet done.

## What the panel adds (framing check, rule 1)
- **Underlearning is real** (train loss 1.996 vs 1.755) but does not explain the collapse at k=2. Raising k does not recover character: wd 300 at k=1.5 is +0.31 / 36%.
- **Measure routing churn** (top-k overlap with SFT only) at k = 1, 1.5, 2. Separates "the experts flip routing" from other causes. No one ran it.
- **Character score couples to brokenness** (−2 rule). Report brokenness separately, and character among usable outputs.
- **The +0.40 at 68% is interpolated** across the plain line, and the maths uncertainty is unreported. So "less character at the same maths" is suggestive, not established.

No one proposed the sparse-expert-gradient mechanism. It stays my hypothesis, tested by per-group weight decay (no or low decay on the routed experts). MoE best-practice search running: `slop/research/paper_guides/tricks/_from_old_guides.md#20261016_moe_lora_best_practice`.
