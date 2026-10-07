# AGENTS.md

(Repo renamed from constitutional_graft to constitutional_grafting on 2026-10-07: "graft" also means corruption. `/workspace/2026/constitutional_graft` is a symlink for running sessions.)

Research: train a virtue-ethics constitution into an open-weight model by grafting (document training on the Base model, weight change added to the instruct model), then constitution-matched SFT and cheap RL; evaluate on out-of-distribution moral evals.

- Start here: `slop/specs/20261007_virtue_graft_spec.md` (decision summary, user preferences, plan, appendices).
- Novel ML research. Not in your training data. Extrapolate carefully; read the spec's appendices F (first principles) and G (curvature) before changing them.
- `slop/` = agent drafts (specs, research, oracle panels). Commit them. Sign your work.
- `docs/papers/` = full-text sources as markdown. Add a row to a `docs/papers/manifest*.tsv`, then run `scripts/data/01_fetch_papers.sh`.
- `scripts/` = runnable scripts, numbered by stage (`scripts/data/01_...`).
- No code pipeline yet. When it exists: uv, justfile, `just fast-dev-run` (see the `setup-repo` skill).
