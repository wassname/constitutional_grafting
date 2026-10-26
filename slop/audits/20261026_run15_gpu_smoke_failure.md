# Run15 first-lease GPU smoke failure

Target: guarded lease57812278, controller `proc_da6b`, worktree `/workspace/2026/constitutional_grafting/.local/worktrees/run15_heal`. The production-healing question remains unanswered. -- PI/OpenAI (Sol), 2026-10-26

| Stage | Expected | Observed | Expected? | Clue | Missing measurement | Consequence |
|:--|:--|:--|:--|:--|:--|:--|
| Data/masks | Approved nonempty thoughts and EOS; empty replay thought excluded |269traces; mixed132traces+331historical teacher targets; CPU mask checks pass | yes |`data/train/manifest.json`, `loss_mask_final.log` | Actual consumed GPU batch not retained | Data intent checked; runtime mask remains partly inferred |
| Instruct control | Complete native both-mode outputs |140rows/214turns each mode; no blanks; GSM56/60on,54/60off; ordinary22/22both | yes |`baseline_quality.json`, raw wire and receipt | Character judging not run yet | Valid control artifacts, not a healing result |
| Donors/D merge | Four pinned adapters, ordered FP16 merge |All4remote hashes passed; D merge receipt matches | yes |`controller.log`, `lease/box_runs/merge_D.json` | Full D behavioral evaluation not reached | Identity of merged artifact supported |
| GPU tiny backward | Finite gradients and a real adapter update |CE12.45, `grad_norm:nan`, sigma/penalty/lambda0 | no |`tiny_heal_train.log:356` | Pre-step LR, AMP scale/skip, per-module gradients, before/after tensors | First observed numerical failure; no update proof |
| Spectral calibration | Finite positive reference sigma after learning begins |Next forward divides by zero | no |`spectral_plugin.py:77` in executed source; traceback | Whether LR0 or a skipped step kept B zero | Calibration clock assumption is unsafe |
| Production trace/mix | Train/checkpoint/evaluate both |Not reached | no |`job.log:1910-1930` | All healed-model outputs and metrics | No positive or negative scientific result |
| Persistence/closure | Retrieve evidence, destroy exact instance |Logs and control outputs retrieved; provider absence confirmed | yes |`provider_closure_verified.json` | Provider itemized invoice | Estimated GPU$2.67347, not shared-account credit delta |
| Recovery | Explain defects before another paid run |27scoped CPU tests; independent GO; one replacement authorized | yes |`cpu_retry_final.log`, `cpu_retry_data_gates.log`, `preflight_retry_review_final.md` | New GPU behavior | Replacement tiny remains mandatory |

Paths in this table are relative to `slop/eval/run15_heal/` unless a code file is named.

## Provenance and complete-read coverage

Command: `/workspace/2026/constitutional_grafting/.venv/bin/python scripts/eval/58_run15_heal_rental.py run`, piped to `controller.log`. Process exited1 after5119seconds. The entire controller340lines, remote job1930lines and training423lines were read sequentially. The job's long plan dump was read, not substituted with its tail. Full two-row tiny input, resolved tiny config, native parser examples, baseline fixed panel and selected complete native thoughts/finals were read. Baseline selection/coverage is recorded in `baseline_read_coverage.json`; it precedes any heal result.

Executed source is pinned in `lease/executed_source_sha256.json`: runner57 `993002d8c17e48b35f7fdf615dc3e35efa9f4c4fb6f9507fcdffcec24fe882a7`, spectral plugin `1be42dea99b93d379fbfc1ceab3e948c8c93b648f5e1d60a76fd7e670c3318a7`. These identify execution more reliably than the current branch, which now contains fixes. Image tag: `axolotlai/axolotl:main-20261009-py3.12-cu130-2.14.1`; runtime reports Torch2.14.1+cu130; serving vLLM0.31.0. Exact Axolotl commit/image digest and complete installed dependency freeze were not captured, limiting exact reproduction of the fused-kernel failure. Instruct revision `59d61f3ce65a6d9863b86d2e96597125219dc754` and all donor/input hashes are recorded.

The tiny model's training seed was15, but its random base was constructed before an explicit seed was set. Its exact initialization seed/weights were not retained. Therefore same-seed reproduction of the NaN is unavailable; do not describe the GPU numerical cause as localized. The corrected tiny explicitly seeds construction. Pure warmup arithmetic was reproduced on CPU with seeds15and16.

## What happened, in order

The intended scientific discriminator, from `.pi/goals/ad3e95-v12.md`, was:

> with thinking on, few blank finals and visible-final character clearly above Instruct-on, maths kept; with thinking off, character unchanged from D.

