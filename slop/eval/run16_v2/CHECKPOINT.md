# Run16 CHECKPOINT — attempt2, not final

Resume this same worker/worktree when a watched event lands. **Do not create another rental. Do not wait in bash.** The first child process is not presumed alive; the durable jobs below own the current run. Worktree `/workspace/2026/constitutional_grafting/.local/worktrees/run16`; branch `run16-v2-best-practice`. Parent/intercom bridge: const_v2.

## Current lease and budget

- **Vast57919543**, `cg-run16-v2`, RTX PRO6000S, running/SSH-ready; **$1.9185185185/h**. Setup, watchdog (auth200) and six concurrent donor uploads started directly from the new controller.
- Created2026-10-27 **05:00:39 UTC**. Independent exact-ID destruction deadline: **2026-10-28 05:30:39 UTC** (24.5h). Runner deadline: **2026-10-28 04:00:39 UTC**. No repair may extend these deadlines.
- Active state `.local/run16_v2_rental.json`; guard/lease receipts under `lease/`. Latest API running confirmation and elapsed-cost estimate: `lease/checkpoint_live.json`.
- First-lease conservative allowance **$4.25** (actual GPU estimate$3.4879 plus traffic; supervisor estimated≈$4); replacement GPU estimate **$0.1041** at05:03:54UTC. Project model/judge API calls still0.
- Maximum cumulative reservation: **$64.29** at max rate$1.92; **$64.2537** at this offer's rate, including prior$4.25 +$13 judges/review/traffic/margin. No core cells removed. Optional(c) remains first to skip if measured time/spend cannot fit. Plain-Base chat remains unapproved and UNWIRED.

## What failed, what changed, and evidence

First lease57903770 failed before any training: `tiny_smoke` passed `env=env` to a callback accepting `extra`. It was destroyed; fresh API confirmed0 instances before the authorized replacement. **All first-lease evidence was moved with git to `lease_attempt1/`, not discarded**, including `box_runs/job.log`, closure, guard, quote, old checkpoint and upload logs. One-line cause README is there. The original raw logs are unchanged, including whitespace. Old pueue jobs4209/4212/4214–4217 are finished/failed; do not revive them.

- **39fb9ba7:** fixed callback to `extra=env`; added a CPU dry-run that executes real62 `main` AND `tiny_smoke`, with explicit axolotl/vllm/merge/stage stub executables. No paid calls/GPU/scientific fake results.
- **891a7c4d:** preserved failed evidence and added controller repair hold plus six-stream scheduling.
- **f4c326cd:** supervisor-approved replacement preflight; all executable/input/source hashes frozen.
- **16 CPU tests passed** (`retry_driver_recovery_tests.log`):8 full driver branches, regression that reintroduces the original callback bug and proves replay catches it, and7 first-step/recovery/scheduling checks. CLI replay also passed every operational branch (`driver_dry_run_all.log`). Covers normal/fallback bases; selector failure before/after artifact creation; tiny smoke, training, projections, evals; invalid/timed-out coherence approval; optional(c) run/skip/timeout.
- Recovery tests distinguish random smoke/tokenization from production optimizer progress, hold+approved restart, exact60min expiry, runner-deadline clamp, no post-update repair, and six streams scheduled before doc waits with monitoring before late control upload completes.
- Replay is an orchestration test, NOT native-image/GPU validation. Actual3-step Axolotl smoke still runs before production. Full historical-plugin/projector and draft-sandbox checks from attempt1 remain recorded.

## Approved smoke repair0 — restarted, not a new lease

