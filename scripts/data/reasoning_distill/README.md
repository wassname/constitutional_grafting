# Reasoning distillation

Kimi answers training conversations with Musonius's constitution in context. Its provider-exposed reasoning and answer are preserved together. Opus reviews the candidates against wassname's reasoning criteria and the constitution. This tests candidate-data quality; no downstream reasoning improvement has been shown.

Current first-batch result: `slop/data/reasoning_distill/20261027_pilot/report.md`. Opus judging was blocked after one honest retry; nothing is training-approved. Only batch 0 ran.

## Stages

Run from the repository root with `uv run --no-sync python scripts/data/reasoning_distill/<script>`. `RUN` is a single directory name beneath `slop/data/reasoning_distill/`.

| Stage | Command arguments | Output |
|:--|:--|:--|
| Freeze | `01_select.py RUN --n-per-shape seeded_dilemma=20 ordinary=3 … --cap-usd X` | Seeded `prompts.jsonl`, config, frozen system texts and source snapshots |
| Generate (paid, explicit batch) | `02_generate.py RUN --batch 0` | Full request/HTTP receipts under `api/`, usage, extracted `raw.jsonl` |
| Screen (offline) | `03_screen.py RUN` | Regex flags and quotes, never automatic filters |
| Prepare judge input (offline) | `04_judge_packets.py RUN --batch 0` | Complete candidate groups, frozen rubric and material hashes |
| Judge (explicit Opus subagent or batch) | Follow `judge/rubric.md`, read the packets, return JSONL under `judge/replies/` | Reviewer labels; preserve model/run identity and attempts separately |
| Validate and merge (offline) | `04_judge_packets.py RUN --batch 0 --merge` | Hash/quote/coverage-checked `judged.jsonl`; fails if incomplete |
| Report (offline) | `just reasoning-distill-report RUN` | `report.md`, full seeded example groups and reader findings |

The report consumes the run's `spot_check_selection.json`, curated `reader_verdicts.jsonl` and `reading_notes.md`; these are review inputs, not automatically generated approvals. Current files provide the initial example. Reader and Opus labels remain separate.

Framings: `const` adds “your constitution … follow it”; `self` supplies the first-person text alone. Both preserve the original conversation's role-specific system messages. The teacher sees no guide, visible-reasoning format request or previous target answer. Default k=2 draws per framing, 10 prompts per batch, seed 27. Native shorthand, planning voice and keyword matches are not automatic defects.

New paid runs use this project's `.env` through the maintained `constitutional_grafting.data.model_requests` transport. It saves exact requests/responses, refuses duplicate submissions, and leaves unresolved attempts for inspection. A per-run lock and worst-case in-flight reservations enforce the configured cap. Moonshot AI is pinned by default, with fallbacks disabled. Changing model/provider is an explicit configuration decision, not a retry policy.

The first batch used earlier code. Its source snapshot is kept in the run, and its missing wire envelopes are recorded in `provenance/manifest.json`. Do not treat reconstructed requests as contemporaneous captures. The maintained generator can replay that completed batch offline, but refuses new paid requests in the legacy run; freeze a new run for new sampling.

No training export, GPU run or automatic scaling is part of these commands. Real API calls require a separately approved budget. No requests are made by report rebuilding or a complete cache replay.

Regression checks: `uv run --no-sync python -m unittest discover -s tests/regression -p 'test_reasoning_distill.py' -v`.

-- PI/Claude; revised PI/OpenAI (Sol)
