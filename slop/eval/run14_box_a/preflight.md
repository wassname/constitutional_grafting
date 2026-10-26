# Run14 preflight

PI/OpenAI (Sol), 2026-10-26. Approved brief: `slop/plans/20261026_box_a_control1_projection.md`; parent separately approved one rewritten-chat dose at0.5, not interpolation through the damaged1.5point. No rental yet.

Goal: test generic-control subtraction and two-sided post-training-subspace projection at matched character preference. Redundant instruction-following is a hypothesis: Base has some instruction-following ability, and Base→Instruct changes include more than instruction-following.

## Inputs and controls

- The adapter in D was trained on1636chatr12rows, SHA256 `91e95a6eceff6841190e2485006493b1967e0dc9cc4f954da5e8c7a488a79042`, not today's1625rows. Reconstructed into `.local/run14_executed_chatr12/` with the subsequent rule-removal row filter disabled. The complete file hash matches the stage7upload receipt. Target788,606assistant-supervised tokens; no extra special tokens during per-segment counting.
- Local generic pools:7,423control requests (6,723GSM8Ktrain,400NoRobots,300new neutral ordinary-help requests) and1,000disjoint save-only thinking requests (750/150/100). Initial3,700control requests retain the planned shuffled mixture; remaining GSMtrain requests are a fixed reserve if needed to reach the token target. No human answers reused. All frozen character/boundary/demo/panel/POV requests and GSM60 are excluded by normalized exact/substring and12wordoverlap; actual pool files saved.
- Initial prompt read found sentiment-reversal and speaker-perspective requests in NoRobots Rewrite. Entire category excluded before generation. Rejected package and read finding retained under `preparation/rejected_rewrite_category/`. Main agent read559NoRobots candidates in full, excluded9explicit normative/moral/philosophical lessons, and read all refills; all550selected prompts are covered in `no_robots_prompt_review.json`. Teacher answers are not yet generated or reviewed.
- Finished untouched-Instruct off-replies only (the parent assigned heal-pool generation to a separate OpenRouter worker; no GPUthinking stage here); truncated originals retained but excluded from training. Keep refusals as generated, count them through full reading. Whole-row token matching within0.05%; no correctness/refusal filtering. Empty think block unlabelled, EOS labelled. Same donor,2epochs,ranks/targets and spectral_frac0.01as D. Token matching does not match rows, optimiser steps or warmup duration.

## Projection

For each original checkpoint weight matrix, compute exact full SVD of `W_I−W_B` in fp32. Keep top16/64singular vectors. For each low-rank update `2 B A`, save

    A_projected = A − (A V_k) V_kᵀ
    B_projected = B − U_k (U_kᵀ B)

Same rank/scaling, fp32 adapter factors; document adapters unchanged. Expert factors use the PEFT packed-expert layout, not a single flattened matrix. Report removed-component Frobenius/original Frobenius and removed-energy fraction per module class and expert. This operation removes cross-directions too, not only the diagonal singular components.

CPU checks:24tests and7subtests pass, covering exact two-sided projection, idempotence, left/right annihilation, real PEFT0.21.1 delta parity, signed expert merging, off-wire preservation, retrieval and deadline failure paths (`preparation/preflight_tests.log`). All330adapterstems map into BOTH pinned checkpoint indexes (`preparation/checkpoint_key_audit.log`). Projection functions have runtime tensor-shape checks. A real random-small Qwen MoE three-step training smoke and five-module actual-checkpoint projection smoke will precede full training on the box. No GPU smoke has yet run.

## Predictions and alternatives

Subjective competing explanations before outcomes:35%shared post-training overlap can be removed with an improved matched-character capability/format trade-off;45%it is entangled with useful character or instruction-following and subtraction/projection mostly weakens or damages it;20%implementation/measurement/unknown problems dominate. These are rough planning bets, not calibrated probabilities.

- A scalar weakening can improve apparent damage: new D×0.5and existing D×1bracket the coherent reference where possible. D×1.5is excluded because of documented coherence damage, not because its score is worse. No bracket means no identified matched-effect claim.
- A wrong expert layout or projection sign can look like a method failure: exact tensor operations, checkpoint-key/shape checks, unchanged rank/scaling and per-group norm records distinguish it.
- A control can carry persona/moral requests or learn the wrong format: input read, first32normal-path teacher replies plus independent review, complete final control-data read, loss-mask check and control-alone graft are the checks.
- A judge can reward principled words while actions/facts are wrong: retain pinned judge for comparability, then read every new fixed panel and both samples of payday/fridge/email, including failures.

Reference values: untouched Instruct is character0by definition, GSM53/60 and ordinary22/22; D is+0.89,55/60,19/22. Maths already exceeds baseline by2items, so report percentage-point changes rather than a percentage reduction in a nonexistent positive maths loss. One training seed, two generation samples; no training-seed uncertainty estimate.

## One-lease reservation

The earlier qualified datacentre quote (RTXPRO6000S96GB,32effective CPUs,129GBRAM,500GBdisk,$1.91852/h) is no longer available. Current waiting/fallback authority is in `budget_decision.json`; keep the quality filters. The old guarded plan below remains inactive until a fresh offer is selected and reported. Lower-price hosting_type0offers excluded.14h hard cap, runner stops1.5h early for retrieval; independent exact-instance deadline plus lost-heartbeat watchdog. Reserve at max$1.92/h: GPU$26.88 + traffic$0.80 + judge$2 + independent review$2 + termination$1 = $32.68/$35. No replacement lease.

Server-GPU stage estimates, not measurements: setup/uploads1.7h(overlap); off teacher0.9h; control read up to1h (overlaps the required lower-dose reference evaluation); train2.3h (depends on actual rowcount); exact projection2h; eight eval cells2.8h; retrieval1.5h; smokes about0.25h. Rough total12.1h after overlap. After generation, actual rowcount feeds a historical-step-based forecast; only the final optional projection dose may be omitted, otherwise the core must fit before training. Max-Q requires a separate speed forecast, not this server estimate. Faster execution ends billing early. Before renting, refresh stock/rate and validate inputs before creation. Wassname confirmed auto-funding through the parent: `funding_confirmation.json`; this authorizes using auto-billing if prepaid credit alone is below the reservation. The total cap and exact-instance safeguards do not change.

Independent initial review and checked responses: `preflight_independent_initial.md`, `preflight_review_response.md`. The final targeted check found no launch-breaking defect in the new mechanics. Remaining actionable points are fixed: explicit eval PYTHONPATH, offer-based traffic reserve, exact offer-report binding, and old/new off-wire/scoring parity (`preparation/off_protocol_parity.log`). `preflight_approved.json` approves technical preparation, not ungenerated data or results. `offer_selection.json` is deliberately absent until a fresh quote is reported; without it no lease can be created. Nothing pushed.