The approved recipe first makes D from ordered FP16 additions to Instruct, then trains a small removable LoRA on that frozen recipient. Historical teacher targets replace new D-generated replay by explicit approval. The variants match assistant-token totals, not neutral exposure, sequence tokens or optimizer-step counts. EOS is also repaired. Those distinctions affect later attribution even if optimization succeeds.

The native Instruct control completed. `baseline_quality.json` records:

```json
"on": {"wire_verified_rows": 140, "math_correct": 56, "math_completed": 56, "ordinary_correct": 22.0}
"off": {"wire_verified_rows": 140, "math_correct": 54, "math_completed": 54, "ordinary_correct": 22.0}
```

These are selected fields, not a claim that all outputs were flawless: on-mode had1loop/1cutoff, off-mode1language-switch/5cutoffs, and neither mode had blanks. Counts come from214turns per mode. Fixed full replies and preselected payday/fridge/email examples were read; `results.md` holds the observations. No healed-model comparison exists yet.

Controller chronology:

> REMOTE ADAPTER VERIFIED stoic
> REMOTE ADAPTER VERIFIED const
> REMOTE ADAPTER VERIFIED other
> REMOTE ADAPTER VERIFIED rewr

Then `job.log` reports:

> EARLY BASELINE ACCEPTED: same plan/executor and hashed complete both-mode outputs
> D PARENT MERGED: pinned Instruct, ordered fp16 docs+rewr updates, frozen for both heals

The tiny uses the real Qwen-MoE loader, Axolotl, routed/dense LoRA targets, fused kernels and spectral plugin, reduced to two layers. It is a runtime check, not a learning benchmark. The actual trace input, from `lease/box_runs/tiny_smoke.jsonl`, is:

```json
{"id":"trace","segments":[{"text":"<|im_start|>user\nWhat is 2+2?<|im_end|>\n<|im_start|>assistant\n","label":false},{"text":"<think>\nTwo and two are four.\n</think>\n\n4.<|im_end|>","label":true}]}
```

The replay uses the same user question and an unlabelled native empty-think prefix, then labelled `4.<|im_end|>`. This is a smoke fixture, not a D answer. No tiny generated output was saved. Actual GPU token-label arrays were not saved; CPU tokenization tests check the boundary intent.

The runtime confirms storage before training:

> HEAL FROZEN PARENT {"frozen": {"torch.float16": 16086232}, "trainable": {"torch.float32": 15360}}

The first Trainer boundary is the first numeric anomaly:

> {'loss': '12.45', 'grad_norm': 'nan', 'learning_rate': '0.0001', 'train_text_loss': '12.45', 'train_spectral_penalty': '0', 'train_total_loss': '12.45', 'train_spectral_sigma_max_mean': '0', 'train_spectral_lam': '0', 'ppl': '2.554e+05', 'memory/max_active (GiB)': '0.34', 'memory/max_allocated (GiB)': '0.34', 'memory/device_reserved (GiB)': '0.36', 'tokens/trainable': 17, 'tokens/total': 128, 'epoch': '1'}

Source: `lease/box_runs/tiny_heal_train.log:356`. For vocabulary248320, uniform next-token NLL is ln248320=12.42247 and uniform token accuracy1/248320≈0.000004. Thus finite random-model CE is unsurprising; it says nothing about gradient finiteness or scientific healing. The logged sigma summarizes earlier forwards, not a post-update measurement. Logged LR can be the scheduler's next LR, not the LR used by the preceding optimizer step.

The next forward crashes:

```text
File "/workspace/cg/scripts/train/spectral_plugin.py", line 77, in compute_loss
    lam[0] = float(frac) * ce / sig
ZeroDivisionError: float division by zero
```

No `START TRAIN trace` or `START TRAIN mix` follows. The controller retrieved evidence and reports:

> RENTAL DESTROYED 57812278

Provider closure JSON contains `"absent_confirmed": true`, `"elapsed_hours":1.4209403719504674`, `"estimated_gpu_usd":2.6734729968618467`. The larger account-credit decrease includes other resources and is explicitly not reconciled to this job's invoice.

## Ranked, nonexclusive explanations

### H1: calibration assumes Trainer steps imply nonzero weights (bug, Almost Certain,95%)

Mechanism: LoRA B starts zero. With one warmup step, the first optimizer LR can be zero, leaving B and sigma zero even with healthy finite gradients. Executed code calibrates at `step >= max(1, warmup_steps)` then computes `float(frac)*ce/sig` without checking for a learned nonzero update.