- At06:26UTC the real Axolotl validator rejected the tiny smoke: inherited `warmup_ratio=.1` coexisted with explicit `warmup_steps=2`. No production update occurred; controller preserved the box and uploads in its60-minute repair hold.
- const_v2 explicitly approved the smoke-only correction for **57919543/index0**. Commit **07c07cf6** removes the ratio key entirely only from tiny-smoke YAML. Production warmup/config/data are unchanged.
- Strengthened stub Axolotl and full replay to reject ANY generated YAML containing both warmup keys. New mutant regression removes the fix and reproduces the native rejection. **17 tests pass; all8 CLI driver scenarios pass** (`repair0_warmup_tests.log`, `repair0_driver_dry_run.log`).
- SHA-pinned approval was consumed and the controller uploaded/verified **edb54216b6acc41e3a703f1af4227731edc508fee15453ecf997ac0fd5c6779c**, archived failed remote logs and restarted the driver. `lease/repairs/0/restart_verified.json`: tmux running, no job.exit, actual generated smoke YAML has steps2 and NO ratio. This confirms restart, NOT smoke success yet.
- Original failure config/logs, holding event, submitted approval and verification are preserved under `lease/repairs/0/`. Consumed approval: `lease/driver_repair_0.approved.json`. Original preflight source hashes are superseded only by this explicit one-file repair receipt.
- **Original repair expiry remains epoch1793085993.412522 (2026-10-27 07:26:33 UTC), NOT extended.** Hard lease deadline is also unchanged. `lease/driver_failure.json` status `restarting`/index0 describes this repaired failure. Watch immediately for a NEW holding status/index1 if another pre-production failure occurs; it shares the original expiry and requires new supervisor approval.
- Watch `lease/box_runs/tiny_smoke.json` for actual native-smoke completion, then first20/EOS events. Existing jobs4218–4223 remain active/queued; no replacement or new jobs were created for this repair.

## Active durable jobs

| Job | Group | Wait / role |
|:--|:--|:--|
| **4218** running | run16 | Current single-lease controller, `controller_attempt2.log`: setup +6 streams; start driver when stoic/const/other verify; remaining adapters upload during training. Monitor, bounded early repair, final retrieval and exact-ID destruction. |
| **4219** running | run16-evidence | Collect until `lease/box_runs/eos_first20.json`; monitor finite historical spectral metrics/calibration. `collect_first20.log`. |
| **4220** queued | run16-evidence | Then collect until `lease/box_runs/eos_trained.json`; `collect_new_D.log`. |
| **4221** queued | run16-evidence | Then collect full replies, CPU /22,/38 and sandbox draft checks, pinned JEV judgments/read packets; stop at `anchored_gate_ready.json`. `collect_gate.log`. |
| **4222** queued | run16-evidence | Then collect anchored training/evals; stop at `optional_c_ready.json`. `collect_optional.log`. |
| **4223** running | run16-artifacts | Wait for selector gate; copy4 moment shards to `.local/artifacts/run16/selector` and SHA-verify. Watch `selector_moments_verified.json`. |

Evidence group is serial; collectors advance automatically. No duplicate collectors/judges. Collectors now tolerate a pre-production repair hold and remove stale remote-deleted `job.exit` via rsync, preserving their locally generated first20 receipt.

## Watchers to install NOW, in order

**Always-on failure watcher:** `lease/driver_failure.json` (controller writes locally immediately). If `status=holding`, resume worker urgently: **up to60min total**, bounded by runner deadline; uploads, heartbeat and hard deadline stay active. Also watch controller4218 exit / `lease/post_production_failure.json`. Post-production failure retains retrieve→destroy behaviour, NOT a hold.

1. `lease/box_runs/eos_first20.json`: inspect first20 production steps. Spectral calibration is normally not due until~78 steps; absent at20 is not failure. Stop/ask on nonfinite or zero actual calibration; collector already suspends owned foreground job if detected.
2. `lease/box_runs/eos_trained.json`: **immediately relay adapter path and binary SHA to const_v2 → cg_exp_curve**. Read `eos_config_diff.json` and training evidence.
3. `lease/box_runs/selector_gate.json`: relay failed selector check to cg_exp_curve; never graft a failed cell. Keep moments/logs. Also watch `selector_moments_verified.json`.
4. `lease/box_runs/chat_evaluated.json`: relay completed block; full prompts/replies under `read_packages/<model>/full_replies.md`. Parent launches Sol readers if needed; full coverage, not crops alone.
5. `lease/box_runs/documents_evaluated.json`, then `lease/box_runs/anchored_gate_ready.json`: after Base heldout loss, send plain/anchored fixed panels and full sampled-turn flags to parent. Parent decides coherence/fallback approval.
6. `lease/box_runs/anch_trained.json`, then `anchored_chat_evaluated.json`: preserve SHA/config, relay milestones and read packets.
7. `lease/box_runs/optional_c_ready.json`: decision required within20min. Implement/check actual optional driver69 ONLY if reviewed method and measured budget/time fit; otherwise explicitly skip. Queue collector `--until-event complete` for final extra cells.
8. `lease/box_runs/complete.json`, `job.exit`, and root `provider_closure_verified.json`: final controller retrieval and destruction. Independently confirm exact instance absent through API; cost receipt, results/audit/journal/full reads/different-family review and final scoped commits remain due.

