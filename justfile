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
    uv run --locked python tests/regression/test_rental_retrieval.py

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

# Run-10 training data from cached sources, scores, reviews and repairs; no model calls. Fails if any training file's sha256 changes.
# Paid steps that produced the caches: 71 (identity rows), 75 (chunk scores), 78 (general-row screen); Sol reviews chose the 50 reverts and 310 drops. -- PI/Claude
run10-data:
    uv run scripts/data/72_stoic_corpus.py
    uv run scripts/data/72_stoic_corpus.py select
    uv run scripts/data/74_other_traditions_corpus.py build
    uv run scripts/data/74_other_traditions_corpus.py select
    uv run --with 'transformers>=4.57' --with jinja2 --with loguru --with httpx python scripts/data/77_general_instruction.py
    uv run --with 'transformers>=4.57' --with jinja2 --with loguru --with httpx python scripts/data/73_chat_set_v3.py
    uv run python scripts/data/76_run10_train_files.py > /dev/null
    git diff --exit-code data/train/run10/manifest.json && echo "run-10 training files reproduced byte for byte"

# Run 10 rentals (paid, vast.ai): one finite lease each; retrieves adapters to ~/.local/share/cg_run10_adapters and logs to slop/eval/run10/<stage>/, then destroys the box. -- PI/Claude
run10-stage1 hours="9":
    uv run --no-project scripts/eval/37_run10_rental.py run --hours {{hours}}

# Chat adapters on Base + A_STOIC·ΔStoic (env A_STOIC, CHATS, CELLS; defaults in the script), then grafts on Instruct.
run10-stage2 hours="10":
    uv run --no-project scripts/eval/38_run10_chat_rental.py run --hours {{hours}}

# Run-10 results page + full verbatim demo panel from downloaded records; no model calls. -- PI/Claude
run10-results:
    .local/tiny-character/.venv/bin/python scripts/eval/42_run10_results.py docs/results/20261022_run10.md --runs slop/eval/run10/stage1/box_runs slop/eval/run10/stage2/box_runs --strength slop/eval/run10/strength --judged slop/eval/run10/stage1/judging/doses slop/eval/run10/stage1/judging/high_doses slop/eval/run10/stage2/judging/cells --summary slop/eval/run10/stage2/reading.md
