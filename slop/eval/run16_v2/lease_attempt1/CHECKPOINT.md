# Run16 CHECKPOINT — not final

**Resume this same executor/run; do not create another rental.** Parent const_v2 explicitly authorized this checkpoint because all bash calls are hard-capped at60s, including `pueue wait` with a larger tool timeout. Parent owns event watchers and will use subagent resume. Durable jobs continue independently.

Executor: PI/OpenAI (Sol). Worktree `/workspace/2026/constitutional_grafting/.local/worktrees/run16`, branch `run16-v2-best-practice`. No push. Main checkout is shared and has unrelated dirty files: do not modify it.

## Live rental and spend

- **Vast instance57903770**, label `cg-run16-v2`; RTX PRO6000S, **$1.9185185185/hour**,500GB disk.
- Created **2026-10-27 02:14:44 UTC**. Exact-ID systemd destruction timer active/enabled for **2026-10-28 04:14:44 UTC**. Runner deadline is90min earlier. Guard state: `.local/run16_v2_rental.json`; armed receipt `lease/deadline_guard_armed.json`.
- API check at **2026-10-27 03:17 UTC**: running; GPU0% because donors are uploading; both pinned HF snapshots/setup already complete.
- Elapsed-rate GPU estimate **$1.9941** at that check; **0 project API/judge calls so far**. Traffic not invoice-reconciled; reserved$3. Worst-case whole-lease reservation **$62.88/$65**, including$6 judges,$2 review,$3 traffic,$2 margin. Do not treat account credit as funding shortage (auto-top-up approved).
- `lease/live_checkpoint_metrics.json` is the last live API snapshot. Network fields there are provider counters of uncertain units, not a reconciled traffic invoice.
- The original controller4208 was deliberately SIGTERM'ed during the parent-approved SAME-LEASE transport handoff. There was no provider create/destroy. Handoff receipt `lease/controller_transport_handoff.json`.

## Durable pueue jobs

| Job | Group | Purpose / file waited for | Next action |
|:--|:--|:--|:--|
| **4209** running | run16 | `60_run16_rental.py parallel-attach`: six-stream SHA-verified uploads, launch once stoic/const/other ready; other uploads continue during training; monitor, retrieve, destroy exact instance | Leave running; investigate its log if it exits. `controller_parallel.log`. |
| **4212** running | run16-evidence | `67_run16_collect.py --until-event eos_first20`; writes `lease/box_runs/eos_first20.json` | Read receipt and early training log. It suspends foreground training on nonfinite spectral/loss metrics or zero calibration and raises: ask const_v2 if that happens. |
| **4214** queued | run16-evidence | After4212, collect until `lease/box_runs/eos_trained.json`; keep same spectral safeguard active | Immediately relay adapter path and SHA to const_v2, who forwards to cg_exp_curve. |
| **4215** queued | run16-evidence | After4214, copy all run evidence; create full read packets; independent CPU /22,/38 checks and sandbox draft checks; approved pinned v2 JEV judging; wait for `anchored_gate_ready.json` | Relay each completed block. Send plain/anchored panels+flags to const_v2 for the gate. |
| **4216** queued | run16-evidence | After4215, same collection/judging; wait for `optional_c_ready.json` | Covers anchored training/evals; optional-c decision required within bounded20min window. |
| **4217** running | run16-artifacts | `71_run16_selector_archive.py`: wait for remote selector gate, copy ALL4 moment shards to `.local/artifacts/run16/selector`, compare every remote/local SHA | Watch `selector_moments_verified.json`. Moments must survive teardown, including failed selector gates. |

Groups `run16-evidence` are serial: queued collectors start automatically. Do not launch duplicate collectors/judges. Logs: `collect_first20.log`, `collect_new_D.log`, `collect_gate.log`, `collect_optional.log`, `selector_archive_controller.log`.

## Parent watcher sequence (all relative to this results directory)