## Pre-production failure repair procedure

`60_run16_rental.py` inspects ONLY production EOS progress/checkpoints/final marker, not tiny-smoke or tokenizer bars (`run16_recovery.py`). Any observed first production update makes failure post-production and immediately returns to retrieve/destroy. Before that, a failed/disappeared driver creates `lease/driver_failure.json`, mirrors it to box runs and holds. The hold is shared across retries, never reset beyond60min and never extends the guard.

1. Read complete failed logs and identify cause; no blind retry. Run the local real-driver replay/regression tests with the proposed fix.
2. Write root `driver_repair.approved.json` with exact current instance/index, reason and SHA map of approved changed CODE paths, for example:

```json
{"instance_id":57919543,"failure_index":0,"reason":"investigated cause; local replay passed","source_sha256":{"scripts/eval/62_run16_box.py":"ACTUAL_FILE_SHA256"}}
```

3. Controller uploads and remotely verifies those exact sources, rechecks that production has NOT started, archives failed job/smoke/EOS logs under remote `driver_failures/attempt_N`, clears ONLY random-smoke scratch outputs, consumes approval and restarts driver. It does not automatically retry a failure without approval. Invalid/stale instance/index or changed SHA fails closed; take care writing the receipt.
4. Expiry or any post-update failure: retrieve then destroy. No third rental is authorized.

## Coherence and optional decisions

Parent-approved root `anchored_gate.approved.json` needs `base` in `anchored_docs` or pre-agreed different-recipe fallback `anchored_const2`, plus `full_panel_read:true`, `flags_read:true`, reason. Upload with:

```bash
uv run --locked python scripts/eval/60_run16_rental.py approve-gate
```

Optional(c) actual `69_run16_ortho.py` is **not implemented**. A `run` decision must not be written until it exists, passes tests/review, and its actual SHA and projected_total_usd≤65 are in `optional_c.approved.json`. Otherwise write `{"action":"skip","reason":"actual budget/time reason"}`. Reviewed projection/plugin sources and commands are preserved in `ortho_commands_received.md`/`ortho_review_received.md`. Basis14GiB is exported during required P64 SVD. Slow-stop limit is12s ADDED overhead/update beyond new-D measured time; check native parameter identity/residuals. No plain-Base chat ablation has been added; await wassname/parent decision.

## Scientific/protocol constraints unchanged

- Main judged set: **196 items, SHA5ea2684b…**, frozen a66d2ae protocol/archive, JEV pair+turn, T=.7 seeds0/1, run8 change text, thinking OFF. Do NOT recopy current tiny-char v2, which was overwritten in place with232 items.
- Core chat: same run10 config/rank/targets/2epochs/Base+docs; only EOS-fixed data path differs after artifact-path normalization. Data1636 rows,903 EOS additions, SHA284895029f…. No loss on empty think blocks; no ALLOW_MISSING_EOS. Historical spectral source EXACT SHA `b654c4ff9a3366709c9a2abd0bb254a11da7f41bc5b2dfe8b83fae48144301e6`, fraction.01. Random3-step smoke alone uses warmup_steps2; production warmup remains untouched.
- Separate **run8 small tasks/22**, **v2 capability/38**, **draft code/40** and **draft tools/32** columns. Draft36 items pinned a0b0683/dbe82f1e, zero judge calls, readonly/no-network/nobody Docker. Shared legacy GSM IDs changed questions. Versioned96 v1 items are identical in196-item v2; only49 exact prompt/check tuples overlap run14's customized70. Do not make direct historical-score comparisons.
- New P64/P128 and output-side P64, char/cap selector4acffd4a; old P64 recomputed and hash-compared to run14, not uploaded. Failed selector adapter is never registered in eval logger.
- Documents: any coherent moral/persona change and Base heldout loss, NOT preferred-character score. Raw/common-coherent ABX script66 is still to be run. Chat: paired intervals, both-finished maths and matched-character interpolation only within measured half…one bracket, no extrapolation.
- Cached metrics68, answer-panel52 and full read-package65 tooling exist; real-data validation, new-item keywords/decisions, plots, full T0 appendix, reading notes, final results and independent review are NOT done. No scientific outcome is claimed.

This is the authorized replacement checkpoint, not the FINAL research handoff. -- PI/OpenAI (Sol), 2026-10-27
