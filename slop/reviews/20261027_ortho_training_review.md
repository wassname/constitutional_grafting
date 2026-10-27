# Fresh-eyes review: training-time orthogonal projection

**Commit:** `e8a4dcfa1e124c0866784d640e6729568e97f08a`  
**Reviewer:** PI/Astra

**Verdict:** No blocking optimizer-order, parameter-copy, or expert-layout bugs found for the intended single-device, default-adapter configuration. One P2 mismatch remains with the requested *exact original tau subspace* contract. If the documented fp16 approximation is acceptable, no blocking bugs found; otherwise fix the basis precision before training.

## Ranked finding

### P2 — FP16 export changes the protected subspace; QR does not restore the original one

**Locations:** `scripts/train/16_project_chat_adapter.py:127-131`; `scripts/train/ortho_plugin.py:37-42`.

Every production basis is rounded to fp16. QR subsequently makes the rounded columns orthonormal, but preserves their **rounded span**, not the original SVD span of `W_Instruct − W_Base`. Thus the callback enforces the complement of a nearby subspace, not precisely the requested original top-64 subspace. Its residual logging uses the nearby basis and cannot reveal this difference. This is documented in the implementation report, but it is a real distinction from ordinary FP32 projection roundoff and from the task's stated invariant.

**Reproduction:** seed 64, two matrices with production gate/up dimensions 1024×2048, LoRA rank 16, protected rank 64. Calling the actual `project_factors`:

| Basis used for projection | `||U_originalᵀ Δ||F / ||Δ||F` | `||Δ V_original||F / ||Δ||F` |
|---|---:|---:|
| Original FP32 orthonormal columns | 1.00e-7 | 7.45e-8 |
| FP16 columns, converted to FP32 and QR'd | 5.15e-5 | 3.60e-5 |

The working-basis factor residuals remain similarly small in both cases. The regression's `3e-4` tolerance against the original SVD deliberately permits this discrepancy; it does not establish the exact-space claim.

**Concrete fix:** save the U/V columns in FP32 and retain FP32 projection; this doubles basis-file size to about 14.04 GiB but does not double the already-FP32 resident training bases. Alternatively explicitly accept a quantified approximate-subspace contract, and log normalized leakage against the original basis on a representative verification set. No finite-precision implementation is literally exact, but FP16 storage adds avoidable error orders of magnitude above the arithmetic baseline.

## Requested checks

1. **Optimizer boundaries and live parameters — correct in reviewed configuration.** `OrthoCallback.pairs` holds the actual `Parameter` objects, and `copy_` changes their storage in place; it does not replace them or leave the optimizer using stale parameters. Standard Trainer calls `on_step_end` after `optimizer.step`, scheduler handling, zeroing gradients and advancing the step, before log/save/eval. Accumulation microsteps instead call `on_substep_end`. Initialization and `on_train_begin` also project. The latter follows ordinary checkpoint restoration, so resumed factors are constrained before their first forward. An AMP-skipped optimizer boundary also triggers an extra projection, not a missed real update. BF16 training normally does not use the FP16 overflow scaler. Actual checkpoint-resume was **not exercised** by the new test; its step-zero call is train-begin, not a resume test.

2. **Expert layout, sides and key mapping — correct.** A is unpacked as `[expert, rank, input]`; B's PEFT rank-major/expert-minor storage is unpacked as `[expert, output, rank]`. Packing reverses those operations. U acts on B/output; V acts on A/input. The nested gate/up wrapper and outer down wrapper match the exporter and existing PEFT-layout regression. Exact key-set and per-side shape checks reject incomplete/mismatched basis coverage. The default-adapter/target-order assumptions are explicit, not a general multi-adapter implementation.

3. **Spectral interaction — no new defect found.** Spectral loss accesses the same live factors on each forward. Its cached right singular-vector estimate is an initial guess, not a cached delta; the next power iteration uses the projected A/B. After one nonzero iteration its right vector is in the row space of projected A, hence in the permitted input complement. Reinitializing it every step would unnecessarily discard the warm start. Calibration occurs on subsequent forwards using projected factors, rather than the pre-projection optimizer output. One-iteration estimates remain approximate, especially after abrupt updates; that is pre-existing spectral behavior. Existing spectral state/lambda are not checkpoint-persisted, so resume is not an exact replay of spectral calibration; that is also pre-existing, not introduced by this commit.

4. **CPU/GPU synchronization and dtype — correct, but not free.** Both `.to(cpu, float32)` and `copy_` use their blocking defaults; CPU computation cannot race an unfinished ordinary GPU optimizer update or transfer. CPU autocast is disabled, bases and factor calculations are FP32, and `copy_` casts back to the live parameter dtype. This intentionally serializes projection and GPU training. PEFT FP32 factors are the expected case; BF16-stored factors would have a larger rounding residual. The residual calculation accounts for that dtype conversion.

