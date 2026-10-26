## Launch verdict: GO for the single guarded lease

The reviewed fixes resolve my previous P1/P2 findings. No remaining launch-blocking P1/P2 found in this focused re-check. Production training remains conditional on the GPU tiny smoke and 20-step budget gate passing.

### Verified fixes

- **Baseline timing:** `scripts/eval/57_run15_heal.py:81–82,287` now requires `deadline - now > 3 * 3600 + 1200`. On this lease that permits waiting until minute **115**, rather than 75; minute 80 passes.
- **Native-adapter fallback:** lines **311–325** include actual `gen.chat` requests inside the capability probe, preserve HTTP error details, and stop the native server before classified fallback. Explicit OOM/disk/transport messages are excluded by `adapter_incompatible`.
- **Evaluation priority:** lines **91–92,328** use D → both finals → early checkpoints.
- **Precision:** tiny configuration retains `HealPlugin`; `scripts/train/heal_plugin.py:57` asserts:
  > `trainable['torch.float32'] == sum(trainable.values())`
- **Telemetry:** the plugin records consumed sequence/supervised tokens, peak allocated/reserved GPU memory, and the existing 1.5× remaining-step projection.
- **Retrieval:** `scripts/eval/58_run15_heal_rental.py:37–44` checks remote checkpoint adapter-file hashes against downloaded files, supplementing final-adapter verification.
- **Baseline identity:** `scripts/eval/57_run15_heal.py:156` supplies `r15_instruct` as `base_model`.

### Test evidence

Read `slop/eval/run15_heal/cpu_smoke_final.log`:

> `Ran 3 tests in 16.921s`  
> `OK`

This verifies the recorded CPU run, not GPU AMP or serving compatibility. The new regressions exercise the timing predicate, error classifier and ordering helper—not the complete exception-handling lifecycle.

### Residual risks

- **Minor cleanup gap:** a non-HTTP transport error during the native request smoke bypasses the server cleanup paths (`57_run15_heal.py:313–320`). It remains fatal as intended, but leaves vLLM running until rental teardown. Prefer unconditional cleanup on unsuccessful capability probing; inject `URLError` to verify termination.
- Actual setup/training/fallback-evaluation duration remains unmeasured. The minute-115 boundary and three-hour evaluation reserve are guards, not proof the full workload fits.
- Separate on/off judge directories were asserted in the follow-up, not independently verified here.
- Freeze the reviewed source hashes before launch; no shell, network, edits or test execution performed by this reviewer.