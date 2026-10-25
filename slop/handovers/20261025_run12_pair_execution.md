# Run12 paired chat execution

PI/OpenAI (Sol), session01a16bd4, 2026-10-25. Supervisor const_v2 owns design/goals; this session is sole executor. Source of truth: `slop/eval/run12/execution_plan.json`. User approved two missing independent trainings and RESUMED after clarification; do not repeat documents or chatr13. No replacement of a created failed worker without escalation.

## Actual workers

- Mixed: instance57641569, process `proc_189f`, lease `run12mix`, 11.5h cap, deadline2026-10-25T20:42:42UTC (04:42:42AWST). Generic: instance57641120, process `proc_91bc`, lease `run12gen`, 17.5h cap, deadline2026-10-26T02:38:41UTC (10:38:41AWST).
- Independent persistent systemd timers `cg-vast-<ID>-deadline.timer` are active/enabled. Receipts and frozen executable helpers: `slop/eval/run12/run12{mix,gen}/deadline_guard_armed.json` and `deadline_guard/`. Frozen guard SHA71749fdcead481ee97cb9c16bfef752a66ecc1e65aba575aef4626b1caf01fdb. Actual systemd readonly API GET checks passed for both exact IDs; see `deadline_guard_runtime_get.log`.
- Guard requires provider API availability. At absolute cap it destroys even if data remain unpulled. Execution/evaluation reserve4400s for retrieval; copy failure stops GPU until this bounded recovery deadline. Never disable a guard before verified normal destruction.
- Both controllers hold lease/instance owner locks. Do not start a duplicate attach/retrieval/destroy. Heartbeat stays active through retrieval and uses hard-deadline timeout.
- First offers vanished before creation; those attempts incurred no rental and have preserved failure logs. A guard self-freeze bug was caught by independent review before any guard activation and fixed with first-occurrence replacement +compile/runpy regression. Six safeguard and three retrieval regressions pass; independent review evidence is `slop/audits/20261025_vast_skill_evidence/`.
- At this checkpoint generic passed pinned Base/runtime/CPU-merge setup and is uploading donor adapters; mixed is booting/preflighting. No training metric has been read yet. Native process watches wake on setup/data/start-train/errors and eventual completion.

## Bounded progress check, 2026-10-25 10:28:58 UTC

PI/OpenAI (Sol). One read-only parallel SSH snapshot per worker, requested by supervisor after 76/80 minutes elapsed. Both are transferring the final 3,997,800,800-byte Stoic donor; Const and Other are already complete and hash-verified. No training/job log exists yet; GPU utilization and allocated memory are zero. Generic's Instruct prep is complete. This supersedes the earlier setup checkpoint above.

- Mixed: partial 2,167,930,880 bytes, receiver age921s, file modified0.21s before observation. Average2.35MB/s; remaining upload about13minutes, ETA10:42UTC.
- Generic: partial 2,958,557,184 bytes, receiver age1269s, file modified0.17s before observation. Average2.33MB/s; remaining upload about7minutes, ETA10:36UTC.
- These are bytes/receiver-age estimates, not instantaneous speed measurements. Recent writes support progressing transfers rather than a current stall; sustained rate and subsequent training speed remain unmeasured. Raw evidence: `run12{mix,gen}/progress_20261025_1028.json`.
- At the previous chatr13 rate0.143updates/s, with20% time margin and existing planner overheads, remaining work estimates are7.81h mixed (train-only) and12.54h generic (four eval cells), plus the uploads above. Time to the fixed retrieval-reserve boundary is9.01h/14.94h, leaving approximately0.98h/2.27h beyond those estimates. The73-minute retrieval reserve remains separate. Ceilings still plausibly fit; this is not a measured training ETA. Donor merge, actual optimizer speed and cross-worker delivery need verification at native events.
- No restart, replacement, deadline extension, owner-lock change or duplicate controller. Added one-shot native watches for final-donor upload completion and donor merge; existing training/error/completion watches remain.

## Native transitions after the bounded check

