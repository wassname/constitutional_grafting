# Local checks and reports; GPU training uses the recorded Axolotl image. -- PI/Sol
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# Locked CPU dependencies; no model downloads or calls. -- PI/Sol
setup:
    uv sync --locked

# Source checks and maintained format/replay checks; NOT a full training smoke. -- PI/Sol
check:
    uv run --locked python scripts/train/07_cpu_check.py --syntax-only
    uv run --locked python tests/regression/test_demo_panel.py
    uv run --locked python tests/regression/test_gsm8k_cutoff.py
    uv run --locked python tests/regression/test_heal_review_gate.py

# Current22-condition comparison from downloaded records; no model calls. -- PI/Sol
results lease="exact1":
    uv run --locked python scripts/eval/35_subset_report.py --exact {{lease}}

# Full figure requires all22 completed/graded conditions; no model calls. -- PI/Sol
results-plot lease="exact1":
    uv run --locked python scripts/eval/35_subset_report.py --exact {{lease}} --plot

# Earlier norm-matched diagnostics, not substitutes for the exact-dose grid. -- PI/Sol
diagnostic-results:
    uv run --locked python scripts/eval/35_subset_report.py

# Historical Gemma/frontier exports; rebuilding these writes data/train. -- PI/Sol
parse-frontier:
    uv run scripts/data/26_frontier_batches.py parse docs
    uv run scripts/data/26_frontier_batches.py parse sft

prepare-frontier:
    uv run scripts/train/01_prepare.py

check-frontier-exports:
    uv run --no-project scripts/train/07_cpu_check.py

check-demos:
    uv run --locked python scripts/train/04_demo_smoke.py

# Run-1 only; can call the paid Jev judge for uncached replies. -- PI/Sol
run1-report:
    uv run scripts/eval/16_run1_report.py

# Historical remote stages; an explicit stage is required. -- PI/Sol
run1-remote stage *more:
    bash scripts/train/03_remote.sh {{stage}} {{more}}
