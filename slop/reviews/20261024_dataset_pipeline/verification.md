# Dataset pipeline: implementation and verification

Implemented the approved small-library/thin-command layout. Cached replay checks runtime; no new training corpus or prompt-quality result is claimed.

## Before → after

- Separate `80`/`83`/`86`/`88` scripts and date-bound directories → one fixed chat build, numbered stages, explicit input and output names.
- Repeated API clients and credentials read on import → shared request/response cache, lazy project-local credentials, explicit budgets and pre-send/submission receipts.
- Verdicts attached by row id, identity filtering and unanimous-objection wording → exact membership/content/setup binding, identity included, actual disagreements retained, rejected rewrites block export.
- All A–E work held until a document finishes → per-step saved results, independent rechecks and feedback-based rewrites with immutable original artifacts.
- Builders writing active training releases → pinned offline replay into a separate directory; existing training/eval consumers stay unchanged.

Reusable functions: `src/constitutional_grafting/data/`. Commands: `scripts/data/{build_chat_dataset,generate_constitution_documents,cached_model_requests,reproduce_training_datasets,smoke_dataset_pipeline}.py`. Maintained usage: `docs/data_provenance.md`. Vocabulary: `jargon.md`.

## Observed checks

| Check | Observation | Evidence |
|:--|:--|:--|
| Historical replay | All 12 run10 and 11 run11 expected file hashes match | `final_replay.log` |
| Cold runtime smoke | 2 actual cached chats + 1 actual cached A–E document; 1.05 s; $0 API/GPU | `cold_smoke.log` |
| Chat transformations | Historical accepted rewrite applied; warranted refusal retained; repeat output hash identical; edited user context becomes pending | `cold_smoke.log`, `.local/dataset_pipeline/cold_smoke_final/smoke_result.json` |
| Document resume | A–E replayed; changing only E's attempt leaves D's artifact hash unchanged; missing document judgements prevent export | Same smoke result |
| Regression checks | 7 pass, including identity classification, stale judgement/rewrite rejection, double-submit guard, complete context and rejection blocking export | `regression.log`, `tests/regression/test_dataset_pipeline.py` |
| Protected files | 23 release files and 8 other consumers unchanged; only the peer-owned current `89` differs | `protected_audit.json` |
| Subscription workflow | Static validation returned `ok: true`; execution not yet verified | Native `subagent action=validate`; workflow file |

Commands:

```bash
just data-smoke
uv run --locked python scripts/data/smoke_dataset_pipeline.py --output .local/dataset_pipeline/cold_smoke_final
uv run --locked python tests/regression/test_dataset_pipeline.py
just data-replay run11 .local/dataset_pipeline/final_replay_run11
```

Run11 replay also rebuilds and checks run10. Expectations were not regenerated from the new outputs. The cached smoke imports actual historical writer/classifier/reviewer artifacts with their source hashes, explicitly marks them historical, and exports only `smoke_only`. Its full-read fixture says `READ_FOR_RUNTIME`, which a production build does not accept as training approval. It does not establish that the revised prompts produce good data.

## Shared-worktree change caught by replay

The first final replay stopped with:

> changed historical input: scripts/data/89_run11_data.py: be5f3a4fd32e0e4cbe281a0cfec1155dc2497d1d6bf43a06d21281ca7d2f3142 != f9bf1ee0ebc9877b57b2c2db514aaa6f0698a8bb058bea6bd911c9fdc777cefa

`const_v2` confirmed ownership: it added a separate matched-control command, without changing the original docs/chats outputs (intercom `ce65e60c-6c93-4e9b-8076-308ee2fa4fc4`). This refactor did not change or revert that file. Replay now reads the exact historical `89` from git `045d6d615626ccebd5b610e87456aec0fcffc50e`, verifies its original hash, and saves it under the separate replay output. Final replay passed the unchanged expected data hashes.

## Limits and remaining checks

- No OpenRouter generation/submission was run during implementation. Sync/batch live integration is not established by a cached runtime smoke; full raw attempts/results are retained for later approved tests.
- The requested independent glossary/reference-tools children initially failed before starting: native host dependency resolution reported missing `@earendil-works/chord` and `@earendil-works/chord/context` (workflow `b7a978b2-ce61-4de7-84e6-c84c909f55e3`). No child output exists from that attempt. Parent source reading is attributed in `approval.md` and `jargon.md`.
- New prompt pilots, real-world factual checks, full reads and the normal budget approval remain required before new training. No lease, training command, model merge or held-out evaluation file was changed by this refactor.

-- PI/OpenAI (Sol)
