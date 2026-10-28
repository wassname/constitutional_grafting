| Area | Status | Finding | File |
|---|---|---|---|
| Clean | fix | Scratch experiments are outside prescribed stage directories; review-package metadata is stale. | `scripts/scratch/20261028_fidelity_calib_score.py:1`; `scripts/data/v2/review_package.py:122` |
| Entry point | fix | Good central driver, but older documentation dominates discovery and CLI defaults disagree. | `scripts/data/v2/build.py:42`; `docs/data_pipeline.md:11` |
| DAG | fix | File-based structure survives; hidden dependencies, unchecked edits and incomplete review integration remain. | `src/constitutional_grafting/data/v2/retry.py:20`; `src/constitutional_grafting/data/v2/edit.py:102` |
| Large files | note | Supplied inventory shows no file over 1 MB; six PNGs and substantial generated review data are committed. | `slop/reviews/20261028_merge_review_inputs.md:176–210` |
| Disk | note | Workspace has 1.2 TB free; root has only 128 GB. Rental capacity needs a download-size estimate. | `slop/reviews/20261028_merge_review_inputs.md:258–265` |
| Smoke | fix | Check suite passed; cached v4 chat run succeeded, but no maintained v2 smoke or required local real-driver GPU smoke. | `justfile:16–23`; `data/logs/v4_small.log:1–16` |

## Scope and evidence

Read-only review of supplied range inventory, complete v2 modules/configs, drivers and relevant documentation; read AGENTS.md and ml-debug. No commands executed here: shell evidence comes from the parent’s input artifact. Current README/AGENTS were consulted for navigation/rules, not treated as merged changes. No files with `human` in their paths were opened or changed. Full commit diffs and exhaustive private-text inspection were unavailable.

## Concrete findings

### 1. Entry point and cleanup

`build.py` is a clear central orchestration point; combine/package are reasonable companion commands, not competing generators.

However, direct invocation defaults to **v2** (`scripts/data/v2/build.py:42`), whose config has no `export` section; `Export.run` requires `run.config["export"]["tokenizer"]` (`src/constitutional_grafting/data/v2/export.py:33`). **Inference:** a fresh default chat build fails at export, potentially after paid work. Check by resolving the default config and running export on a fixture. `just data-v2` defaults to v3 instead.

Point the main README, AGENTS “Training-data practice” link, `scripts/data/README.md`, and `docs/data_pipeline.md` to `scripts/data/v2/README.md`. Label `data-build`/`data-documents` as the older checked-review pipeline, retaining historical replay. Moral-deliberation already says “Prototype and experiment evidence” (`scripts/data/moral_deliberation/README.md:3`); link directly to the new driver rather than only its plan.

The v2 README omits combine, fidelity and `10_identity`, calling step 10 `10_read` instead (`scripts/data/v2/README.md:33`). The package omits identity from `STAGES` and always prints “Teacher DeepSeek”, including Kimi v3/v4 (`scripts/data/v2/review_package.py:23,122`). Update these before relying on packages for review.

The range adds 17 `scripts/scratch/` experiments. They belong under `slop/` as research artifacts, or `scripts/data/` if maintained runnable stages, per AGENTS:136–137. Example: the fidelity calibration scorer reads one fixed experiment directory (`scripts/scratch/20261028_fidelity_calib_score.py:11–12`). Their historical utility is plausible; deletion as “dead” is not established.

### 2. DAG: structurally sound, not fully explicit

`Step` writes rejected rows before the completion marker and skips existing outputs (`src/constitutional_grafting/data/v2/pipe.py:47–60`). Named folders prevent collisions despite both Generate and Route using **04**. Renumber or document this clearly; it is not itself a cycle.

Hidden edges remain:

- Retry reads Jev/Judge rejection files independently of its input (`retry.py:20`).
- Seeds reads every preceding batch in config order (`seeds.py:119–123`). Thus fresh `medium` also requires earlier document seeds.
- v4 seed/request reuse is described only as pre-existing symlinks (`configs/data/v4.yaml:2`); the driver neither creates nor validates them. A clean checkout needs explicit bootstrap instructions and external source/tokenizer paths.

Existence-based skipping also means deleting only an upstream folder does **not** refresh downstream outputs. README:5’s “Delete the folder to rerun it” needs a downstream-invalidation warning. Test by changing an upstream fixture while retaining later outputs.

**Dropped check:** Edit computes `persona_left` but accepts solely on `changed_substance` (`edit.py:40–44,99–106`). An editor returning no edits can leave the very defect that triggered EDIT. Export screens teacher names, not general persona talk. Confirm with a no-op edit fixture scoring high on `persona_left`.

**Fidelity is best-effort, not a gate:** missing replacement spans are merely collected in `edits_not_found`; the answer is still returned (`route.py:126–134`). Later Jev/Judge checks provide protection, but there is no post-fix fidelity verification. Identity likewise catches any exception and retains the unedited row (`identity.py:59–60`). Neither proves corruption; both can make a successful build conceal failed repair objectives. Surface counts and test unmatched-span/API-error fixtures.

Full reading remains manual, not enforced before export. The newer route also composes another answer from retained notes; do not describe that as an untouched native reasoning/answer pair.

Paid caching works for saved responses, but “never pays twice” overstates it: `model_requests.py:68–73` explicitly retries possibly billed abandoned requests. Reconcile receipts before retrying where possible.

### 3. Size and privacy

Parent-reported largest changed blobs:

- `RESEARCH_JOURNAL.md`: **436,234 B**
- `slop/reviews/20261027_v2_medium_package/filters.md`: **397,444 B**
- `slop/reviews/20261027_v2_small_package/judge.md`: **368,629 B**
- `slop/reviews/20261027_teacher_test_v2/packets/w2s_baby_eating_aliens.md`: **354,870 B**

Reported aggregate: **13,520 KB**. Six `rejections_by_stage.png` binaries are listed at input-artifact:205–210. Review packets are generated data, but AGENTS permits committed reviews; binary presence alone is not a defect. No standalone book file appears in the range inventory. Embedded private passages remain **unverified**: inspect packet contents against private sources before publication. Uncommitted book material is outside this review.

### 4. Disk and smoke

Reported `data/cache` is **1.9 GB**, scratch **271 MB**. A comparable v4 rebuild should comfortably fit workspace; that is an estimate, not a measured peak. Keep model caches/downloads off root. Rental downloads fit only conditionally: obtain checkpoint count, sizes and temporary duplication requirements first.

Maintained checks include `check`, `check-projection`, `check-demos`, `check-frontier-exports`, legacy `data-smoke`, replay, and stubbed `run16-driver-dry-run`. No dedicated v2 smoke exists.

The supplied check result is exit 0. The complete v4 log shows **40 exported rows**, loss-mask success and exit 0, but uses another worktree and skips seeds/requests. It does not establish clean bootstrap, document-branch coverage or offline cache-miss behavior.

AGENTS:134 requires local-GPU tiny-random execution of the real driver before rentals. Parent reports only a rental-side smoke and unavailable local GPU tooling. That prerequisite remains unmet.

-- GPT reviewer