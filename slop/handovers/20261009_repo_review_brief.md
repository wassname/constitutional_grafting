# Brief: repo review against wassname's conventions (setup-repo), read-only

Written by Claude (Opus 5.5), 2026-10-09, for a Herdr pane agent. wassname: "maybe run /review re /setup repo and so on".

Repo: /workspace/2026/constitutional_grafting. Read first: AGENTS.md (repo and ~/.pi/agent/AGENTS.md), the `setup-repo` skill (~/.pi/agent/skills/setup-repo/SKILL.md), `clean-repo` and `token-efficient-logging` skills, RESEARCH_JOURNAL.md (last 3 entries), the earlier review `slop/reviews/20261009_pipeline_review_astra.md` (findings 2, 5, 6, 7, 10, 11 are still open).

## What to review

1. **Conventions (setup-repo):** no pyproject/uv project, no justfile, no `just fast-dev-run` smoke test. What is the minimal setup that fits this repo (data scripts run with `uv run` and inline deps; training runs on a rented box via Axolotl)? Propose a concrete justfile (recipes and the commands they run), and say what a smoke test of the real pipeline would cover here (data -> 01_prepare -> a tiny training step -> one eval) without a GPU or with a tiny model.
2. **Entry points and paths:** is it obvious where to start, and what each file under `scripts/` is for? Dead or superseded scripts (scripts/data 02-11 and 20-21 are the v1/v2 pipelines; scripts/scratch has many experiments): which can go, which feed current data. Semantic paths (numbering gaps, `25b_`, `astra_echo/` package next to numbered scripts).
3. **Current data pipeline** (26, 27, 28, 29, 30 + scripts/data/astra_echo/, 31, 32; constitution.py): repeatability, caching, resume, provenance in `meta`, fail-fast vs silent fallbacks, duplicated code (e.g. OpenRouter/Echo clients, lint, section parsing), and concurrency (parallel shards append to one items.jsonl; batches.jsonl under a lock).
4. **Training and eval** (scripts/train/01-06, configs/train/*.yml, scripts/eval/10, 15, 16): does 01_prepare build what the configs read; is the loss mask right (read data/train/examples.md); are evals reproducible; is the run-2 eval plan in 03_remote.sh correct.
5. **Docs:** is there one maintained source of truth (README vs AGENTS.md vs spec vs plans), or stale copies that disagree with the code?

## Rules

- **Read-only.** Do not edit code, data or configs: three pipelines are running (pueue group api: Opus docs lane, Echo restyle shards, astra->Echo lanes owned by another pane agent). Commit only your report.
- Findings with file:line and a quote of the code; rank by impact on the research (wrong training data or silent data loss first, cosmetic last); for each, the smallest fix. Separate observation from inference; use calibrated words.
- Say what is fine, too, briefly.
- Report: `slop/reviews/20261009_repo_review.md`, signed. Then message the parent session via intercom with the path and the top 5 findings.