1. **`lease/box_runs/eos_first20.json`** — resume worker; inspect first20 steps. Calibration is normally not due until~78 updates, so absence of calibration at step20 is NOT failure. Watch later finite positive calibration too.
2. **`lease/box_runs/eos_trained.json`** — immediate new-D adapter receipt relay. It contains the remote path and binary SHA. Preserve config-diff receipt `eos_config_diff.json`.
3. **`lease/box_runs/selector_gate.json`** — read pass/fail and relay failure to cg_exp_curve. Source4acffd4a enforces removed-component energy match and ridged-energy ordering. Failed selector is NOT grafted; all logs/moments retained. Also watch `selector_moments_verified.json` for durable copies.
4. **`lease/box_runs/chat_evaluated.json`** — relay block milestone. Full read packets accumulate under `read_packages/<model>/full_replies.md` with frozen selection and source hashes; ask parent for Sol readers if needed. All prompts and full replies, not crops.
5. **`lease/box_runs/documents_evaluated.json`**, then **`lease/box_runs/anchored_gate_ready.json`** — after Base heldout loss, driver waits for gate. Parent should read fixed T0 panels and full sampled-turn flags for plain versus anchored; fallback panel is available too. Parent decides gate.
6. **`lease/box_runs/anch_trained.json`** — preserve adapter path/SHA and config diff; relay milestone.
7. **`lease/box_runs/anchored_chat_evaluated.json`**, then **`lease/box_runs/optional_c_ready.json`** — relay block, decide (c) from measured spend/time, then run or explicitly skip. Do not let this gate timeout accidentally.
8. **`lease/box_runs/complete.json`** / **`lease/box_runs/job.exit`** / **`provider_closure_verified.json`** — controller retrieves all adapters and destroys exact instance on job completion/failure; verify absence via API. Queue another collector with `--until-event complete` when making optional decision so final extra cells are copied/scored too.

Backstop watches: nonzero pueue4209 or collector exit; `lease/box_runs/job.exit` before expected event. Do not automatically retry failures. The independent hard deadline survives worker/controller loss.

## Gate commands and shapes

Work from this worktree. Parent-approved gate JSON goes at `slop/eval/run16_v2/anchored_gate.approved.json`:

```json
{"base":"anchored_docs","full_panel_read":true,"flags_read":true,"reason":"actual read findings and flag comparison"}
```

`base` may instead be `anchored_const2` ONLY for the pre-agreed fallback. Then:

```bash
uv run --locked python scripts/eval/60_run16_rental.py approve-gate
```

Fallback is a different recipe, not D. Driver rewrites its executed model equations accordingly.

For (c), `optional_c.approved.json` must have action `skip` and a real reason, OR action `run`, reason, projected_total_usd≤65 and SHA of the actual `69_run16_ortho.py` entrypoint. **That entrypoint is not implemented yet**; do not approve a run before implementing/checking it. Reviewed source/commands are in `ortho_commands_received.md`, `ortho_review_received.md`; source plugin/projection pinned7ea93f1e. A14GiB basis is saved during required new-D P64/P128 SVD (`outputs/ortho_basis.safetensors`). Core chat shell deletes the merged donor, so a later remerge must verify exactly Base+.5Stoic+Const+Other. Parent clarified slow limit is **12s ADDED overhead/update**, not12s total. Compare against measured new-D throughput; enforce budget/time and near-zero actual factor residuals; check Axolotl/scattermoe parameter-object identity. CPU historical-plugin compatibility tests now pass.

## Locked implementation/protocol decisions already approved

