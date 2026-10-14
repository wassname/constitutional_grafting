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
- [/] goal B: Qwen graft covers routed experts
  - [x] `configs/train/qwen3/`: experts via `lora_target_parameters`, per-expert r16, dropout 0, router frozen (Axolotl docs, Unsloth default). 02_merge.py fails if experts unchanged.
  - [x] CPU test passes: experts get a delta, reload/merge parity, k-scaling linear, rank_pattern applies (`tests/regression/test_moe_expert_merge.py`).
  - [ ] 2-3 step GPU smoke run on the training image: expert lora_B grads nonzero, peak memory, merged expert weight changed.
  - failure modes: scattermoe fastpath absent in our image; OOM at seq 8192.
- [ ] goal C: heal a strong graft in a few batches (wassname: "retrain it to coherence should only take a few batches")
  - [ ] Start from graft x4 (Gemma); separate rank-8 repair LoRA; no new character labels. Checkpoint ladder 8 / 32 / 128 updates (batch 4 x 8k: 0.26 / 1.0 / 4.2M tokens). Precedent: NVIDIA healed pruned Qwen3-8B with 100 iterations of WikiText (~1.6M tokens).
    (a) no heal; (b) generic long text NLL (WikiText + broad chat) with 10-20% coherent graft-expressive replay so the heal does not pull it back to bare; (c) steer-heal-love heal: own filtered completions + hinge reverse-KL to instruct, `kl_agg=rmse`, `barrier_ref=base` (repo defaults are mean / prev).
  - [ ] Free first: sweep k between 2 and 4 to find the coherence edge. Backlog: on-policy distillation from graft x2; GRPO with an anti-repetition reward. Not entropy minimisation (can reinforce loops).
  - [ ] Compare against plain graft x2: healed x4 must beat x2 at equal loop rate and capability.
  - failure modes: heal washes the graft out (steer-heal-love saw this once, with a filter that dropped trait-laden completions); heal only reproduces x2.
  - deliverable: x2 | x4 | healed x4 (b, c) | SFT only, on tiny-char head-to-head and demos, with loop rate and capability.
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
