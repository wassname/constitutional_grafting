# scripts/data reorganisation verification — 2026-10-27

## Scope and outcome

- Reconciled `0c989b13` (27 scripts already archived, EOS now 94) and the existing `data-corpora` recipe. Archived 28 remaining one-offs plus the two Astra support files; renamed 12 maintained CLIs, retained the import-only 77 shim. Added maintained/scratch maps; linked provenance once.
- Kept public just recipe names/arguments, current package modules, dataset/prompts/selection and release YAML expectations unchanged. `moral_deliberation/`, JS workflow and `scripts/train/01_prepare.py` were not edited. Other sessions' README/AGENTS/data/human/vendor/research changes are excluded from staging; the existing unstaged moral-deliberation recipe rename in justfile is preserved but excluded from this commit.
- Smoke passes. Run10: **12/12** output hashes; run11: **11/11** plus its nested **12/12** run10 hashes. Training files unchanged. New path tests: **6 passed**. Touched existing CPU regressions: **25 passed**, one real model merge/train/inference test deselected because this locked CPU environment has no PyTorch/PEFT; no GPU work performed.
- `just data-corpora` deliberately **not run** (writes in place). No teacher calls, new judgements, paid APIs, training or source-corpus rebuilds.

## Execution notes

The first run11 command into `.local/dataset_pipeline/replay_run11_reorg` was killed by the tool's hard 60s cap despite timeout=600. No hash mismatch occurred. Background shell execution is unavailable here. Supervisor reran the unchanged public recipe into the fresh `_retry` directory with process tooling; exit 0, full log `.local/scripts_reorg/replay-run11-retry.log` (supervisor appended `exit=0`). That successful replay is the accepted run11 evidence below.

An initial new path-test assertion incorrectly looked for `other.EVAL_TOPICS`; the real dependency is `other.st.EVAL_TOPICS`. Corrected that assertion; all six final tests pass. No production correction was needed.

Final all-tracked executable grep additionally found four dated review-package Python callers of 50/03. Supervisor explicitly approved resolving their original source bytes with `git show` at the pre-reorganisation commit `c55b00f7540dfe3b10c276780cf6d14072f092d1`, keeping old manifest keys/input hashes and as-run generator identity rather than updating expectations. Those scripts were syntax/pin checked, **not executed**, because they write historical review artifacts. Their existing manifests/data were untouched. Other historical prose, release git-tree keys and source-example metadata intentionally retain as-run paths; the README index locates current code.

Caller audit covered tracked Python/shell/JS/config files outside data/vendor and the active moral-deliberation branch, including basename and constructed-path searches (82 loader, eval23, review08, scratch fiction writers). Remaining old live-looking matches are comments, unchanged release git-tree keys, and the explicitly git-pinned review reads. Root checks parse all archived ROOT assignments without importing paid/side-effectful historical modules. Maintained/help import tests execute 13 real CLIs with `--help`; shim/filter tests use actual modules and cached renderer.

## Commands and output tails

Full runtime logs are local under `.local/scripts_reorg/`; persisted tails below contain the acceptance results.

### `just --list`

