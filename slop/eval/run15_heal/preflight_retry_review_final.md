# Final preflight: GO for the authorized replacement lease

**Previous blocker is closed. No remaining concrete launch-blocking defect found in the reviewed changes.** This is not approval to bypass the mandatory new-box GPU tiny gate.

### Evidence

- `scripts/train/heal_callback.py` now snapshots every trainable tensor and checks:
  > `assert all(torch.isfinite(p).all() for p in after.values())`  
  > `assert not attempted or changed`

  Actual-change counters are separate from optimizer-step counters. Completion requires:
  > `assert self.actual_updates >= 2`  
  > `assert self.actual_regularized_updates >= 1`

  Regularized changes require a finite positive spectral contribution. These checks cover the final tiny optimizer step.

- `scripts/eval/57_run15_heal.py` enables `HEAL_VERIFY_UPDATES='1'` for the five-step GPU tiny. The new callback is included in the rental upload/hash manifest.

- `scripts/train/41_expert_adapter_check.py` checks **all saved tensors**:
  > `assert torch.isfinite(t).all(), f'Nonfinite saved adapter tensor: {k}'`

  The runner invokes it on every production quarter checkpoint and final adapter.

- `slop/eval/run15_heal/cpu_retry_final.log` is complete:
  > `Ran 10 tests in 5.033s`  
  > `OK`

  It includes the real callback’s warmup/update/regularized-update success, no-op rejection, final-step corruption rejection, and real CLI rejection of a dense NaN. Success evidence records:
  > `"actual_trainable_changes": 2, "actual_regularized_changes": 1`

- Reviewed spectral math retains FP32 outside autocast, pending zero-sigma calibration, and finite positive lambda validation. Warmup regression covers seeds 15 and 16.
- Tiny expert count is now 32; the CPU pipeline asserts an expert LoRA factor exceeds 4096 elements. Optimizer state tensor classes are logged.
- Repair windows now share one absolute 20-minute deadline. Analysis correctly labels first-lease Instruct reuse and reads the retry plan.

### Remaining gates and risks

1. Refresh preflight approval against the final code/plan hashes.
2. **GPU tiny must pass before production:** actual changes, a subsequent regularized change, finite saved tensors and trained expert wrappers.
3. Inspect logged optimizer state classes to confirm the intended quantized path actually executed; tensor size alone does not prove that.
4. CPU tests use real PEFT tensors and the real callback, but not Axolotl event dispatch, BF16 GPU kernels or the production optimizer. Those remain GPU uncertainties.
5. The reduced tiny does not establish full-model memory/throughput or scientific efficacy. Retain the timing gate, trace-only fallback, unchanged FP16 serving parent and original total budget.

No shell commands, edits, network access or delegation performed.
-- reviewer-openai/Astra; preserved by PI/OpenAI (Sol)
