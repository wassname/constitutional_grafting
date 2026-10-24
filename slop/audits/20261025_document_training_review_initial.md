# Independent read-only audit: run 11 lease 1 document trainings and pending Base-loss comparison

Author: reviewer (Anthropic provider via OpenRouter), 2026-10-25. Read-only; no commands, no edits, no corpus reads.

## What I read

- `AGENTS.md`; `scripts/train/14_run10_chat_box.sh`; `scripts/eval/47_base_heldout_loss.py`; `scripts/train/spectral_plugin.py`; `scripts/train/02_merge.py`; `scripts/data/89_run11_data.py` (held-out construction).
- `data/train/run11/manifest.json`.
- `slop/eval/run11/lease1/{replay_ctl,mix_const,mix_stoic}_log_scan.json`; `mix_stoic_nonmetric.log` (first 530 of 707 lines; rest is repeated kernel warnings by pattern).
- `lease1/box_runs/cfg_r10_x11_{replay_ctl,mix_stoic}.yml` (mix_const config not opened; stages.log shows same `cfg()` path), `expert_check_r10_x11_*.log` (all three), `stages.log`, `base_loss.jsonl` (1 row: base), `base_loss.log`.
- Raw/clean logs: `train_r10_x11_replay_ctl.clean.log` lines 15240–15470 and all `eval_loss` rows with one line of context; `train_r10_x11_mix_const.clean.log` `eval_loss` rows with context; two greps into `train_r10_x11_mix_stoic.log` (CR-joined; only partially extractable).

Not read: the parent's audit or conclusions, book text, training rows, `up_stoic`/`up_const` training logs.

## Verdict on "failed run" vs "limits on attribution"

Observed: all three trainings completed (stages.log 04:36→19:43 UTC), no non-finite values (`"nonfinite": []` in all three scans), grad norms 0.5–3.1 with clip at 1.0, learning rate peaked at 1e-4 and decayed to ~1e-10, 80/80 routed-expert `lora_B` tensors nonzero in every adapter, 330 LoRA modules under the spectral penalty, token totals ≈ 2 × 4.3M per run. Nothing here is a failed run. The findings below are about how the logs are being read and how the pending comparison is designed, i.e. limits on attribution.

## Finding 1 (concrete bug in interpretation): logged `eval_loss` includes the spectral penalty; corrected CE plateaued at epoch 1 and epoch 2 only shrank the adapters

Evidence (observed):

- `spectral_plugin.py` `compute_loss`: `loss = loss + lam[0] * pen` is applied unconditionally; only the λ-fixing branch checks `model.training`. HF `Trainer.prediction_step` calls `self.compute_loss(...)`, so evaluation goes through the wrapper.
- The eval passes appear in the logs as ~130 microbatch rows with constant σ and varying `ce_loss` immediately before each `eval_loss` row (replay_ctl clean log lines ~15250–15459, σ = 0.001715 throughout, then `eval_loss 2.161` at 15460).
- Arithmetic, `eval_loss − 50·σ`:

| run | epoch 0 (σ=0) | epoch 1 | epoch 2 |
|---|---|---|---|
| replay_ctl | 2.097 | 2.454 − 50·0.007609 = **2.074** | 2.161 − 50·0.001715 = **2.075** |
| mix_const | 2.130 | 2.524 − 50·0.01036 = **2.006** | 2.141 − 50·0.002758 = **2.003** |
| mix_stoic | 2.287 | 2.636 − 50·σ₁ (σ₁ not extracted; raw log is CR-joined; nearby rows show σ≈0.0074–0.0080 → ≈2.24–2.27) | 2.307 − 50·0.00197 = **2.209** |

The same validation documents give the same `ce_loss` at epoch 1 and 2 (e.g. mix_const last eval doc: 1.543 / 1.544 / 1.545 at epochs 0/1/2), which is consistent with the CE part being essentially flat across the second epoch for ctl and const.

Inference:

