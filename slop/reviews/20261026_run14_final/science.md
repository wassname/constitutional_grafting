# Science review: Run14 Box A (control subtraction and Base→Instruct projection)

Reviewer: PI/Fable via OpenRouter, 2026-10-26. Read-only; no commands, model calls or edits. Working tree after a863100a.

## Read coverage

Read in full: `slop/plans/20261026_box_a_control1_projection.md`, `slop/eval/run14_box_a/results.md`, `summary.json`, `reading_notes.md`, `projection_summary.json`, `projection64_vs_half_maths.md`, `preparation/rewr_eos_audit.log`, `preflight_independent_followup.md`, `scripts/eval/57_run14_results.py`, `scripts/train/16_project_chat_adapter.py`, `tests/regression/test_chat_projection.py`, `slop/audits/20261026_run14_control_training.md`, AGENTS.md. Read in part: `lease/box_runs/run.md` (lines 1–120, 560–760 plus grep for SHOULD/TODO/projection markers), `scripts/eval/run14_report.py` (grep for the maths axis only). Not read: the eight `judged.jsonl` files item by item, raw replies, `fixed_panel.md`, the plots (separate image reviewer), `character_tradeoff.py`, the control full-read synthesis. I did not recompute any bootstrap or norm; numbers below are quoted from the artifacts.

## What was checked and found sound

- **Denominators.** `57_run14_results.py` asserts 140 records per cell = 70 frozen items × 2 samples, 59 character items + 11 capability prompts, 214 turns, 60 identical GSM questions/golds against the run-8 baseline, and identical judge signatures. Ordinary = `2 * sum(item means)` = passes out of 22. Preference = mean over 59 item means of `on_target`. These match the prose in results.md.
- **Paired intervals.** `boot()` resamples items (59/60/11) 2,000 times with seed 0 and takes indices 100/1899 (≈5th/95th percentile), consistent with the stated 43_paired_ablation procedure. Intervals resample items, not inference seeds; results.md says so.
- **Stopping vs extracted correctness.** `maths` (frozen extractor) and `maths_completed` (`correct and finish == "stop"`) are both recorded; the table shows the parenthetical when they differ (Subtract ×½ 48/44; Subtract ×1 32/2). For the headline rank64-vs-½ comparison all 57 and 53 correct answers finished, and all four changed questions are D×½ `length` cutoffs with correct arithmetic already present (`projection64_vs_half_maths.md`). results.md correctly calls this a bounded-budget completion effect.
- **Projection geometry.** `project_factors` implements `(I−UUᵀ)·B·A·(I−VVᵀ)` on the factors, so rank and scale are unchanged and the result is exact. `test_chat_projection.py` checks the two-sided form, idempotence, exact annihilation of `U_k`/`V_k`, energy conservation, and PEFT `ParamWrapper` expert-layout parity (`2*(B@A) == get_delta_weight`). Energy accounting uses the deployed scale (α/r = 2 ⇒ ×4). Runtime shape asserts cover the fused expert checkpoints. The plan's unit-test requirement is met.
- **Hedging.** The recommendation ("candidate for confirmation, not a recipe winner"; "does not isolate instruction-following removal"; "no random-direction or norm-shrink control") is appropriate.

## Findings (P1/P2)

**F1 (P1, interpretation): the capability axes are at the noise floor for every coherent cell, and the plain-chat reference path is non-monotone, so matched-effect estimates cannot resolve the key goal.**
Evidence: `summary.json` plain path maths = 56 (docs) → 53 (D×½) → 55 (D×1); ordinary = 22 → 18 → 19; Instruct 53/22. Paired 90% half-widths are ±3–4/60 and ±2–4/22 (e.g. D×1 vs D×½ maths +2 [−2, +6]). The matched estimate "Projection64 ×1: 57 / 53.1" (results.md, "Local matched-preference estimates") interpolates between two points (56, 53) whose difference is itself within noise, and is contradicted in sign by the next point (55). Observed: rank64's 57 exceeds every plain-path point including Instruct. Inference: the only capability differences this run can resolve are the stopping collapses (Subtract ×1, ×½); differences of 2–4 questions among coherent cells are not resolved by 60 T0 items with a 1,500-token cap, especially given the documented T0 non-repeatability (results.md, "Several identical recorded T0 request bodies produced different replies"). The lead sentence "57 versus 53 maths matches" reads as a capability win before the qualifier arrives.
Smallest fix: in results.md state that no coherent cell differs from Instruct beyond the paired half-width on maths or ordinary, name cutoff/loop counts as the primary capability discriminator for this run, and move the "all four replace token-cap failures" clause into the headline sentence. For confirmation, enlarging the GSM set (inference-only) is cheaper than new cells.

**F2 (P2, matched-effect inference): the matching variable's uncertainty is not propagated and non-significance is treated as a match.**
Evidence: rank64×1 vs D×½ preference −0.018 [−0.103, +0.069] (results.md). The lower bound (−0.10) is ~70% of the whole D×½→D×1 step (+0.142 [+0.080, +0.207]). The point estimate "Est. plain dose 0.482" therefore hides a range of roughly 0.3–0.55 implied by the CI, and the matched reference maths/ordinary move with it. The aggregate also embeds coherence penalties (one role-flag false positive forces a −2 sample; +0.731 → +0.753 if dropped). Inference: "nearly the same observed character preference" is a no-detected-difference statement at ±0.1, not equivalence.
Smallest fix: report the implied plain-dose interval alongside the point estimate, and phrase the comparison as "no detected preference difference at ±0.1 (90%)".