Evidence: the executed traceback quotes that exact division; the tiny config has `max_steps:3`, `warmup_ratio:0.1`. CPU warmup tests with two seeds leave calibration pending after zero-LR and make it finite after a genuine update.

Contrary evidence: original pre-step LR was not captured; AMP skipping is another explanation for persistent zero B. Thus this establishes a real unsafe assumption, not which mechanism alone caused the original zero.

Discriminator/action: record pre-step LR, actual tensor changes and positive sigma. Calibrate on finite positive-sigma forwards only, and fail at training end if calibration never becomes available. This is implemented. Interpretability: engineering mechanism partial; scientific efficacy no.

### H2: FP16 backward/AMP overflow (bug, Likely,65%)

Mechanism: FP32 adapter storage does not force FP32 intermediate/backward operations. Finite forward loss can coexist with FP16 backward overflow and skipped or corrupt updates.

Evidence: `"torch.float16":16086232` frozen parameters and the sole `"grad_norm":"nan"` record precede calibration failure in `tiny_heal_train.log:294,356`.

Contrary evidence: scaler state, actual autocast context, per-module gradients and before/after weights are missing. The launcher's `mixed_precision='no'` warning does not establish Trainer AMP behavior. A kernel-specific defect also fits.

Discriminator/action: explicit BF16 training copy, finite-gradient checks, optimizer skip/scale, actual-change snapshots and saved-tensor finiteness in the new GPU tiny. BF16 success would validate the new combination, not isolate overflow causally, since spectral math also changed. Interpretability: partial diagnosis; scientific efficacy no.

### H3: fused-kernel or spectral autocast precision path (bug, Unlikely,35%)

Mechanism: an operation may execute in lower precision despite `.float()` operands; alternatively a fused backward kernel may fail only on reduced geometry. Original CPU eager tests cannot test those GPU paths.

Evidence: original spectral source casts operands to float but does not disable enclosing autocast; the GPU log enables fused LoRA, scattermoe, CCE and linear-attention kernels. PyTorch2.14 documentation says: “`autocast(enabled=False)` subregions can be nested in autocast-enabled regions,” giving explicit control of dtype. Source: https://docs.pytorch.org/docs/2.14/amp.html , retrieved through Context7.

Contrary evidence: original logged sigma is finite zero, not NaN; therefore spectral forward poisoning was not observed. BF16 donor training elsewhere worked, but this exact tiny geometry and optimizer branch were untested.

Discriminator/action: FP32 spectral operations outside autocast; CPU FP16/BF16-autocast zero-B backward tests; inspect new GPU gradients/state classes. If BF16 still fails, localize the first nonfinite operation and use a narrow unfused comparison before changing the objective. Interpretability: partial engineering risk; no efficacy inference.

### H4: acceptance metric mistakes attempts for learned updates (measurement, Almost Certain,99% for the intermediate code)

Mechanism: after the first repair, an unskipped positive-LR counter could advance even for a no-op optimizer; a later bad dense tensor could escape an expert-B-only saved check. This was a follow-up review finding, not the original crash's cause.

Evidence: `preflight_retry_review_v1.md` quotes `if not skipped and self.pre_lr > 0:` followed by update-counter increments. Original validator checked only expert B norms; infinity passes a bare positive-norm check.

Contrary evidence: no such no-op/corruption was observed in production; it is an acceptance gap demonstrated by adversarial unit cases.

Discriminator/action: real callback snapshots every tiny trainable tensor, requires a genuine later regularized change, and rejects post-calibration no-op/final-step corruption. Real saved-adapter CLI checks every dense/expert tensor. CPU callback/CLI regression cases pass; GPU integration remains pending. Interpretability: credible code defect, not a scientific result.

### H5: downstream evaluation or causal shortcut (harness/data, Remote5% for an unnoticed harness defect; known design confound)

Mechanism: scoring hidden thoughts instead of visible finals could make an unrepaired model look healed; teacher replay or EOS supervision could explain a later improvement without trace-specific learning.

Evidence: original goal explicitly requires visible-final character; current recorder saves native raw requests/responses and separately records reasoning/final channels. Data manifest says replay is historical teacher targets, not D outputs. `replay_eval_overlap.json` finds no exact normalized overlap with frozen70, but one identity-prompt substring; semantic novelty is not proved.

Contrary evidence: native parser normal/budget/cutoff cases and complete first-baseline wire checks pass. Evaluation cannot explain the training traceback.

Discriminator/action: score final-only projections, retain empty/cutoff cases, compare against same D off/on and reused Instruct, read actual tool actions, label fixed identity demonstrations near-training. Do not attribute a mixed-vs-trace difference solely to rehearsal; neutral exposure/EOS differ. Interpretability: current engineering failure unaffected; future efficacy conditional on these checks.