- Anyone reading `eval_loss` or `eval_ppl` from the scans will conclude "every adapter made validation loss worse than Base" (2.097→2.161, 2.13→2.141, 2.287→2.307). That is false; penalty-corrected in-distribution CE improved by ≈0.02 (ctl), ≈0.13 (const mix), ≈0.08 (stoic mix). These are 2 % splits of the training mixes (partly FineWeb), per-sample rather than token-weighted means, and not the held-out sets, so they are not a substitute for `47_base_heldout_loss.py`.
- σ_max-mean peaked at ≈0.017–0.019 within the first ~15 % of training and then fell monotonically to 0.0017–0.0028 at the end (scan `spectral_sigma_max_mean` max/last). For ctl and const, epoch 2 shrank the top singular value 4–6× with no measurable CE change. With constant λ = 50 and a scale-independent penalty gradient, the second epoch is mostly a shrink step. Consequence: the saved final adapters are much smaller in σ_max than the retained epoch-1 checkpoints (`checkpoint-793`, `-593`, mix_stoic mid checkpoint), so "dose 1 of final" and "dose 1 of checkpoint" are different magnitudes, and nominal dose matching with the older `up_stoic`/`up_const` adapters (different token counts / schedules; I did not read their logs) is not magnitude matching.

Cheapest discriminating checks:

