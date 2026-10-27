# Moral deliberation data

Prototype and experiment evidence. New production builds follow `docs/plans/20261027_reasoning_dataset_v2.md` and its versioned-file layout. Do not carry this prototype's own-data hash/manifest scaffolding into that build; retain hashing for paid request caching.

Kimi answers source-grounded questions with Musonius's constitution in context. Its provider-exposed notes and answer are preserved together. Cached Haiku checks assist a full-pair read; they do not approve training data. No downstream learning result has been shown.

Cost prototype: `slop/data/moral_deliberation/20261027_cost_quality_review/report.md`. Four fresh questions, low versus max, all eight pairs read. Initial 40-pair audit: `slop/data/moral_deliberation/20261027_pilot/report.md`. Opus review was blocked; Haiku returned labels. No training export is approved.

## Stages

Run from the repository root with `uv run --no-sync python scripts/data/moral_deliberation/<script>`. `RUN` is a single directory name beneath `slop/data/moral_deliberation/`.

| Stage | Command arguments | Output |
|:--|:--|:--|
| Freeze | `01_select.py RUN --source SEEDS.jsonl --n-per-shape SOURCE=COUNT … --cap-usd X` | Seeded `prompts.jsonl`, config, frozen system texts and source snapshots |
| Generate (paid, explicit batch) | `02_generate.py RUN --batch 0` | Shared full request/HTTP cache under `.local/moral_deliberation/shared_api/`, usage and extracted `raw.jsonl` |
| Verify completed replay (offline) | `02_generate.py RUN --batch 0 --offline` | No request; an incomplete run fails before networking |
| Cached Haiku checks (paid on cache miss) | `07_cached_quality.py WORK --runs RUN_PATH … --cap-usd X` | Blind whole-pair labels, exact evidence checks, raw receipt and shared request cache |
| Verify Haiku replay (offline) | Same command with `--offline` | No request; missing cache fails |
| Screen (offline) | `03_screen.py RUN` | Regex flags and quotes, never automatic filters |
| Prepare judge input (offline) | `04_judge_packets.py RUN --batch 0` | Complete candidate groups, frozen rubric and material hashes |
| Judge (explicit Opus subagent or batch) | Follow `judge/rubric.md`, read the packets, return JSONL under `judge/replies/` | Reviewer labels; preserve model/run identity and attempts separately |
| Validate and merge (offline) | `04_judge_packets.py RUN --batch 0 --merge` | Hash/quote/coverage-checked `judged.jsonl`; fails if incomplete |
| Report (offline) | `just moral-deliberation-report RUN` | `report.md`, full seeded example groups and reader findings |

The initial pilot report consumes `spot_check_selection.json`, `reader_verdicts.jsonl` and `reading_notes.md`; these are review inputs, not automatic approvals. `06_review_results.py RUN` validates the initial native-process and whole-pair reviews separately. Reader and model labels remain separate. The cost prototype also records `parent_reads.jsonl` and `cost_quality.json`.

Framings: `const` adds “your constitution … follow it”; `self` supplies the first-person text alone. Both preserve the original conversation's role-specific system messages. The teacher sees no guide, visible-reasoning format request or previous target answer. Defaults are one draw, first-person framing, explicit low effort, 10 prompts per batch and seed 27. The initial factorial pilot used two framings and two draws; its frozen settings are unchanged. Native shorthand, planning voice and keyword matches are not automatic defects.

New paid runs use this project's `.env` through the maintained `constitutional_grafting.data.model_requests` transport. It saves exact requests/responses, refuses duplicate submissions, and leaves unresolved attempts for inspection. Cache identity includes the complete request, model, parameters and sampling attempt, not the run name. Prior run caches are imported without altering their receipts. A reused completion is not an independent new draw. A per-run lock and worst-case in-flight reservations bound the configured cap. Use one worker for small caps; concurrent worst-case reservations can hold back unsent jobs even when actual costs are low. Moonshot AI is pinned by default, with fallbacks disabled. Changing model/provider is an explicit configuration decision, not a retry policy.

The first batch used earlier code. Its source snapshot is kept in the run, and its missing wire envelopes are recorded in `provenance/manifest.json`. Do not treat reconstructed requests as contemporaneous captures. The maintained generator can replay that completed batch offline, but refuses new paid requests in the legacy run; freeze a new run for new sampling.

No training export, GPU run or automatic scaling is part of these commands. Real API calls require a separately approved budget. No requests are made by report rebuilding or a complete cache replay. A frozen-input hash rejects edited prompts, system text or config before call-ID cache reuse.

`00_seed_sources.py` is an offline source-import prototype, with explicit `--fetch-wildchat` for pinned acquisition. Fresh seed/layout/export work is owned by the v2 plan in `docs/plans/20261027_reasoning_dataset_v2.md`. `08_language_pilot.py` is prepared but unexecuted; its translations must be labelled and checked, not presented as native English notes. No book text may be published.

Regression checks: `uv run --no-sync python -m unittest discover -s tests/regression -p 'test_moral_deliberation.py' -v`.

-- PI/Claude; revised PI/OpenAI (Sol)
