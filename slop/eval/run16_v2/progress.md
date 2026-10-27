# Run16 progress

Executor PI/OpenAI (Sol); supervisor/intercom bridge const_v2. Branch `run16-v2-best-practice`, own worktree `.local/worktrees/run16`; no push. **Research run remains in progress; see current `CHECKPOINT.md`.**

## Attempt1: failed before training, preserved

- Preflight data hashes, EOS-only transformation, donor receipts, CPU tiny-model/projection/checker tests passed.
- Instance57903770 was destroyed after `tiny_smoke` called its callback with unsupported `env=`. No tiny or production training occurred. GPU estimate$3.4879, supervisor all-in estimate≈$4.
- All failure/lease/guard/upload evidence moved with git into `lease_attempt1/`, including original raw logs and one-line cause README. Fresh API confirmed0 instances before replacement. Cause/audit: `slop/audits/20261027_run16_driver_failure.md`.

## Follow-up repairs completed before replacement

- [x] Fixed callback to `extra=env` without changing production method/config.
- [x] Real62 driver CPU replay through8 operational branches with stub axolotl/vllm/merge/stages; regression explicitly recreates and catches original TypeError. CLI replay passes; no API/GPU calls.
- [x] Controller holds a pre-first-production-step driver failure for up to60min; writes failure event, keeps heartbeat/deadline, requires investigated exact-instance/index/SHA hotfix approval, archives logs and restarts. No automatic blind retry. Post-update failures still retrieve/destroy.
- [x] Six streams directly from fresh controller; doc donors start training first; other uploads continue; monitor does not wait for late control upload to finish. Collectors tolerate approved repair and remove stale remote-deleted exit markers.
- [x] Combined driver/recovery/scheduling suite: **16 passed**. Historical native-integration risk is not claimed solved by stubs; real3-step GPU smoke remains mandatory.
- [x] Supervisor reviewed/approved replacement. Prior-spend allowance$4.25 +24.5h×max$1.92 +$13 reserves = **$64.29/$65**. No core cells dropped; optional(c) remains first to skip if needed. Plain-Base chat remains UNWIRED, awaiting user decision.

## Attempt2: running

- [x] Instance **57919543**, `cg-run16-v2`, RTX PRO6000S at **$1.9185185185/h**; actual worst-case cumulative reservation$64.2537. API running/SSH-ready; watchdog auth200.
- [x] Independent exact-ID destruction deadline **2026-10-28 05:30:39 UTC**; runner ends90min earlier. Repair cannot extend it.
- [/] Controller **4218**, `controller_attempt2.log`: setup and six verified donor uploads, then real tiny smoke/new-D training.
- [/] Observer **4219** waits for first20; queued **4220/4221/4222** cover adapter receipt, full blocks/read packets/judging, anchored approval and optional decision. **4223** preserves selector moments. Parent watches failure event immediately and resumes this same worker at milestones; no bash waiting.
- [ ] New D trained and adapter/SHA relayed; projections/selector, all frozen evaluations, document coherence approval, anchored chat training/evals.
- [ ] Optional(c) actual driver implementation only if budget/time fits; no plain-Base training without approval.
- [ ] Full reads, matched-effect and paired/both-finished analysis, plots/results, different-family independent review, audit/journal, final teardown/API absence and cost receipt.

## Smoke repair0: approved and restarted on same box

- Native Axolotl rejected simultaneous warmup_steps2 and inherited warmup_ratio.1 before production; recovery hold worked and preserved uploads/instance57919543.
- const_v2 approved index0 smoke-only repair. Commit07c07cf6 deletes warmup_ratio only from generated tiny-smoke YAML; production config unchanged.17 CPU checks and all8 replay cases pass, including rejection of the original conflicting configuration.
- Controller consumed SHA-pinned approval, uploaded exact driver SHAedb54216…, archived failed logs and restarted. Remote verified tmux running, no exit marker, smoke steps2 with ratio absent. Actual GPU smoke success remains pending.
- Failure artifacts and restart verification: `lease/repairs/0/`; original hold expiry07:26:33UTC and hard destruction deadline unchanged. Parent must watch for new failure index1 and native `tiny_smoke.json`, then first20. Jobs4218–4223 unchanged. No additional rental or plain-Base cell.

## Protocols remain separate and frozen

- Main character judging:196 items SHA5ea2684b, a66d2ae pinned protocol, JEV pair+turn, T=.7 seeds0/1, thinking off. Current overwritten232-item tiny-char path is NOT recopied.
- Separate run8 small tasks/22 with original checks; v2 capability/38; optional draft code/40 and tools/32 pinned a0b0683/dbe82f1e, no judge, credential-free readonly/no-network/nobody Docker.
-96 versioned v1 items identical to frozen v2; only49 exact prompt/check tuples overlap run14's customized70. No direct historical-protocol score comparison.
- Core SFT uses old-D exact spectral source b654c4ff…, fraction.01,2epochs, unchanged ranks/targets/Base+docs. Only EOS data differs after artifact path normalization.1636 rows,903 EOS appends, fixed SHA284895029f…; no empty-think loss or missing-EOS override.
- Documents measured by coherent change/heldout Base loss, not preferred character. Final chat comparisons at matched character, raw and both-finished maths; interpolation bracketed and labelled. No scientific outcome has yet been measured.

-- PI/OpenAI (Sol), 2026-10-27
