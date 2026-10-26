# Replacement-lease preflight: NO-GO pending one numerical-gate fix

**The original zero-init/warmup defect is repaired plausibly. The remaining blocker is that the promised “actual regularized update” gate counts optimizer attempts, not parameter changes.** No new GPU failure is established.

Read all requested source files, tests, CPU logs and the complete retry plan. Also inspected expert-adapter verification, inherited rental monitoring/retrieval, setup and deadline enforcement. No commands, edits, network access or delegation.

## Launch-blocking acceptance gap

### Successful/regularized-update counters do not establish actual updates

`scripts/train/heal_plugin.py:33–38`:

> `if not skipped and self.pre_lr > 0:`  
> `self.trainer._heal_successful_updates += 1`  
> `if self.pre_lambda > 0:`  
> `self.trainer._heal_regularized_updates += 1`

The final assertions at lines 76–77 check these counters. The logged `lora_B_fro_sum_after_step` is neither compared against its pre-step value nor asserted finite.

**Affected inputs:** a finite zero-gradient/no-op optimizer step after an initial successful update, or an optimizer that corrupts parameters on the final step. These are discriminator cases, not observed outcomes.

The subsequent `scripts/train/41_expert_adapter_check.py:19–23` verifies only expert B norms:

> `n_nonzero = sum(v["norm"] > 0 for v in report.values())`

Existing nonzero B proves an earlier change from zero initialization, **not a subsequent regularized change**. Positive infinity also passes `norm > 0`; dense adapters are not checked.

**Smallest repair:** for the tiny gate, compare finite trainable tensors before/after optimizer steps and require a genuine change on a step whose backward included a positive finite spectral penalty. Check every saved adapter tensor for finiteness. Keep optimizer-attempt counters, but name them accordingly.

**Disproof/acceptance test:** a callback-level CPU test must reject an unskipped, positive-LR no-op after calibration and reject final-step parameter corruption; a real update followed by a regularized update must pass. Current supplied tests do not exercise these callback assertions.

## Changes that pass static review

- **Zero initialization / autocast:** `scripts/train/spectral_math.py:18` explicitly disables autocast; spectral operands are FP32. Calibration selects `sigma > 0` observations, rejects nonfinite/negative input statistics, and leaves all-zero histories pending. No epsilon was added to the calibration denominator.
- **Warmup:** `spectral_plugin.py` waits beyond the warmup threshold and then for positive sigma; it no longer equates the first Trainer boundary with a nonzero update. End-of-training calibration assertion prevents silently completing with lambda zero.
- **Precision:** runner config selects BF16 training and FP16 disabled. `HealPlugin` requires predominantly BF16 frozen storage and FP32 trainables. Serving remains explicitly FP16; training-on-`D_bf16`, serving-on-`D_fp16` is recorded.
- **Callback lifecycle:** standard fresh-run ordering supplies `pre_lr`, `pre_lambda` and gradient count before `on_step_end`. Timing starts at global step 2 and measures through step 20. No definite lifecycle crash found; installed remote Trainer dispatch remains untested.
- **Five-step tiny:** configured at `57_run15_heal.py:61`; finite-gradient assertions and calibration checks run before production. Strengthen the actual-update gate above.
- **Trace-only path:** `train()` skips mixed when its projection exceeds remaining reserve, writes dynamic required adapters/comparison models, and builds evaluations from `trained`. `59_run15_heal_results.py:186` loads that dynamic model list for CLI analysis. No unconditional mixed-file requirement found in that path.
- **Provenance:** baseline reuse verifies source receipt, original plan, frozen manifest, generator hash, server argv, output hashes and vLLM 0.31.0. Training data and all four remote donor files are SHA-checked before consumption. The reviewed retry controller does not consume local donor weight bytes.
- **Budget:** retry plan records **$19.950341391861848**, consistent with the supplied reserves. Offer checks use 400-GB allocation and enforce the cap before creation. Exact-ID destruction deadline is independently armed; retrieval failure stops the instance while retaining the existing destruction deadline.

## Supplied validation evidence

- `slop/eval/run15_heal/cpu_retry_core.log`: **“Ran 6 tests … OK.”**
- `slop/eval/run15_heal/cpu_retry_data_gates.log`: **“Ran 17 tests … OK.”**

These support spectral zero-init/autocast math, warmup simulation, data gates, and FP32 Qwen-MoE merge/train/reload. They do **not** validate Axolotl callback integration, GPU fused kernels, BF16 training or the optimizer-update gate. The CPU log explicitly reports fallback from unavailable fast kernels.

## Nonblocking residual risks / corrections

- BF16 kernels, optimizer behavior, full-model memory and throughput remain GPU uncertainties; require the repaired real tiny gate before production.
- Baseline reuse preserves provenance, not hardware-equivalent numerical execution. Report Instruct as **reused from the first lease**, rather than “fresh” as currently written in `59_run15_heal_results.py:136` and the retry-plan evaluation description.
- Controller permits **two** explicit repair windows, each up to 20 minutes (`58_run15_heal_rental.py:220–229`), not one cumulative 20-minute window. Hard deadline remains unchanged. Tighten if “bounded20min” meant total repair time.
- Repair receipts assert that patched hashes exist but do not themselves verify remote patched bytes. Operator repair procedure must preserve/verify those hashes and remove stale job-exit state before resuming.
- Calibration input checks are good; explicitly checking the resulting lambda is finite would further harden extreme-small-sigma cases.
- Receiver SHA checks are visible; source-owner read-only transport, source before/after SHA and atomic-install receipts were not supplied for this review.

**Decision:** fix and test the numerical acceptance gate, refresh the hashed preflight approval, then proceed only with the authorized replacement’s GPU tiny—not directly to production.
-- reviewer-openai/Astra; preserved by PI/OpenAI (Sol)