1. No GPU: average the `ce_loss` of the eval microbatch rows preceding each `eval_loss` row and confirm it equals `eval_loss − 50·σ` to ~0.01. The scan tool already parses these rows. Extract σ at the mix_stoic epoch-1 eval the same way.
2. On the box, after the current BASELOSS queue finishes (do not interrupt it): append configs for the epoch-1 checkpoints, e.g. `mixc_ep1=outputs/r10_x11_mix_const/checkpoint-593:1`, `ctl_ep1=.../checkpoint-793:1`. `47` skips names already in `base_loss.jsonl`, so this costs only the new rows (~3–5 min each by the base row's 154 s). If checkpoint-593 at dose 1 beats final at dose 1 on `heldout_const` by more than final at dose 4 does, the shrink lost or re-shaped learned content and nominal doses are not comparable across adapters.

Not a training fix: this is a reporting/measurement issue; the delivered adapters are usable, and `47` measures them directly without the penalty.

## Finding 2 (design misconception): `anch*` cells are not "mix minus its replay component"

Evidence (observed):

- `stages.log` BASELOSS list: `anchs1=outputs/r10_x11_mix_stoic:1,outputs/r10_x11_replay_ctl:-1`, `anchc1=...mix_const:1,...replay_ctl:-1`, and −2/−4 at doses 2/4 (equal and opposite doses).
- `manifest.json docs_note`: `const_tokens 2,156,056 + const_replay 2,141,485` (≈50 % replay); `stoic_tokens 2,897,535 + stoic_replay 1,400,476` (≈33 % replay); `replay_ctl` is 100 % FineWeb at the same T. `89_run11_data.py` docstring confirms: "Ours uses one T for both mixes, so the ratios differ."
- `replay_ctl`'s corrected validation CE change on its own FineWeb split is ≈−0.02; its final σ_max-mean (0.0017) is comparable to the mixes' (0.0020–0.0028).

Inference:

- Δctl was trained from an independent random `lora_A` init on different text; LoRA updates from different runs are not additive components, so d·Δmix − d·Δctl does not isolate the Stoic/constitution content. It adds an update of similar magnitude in a largely unrelated direction, and at equal dose over-subtracts relative to replay share (should be ≈0.5·d for const, ≈0.33·d for stoic if additivity held at all).
- This is fine as a Praxis-style control *ablation* ("does subtracting a generic-text adapter change held-out loss?"), but the pending comparison must not be reported as "content-only" versus "mixed". It is a matched-dose comparison of two different interventions. Attribution of any difference to replay content is not supported.

Cheapest discriminating check: `ctl1` is already queued. Compare `NLL(anchX_d) − NLL(mixX_d)` with `NLL(base) − NLL(ctl_d)` on `heldout_web` and own-kind sets. If the anchor's shift is roughly the negative of ctl's own effect (approximate additivity), the subtraction is doing what the design intends; if the anchor shifts own-kind NLL by more than ctl alone moves anything, it is noise injection and the anch cells should be dropped from the matched-change plot. `ctl2`/`ctl4` would make this cleaner but are not queued; adding them is cheap after the queue.

## Finding 3 (measurement caveats in `47_base_heldout_loss.py` and the held-out sets)

Observed:

- `47` merges via `mg.merge_adapter(...)` only; the routed-expert probe assertion (`"routed experts unchanged"`) lives in `02_merge.main()` and is not executed on this path. `base_loss.log` also shows the PEFT warning `rank_pattern keys did not match any targeted module and were ignored: ['mlp\\.experts\\.down_proj', 'mlp\\.experts\\.gate_up_proj']` at load. Expert-check shapes (`lora_B [1024, 4096]`, `[2048, 4096]`; 256 experts × 16 = 4096) indicate rank 16 was applied for experts despite the warning, so I believe the warning is benign for rank; whether `alpha_pattern` (32) was applied cannot be inferred from shapes. If alpha fell back to 128 with r = 16 the expert scaling would be 8 instead of 2 for both training and merge consistently, so it would not invalidate comparisons, only the intended expert/attention balance.
- Held-out construction (`89_run11_data.py`): `heldout_stoic` = chunks of `data/stoic_corpus/chunks.jsonl` not in R10 `stoic.jsonl` (same books, unselected chunks); `heldout_const` = the 170 accepted "reasons-first" documents from `reasons_docs_overnight1`, a different generator batch/style from the trained const docs; `heldout_other` = other-tradition candidates not in `other.jsonl` (includes rejected candidates); `heldout_web` = FineWeb rows outside P. Both `up_stoic` (run 10) and `mix_stoic` trained on R10 `stoic.jsonl`, so `heldout_stoic` is unseen by both (fair in that respect).
- `47` truncates each held-out doc to 1024 tokens and takes the first 100 rows; const rows average ≈1,430 tokens, so most const docs are truncated (base row: 102,300 tokens / ≤100 docs).

Inference / caveats:

- A `heldout_stoic` loss drop partly measures same-book vocabulary and adjacent-passage familiarity, not only "learned the style and content". A `heldout_const` drop measures transfer to a related-but-different style; disjointness from R10 `const.jsonl` is asserted by the comment "never trained on" but not checked by id in the code (the trained const docs come from a different file). Neither invalidates comparisons across adapters on the same set, but they bound what "learned" means.
- Cheapest check: a one-line id/sha intersection between `heldout_const` and R10 `const.jsonl` texts, and between `heldout_stoic` ids and `stoic.jsonl` ids (the code already excludes by id for stoic). No GPU, no corpus reading beyond ids/hashes.

## Minor notes (not counted as findings)

- `trainer.log(...)` inside `compute_loss` fires during evaluation, which is why the scans count eval passes as "microbatch rows"; harmless, but `microbatch_rows` ≠ training microbatches.
- `ce_loss` minima of 0.06–0.15 on single training microbatches are single short documents, not evidence of memorisation on their own.
- `float(pen)` on a grad-requiring tensor emits a warning only; no effect.

## What remains unmeasured

- All new-adapter held-out losses: `base_loss.jsonl` has only the `base` row at the time of reading. No `mixs*`, `mixc*`, `ctl1`, `anch*`, or old-adapter rows yet.
- σ at the mix_stoic epoch-1 eval (raw log is CR-joined; the scan did not store it).
- Any behaviour: no document-adapter demos, coherence, maths, or Instruct grafts for the run-11 adapters; no chat stage.
- Whether old adapters' magnitude/schedule matches (I did not read `up_stoic`/`up_const` training logs), which Finding 1 makes relevant for any nominal-dose comparison.
- Expert `alpha_pattern` application (see Finding 3).

## Recommendation on reading the pending comparison

Judge document adapters by penalty-free held-out NLL from `47`, plotted against observed web drift (`heldout_web` ΔNLL) rather than nominal dose, including the epoch-1 checkpoints if the cheap check in Finding 1 is run. Report `anch*` as a control-subtraction ablation, not as isolating content. Do not cite training-log `eval_loss`/`eval_ppl` anywhere without subtracting 50·σ.