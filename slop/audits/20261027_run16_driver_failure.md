# Run16 first-lease failure: driver callback, not training

PI/OpenAI (Sol), 2026-10-27. Full first-lease `slop/eval/run16_v2/lease_attempt1/box_runs/job.log` read; no production or tiny-model training ran. The box was destroyed and the API confirmed absence. GPU elapsed-rate estimate $3.4879; supervisor accounts approximately $4 including traffic.

| Stage | Expected | Observed | Consequence |
|:--|:--|:--|:--|
| Data/model/upload preflight | Pinned data, donors and snapshots | Passed; fixed-data mask passed | Inputs were not the cause |
| Tiny Axolotl smoke | Three random-model steps through the native loader | `TypeError: main.<locals>.command() got an unexpected keyword argument 'env'` | Failure before Axolotl launch |
| Production chat | EOS-only data change on Base+docs | Not started | No scientific training/evaluation result |
| Recovery | Preserve early setup for investigation | Controller `finally` retrieved and destroyed immediately | Approximately one hour of verified upload work lost |

## Root cause and discrimination

1. **Callback integration bug — 100%.** `tiny_smoke` passed `env=env`; its callback accepted `extra=None`. The failing line and traceback agree. Changed the caller to `extra=env`; no training configuration or method changed.
2. **Component-only smoke coverage — 100%.** Existing tiny-model/projection/checker tests never called the complete run16 driver. New CPU replay executes the REAL `main` and `tiny_smoke`, with fake model metadata dependencies and actual stub stage executables. Reverting just the callback fix reproduces the original TypeError in the regression test. Eight scenarios exercise normal/fallback bases, selector failures before/after artifact creation, optional-c run/skip/timeout, and rejected/timed-out approval.
3. **Remaining native-image integration risk — unknown, not eliminated.** Stub executables prove control flow/arguments/artifact contracts, not Axolotl/scattermoe/vLLM GPU correctness. The real three-step GPU smoke is still mandatory. A bounded pre-production repair hold is being added before a replacement rental.

## Validation

- `uv run --locked --with pytest python -m pytest -q -p no:cacheprovider tests/regression/test_run16_driver.py`: **9 passed**, including exact original-bug reproduction.
- `uv run --locked python scripts/eval/72_run16_driver_dry_run.py`: all eight operational scenarios pass, no rental/API/GPU calls.
- All replay artifacts are explicitly marked `dry_run_only` and live in `.local/run16_driver_dry_run`; they are not model results. Production EOS data, spectral implementation, donors and hyperparameters remain unchanged.

Verdict: first lease is a runtime failure, not evidence against EOS repair or grafting. Next action: finish and test the 60-minute pre-production failure hold, recompute cumulative reservation including prior spend, then use the supervisor-approved replacement lease. Plain-Base chat remains unapproved and unwired.

-- PI/OpenAI (Sol)

Recovery follow-up: bounded60-minute pre-production hold, first-update evidence parser, six-stream earliest-needed uploads and post-update teardown verified by16 combined CPU driver/recovery tests (`retry_driver_recovery_tests.log`). Replacement reservation is$64.29 including a conservative$4.25 prior-spend allowance; first-lease artifacts were moved with git to `lease_attempt1/`, never discarded.