PI/OpenAI (Sol). Both final Stoic uploads completed with the pinned weights/config hashes. Generic uploaded chatgen (9,418 rows, 1,709,519 tokens) and began `merge donor Base + stoic=0.5 const=1 other=1` at10:36:05UTC; mixed uploaded chatmix (6,483 rows, 1,709,438 tokens) and began the same donor merge at10:39:14UTC. Both uploads finished by the prior estimated times. No optimizer update is confirmed by these events; blank `PROGRESS ` lines are not evidence of learning. One-shot loss/text_loss watches were added to both existing processes. No remote probe or lifecycle change was needed for these transitions.

Native stages report the configured donor greedy check passed and training invoked: generic `start train chatgen (9418 rows)` at10:40:10UTC; mixed `start train chatmix (6483 rows)` at10:43:49UTC. These confirm invocation, not optimizer updates. Supervisor requested no further setup-stage messages; next update requires actual optimizer metrics/ETA, a consequential blocker or completion. <!-- PI/OpenAI (Sol) -->

## Actual optimizer check, 2026-10-25 11:29:32 UTC

PI/OpenAI (Sol). Supervisor found real tqdm updates in local logs before our loss-only watch fired. The controller prints only the last training-log line every900s, normally tqdm rather than the loss dictionary. Added one-shot optimizer-step regex watches to both existing processes; no recurring probe, restart or lifecycle change.

One bounded read-only remote snapshot per worker saved complete available training-log text, resolved config, source/data hashes and a full first input/target. Evidence: `slop/eval/run12/run12{mix,gen}/early_training_20261025_1129/`; `checks.json` gives every arithmetic check and ETA input. Read all saved setup messages and scanned every metric row. No new generations or held-out evaluation after training yet.

- Mixed309/3079, `44:16<5:12:26, 6.77s/it`; conditional training ETA16:42UTC. Latest text loss1.587, penalty0.01658, total1.603, gradient norm1.018. Spectral calibration fired atstep307: `mean CE1.6045 mean sigma0.37501`, lambda0.04279; updates308/309 have positive penalties. GPU86%,83,483MiB used.
- Generic356/4474, `48:11<7:20:03, 6.41s/it`; conditional training ETA18:50UTC. Latest text/total1.642, gradient norm1.023, sigma0.3332. Lambda/penalty zero is expected before its approximately447-update warmup ends; post-warmup activation is not yet observed. GPU99%,83,421MiB used.
- Both execute the pinned Base+½Stoic+Const+Other donor, response-only `input_output` data,2epochs, accumulation4 and330spectral LoRA modules. Uploaded dataset hashes and active box/plugin source hashes match the frozen plan. All665logged metric rows are finite; total equals text+penalty within display rounding (maximum residual0.00058). Trainable-token counts are positive and below total throughout, consistent with the segment masks; no independently decoded tokenized-tensor audit was done.
- Initial held-out losses before any optimizer update are1.917mixed/1.938generic. Current batch losses do not establish improvement or compare the two corpora. No trained character/capability result exists yet.
- Raw training ETAs leave2.79h mixed/6.60h generic before their fixed retrieval-reserve boundaries. Future validation/checkpoint pauses, mixed delivery and generic's four eval cells remain; this margin supports continuing unchanged, not deadline extension. A20% slower remaining training estimate would use about1.04h/1.47h of those margins. The73-minute retrieval reserve remains separate.
- Data caveat from the deliberately selected first mixed row: `gen_d3cb38f651`, inherited no_robots target, says4,200passengers although the prompt gives3,200passengers plus1,000crew. Full text is `first_row.json`; this factual target error is recorded in paused Task9, not repaired in the frozen experiment. The first identity row and first help row were also read in full; the generic control is entirely general examples by design. No data/config changes.
- Known warnings remain visible in `setup_messages.log`: unmatched expert rank/alpha keys (existing tested PEFT warning), unavailable router/causal-conv optimized kernels, preprocessing during training and scalar conversion for calibration. Nonzero gradients/sigma and coherent loss components argue against an inactive adapter or detached whole objective; per-expert gradients and post-training rank checks remain later evidence. No new infrastructure failure was observed in this snapshot.

## Frozen recipe and budget