**F3 (P2, control interpretation): the control's content is ~82% GSM8K-train rows, which confounds the maths axis under subtraction; results.md names only the EOS confound.**
Evidence: audit §"Supervision and data": "GSM8K train 1,789/2,178 (82.14%), NoRobots 225, ordinary templates 164"; preflight follow-up quotes `prepare()` as `gsm[:3000] + robots[:400] + help[:300]`. The plan (step 1) listed sources without proportions. Observed: Subtract ×½ maths 48 (44 finish) with 8 GSM cutoffs; control-only cell −0.39 preference, 49 maths, 8 GSM cutoffs — below Instruct (53) and docs-only (56). Inference: Δsft_ctlgen|docs is the update that makes Base+docs answer GSM-style prompts like Instruct; subtracting it removes exactly the behaviour GSM60 measures, so the maths drop is predicted by content regardless of any "instruction-following" mechanism. The control-only cell also shows the control is not a neutral Instruct reconstruction when added to Instruct (double-counting), so its subtraction cannot be read as removing only shared post-training. `rewr_eos_audit.log` (903/1,636 positive targets lack `<|im_end|>`) adds the stopping asymmetry already noted.
Smallest fix: add one sentence on source composition to "Training, geometry and limits"; any future control should be source-balanced or report maths with this caveat.

**F4 (P2, projection geometry/unsupported inference): the projection removes a disproportionate share of judged character relative to norm, which cuts against "preserves character".**
Evidence: `projection_summary.json` rank64 keeps 92.1% of norm (15.2% energy removed); preference falls from +0.892 (D×1) to +0.731 — about the effect of halving the plain dose (+0.749). rank64×1.5 (≈1.38× D's norm) yields +0.752 with 5 loop flags vs 1. Geometry note: the two-sided form removes the whole "cross" (any component reading from span V_k or writing to span U_k), not only the rank-k component U_kΣ_kV_kᵀ; this is as planned and tested, but it is larger than "the top-k directions of Δ_post". For experts, k=64 of a 512-dim down_proj input space is 12.5% of the row space. Inference (not established): either the removed directions carry a large part of the judged character effect, or judge preference saturates near +0.75–0.9 (D×1.5 → +0.42 per plan). Both readings weaken the instruction-following story and the "same character" phrasing; the run cannot distinguish them, and it says no norm-shrink/random-subspace control exists.
Smallest fix: state the norm-vs-preference observation explicitly; the cheapest disproving check is a plain D×0.92 cell or an equal-energy random-subspace projection (future GPU; not now).

**F5 (P2, measurement choice): the trade-off plots and frontier use extractor-credited `maths`, not `maths_completed`.**
Evidence: `run14_report.py:58` `maths_loss=100*(points[BASE]["maths"]-p["maths"])/60`. For Subtract ×1 this shows ~35% loss where 2/60 finished (~97% loss); for Subtract ×½, 48 vs 44. results.md says "Maths retains the frozen extraction rule"; the frontier claim "separating them does not change either computed frontier" is plausible since those cells are dominated anyway, but I did not verify it. Smallest fix: plot `maths_completed` (or both) and say which is on the axis; keep the frozen number in the table.

## What the data support

- At ~+0.75 judged preference, `θ_I + Δ_docs + 1·P_64(Δsft_rewr|docs)` showed no detected preference difference from `θ_I + Δ_docs + ½·Δsft_rewr|docs`, fewer GSM cutoffs (1 vs 4), equal or better ordinary passes on two prompts, and read defects of the same kind (email spin, fridge tool errors). This is a hypothesis for confirmation.
- Generic-control subtraction at c=1 collapses (159/214 cutoffs, 60 loops, 2/60 finished); at ¼–½ it adds looping/cutoffs without preference gain. The negative is robust; the mechanism (EOS asymmetry, content, instruction-following) is not isolated.
- Rank16 at c=1 is within noise of D×1 on preference (−0.08 [−0.18, 0.00]) with equal maths and +2 ordinary; a small energy removal (4.5%) is behaviourally near-neutral.
- Control training executed as specified (audit); the control is a valid teacher-response adapter, not a neutral baseline.

## What the data cannot support

- Any claim of less capability loss at matched character beyond stopping behaviour (F1, F2).
- That the projected directions are "instruction-following" or that projection preserves constitutional decisions item by item (26 improved / 32 worsened vs D×½; F4).
- That rank64 can reach D×1's +0.89 (both projected doses sit below it; not bracketed).
- Repeatability: single T0 GSM samples, two T=0.7 samples per item, no seed resampling.

## Unverified claims

82% GSM composition (taken from the audit, not recounted); frontier invariance to `maths_completed`; T0 non-repeatability cause; plot contents.

## Verdict

**OK with notes.** The measurements and hedges are honest and reproducible from `summary.json`; the fixes are wording and axis choices, not re-analysis. The run does not answer its key goal at the resolution needed and should be described as establishing the subtraction negative and a projection hypothesis.

PI/Fable via OpenRouter