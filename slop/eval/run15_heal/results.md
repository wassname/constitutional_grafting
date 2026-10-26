# Run15: can a small heal restore thinking mode without losing character?

Both repair adapters are trained; scientific evaluation is running. -- PI/OpenAI (Sol), 2026-10-26

The first lease stopped at the real GPU smoke: finite text loss, a nonfinite gradient, then a zero denominator in spectral calibration. No production heal trained. The instance was retrieved and destroyed (`provider_closure_verified.json`). This does not answer whether healing preserves character.

The repaired pipeline passed 28 scoped CPU tests, independent review and the real GPU tiny with actual-update checks. Both repair adapters completed training; both final adapters and all eight quarter checkpoints are retrieved and SHA-verified. Native serving accepts them. The approved replacement 57831547 is evaluating both modes. Character retention and capability gains are not established yet. Box A was accessed only by its owner for the read-only transfer.

Fresh unhealed D reproduces the channel failure: 183/214 thinking-on finals are blank, all ending during reasoning; none are blank thinking-off. Ordinary checks are 20/22 in both modes. Maths completed-correct is 54/60 on and 56/60 off, versus Instruct's 56/60 on and 54/60 off. The main measured damage is the character-response channel, not a large maths loss (`baseline_D_quality.json`). Character judging is pending.

## What is being compared

θ_B is Qwen3.5-35B-A3B Base; θ_I is its pinned Instruct sibling.

- Δ_docs = ½·Δtxt_stoic + Δtxt_const + Δtxt_other, document adapters trained separately on Base.
- Δsft_rewr|docs was trained on Base+Δ_docs.
- **D = θ_I + Δ_docs + Δsft_rewr|docs**, historical id `r10_stoic0.5_const1_other1_cx_chatr121`.
- `r15_D` is a fresh ordered-fp16 merge of that same recipe.
- `r15_heal_trace` = θ_D_fp16 + Δheal_trace|D_bf16; traces-only repair.
- `r15_heal_mix` = θ_D_fp16 + Δheal_mix|D_bf16; mixed trace/teacher-target repair.

Both heal adapters train on a frozen BF16-rounded copy of D; evaluation adds them to the original FP16 D. This is an explicit numerical training/serving difference. Instruct controls are reused from the first lease after input/generator/FP16-server/vLLM0.31.0/output-hash checks; they are not regenerated on replacement hardware.

These repairs are not new Base-trained character donors or graft-only evidence. Rank8/alpha16, LR1e-4, spectral fraction0.01, one epoch; quarter checkpoints retained. Full final-model evaluations in both modes use the run13 native recorder, pinned70×2 character/ordinary items, GSM60 and fixed temperature-zero panel. Early checkpoints get the fixed panel plus preselected payday/fridge/email reads, not full character scores.

## Data and deliberate differences

Full reads released269traces. Traces-only has320,279 supervised assistant tokens. Mixed has132traces+331replay rows,320,306 supervised tokens; it trades half the neutral-trace exposure for replay and uses more optimizer updates/sequence tokens. These are token-budget-matched pilots, not an isolated causal replay test.

Approved deviation: replay comes from D's approved historical **training teacher targets**, not newly sampled D answers. Answer text is unchanged. Before seeded subset selection, EOS is appended to903/1,636 historical rows where missing. D itself was trained without EOS on most character targets, so a repair may partly be learning to end the turn, not recovering reasoning alone. Original targets and release hashes remain in `data/trace_release.json` and `data/train/manifest.json`.

## Checks so far

- Real CPU Qwen-MoE merge/train/reload/parity, spectral autocast/warmup and actual callback update checks: 11 tests pass (`cpu_trained_pipeline.log`). A no-op after calibration and final-step corruption are rejected; all saved dense/expert tensors are checked finite.
- Data and read-gate tests: 17 pass (`cpu_trained_data_gates.log`). Masks exclude empty thoughts and include EOS (`loss_mask_final.log`).
- Independent Astra preflight: GO (`preflight_retry_review_final.md`). Numerical GPU proof comes from the real smoke below, not CPU tests.
- Real GPU tiny passed5steps; bystep4 it proved4actual tensor changes and3regularized changes, with34finite gradient tensors and trained/finite saved experts (`lease_retry/box_runs/tiny_heal_numeric.jsonl`).
- Full-model timing passed: 11.1 seconds/step trace and 12.3 mixed, excluding the first two. Both fitted the reserved budget. Trace trained 68 steps on 320,279 labelled tokens; mixed trained 116 on 320,306. Full logs read. Both have 80/80 nonzero expert banks; all saved tensors are finite (`lease_retry/box_runs/{timing,experts}_{trace,mix}.*`). Mixed has finite clipped gradient spikes, not a nonfinite failure.
- Native smoke passed for all nine base/final/early models, each returning `4.` and stop on the same arithmetic prompt. This is not complete native-versus-merged numerical parity or evidence of character retention. Healed-model scoring and full-panel reads are pending.

Replacement guard destroys exact57831547 by05:03:19AWST27October; runner ends45minutes earlier. Current all-in reserve $19.95035 includes the first failed lease within the original$20cap. No further lease is approved.

Evidence: `controller_retry.log`, `lease_retry/lease.json`, `lease_retry/deadline_guard_armed.json`, `retry_plan.json`, `preflight_retry_approved.json`, `MENTAL_MODEL.md`. Source commitc19a804a, branch `run15-thinking-heal`. Failure audit: `../../audits/20261026_run15_gpu_smoke_failure.md`. No public push.