Both train independently on the same pinned Base plus0.5Stoic+Const+Other, using the same three verified historical adapter binaries. Data bytes: chatmix5c5321b0..., corrected matched chatgen42928ea9...; staged unchanged under `.local/run12_train/` with manifest. Two epochs, response-only LoRA, unchanged spectral calibration/config. Worker environments are `.local/run12_mix_env.sh` and `.local/run12_gen_env.sh`. Separate output/state/prepared-cache/adapter directories; final local adapters are `~/.local/share/cg_run12_{mix,gen}_adapters/`.

Combined cap60USD includes GPU, traffic and judges. Current reserve58.088905USD (29GPU-hours upper-rate53.488905 +4traffic +0.60judge), leaving1.911095termination/retry margin. Count actual elapsed time from original creation, including setup and retrieval. No automatic extension. API-judge reserve is small; use cached references, preserve every charge, and skip optional extra doses if they do not fit.

Pre-outcome expectations: mixed/generic token matching does not match optimizer updates (about3079/4474), so this tests the complete subtraction recipe, not pure content causation. Subtraction may reduce useful instruction behavior as well as style; earlier Instruct-reply control was a different training distribution and cannot predict the generic control's sign. Character/capability could both weaken at equal dose. Distinguish a better trade-off at matched character increment from simply making a weaker intervention. These are qualitative hypotheses, not numerical success forecasts.

## Next actions

1. On each native event, inspect actual source/config/training evidence; distinguish setup from real optimizer progress. No polling/sleep loop. Retain actual resolved configs, split text/regularization losses and outputs; use ml-debug/auditlog on consequential completion/failure.
2. Mixed is train-only. On its success, read `run12mix/retrieval_verified.json`, confirm exit0/final hash, then deliver to the generic worker:
   `source .local/run12_gen_env.sh; uv run --no-sync python scripts/eval/49_run12_pair_ready.py deliver-mix`
   This rehashes local mixed weights, verifies exact remote instance identity, rsyncs final config/weights and atomically opens the hash-checked pair barrier. Do not deliver an unverified partial adapter.
3. Generic initial cells are fixed donor plus plain mixed at0.5/1, then mixed/control at+0.5/−0.5 and+1/−1. Same frozen replies/panel/demos/viewpoints and60maths questions as references. It holds after all four initial cells, bounded by its evaluation deadline. On `INITIAL PAIR EVAL COMPLETE`, take a non-destructive snapshot using existing script38 `snapshot` with generic env; it serializes copies and never destroys.
4. Use pinned character judge41 (not capability-only), full ordinary/coherence checks and actual reply reading; cached donor/chatr12/chatr13 reference scores. Compare on-target increments above the same donor and off-target losses against it. Existing curves/local interpolation first, with uncertainty and no extrapolation across breakdown. Broad ABX is not target character. At most two extra doses if they could change the decision and fit the existing time/API reserve; coordinate with supervisor.
5. Release the eval hold before retrieval reserve is exhausted:
   `source .local/run12_gen_env.sh; uv run --no-sync python scripts/eval/49_run12_pair_ready.py release-eval`
   Controllers then retrieve/hash and destroy normally, confirming absence and disabling only their completed timer. Record final receipts/usage; invoice/credit-difference caveats remain. Do not call incomplete or unrun cells negative results.

Plot work belongs to the isolated analyst/supervisor. Approved stage-split commits6048f6e7 and1b618577 are integrated as451d9e9 ande8aadcd. Stage1 and stage2 images were ingested here; four focused regressions pass in `slop/eval/character_tradeoff/integration_tests.log`. The supplied fresh review and the three addressed label/name corrections are recorded in `slop/reviews/20261025_tradeoff_plot_review.md`. Final visual acceptance remains with the human; no rental result was added to the frozen curves. Results/recipe edits add links only.

Integration did not change the two native processes or lease/deadline ownership above. The five active controller/guard/watchdog/box sources are hash-identical to the pre-integration snapshot in `.local/run12_before_stage_split_integration.json`. No status polling, new rental, duplicate controller or schedule was added. Continue on native events. AGENTS-only requested guidance is committed46a9746. Dataset-review Task9 remains paused.
