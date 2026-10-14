# Grafting, tested properly — draft plan, not approved

PI/Claude (Opus 5.5), 2026-10-14. Replaces `20261013_character_retention.md` and goal 2 of `.pi/goals/ad3e95-v3.md`.

> "we should try properly either closer to the paper or with more well thought out divergences (e.g. adding healing might be worth it, and rewording data to be on policy might be worth it)"
> "originally I said 'why not graft at 4x, but heal by SDFT' ... it was meant to just 'heal' the transplanted weights"
> "we still want a striking demo but we need to rework our approach" — wassname, 2026-10-14 (spelling corrected)

Aim: the most generalising virtue-ethical character for the least capability cost. Mechanism tests use the frozen v4 constitution and saved data; the final run waits for the constitution fixes.

- [ ] goal A: graft last. Does the graft add to SFT when it is added after it?
  - [ ] Gemma: merge saved run 4 SFT-only, then add run 3 graft at k=1,2. No training. Same frozen 70 items, 4 samples.
  - [ ] Compare: bare, graft x2 alone, SFT only, graft→SFT (saved), SFT→graft. Direct head-to-head SFT→graft vs SFT only.
  - failure modes: graft added twice (healed weights as start); graft-last breaks coherence at k=2; judge ceiling hides a real gain.
  - deliverable: tiny-char head-to-head with intervals, plus 3 short demos, in `docs/audits/run5.md`.
- [ ] goal B: Qwen graft covers routed experts
  - [ ] LoRA on `mlp.experts.*` per Axolotl/PEFT (research: `slop/research/20261014_qwen35_moe_expert_lora.md`); merge probe checks an expert weight changed.
  - [ ] CPU test on a tiny random Qwen3.5-MoE: merged delta is nonzero on experts and scales linearly with k.
  - failure modes: experts silently skipped by scattermoe kernels; merge drops ParamWrapper deltas.
  - deliverable: regression test passing, config diff committed.
- [ ] goal C: a real healing step at a strong dose
  - [ ] Choose the repair method from `slop/research/20261014_healing_after_weight_edits.md` (candidates: SDFT/on-policy self-distillation, KL to a coherent teacher on generic prompts, replay). No new chat labels.
  - [ ] Graft x4 (Gemma) and x2 (Qwen, with experts), heal, then measure. Teacher choice decides what survives; record it.
  - failure modes: healing restores coherence by washing out the graft (score falls back to bare); the heal data leaks character content, so it is SFT again.
  - deliverable: graft xk | healed xk | graft x2 | SFT only, on tiny-char and demos, with loop rate and capability checks.
- [ ] goal D: closer to the paper (only if A-C leave the question open)
  - [ ] anchored graft (docs+replay minus replay-only); native control (documents on Instruct); Praxis reality-drift and preference checks.
  - deliverable: damage at matched character effect, graft vs native.
- [ ] goal E: striking demo and trustworthy eval
  - [ ] Re-check tiny-char scores judged in the Sol window (Qwen2, cwsteer). Ask tiny-char for absolute or head-to-head scoring where the vs-base score saturates.
  - [ ] Demo panel on the best model: base vs trained, verbatim, prompts no call-centre assistant would answer that way.
  - deliverable: demo at the top of the audit, read by wassname.

## UAT / Verification

- Success: SFT→graft or healed-graft beats SFT only on the head-to-head (interval above 0) on OOD families (w2schar, tiny_stoic, contested), with loop rate and capability within the noise of SFT only, and the demos show it.
- Likely failure: no difference. Read transcripts and the judge's reasons, check merges (weight-delta probe) before concluding redundancy.
- Sneaky failure: score gain from style or length, or from a double-added update. Caught by demos, the merge report and order-reversal rates.

## Appendix: open choices

- On-policy rewording of SFT/doc data (Karan projection, Echo restyle): candidate for the final run, not the mechanism tests.
- Cost: goal A ~ $5 GPU + judging; goal C one training box run (~$10-15).
