# Run12 paired chat execution

PI/OpenAI (Sol), session01a16bd4, 2026-10-25. Supervisor const_v2 owns design/goals; this session is sole executor. Source of truth: `slop/eval/run12/execution_plan.json`. User approved two missing independent trainings and RESUMED after clarification; do not repeat documents or chatr13. No replacement of a created failed worker without escalation.

## Actual workers

- Mixed: instance57641569, process `proc_189f`, lease `run12mix`, 11.5h cap, deadline2026-10-25T20:42:42UTC (04:42:42AWST). Generic: instance57641120, process `proc_91bc`, lease `run12gen`, 17.5h cap, deadline2026-10-26T02:38:41UTC (10:38:41AWST).
- Independent persistent systemd timers `cg-vast-<ID>-deadline.timer` are active/enabled. Receipts and frozen executable helpers: `slop/eval/run12/run12{mix,gen}/deadline_guard_armed.json` and `deadline_guard/`. Frozen guard SHA71749fdcead481ee97cb9c16bfef752a66ecc1e65aba575aef4626b1caf01fdb. Actual systemd readonly API GET checks passed for both exact IDs; see `deadline_guard_runtime_get.log`.
- Guard requires provider API availability. At absolute cap it destroys even if data remain unpulled. Execution/evaluation reserve4400s for retrieval; copy failure stops GPU until this bounded recovery deadline. Never disable a guard before verified normal destruction.
- Both controllers hold lease/instance owner locks. Do not start a duplicate attach/retrieval/destroy. Heartbeat stays active through retrieval and uses hard-deadline timeout.
- First offers vanished before creation; those attempts incurred no rental and have preserved failure logs. A guard self-freeze bug was caught by independent review before any guard activation and fixed with first-occurrence replacement +compile/runpy regression. Six safeguard and three retrieval regressions pass; independent review evidence is `slop/audits/20261025_vast_skill_evidence/`.
- At this checkpoint generic passed pinned Base/runtime/CPU-merge setup and is uploading donor adapters; mixed is booting/preflighting. No training metric has been read yet. Native process watches wake on setup/data/start-train/errors and eventual completion.

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

Plot work belongs to the isolated analyst/supervisor. Initial plot integration6936de8 is historical, not accepted as final presentation; do not edit plot files or integrate a new analyst commit without the owner's handoff. AGENTS-only requested guidance is committed46a9746. Dataset-review Task9 remains paused.
