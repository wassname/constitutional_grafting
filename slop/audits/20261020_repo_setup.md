# Repository setup audit

PI/Sol, 2026-10-20. Scope: safe local setup and replay; leave the active rental/source snapshot and unrelated work intact.

## Verdict

Not fully clean or fresh-clone reproducible. The broad paths are sensible, but the current run has machine-local dependencies and no full tiny training/grafting/evaluation smoke. Those are open issues, not covered by passing unit checks.

## Fixed and checked

- Added a root CPU `pyproject.toml`, `uv.lock` and Python3.12 selection. Eight-day dependency hold retained, equal to the existing global hold. GPU training packages are not installed into this CPU environment.
- `just setup`, `just check`, `just results exact1` are the current local entry points. Parsing/rebuilding older frontier/Gemma data is explicitly separate; `just check` no longer rewrites training exports.
- `just results` is offline. The old paid run-one report is explicitly named `run1-report`, not a generic report default. Historical remote execution requires an explicit stage.
- Pinned evaluator path is project-local `.local/tiny-character`, or explicit `TINY_CHARACTER_DIR`; protocol hashes must match. On this machine that path is a symlink to the unchanged existing pinned checkout, not a modified evaluator.
- Ignored only machine caches/editor state (`.vscode`, `.pytest_cache`, pyc); did not hide experiment evidence, delete results or stage human files.
- Passed `uv lock`, `uv sync --locked`, `just --dry-run`, `just check`, `just results`. Python3.12.3;43locked packages;125Python and19shell files checked;10maintained replay/format tests pass. Actual log: `.local/repo-setup/check.log`.
- Recorded installed training/inference package versions in `slop/eval/run9/exact1/software_versions.json`, using metadata only: no model loading or new inference. This is a version snapshot, not an immutable image digest/wheel lock.

## Path map

| Path | Meaning |
| :--- | :--- |
| `constitution/` | Character source and rendered text |
| `data/subsets/train_*.jsonl`, matching metadata/manifest | Frozen current donor-training inputs |
| `configs/train/qwen3/` | Reference training settings; per-run resolved settings are authoritative |
| `scripts/{data,train,eval}/` | Runnable stages; historical numbered scripts remain |
| `slop/eval/run9/<lease>/box_runs/` | Copied raw run evidence; only completed cells enter reports |
| `slop/eval/run9/<lease>/{estimates.md,demo_panel.md}` | Generated current results and full demos |
| `.local/` | Ignored private runtime state and local evaluator alias |
| `~/.local/share/cg_run9_adapters/` | Binary weights on this machine, not a portable artifact registry |

## Remaining gaps

1. No true `fast-dev-run` through donor train → merge → generation → judge → heal → remerge/eval, with tiny scale and runtime type checks. Current inference smoke and10unit tests do not establish that. Do not create a fake smoke alias or claim training passed.
2. GPU image is named by a dated tag, not proven pinned to its executed digest. vLLM itself is pinned, but its full transitive environment was installed without a committed GPU lock. Version capture improves auditability, not exact environment recreation.
3. Weights have verified SHA-256 values but only a machine-local location; no published/private artifact-fetch recipe. Raw replies/configs are unevenly committed across historical runs. A fresh clone cannot yet recreate every report or download every saved adapter with one command.
4. README/AGENTS and other files already had unrelated uncommitted edits; preserve them. This audit adds local setup information without pretending the whole working tree is clean. Before this pass there were13modified and598untracked files, mostly historical/current evidence, not598independent code problems.
5. Many historical stage scripts and run folders remain; they should be simplified by dependency tracing after this comparison, not moved/deleted while a rental and report depend on them.

## Replaying local results

```bash
uv sync --locked
git clone https://github.com/wassname/tiny-coherent-character.git .local/tiny-character
git -C .local/tiny-character checkout 2d697390de6ddc4f75de272f36750186f04c724d
just check
just results exact1
```

The last command needs the retained run records; it neither rents a GPU nor judges new answers. Paid judging additionally uses the pinned evaluator's recorded environment; that environment bootstrap has not been tested from a fresh clone here.

Next: finish the approved comparisons, commit/fetch the required evidence and weights, then add one real scale-only tiny pipeline workflow instead of more per-bug test files. Do not weaken the dependency hold, replace the pinned evaluator, or interrupt the active job for a directory reshuffle.
