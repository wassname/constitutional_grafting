# Independent tiny-heal diagnosis

**Conclusion:** The first observed numerical failure is `grad_norm: nan`, before spectral calibration crashes. Separately, calibration assumes that one Trainer step implies a nonzero LoRA update; LR warmup makes that assumption unsafe even with finite gradients. Fix both before production. This run provides no negative evidence about healing.

## Evidence and event order

Read completely: repository `AGENTS.md`, `ml-debug/SKILL.md`, all six requested files, router plugin, inherited training config, both tiny examples, and the run mental model. No commands executed or files edited.

1. `slop/eval/run15_heal/lease/box_runs/cfg_tiny_heal_smoke.yml` selects:
   > `bf16: false`, `fp16: true`, `warmup_ratio: 0.1`, `max_steps: 3`

   Accumulation is four, but the dataset has only two examples.
2. `slop/eval/run15_heal/lease/box_runs/tiny_heal_train.log:294` confirms:
   > `HEAL FROZEN PARENT {"frozen": {"torch.float16": 16086232}, "trainable": {"torch.float32": 15360}}`

   FP32 adapter storage does **not** establish FP32 backward intermediates.
3. First completed Trainer boundary, log line 356:
   > `'loss': '12.45', 'grad_norm': 'nan', 'learning_rate': '0.0001'`

   Same record reports text/total loss 12.45, spectral penalty, sigma and lambda all zero. These sigma metrics summarize preceding forwards, not a post-update measurement.
4. The next forward reaches `scripts/train/spectral_plugin.py:74–77`:
   > `if step >= max(1, trainer.args.get_warmup_steps(trainer.state.max_steps)):`  
   > `lam[0] = float(frac) * ce / sig`

   Log lines 409–411 end with:
   > `ZeroDivisionError: float division by zero`

**Observed:** nonfinite gradient norm precedes division by zero. **Not observed:** whether the optimizer skipped, its actual pre-step LR, scaler state, individual gradients, or a changed adapter tensor.

## Mechanisms ranked separately

### Why `grad_norm` is NaN

1. **FP16 backward overflow / AMP interaction — leading hypothesis, not established.** Finite CE with nonfinite gradients fits overflow in scaled backward, particularly through fused kernels. The log enables FP16, fused LoRA, scattermoe, CCE and linear-attention kernels. The launcher's `mixed_precision='no'` warning does not prove Trainer AMP was disabled.
   - **Discriminator:** actual autocast dtype, scaler scale/found-inf/skip status, and first nonfinite gradient by module. Same seeded tiny workload with BF16 mixed precision should become finite if exponent range is decisive.
2. **Kernel-specific backward/dtype defect.** FP32 LoRA storage plus low-precision fused operations can expose a kernel path absent from the CPU regression.
   - **Discriminator:** if BF16 still fails, isolate the first failing operation with finite checks and a narrow unfused comparison, without changing the objective.
3. **Spectral backward precision interaction; lower-ranked but unexcluded.** `spectral_penalty()` uses `.float()`, but that alone does not disable enclosing autocast. At zero B the intended FP32 spectral gradient should be finite and zero; multiplying a bad backward contribution by zero is not a reliable numerical safeguard.
   - **Discriminator:** test the real spectral function at zero B, including gradients and actual intermediate dtypes, under the training autocast context.

Excessive learning rate is a weak explanation for the **first backward**, before evidence of any parameter update. Evaluation/parser faults cannot explain this traceback.

### Why sigma is zero

1. **Expected zero-B initialization plus potentially zero-LR first step.** Standard cosine warmup with one warmup step starts at LR zero. A first finite optimizer step can therefore leave B unchanged; the logged `0.0001` can be the scheduler's subsequent LR. The plugin nevertheless calibrates at `global_step == 1`.
   - **Uncertainty:** installed Trainer/scheduler source and pre-step LR were not supplied. Record them to disprove this mechanism.