```text
Available recipes:
    answer-panel                         # Answer panel: every tiny-character question, each checkpoint's cropped replies grouped by answer; no model calls. -- PI/Claude
    check                                # Source checks and maintained format/replay checks; NOT a full training smoke. -- PI/Sol
    check-demos
    check-frontier-exports
    check-projection                     # Weight-projection maths on CPU torch in a throwaway env (the locked env has no torch). -- PI/Claude
    data-build recipe input name         # Offline build/resume; exits 2 with exact pending model/judgement jobs. Refusal checks are included. -- PI/Sol
    data-collect-batch record
    data-corpora offline="1"             # offline=1 stops instead of paying for unscored chunks. Writes data/stoic_corpus/, data/other_corpus/, data/train/run10/general.jsonl. -- PI/Claude
    data-documents recipe seeds name     # Fixed A–E document build, offline; shared model and judgement steps remain explicit. -- PI/Sol
    data-generate workdir budget_usd     # Explicit paid requests only; run the build again afterwards. -- PI/Sol
    data-replay release output           # Historical hashes are checked-in expectations; existing training files are read-only. -- PI/Sol
    data-smoke                           # Real tiny cached inputs, $0 API/GPU; runtime checks only, not prompt-quality approval. -- PI/Sol
    data-submit-batch workdir budget_usd # Batch alternative to data-generate; collect the printed record, never resubmit it. -- PI/Sol
    default
    diagnostic-results                   # Earlier norm-matched diagnostics, not substitutes for the exact-dose grid. -- PI/Sol
    heal-answer-panel                    # Both-mode thinking-heal answer panels from completed pinned judgments; no model calls. -- PI/OpenAI
    heal-summary                         # Verify recorded finals and regenerate run15 statistics/read packets; no model calls. -- PI/OpenAI
    moral-deliberation-report run        # Reasoning distillation: regex screen and report for RUN (no API calls); stages in scripts/data/moral_deliberation/README.md. -- PI/Claude
    parse-frontier                       # Historical Gemma/frontier exports; rebuilding these writes data/train. -- PI/Sol
    prepare-frontier
    reasoning-pilot                      # Rebuild full reasoning-pilot read/samples/summary from frozen cache; no API calls. -- PI/Sol (reader)
    results lease="exact1"               # Current22-condition comparison from downloaded records; no model calls. -- PI/Sol
    results-plot lease="exact1"          # Full figure requires all22 completed/graded conditions; no model calls. -- PI/Sol
    run1-remote stage *more              # Historical remote stages; an explicit stage is required. -- PI/Sol
    run1-report                          # Run-1 only; can call the paid Jev judge for uncached replies. -- PI/Sol
    run10-data output=".local/dataset_pipeline/replay_run10"
    run10-results                        # Run-10 results page + full verbatim demo panel from downloaded records; no model calls. -- PI/Claude
    run10-stage1 hours="9"               # Run 10 rentals (paid, vast.ai): one finite lease each; retrieves adapters to ~/.local/share/cg_run10_adapters and logs to slop/eval/run10/<stage>/, then destroys the box. -- PI/Claude
    run10-stage2 hours="10"              # Chat adapters on Base + A_STOIC·ΔStoic (env A_STOIC, CHATS, CELLS; defaults in the script), then grafts on Instruct.
    run12-results                        # Frozen paired-chat report and stage-separated figures; CPU only. -- PI/OpenAI (Sol)
    run14-results                        # Rebuild run14 metrics, figures and full/cropped panels without model calls. -- PI/OpenAI (Sol)
    setup                                # Locked CPU dependencies; no model downloads or calls. -- PI/Sol
```

### `just data-smoke`

```text
50_check_constitution_document: 1/1 saved stage results
10_analyse_source_reasoning: 1/1 saved stage results
20_derive_constitutional_reasoning: 1/1 saved stage results
30_plan_constitution_document: 1/1 saved stage results
40_write_constitution_document: 1/1 saved stage results
50_check_constitution_document: 0/1 saved stage results

## Result

Runtime passed in 0.50s. API/GPU cost: $0. These are historical-result replays, not new prompt-quality judgements.

| Pipeline                      | Runtime result   |   Examples | Checks                                                                    |
|:------------------------------|:-----------------|-----------:|:--------------------------------------------------------------------------|
| Chat rewrite + refusal checks | passed           |          2 | Accepted historical rewrite applied; warranted refusal retained           |
| Document A–E + recheck        | passed           |          1 | Recheck leaves the saved document intact; missing judgements block export |

Full result: `.local/dataset_pipeline/smoke/smoke_result.json`

Chat: `/workspace/2026/constitutional_grafting/.local/dataset_pipeline/smoke/processed/tiny_real_examples/chat.jsonl` (smoke_only, not a training release).
.local/dataset_pipeline/run.md
```

### `just data-replay run10 .local/dataset_pipeline/replay_run10_reorg`

```text
  "doc_3675c7b5e6"
 ]
}
fresh-loop edits applied: 0/0
chatr12: 895 rewritten replies, 102 kept old by review
chatr13: 38 refusal fixes, 173 plain-help rows
PASS run10: 12 pinned output hashes match; no training files changed
```

### `just data-replay run11 .local/dataset_pipeline/replay_run11_reorg_retry`

```text
2026-10-27 13:27:52.671 | INFO     | run11_packaging:write:73 - heldout_other: 200 rows, 136610 tokens
2026-10-27 13:27:53.057 | INFO     | run11_packaging:write:73 - heldout_const: 170 rows, 242908 tokens
2026-10-27 13:27:53.335 | INFO     | run11_packaging:write:73 - heldout_web: 200 rows, 127635 tokens
2026-10-27 13:27:59.077 | INFO     | run11_packaging:write:73 - chatr13: 1798 rows, 857795 tokens
2026-10-27 13:27:59.197 | INFO     | run11_packaging:write:73 - chatgen: 4685 rows, 858126 tokens
2026-10-27 13:27:59.421 | INFO     | run11_packaging:write:73 - chatmix: 6483 rows, 1715921 tokens
fresh-loop edits applied: 0/0
chatr12: 895 rewritten replies, 102 kept old by review
chatr13: 38 refusal fixes, 173 plain-help rows
PASS run10: 12 pinned output hashes match; no training files changed
PASS run11: 11 pinned output hashes match; no training files changed
exit=0
```

### `uv run --locked --extra data-replay python tests/regression/test_scripts_data_paths.py`

```text
....[transformers] PyTorch was not found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
..
----------------------------------------------------------------------
Ran 6 tests in 7.466s

OK
```