- Both core trainings use **old-D EXACT spectral_plugin.py** SHA `b654c4ff9a3366709c9a2abd0bb254a11da7f41bc5b2dfe8b83fae48144301e6` (d32324c3). Current FP32-autocast/calibration fixes are intentionally excluded from this EOS-only comparison. Receipt `spectral_implementation.json` and remotely checked `lease/checkpoint_remote_sources.txt`.
- First production training YAML/hyperparameters/donor must equal original run10 `cfg_r10_cx_chatr12.yml`; only data path differs after normalizing output/prepared paths. Data is1,636 rows,903 EOS additions; otherwise parsed data identical to run10 executed hash91e95a6e. Fixed SHA284895029f…. No `ALLOW_MISSING_EOS`. Spectral.01,2epochs, assistant loss, Base+docs, thinking off.
- GPU RANDOM3-step smoke alone now uses warmup_steps2, to avoid legacy calibration at a zero-LR first update. This is NOT a production config change. First20 collector watches only production EOS training.
- Old P64 is recomputed on box from old-D chat, NOT uploaded. Compare its actual SHA to original run14 receipt; driver writes `old_projection_comparison.json`. Record any difference.
- Main judged protocol is **frozen196-item 5ea2684b**, a66d2ae checks/judge, JEV pair+turn judges, run8 change text, T=.7,seeds0/1, thinking off. DO NOT copy the now-overwritten232-item v2 file over it. Own frozen tiny-char archive `.local/tiny-character-run16` is already prepared.
- All96 versioned v1 items are identical in frozen196-item v2. Run14 shares70 IDs but only49 exact prompt/check tuples: do NOT claim all70 are comparable. Different judge protocol also bars direct historical score comparison.
- Original run8 small tasks: separate **11 items/22 replies**, SHA `cf8c41c7…`, original pinned CPU checks. V2 capability: separate **19 items/38 replies**, new frozen checks. Shared GSM IDs changed questions, so never combine columns.
- Optional draft code/tools already wired in~12min, BEFORE training/evals, without delaying launch. **36 items**, sourcea0b0683/dbe82f1e; separate2-sample panel; no judge; own **code/40** and **tools/32** columns. Unchanged new checks run inside readonly/no-network/nobody Docker with no home/project credentials or daemon socket. Image digest in `.local/run16_draft_sandbox/image.txt`; protocol/CPU controls under `draft_code_tools/`. Pinned196-item judged set unchanged. Docker uses existing tiny-char venv read-only for numpy.
- No character score for document cells. `66_run16_document_change.py` does stage-appropriate ABX on157 non-capability/non-instruction v2 items, raw AND common-coherent subset, including same-record null. Not run yet. Do not mistake corruption/style separation for moral change.

## Remaining implementation/analysis work on resume

1. Read actual first20/new-D training evidence; relay adapter receipt immediately. Track actual remaining-time/cost forecasts and prescribed drop order; ask parent before method/budget changes.
2. Check selector diagnostics, old-P64 repeat and each evaluation block; readers receive full preselected packets. Add source-named KEYWORDS/DECISIONS for new read items in52 after reading replies. Regenerate `run16_chat`/`run16_documents` answer panels.
3. Parent gate; second training/evals; optional (c) implementation/decision as above.
4. **Possible additional plain-Base chat ablation is awaiting wassname. Parent explicitly said NOT to wire it yet.** It would go before(c), possibly train while parent reads anchored gate. Await go/no-go.
5. Cached metrics entrypoint68 is written but not validated on real outputs yet. Separate177 judged character items,96-v1 subset, exact49 run14 overlap, legacy/22,v2/38,draft columns; paired90% intervals and common-both-finished maths; bracketed linear matching only between increasing new-D½ and1, no extrapolation; label interpolation and uncertainty. Create trade-off/Pareto plots and final Review-preview results page. No scientific outcomes claimed yet.
6. Full T0 demo appendix for every cell; mark unrun mandatory reference conditions explicitly. Full read coverage/notes, independent different-family report review through parent, audit+ml-debug form, journal, scoped commits/no push.
7. Cost receipt including API/traffic; exact-ID destruction API-confirmed; FINAL relay only after actual completion. Current checkpoint is NOT that handoff.

## Validation and provenance already available

- CPU initial projection/selector:7 passed; updated projection/selector/ortho:12 passed.
- Historical spectral restored: rerun compatible projection/selector/ortho suite **12 passed**,3 expected warnings (`cpu_historical_plugin_compat.log`). Old/new logging APIs are asserted separately, not weakened math constraints.
- Recipe, real tiny Qwen-MoE3 optimizer steps, full v2 and original-small-task CPU matrices: **4 passed**, API$0 (`cpu_eval_recipe.log`).
- Draft checker trusted positive/negative matrix and actual Docker credential/socket/network/write isolation: **2 passed** (`draft_code_tools/cpu_checks.log`). Failure smoke0/40,0/32; positive synthetic-code40/40 and canonical BFCL32/32. These are clearly labelled CPU controls, NOT model results.
- `git diff --check` and compilation passed. No staged files at checkpoint commit.
- Main commits: `51e72142`, `9d50204d`, `f02f8220`, `75144936`, `fb7435c4`, `c191b9ab`; latest checkpoint commit follows this file.

-- PI/OpenAI (Sol), 2026-10-27
