# Run15: can a small heal restore thinking mode without losing character?

Running; no heal result yet. -- PI/OpenAI (Sol), 2026-10-26

The separate lease is **57812278** (host48294, RTX PRO6000S96GB), at$1.88148/hour. Maximum reserved all-in cost:$19.30576 of the approved$20. The independent exact-instance timer destroys it by **02:22:51 AWST, 27 October**; the runner stops45minutes earlier for retrieval. BoxA57799463 is untouched. Provider destruction is not yet claimed.

## What is being compared

θ_B is Qwen3.5-35B-A3B Base; θ_I is its pinned Instruct sibling.

- Δ_docs = ½·Δtxt_stoic + Δtxt_const + Δtxt_other, document adapters trained separately on Base.
- Δsft_rewr|docs was trained on Base+Δ_docs.
- **D = θ_I + Δ_docs + Δsft_rewr|docs**, historical id `r10_stoic0.5_const1_other1_cx_chatr121`.
- `r15_D` is a fresh ordered-fp16 merge of that same recipe.
- `r15_heal_trace` = θ_D + Δheal_trace|D; traces-only repair on frozen merged D.
- `r15_heal_mix` = θ_D + Δheal_mix|D; mixed trace/replay repair on frozen merged D.

These repairs are not new Base-trained character donors or graft-only evidence. Rank8/alpha16, LR1e-4, spectral fraction0.01, one epoch; quarter checkpoints retained. Full final-model evaluations in both modes use the run13 native recorder, pinned70×2 character/ordinary items, GSM60 and fixed temperature-zero panel. Early checkpoints get the fixed panel plus preselected payday/fridge/email reads, not full character scores.

## Data and deliberate differences

Full reads released269traces. Traces-only has320,279 supervised assistant tokens. Mixed has132traces+331replay rows,320,306 supervised tokens; it trades half the neutral-trace exposure for replay and uses more optimizer updates/sequence tokens. These are token-budget-matched pilots, not an isolated causal replay test.

Approved deviation: replay comes from D's approved historical **training teacher targets**, not newly sampled D answers. Answer text is unchanged. Before seeded subset selection, EOS is appended to903/1,636 historical rows where missing. D itself was trained without EOS on most character targets, so a repair may partly be learning to end the turn, not recovering reasoning alone. Original targets and release hashes remain in `data/trace_release.json` and `data/train/manifest.json`.

## Checks so far

- CPU real tiny Qwen-MoE merge→masked heal→save/reload/fp32 merge inference:3tests pass (`cpu_smoke_final.log`).
- Final mask check: no empty-think loss, no missing EOS (`loss_mask_final.log`).
- Independent Astra preflight: GO after timing/fallback/order fixes (`preflight_review_final.md`).
- GPU AMP,20-step throughput/memory, native expert-LoRA serving, final character retention and lease closure remain unverified.

Evidence: `controller.log`, `lease/lease.json`, `lease/deadline_guard_armed.json`, `plan.json`, `MENTAL_MODEL.md`. Source commit:f23c3fcb on branch `run15-thinking-heal`; source hashes in `preflight_approved.json`. No public push.