### `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 uv run --locked --extra data-replay --with pytest python -m pytest -q tests/regression/test_generic_control.py tests/regression/test_repair_checks.py tests/regression/test_thinking_heal_data.py tests/regression/test_dataset_pipeline.py tests/regression/test_heal_pipeline.py -k 'not test_real_model_merge_train_reload'`

```text
.........................                                                [100%]
25 passed, 1 deselected in 35.19s
```

### `uv run --locked python - <<'PY' # ast.parse/compile touched Python; bash -n touched shell; byte comparisons against HEAD`

```text
PASS: 79 moved/updated Python and shell files parse; no scripts executed
PASS: JS review workflow, training renderer and release YAMLs unchanged
```

### `uv run --locked python - <<'PY' # parse four review callers and verify git-pinned writer SHA against unchanged manifest`

```text
PASS syntax + pinned writer SHA: slop/reviews/20261019_docs_manual_repairs/verify.py
PASS syntax + pinned writer SHA: slop/reviews/20261020_curated_slice/export.py
PASS syntax + pinned writer SHA: slop/reviews/20261020_ordinary_help_package/prepare.py
PASS syntax + pinned writer SHA: slop/reviews/20261020_subset_package/make_samples.py
Historical package scripts not executed: they write review/data artifacts. Original manifest keys/hashes untouched.
```

### `git diff --cached --name-only # before staging`

```text
(empty: no staged files)
```

### `uv run --locked python - <<'PY' # trace one smoke export row through saved stages and EOS transform`

```text
PASS final row ask_55fb2542ca: 4 lineage operations; saved stage digest matches lineage; existing EOS export transform matches final row
Export row SHA256 05d8e9b978d52ff6a0f178b32a3c60684c669a74c080c7d53bb1ea3587a86e5f; request/result file SHA256 12f39936e2f6759f1100371fd0084d6a014255a800d4f60153c007f29c148c5e
No generation/submission invoked; changed-context smoke is pending with two missing requests.
```

Initial tracing compared the exported row directly to the pre-export stage hash; corrected the audit to account for the existing explicit `with_eot` export transform. No pipeline change was required.

### `git diff --check -- scripts tests justfile docs/data_provenance.md slop/reviews`

Passed, no whitespace errors.

## Limits / next review

- Full paid historical producer runs were not exercised; their root/literal dependencies and safe help entrypoints were checked without writing training data. Private source/tokenizer availability is still required for any actual rerun.
- The real-model regression needs the existing torch/PEFT model-test environment; this change only updates its historical module paths.
- Independent reviewer gate remains for the parent orchestrator. No data quality/training approval is inferred from structural/runtime checks.
- Explicit path staging used a justfile index blob containing only this migration's path changes; the other session's moral-deliberation recipe edits remain unstaged. See the shared-index commit incident below; final empty-index proof is reported with the task result.

## Commit packaging / shared-index incident

After all 86 rename-aware paths were explicitly staged and checked, the parent's concurrent commit `af8b83a4e5be87117857a27bb4a4bbdc50d8a96c` consumed this shared index before the worker's `git commit` ran. The worker commit returned “no changes added to commit”. Parent acknowledged the error and instructed: do not reset/amend; commit only any remainder with “completes the reorg committed in af8b83a4”.

Post-commit ownership comparison (`git diff-tree --no-commit-id --name-only -r --no-renames af8b83a4` against the explicit staging list) confirms **all 126 old/new path entries** (86 rename-aware changed files) are included. No migration code is missing or still unstaged. The only intersecting worktree change is the other session's pre-existing justfile moral-deliberation recipe rename; it is deliberately not included here. `git diff --cached --name-only` is empty. This audit packaging note is the only worker follow-up commit remainder.

The parent commit also contains its own data-practice guide, AGENTS link and writer-guidance change; those are **not** part of this worker's structural task. Therefore the reorg is not isolated in its originally requested single descriptive commit, and its trailer is the parent's existing combined attribution rather than the exact worker-requested one. No history rewrite was attempted.

Post-parent-commit `just data-smoke`: passed again ($0 API/GPU), output tail:

```text

Runtime passed in 1.29s. API/GPU cost: $0. These are historical-result replays, not new prompt-quality judgements.

| Pipeline                      | Runtime result   |   Examples | Checks                                                                    |
|:------------------------------|:-----------------|-----------:|:--------------------------------------------------------------------------|
| Chat rewrite + refusal checks | passed           |          2 | Accepted historical rewrite applied; warranted refusal retained           |
| Document A–E + recheck        | passed           |          1 | Recheck leaves the saved document intact; missing judgements block export |

Full result: `.local/dataset_pipeline/smoke/smoke_result.json`

Chat: `/workspace/2026/constitutional_grafting/.local/dataset_pipeline/smoke/processed/tiny_real_examples/chat.jsonl` (smoke_only, not a training release).
.local/dataset_pipeline/run.md
```

-- PI/gpt-6.1-sol, 2026-10-27
