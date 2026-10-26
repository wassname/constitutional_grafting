# Local checks and reports; GPU training uses the recorded Axolotl image. -- PI/Sol
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# Frozen paired-chat report and stage-separated figures; CPU only. -- PI/OpenAI (Sol)
run12-results:
    uv run --no-sync python scripts/eval/51_run12_results.py
    uv run --no-sync python scripts/eval/character_tradeoff.py

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
    uv run --locked python tests/regression/test_document_checks.py

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

# Offline build/resume; exits 2 with exact pending model/judgement jobs. Refusal checks are included. -- PI/Sol
data-build recipe input name:
    uv run --locked python scripts/data/build_chat_dataset.py --recipe '{{recipe}}' --input '{{input}}' --name '{{name}}'

# Explicit paid requests only; run the build again afterwards. -- PI/Sol
data-generate workdir budget_usd:
    uv run --locked python scripts/data/cached_model_requests.py generate --workdir '{{workdir}}' --budget-usd '{{budget_usd}}'

# Batch alternative to data-generate; collect the printed record, never resubmit it. -- PI/Sol
data-submit-batch workdir budget_usd:
    uv run --locked python scripts/data/cached_model_requests.py submit --workdir '{{workdir}}' --budget-usd '{{budget_usd}}'
data-collect-batch record:
    uv run --locked python scripts/data/cached_model_requests.py collect --record '{{record}}'

# Fixed A–E document build, offline; shared model and judgement steps remain explicit. -- PI/Sol
data-documents recipe seeds name:
    uv run --locked python scripts/data/generate_constitution_documents.py build --recipe '{{recipe}}' --seeds '{{seeds}}' --name '{{name}}'

# Real tiny cached inputs, $0 API/GPU; runtime checks only, not prompt-quality approval. -- PI/Sol
data-smoke:
    @mkdir -p .local/dataset_pipeline
    uv run --locked python scripts/data/smoke_dataset_pipeline.py > .local/dataset_pipeline/run.md 2>&1
    @tail -40 .local/dataset_pipeline/run.md
    @echo '.local/dataset_pipeline/run.md'

# Historical hashes are checked-in expectations; existing training files are read-only. -- PI/Sol
data-replay release output:
    uv run --locked --extra data-replay python scripts/data/reproduce_training_datasets.py --release '{{release}}' --output '{{output}}'
run10-data output=".local/dataset_pipeline/replay_run10":
    just data-replay run10 '{{output}}'

# Run 10 rentals (paid, vast.ai): one finite lease each; retrieves adapters to ~/.local/share/cg_run10_adapters and logs to slop/eval/run10/<stage>/, then destroys the box. -- PI/Claude
run10-stage1 hours="9":
    uv run --no-project scripts/eval/37_run10_rental.py run --hours {{hours}}

# Chat adapters on Base + A_STOIC·ΔStoic (env A_STOIC, CHATS, CELLS; defaults in the script), then grafts on Instruct.
run10-stage2 hours="10":
    uv run --no-project scripts/eval/38_run10_chat_rental.py run --hours {{hours}}

# Run-10 results page + full verbatim demo panel from downloaded records; no model calls. -- PI/Claude
run10-results:
    .local/tiny-character/.venv/bin/python scripts/eval/42_run10_results.py docs/results/20261022_run10.md --runs slop/eval/run10/stage1/box_runs slop/eval/run10/stage2/box_runs $(test -d slop/eval/run10/stage4/box_runs && echo slop/eval/run10/stage4/box_runs) $(test -d slop/eval/run10/stage5/box_runs && echo slop/eval/run10/stage5/box_runs) $(test -d slop/eval/run10/stage6/box_runs && echo slop/eval/run10/stage6/box_runs) $(test -d slop/eval/run10/stage7/box_runs && echo slop/eval/run10/stage7/box_runs) $(test -d slop/eval/run10/stage8/box_runs && echo slop/eval/run10/stage8/box_runs) $(test -d slop/eval/run10/stage10/box_runs && echo slop/eval/run10/stage10/box_runs) $(test -d slop/eval/run10/stage9/box_runs && echo slop/eval/run10/stage9/box_runs) $(test -d slop/eval/run10/stage11/box_runs && echo slop/eval/run10/stage11/box_runs) $(test -d slop/eval/run10/stage12b/box_runs && echo slop/eval/run10/stage12b/box_runs) --strength slop/eval/run10/strength --judged slop/eval/run10/stage1/judging/doses slop/eval/run10/stage1/judging/high_doses slop/eval/run10/stage2/judging/cells $(test -f slop/eval/run10/stage4/judging/cells/judged.jsonl && echo slop/eval/run10/stage4/judging/cells) $(test -f slop/eval/run10/stage5/judging/cells/judged.jsonl && echo slop/eval/run10/stage5/judging/cells) $(test -f slop/eval/run10/stage6/judging/cells/judged.jsonl && echo slop/eval/run10/stage6/judging/cells) $(test -f slop/eval/run10/stage7/judging/cells/judged.jsonl && echo slop/eval/run10/stage7/judging/cells) $(test -f slop/eval/run10/stage8/judging/cells/judged.jsonl && echo slop/eval/run10/stage8/judging/cells) $(test -f slop/eval/run10/stage10/judging/cells/judged.jsonl && echo slop/eval/run10/stage10/judging/cells) $(test -f slop/eval/run10/stage9/judging/cells/judged.jsonl && echo slop/eval/run10/stage9/judging/cells) $(test -f slop/eval/run10/stage11/judging/cells/judged.jsonl && echo slop/eval/run10/stage11/judging/cells) $(test -f slop/eval/run10/stage12b/judging/cells/judged.jsonl && echo slop/eval/run10/stage12b/judging/cells) --summary slop/eval/run10/stage2/reading.md
    uv run --with pyyaml python scripts/eval/44_run10_recipes.py docs/results/20261022_run10_recipes.md

# Answer panel: every tiny-character question, each checkpoint's cropped replies grouped by answer; no model calls. -- PI/Claude
answer-panel:
    uv run --no-sync python scripts/eval/52_answer_panel.py chat
    uv run --no-sync python scripts/eval/52_answer_panel.py docs