2. **AMP skipped the first update after nonfinite gradients.** This independently explains persistent zero B.
   - **Discriminator:** scaler skip status and before/after B tensors.
3. **Disconnected updates or underestimated spectral norm.** Lower probability given 17 detected LoRA modules and retained random power vectors, but not excluded.
   - **Discriminator:** measure actual `B @ A` changes and compare tiny-model estimates with exact FP32 SVD.

Thus, fixing NaNs alone may still leave the calibration crash; guarding calibration alone may merely conceal failed optimization.

## Smallest principled repair

- Prefer **BF16 mixed-precision training**, explicitly recording the deviation from FP16 training. Preserve the original merged D artifact and **FP16 serving/evaluation**.
- Distinguish frozen-weight *storage* from compute dtype. `scripts/train/heal_plugin.py` currently asserts:
  > `frozen['torch.bfloat16'] == 0`

  Simply changing the config may violate this assertion because the loader converts weights. Verify whether FP16 frozen storage with BF16 autocast is supported by these kernels. If training uses a BF16 copy, explicitly identify the rounded training parent and keep the serving artifact unchanged; do not claim bitwise-identical training weights.
- Calibrate only after a **verified successful nonzero update**, with finite positive sigma and finite CE. Collect calibration statistics from valid post-update forwards rather than diluting them with zero-initialization history.
- Keep calibration pending explicitly, with a bounded failure condition if updates/sigma never appear. Reject nonfinite values. **No epsilon denominator, silent regularizer removal, or indefinite lambda-zero training.**
- Retain warmup in the regression: it is the discriminator for the calibration assumption. Three Trainer steps may be insufficient if steps are skipped; acceptance must require actual updates and a subsequent penalized backward/update.

## Required validation before full training

`tests/regression/test_heal_pipeline.py` currently runs FP32 direct PEFT/AdamW training:

> `loss = healed(**example).loss`  
> `optimizer.step()`

It does not exercise Axolotl AMP, scheduler, spectral plugin, fused GPU kernels or skipped steps. Its “any nonzero B gradient” assertion also does not prove every gradient is finite.

**CPU regression:** exercise the real spectral plugin with zero B, a zero-LR warmup step, then a genuine update. Verify pending calibration, finite gradients, changed B/BA, finite positive calibration, nonzero penalty, and an update with that penalty active. Test persistently zero sigma and nonfinite statistics as explicit failures.

**Replacement GPU tiny gate:** log, at each optimizer boundary:

- pre-step LR, attempted versus successful updates, AMP/autocast and scaler state;
- finite/nonfinite gradient counts and norms for dense, linear-attention and expert LoRA groups;
- before/after B and effective BA changes, with frozen-parent checks;
- post-update sigma, calibration state/sample count, lambda, CE and penalty separately;
- saved/reloaded adapter finiteness and nonzero effective update.

Require a real update **and** a subsequent spectral-regularized update before production—not merely process exit, checkpoint creation or finite loss.

## Compact ML-debug audit / residual risks

- Complete log read; first anomaly is the sole gradient-norm record. No earlier gradient history exists.
- Logged `SHOULD: total_loss = text_loss + spectral_penalty` holds numerically, but only with zero penalty.
- Both tiny examples were read: real thought/closer/EOS are labelled; replay's empty think block is unlabelled. Actual consumed token masks remain unverified here.
- Loss 12.45 is compatible with a random large-vocabulary model; exact uniform-null loss needs vocabulary size. It is not learning evidence.
- No init generation, held-out comparison, successful-update count, GPU reproduction or per-module numerical trace supplied.
- First boundary took about 112 seconds; peak allocated memory was 0.34 GiB. Kernel downloads/compilation confound throughput; this cannot project production cost.
- Prior CPU success cannot adjudicate GPU numerical mechanisms. Current fixes and their test outputs were not supplied.
- No delegation or reproduction performed, per task restrictions. Scientific outcome remains inconclusive.
-- reviewer-openai/Astra; preserved by PI/OpenAI (Sol)
