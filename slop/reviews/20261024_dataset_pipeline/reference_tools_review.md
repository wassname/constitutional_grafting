# Research: independent dataset-tool comparison

## Summary
Keep the small library; no inspected replacement justifies migration now. Fix judgement-setup invalidation and document-check typing before new production generation.

## Findings
1. **LASR is a recipe reference, not drop-in plumbing.** Root README:361ff calls it “self-contained,” but inspected `ours/pipeline.py` imports `src.naming`, `src.utils`, `src.infra.huggingface`, operators and endpoint machinery. Its generation/rewrite operators and independently runnable corpus checks are useful references; extraction requires import, schema and publication adaptation. [Repository](https://github.com/Matthew-Bozoukov/teaching_claude_why_replication)

2. **LASR resumes stale content.** `pipeline.py::run` executes `if not st.observer and cache.has(pos, st.name): records = cache.load(...)`. `hf_cache.py::StageCache.has` checks file existence; `stage_runtime.py::Checkpoint/run_items` skip by record key, default `scenario_id`, not content hash. Changed prompts/upstream inputs can reuse stale snapshots; deleting one snapshot still leaves partial checkpoints and downstream snapshots. Manifest constitution/config hashes do not gate reuse. Our `model_requests.py::request_key` instead hashes endpoint/body/attempt, including rendered prompts. Changing E’s attempt preserves D; changing constitution invalidates the requests containing it.

3. **LASR’s publication defaults are unsuitable for private books.** `pipeline.py::run` uses `cfg.get("hf_push", True)` and `cfg.get("hf_private", False)`; `StageCache` mirrors snapshots/finals/manifests. Explicitly disable HF push. Our inspected builders write locally; credentials load inside `api_headers`, with sending separated behind budgeted commands. Offline building does not authorize later private-source transmission.

4. **Unsloth is Data Designer’s UI, not another engine.** Documentation says “powered by NVIDIA Nemo Data Designer”; recipes are “stored locally in the browser,” outputs are local, publishing optional, and self-hosted OpenAI-compatible endpoints supported. These are documentation claims, not a privacy audit. It does not demonstrate replacement of subscription judgements, full reads or pinned historical replay. [Documentation](https://unsloth.ai/docs/new/studio/data-recipe)

5. **Data Designer’s resume is stronger but differently scoped.** [Architecture docs](https://github.com/NVIDIA-NeMo/DataDesigner/blob/main/architecture/dataset-builders.md) describe fingerprint-compatible row-group resume. Inspected `packages/data-designer-engine/src/data_designer/engine/dataset_builders/dataset_builder.py` compares stored hash/version and clears partial results: unfinished row-group work is not our per-request durable reuse. Legacy missing metadata/config paths can return COMPATIBLE; external seed-content hashing remains unverified. Inspected `engine/models/telemetry.py` defaults `NEMO_TELEMETRY_ENABLED` to `"true"`, sending model/task/token/byte metadata to NVIDIA. Disable before import for offline use; this is not evidence of document-text telemetry. Engine dependencies include pandas, PyArrow, DuckDB, NetworkX, MCP and SciPy. [Source](https://github.com/NVIDIA-NeMo/DataDesigner)

6. **Distilabel is a useful invalidation reference.** Docs promise intermediate recovery and changed-step/dependent regeneration using topology/parameter signatures. External seed-file content hashing, implementation and offline defaults were not audited. [Caching documentation](https://distilabel.argilla.io/latest/sections/how_to_guides/advanced/caching/)

7. **Our correctness gaps:**
   - `training_example_judgements.py::prepare_judgements` hashes reviewer dictionary/workflow JS, not resolved named reviewer-agent/system instructions. `run_training_example_judges.js` selects that agent by name. Changing its definition can reuse approvals, contrary to the broader setup-invalidation claim. Bind resolved reviewer specifications or explicit versions; record execution identity.
   - `documents.py::parse_json_reply` checks JSON syntax only; E’s gate uses truthiness. With verdict `keep`, nonempty strings such as `acts_follow_reasons: "false"` pass the positive boolean checks when `invented_real_world_facts` is false. Require a strict E schema. Later independent reviews are additional gates, not type validation.

## Replacement/deletion recommendation
**Replace none now.** Overlap is principally `model_requests.py` (roughly 180 lines), not historical/source assembly or approval logic. No inspected replacement preserves immutable receipts, budget controls and no-resend semantics unchanged: **zero lines safely removable on current evidence**. Consider extracting LASR’s surface corpus-diversity checks after import/license review; that adds coverage rather than deletes code.

## Coverage and gaps
Read approval/verification/provenance; local synth README and root README section; LASR run/cache/checkpoint code and corpus-check opening; our complete chat/documents/files/request/judgement modules, workflow/config and regression tests. Fetched public documentation and selected Data Designer code directly; no paid search/model APIs, installs, vendor execution, credentials or private uploads. Parent replay/test claims were not rerun; commit/worktree identity unverified. Public main is unpinned; full dependency/privacy audits remain. No page-fetch failures; guessed local reviewer-agent path was absent, leaving its resolved definition uninspected.

```acceptance-report
{
  "criteriaSatisfied": [{"id":"criterion-1","status":"satisfied","evidence":"Independent source comparison, deletion scope, correctness findings and limitations recorded."}],
  "changedFiles": ["slop/reviews/20261024_dataset_pipeline/reference_tools_review.md"],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": ["Static inspection only."],
  "residualRisks": ["Live integration, seed hashing and resolved reviewer definition unverified."],
  "noStagedFiles": true,
  "diffSummary": "Review artifact only.",
  "reviewFindings": ["Reviewer definition changes can reuse approvals.", "Document E lacks strict boolean validation."],
  "manualNotes": "No staging operations; staging state not checked. Parent verification treated as claims."
}
```
