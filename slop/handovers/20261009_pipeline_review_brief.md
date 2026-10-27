# Brief: review the data v3 frontier pipeline (code quality, repeatability, caching, metadata)

Written by Claude (Opus 5.5) for an astra review subagent, 2026-10-09. wassname asked for a review of "code quality, dataset pipeline, repeatability, caching, metadata cleanliness".

## What the pipeline does

Builds training data for an open-weight model (gemma-4-31b) to take on the character "Musonius" from `constitution/v4.md`. Seeds (situations from other corpora, never their answers) are turned into chat replies (SFT) and documents by frontier writers run through plain `pi` subprocesses, one batch file per call, paced per provider account. Plan: `slop/plans/20261009_data_v3_plan.md`. Reads of outputs: `slop/reviews/20261009_frontier_batches/`.

## Files to review (read all)

- `scripts/data/25_seed_pool.py` (seed pool: sources, stable hash ids, caching in data/raw)
- `scripts/data/scratch/25b_seed_stakes.py` (extra hand-listed seeds)
- `scripts/data/26_frontier_batches.py` (make / next / mark / parse / split / reset_unrun; brief text; pacing; structure check; lint; provenance `meta`)
- `scripts/data/27_run_frontier.sh` (per-account runner calling pi)
- `scripts/data/03_prompt_pools.py` only the functions `wildchat`, `machiavelli`, `best_actions` (reused by the pool)
- State and outputs to inspect, not edit: `data/frontier/sft/batches.jsonl`, `data/frontier/sft/batch_*.md`, `data/frontier/sft/out_*.md`, `data/frontier/sft/items.jsonl`, `data/prompts/v3_seeds/*.jsonl`, `data/prompts/v3_seeds/counts.md`

## Questions

1. Correctness bugs: anything that silently loses, duplicates or mislabels seeds or items (append-only make, split, reset_unrun, parse, numbering, locking between parallel lanes, the runner's error paths, bash editing hazards).
2. Repeatability: can someone rebuild the same seed pool and batch briefs from the repo plus cached downloads? What is not pinned (dataset revisions, model versions served, pi version, thinking level)? What should be recorded per batch that is not?
3. Caching and resumability: what happens on crash mid-batch, provider block mid-stream, partial output, rerun of make, rerun of the pool with bigger targets?
4. Metadata cleanliness: is every item traceable to its seed, source, writer, brief and time? Are fields consistent (e.g. `framing`/`form` set in make but used in parse)? Anything misleading?
5. Validation: does the structure check and lint catch the failure modes it claims? False positives / negatives you can see.
6. Code quality against the project's own conventions (`AGENTS.md`, wassname's: fail fast, no defensive fallbacks, minimal comments for the next reader, simple over clever).

## Output

Write `/workspace/2026/constitutional_grafting/slop/reviews/20261009_pipeline_review_astra.md`: a ranked list of findings (severity, file:line, what goes wrong, a concrete fix), then short answers to 1-6. Quote code lines. Do not edit any other file. Sign it with your harness/model.