5. **Existing offline projection outputs — unchanged mathematics.** Adding basis export uses non-in-place conversions/subtractions and does not modify U/Vh, A/B, or projected output tensors. It still runs the same full SVD, not a rank-dependent randomized SVD. On the former valid production inputs, removing the 256/330 assertions and bounding diagnostic singular-value indices do not change projected factors. Removing the assertions weakens the exporter-only completeness guard, but the training callback still requires an exact basis/live-model key match. The exporter can now mark a smaller valid adapter complete relative to that adapter; production coverage should still be checked as the report instructs.

6. **What passing tests do not establish.** The new integration test is genuinely real Trainer/PEFT/Qwen execution, but uses CPU FP32, a reduced model and initially nonzero B. It does not run the paid image's Axolotl/ScatterMoE path, bitsandbytes optimizer, GPU transfers, or checkpoint resume. I inspected current upstream ScatterMoE fastpath source: it obtains wrapper factors on each forward and leaves wrapper/optimizer tracking intact, supporting the live-parameter analysis. That source is not proof of the exact installed rental image. Confirm installed versions and live parameter identities during the lease's initial steps.

## Runtime and scale

The adapter is approximately 3.723 GiB, so each projection incurs approximately **7.446 GiB aggregate bidirectional transfer**, plus host projection/packing and optional residual measurement. At an effective 12–25 GB/s, ideal transfer payload time alone is approximately **0.64–0.32 s**; pageable memory, many blocking copies, host staging and contention increase it. This is an estimate, not a measured GPU transfer result.

I independently timed the actual projection/packing and residual operations at 256 experts, k64/r16, with eight CPU threads (four timed iterations after warmup):

| Shape | Projection + packing median | Residual median |
|---|---:|---:|
| gate/up: 1024×2048 | 0.0663 s/stem | 0.0187 s/stem |
| down: 2048×512 | 0.1302 s/stem | 0.0171 s/stem |

For 40 of each expert stem, these timings imply **7.86 s projection + 1.43 s residuals = 9.29 s/step**, before dense stems, copying back into parameters, transfers and host contention. This benchmark used random basis tensors because orthogonality does not alter these operations' arithmetic cost; it is not a precision or training benchmark. The implementer's 6–10 s all-in estimate is plausible on a faster host but optimistic relative to this measurement. At 778 steps, this measurement alone extrapolates to **2.0 additional hours**, before the omitted costs. Time the first several real steps and use that measured rate for lease sizing; do not assume PCIe bandwidth is the dominant cost.

## Validation and evidence limits

- Read the complete three scoped files, commit diff, implementation report, spectral implementation, production SFT config and existing projection regressions.
- `OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 just check-projection`: **12 passed, 2 known PEFT pattern warnings, 18.91 s**. The reviewed three files are unchanged from the target commit; HEAD also includes later unrelated char/cap tests, explaining the count versus the implementation report's nine.
- Independent original-space precision probe: passed; quantified the FP16 span discrepancy above.
- Independent production-shape CPU timing: completed; results above.
- No source edits, GPU rental, paid API calls, or additional reviewers. Only this requested review artifact was written. No files were staged.

**PI/Astra**

```acceptance-report
{
  "criteriaSatisfied": [
    {"id": "criterion-1", "status": "satisfied", "evidence": "Reviewed the scoped commit, returned one ranked P2 contract finding with reproduction and fix, and documented all six requested checks and residual risks."}
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {"command": "git show e8a4dcfa; scoped git diff against HEAD", "result": "passed", "summary": "Reviewed commit; the three scoped files still match it."},
    {"command": "OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 just check-projection", "result": "passed", "summary": "12 passed, 2 known PEFT warnings, 18.91 seconds."},
    {"command": "Inline FP32 versus FP16-QR original-space leakage probe using actual project_factors", "result": "passed", "summary": "FP16-QR leakage 5.15e-5/3.60e-5 versus FP32 1.00e-7/7.45e-8."},
    {"command": "Inline eight-thread production-expert-shape projection and residual benchmark", "result": "passed", "summary": "Expert-only extrapolation 9.29 seconds per step before dense factors and transfers."}
  ],
  "validationOutput": ["No blocking optimizer-order, live-parameter or expert-layout defect found for the supported configuration."],
  "residualRisks": [
    "Exact original tau-space contract is not met by fp16 basis export; accept approximation explicitly or export FP32.",
    "Full-scale Axolotl/ScatterMoE/GPU/bitsandbytes and actual checkpoint resume were not executed.",
    "Runtime and memory on the paid host remain unmeasured; CPU timing suggests the upper end of the implementation estimate may be optimistic.",
    "Upstream source inspection is not verification of the exact rental-image versions."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only review of training-time orthogonal projection and SVD basis export; no source changes.",
  "reviewFindings": ["P2: scripts/train/16_project_chat_adapter.py:127-131 and scripts/train/ortho_plugin.py:37-42 — fp16 export plus QR constrains a nearby span rather than the original SVD span."],
  "manualNotes": "PI/Astra. Only the requested review artifact was written. The first broad context search timed out; subsequent searches were narrowed. Test runtime may create normal temporary test artifacts outside source files."
}
```