Unknown numerical mechanisms remain plausible; the listed probabilities are rough nonexclusive judgments, not fitted posteriors.

## Required ML-debug form

| Check | Evidence / limit |
|:--|:--|
| Complete log/config |340controller+1930job+423training lines read; FP16, rank8, alpha16,3steps, warmup.1, spectral fraction.01 |
| SHOULD versus observed | Mask intent supported by CPU tests. Frozen storage confirmed; live freeze equality only CPU-tested. `total=text+penalty` holds12.45=12.45+0, without a trained regularizer |
| Null scale | Uniform NLL12.42247 from vocabulary248320; observed random CE12.45. No meaningful random open-ended GSM answer accuracy claimed |
| Init demo | No generated tiny demo retained; no pre-update loss separated from first logged training aggregate |
| Dummy/control | Zero-initialized LoRA and zero-LR CPU cases expose the calibration assumption; no scientific null comparison reached |
| Baseline/held-out | Instruct control complete; D/heals not evaluated in first lease |
| LR onset/stop | Only post-boundary LR.0001 logged; actual pre-step LR and successful-update onset unknown |
| Full sample | Full trace/replay fixtures read above; actual GPU consumed masks unavailable |
| Worst step | Sole gradient normNaN; CE12.45, penalty0, sigma0, lambda0; no per-module norm localization |
| Surprise | Finite CE with NaN gradient: chasing numerical cause. Zero sigma at first warmup boundary: arithmetic reproduced; original LR/skip contribution unresolved |
| Missing trust evidence | Actual updates, AMP/kernel state, saved-tensor finiteness, production comparisons and raw consumed GPU batch |
| Alternative diagnoses | H1-H5 above; hidden-final scoring cannot cause this traceback; teacher-target/EOS confounds matter downstream |
| Independent view | Fresh-context Astra reviewer: “The first observed numerical failure is `grad_norm: nan`, before spectral calibration crashes.” It also saw the owner's BF16/positive-sigma suggestion, so this was not fully diagnosis-blind or cross-family. Full diagnosis `smoke_failure_review.md`; it found the separate actual-update acceptance gap |
| Cheapest discriminator | CPU zero-LR/real-update/regularized-update and adversarial no-op/corruption; then real BF16 GPU tiny with actual snapshots |
| Runtime/memory | First tiny boundary112seconds including compilation/download effects; allocated.34GiB/reserved.36GiB. Not usable for full-model projection;20step benchmark still needed |

## Decision

1. Resolve condition: **not met**. The quoted thinking-mode/retained-character discriminator cannot be judged without any production heal or healed outputs.
2. Predictions: correct masks are CPU-supported; finite GPU optimization contradicted; token-boundary repair, preserved off-character, retained maths and mixed benefit unresolved. Budget closure/first-instance destruction supported.
3. Earliest unsupported link: native GPU optimizer makes finite actual LoRA changes. New tiny snapshots plus a subsequent regularized change are the immediate test. A completed process/checkpoint alone is insufficient.
4. Validity: scientific classification **inconclusive**. Define an invalid headline as claiming healing success/failure from this first lease; that inference would be unsupported with >99% confidence because production training never ran. The observed engineering failure itself is credible.
5. Highest-information clues: NaN gradient precedes the exception; zero-B plus zero-LR can independently keep sigma zero; no production adapter/output exists. These prevent conflating a calibration repair with a scientific negative result.
6. Missing evidence, ranked: new GPU actual/regularized updates and finite states; full-model memory/throughput; complete final-only both-mode character/maths; exact failed initialization/dependency state. The last item limits causal diagnosis but need not block a validated new recipe.
7. Code changes: FP32 spectral context and positive-sigma calibration; explicit BF16 training parent; actual-update callback/saved-tensor checks; bounded timing/trace-only path. Source commitc19a804a, final preflight GO and27scoped CPU tests.
8. Reinterpretation: finite CE is not healthy training; a Trainer step is not necessarily an update; CPU eager success is not GPU fused success; teacher rehearsal is not D self-replay.
9. What changes the verdict: new GPU tiny establishes runtime viability, not scientific success. Complete same-D versus healed visible replies, held-out score intervals, off-character retention and capability checks can establish the scientific outcome.
10. Next sequence: one already-authorized replacement inside original$20; restricted owner relay and pinned hashes; mandatory GPU tiny;20step timing; trace first and mixed only if it fits; retrieve checkpoints while evaluating; judge/read final-only outputs. Keep the joint numerical changes explicit. Do not buy a precision ablation merely to isolate the old NaN before answering the user's repair question.
