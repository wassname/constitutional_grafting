# Run16: failure 1 repaired without repeating learned stages

**Checkpoint: 2026-10-27 11:29 UTC. Signed: PI/OpenAI (Sol).**

## Operational outcome

- Fixed the real GSM command in `61_run16_cells.py`: `small_tasks.jsonl` and `draft_code_tools.jsonl` no longer follow the single `--items gsm8k_long60.jsonl` argument. Their independent generation commands and separate scoring paths remain unchanged.
- Commit `b2cf2d8c`: native argparse replay, strict `--resume-chat`, explicit same-instance attach, approved bounded post-production repair holds. Supervisor SHA approval is `lease/chat_resume_1.approved.json`.
- SIGKILLed the stopped process group 3870730, task 4218, at 11:07:58 UTC. Python's destructive `finally` could not run. Provider GET confirmed exact instance **57919543** still running. Evidence: `lease/repairs/1/`.
- Controller **4224** started at 11:08:16 UTC. All twelve saved model/config hashes passed at **11:09:08 UTC**. It skipped tiny smoke, EOS training, all completed projections and selector, and entered chat evaluation. Original learned receipts remain unchanged.
- Incomplete Instruct outputs and failed job logs were preserved on-box under `runs/run10/driver_failures/attempt_1/`, not reused or silently appended. The full Instruct cell was regenerated under the same frozen protocol.
- **Real first-cell end-to-end check succeeded:** `r16_instruct.done` now exists; reply/demos/panel/POV/small-tasks/draft/GSM rows are respectively **392/6/4/6/22/72/60**. GSM reports **55/60**, three max-token cutoffs, and zero rescue calls. This is the unchanged Instruct baseline, not a graft improvement or a reasoning-quality claim. See `lease/repairs/1/resume_progress_1129.json`.
- At the 11:14 live check, server `r16_instruct` was healthy, GPU utilization 61%, memory 87,689 MiB, detached driver present, and no job exit record. Controller 4224 remains running; **do not roll it merely to add diagnostics**.

## Preserved learned weights

All hashes below were checked against the existing receipts on the same instance; no retraining or SVD rerun:

| Artifact | Weight SHA256 |
|---|---|
| EOS-fixed chat adapter, `r10_eos_chatr12` | `e6ed8d614f9476385894838b5326a3594142cea52e2e1bc92395c27a8aa8f0e1` |
| Both-sides rank64, `r10_p16_64` | `08101332ea56f8ee62a07576570612777d891cbaa8ffae445a4a7445618f9fd2` |
| Both-sides rank128, `r10_p16_128` | `7523fcee7caed44c8d011cbd4f62ef80e4f20f3791b82e7746d612eed7d3bd60` |
| Output-only rank64, `r10_p16out_64` | `afa48a9eb104d9d579229c00e44bf3b2488785cc63f2c8da37c14a1b3bc3e217` |
| Character-vs-capability selector, `r10_charcap` | `08ddd66ad71279c06ff249569b025ac720b4b7062006dcae8a8c4b1ac3bb6066` |
| Recomputed old rank64, `r10_oldp_64` | `efec33db87e7c6d7eea4b0a2914f26705e844fabb07337e9a5a603e31753f9fa` |

## Backup and recovery policy

- Selector-moment backup **4223 succeeded** at 11:05 UTC; its receipt is `selector_moments_verified.json`.
- Supervisor-approved early backup **4225** started at 11:13:54 UTC, **one stream**, targeting `.local/artifacts/run16/{adapters,projections}/`. Commit `9fc54fc4`. It copies all six retained final adapters and their projection/training receipts, checks physical SHA values and receipt-bound weight hashes, and seeds normal final retrieval atomically. Cross-filesystem copying is tested (workspace and home are different filesystems).
- Its source-hash inventory has **21 files**. At the latest check, all projection/training JSONs plus the complete EOS adapter/config had verified; the next adapter was copying. **Do not claim the full backup complete until `artifact_archive_verified.json` exists with `all_match=true`.**
- Every later driver failure, including anchored training, gets a new failure index (starting at 2), `lease/driver_failure.json` status `holding`, an attempted SHA-verified final/checkpoint adapter snapshot, and up to 60 minutes for a separately SHA-pinned supervisor repair approval. Existing runner/hard deadlines win. Snapshot errors are recorded rather than called verified.
- Completed anchored training/projection can also be reused by recorded hashes. An incomplete anchored output directory is deliberately not silently retrained: it requires an explicit checkpoint/restart repair decision.
- Final acceptance found that rsynced result files lacked a separate SHA receipt. Supervisor explicitly rejected rolling healthy controller 4224 for this. `74_run16_result_hashes.py` and its tests provide a one-off remote `sha256sum --zero` versus local SHA check covering **every retrieved result file**, including missing/changed files. Run it after a stable retrieval, not against changing live logs. It writes a receipt and fails closed on any difference; it is intentionally not hot-wired into 4224.

## Validation and unchanged constraints

- **29 regression tests pass** (`chat_resume_final_tests.log`), including the exact original GSM argv failure, all real cell subprocess native parsers, corrupt-resume rejection before expensive commands, completed anchored-stage reuse, bounded post-production repair, cross-filesystem backups and result SHA checking.
- Maintained `just run16-driver-dry-run`: **11/11 cases pass**, all explicitly CPU/stub-only (`chat_resume_maintained_dry_run.log`). Native-parser tests execute the real `61` command-building flow but stub model work; they are not GPU results.
- Compileall and `git diff --check` pass. All deployed SHA-approved source files were rechecked unchanged at 11:28 UTC.
- Same instance; no replacement, no new training method/dataset/hyperparameters/doses. Unchanged total reserve **$64.29**, below the $65 cap; unchanged 24.5-hour ceiling. Runner deadline **2026-10-28 04:00:39 UTC**, hard destruction **05:30:39 UTC**; independent deadline timer remains active and heartbeat is owned by controller 4224.

## Next milestone

Monitor 4224/4225 for the EOS/raw/projected chat cells and full backup receipt. The later anchored gate still requires the full panel/flags review and explicit approval. Optional orthogonal training remains last and conditional on the original measured-budget/runtime gate. Character/capability trade-offs and final ablations are **not complete**; do not infer them from baseline accuracy or selector retention metrics.
