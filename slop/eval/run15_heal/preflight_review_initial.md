## Verdict: hold launch pending two fixes

Reviewed all six scoped files, comparison scripts 02/38/48/54/56, configuration, applicable root `AGENTS.md`, and `ml-debug`. Files changed during review; findings below use the reread versions of 57/58.

### 1. P1 — Early-baseline deadline can abort a viable lease

**Evidence:** `scripts/eval/57_run15_heal.py:272–275` waits for the baseline but asserts:

> `time.time() < self.deadline - 4 * 3600`

The six-hour lease sets the runner deadline 45 minutes before destruction. Consequently, this assertion allows only **75 minutes from lease creation**, including provisioning, setup and baseline generation. `scripts/eval/58_run15_heal_rental.py` permits setup itself 5,400 seconds; comparison script `scripts/eval/38_run10_chat_rental.py:7` documents approximately 1.7 hours of setup.

**Affected input:** any lease whose baseline remains active after minute 75 when the main runner reaches this loop.

**Observed:** contradictory time allowances in code. **Inference:** substantial risk of aborting before training; no run15 GPU timing establishes actual frequency.

**Minimal fix:** derive the baseline deadline from measured remaining training/evaluation costs, rather than reserving four hours unconditionally. Reject an infeasible schedule before spending on baseline generation.

**Disproof check:** replay orchestration with a clock at creation +80 minutes and an active baseline; it should continue if the remaining measured workload fits.

### 2. P1 — Approved adapter fallback does not cover request-time rejection

**Evidence:** `scripts/eval/57_run15_heal.py:298–303` catches only startup `AssertionError`, additionally requiring a particular “LoRA … unsupported” log expression. The adapter request smoke occurs outside that fallback handler, at lines 319–325:

> `smoke = {tag: gen.chat(...) ...}`

`server()` readiness only checks `/v1/models`; registration is not proof that fused-expert adapter inference succeeds.

**Affected input:** a vLLM build that registers the adapter but rejects its parameter format/rank on first inference; startup incompatibility errors outside the regex are likewise excluded.

**Observed:** those failure paths terminate rather than execute the explicitly approved fp32-accumulation fallback. **Uncertainty:** I have not established that pinned vLLM 0.31 takes one of these paths.

**Minimal fix:** include actual adapter requests in the capability probe; classify and record genuine adapter incompatibility across startup and inference, while keeping OOM, transport and unrelated failures fatal.

**Disproof check:** test the pinned engine with the actual PEFT fused-expert checkpoint, or inject a request-time unsupported-adapter response and verify fallback executes.

### 3. P2 — Fallback schedules trace checkpoints before the mixed final

` scripts/eval/57_run15_heal.py:305` uses:

> `[('r15_D', None)] + list(adapters.items())`

Insertion order is trace final, trace checkpoints, mixed final, mixed checkpoints. Unlike native evaluation, merged evaluation can spend several model merges/reloads on early checkpoints before reaching the second primary comparison.

**Risk:** deadline exhaustion loses the mixed final despite prioritizing finals in the native branch. **Minimal fix:** evaluate D and both finals first in both branches. A simulated slow-merge schedule can verify the ordering independently of GPU performance.

## Evidence and residual uncertainty

- `slop/eval/run15_heal/cpu_smoke_v2.log` records two passing tests. This is useful **fp32 CPU** merge/train/reload evidence, not fp16 AMP validation.
- `tests/regression/test_heal_pipeline.py` uses a float32 parent and direct AdamW; it does not exercise Axolotl, spectral regularization, AMP or vLLM. The GPU tiny smoke removes `HealPlugin`; that plugin also only requires some trainable parameters, not the promised fp32 trainable dtype. Retain its precision checks in the smoke and assert trainable dtype explicitly.
- Data construction repairs EOS **before selection**, hash-pins historical replay, and checks supervised EOS and sequence boundaries. No concrete defect found there.
- Current rate 1.99 gives a nominal reserve of **$19.9569** using supplied preparation cost. Actual review/traffic charges remain unverified.
- Exact-ID ownership/destruction paths appear isolated from Box A; no network calls or edits were made.
- No supplied diff, final frozen source hashes, GPU execution log or completed plan was available. Recheck findings against the final snapshot.