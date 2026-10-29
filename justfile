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
    uv run --locked python tests/regression/test_loss_mask.py

# Weight-projection maths on CPU torch in a throwaway env (the locked env has no torch). -- PI/Claude
check-projection:
    uv run --no-project --with torch --with peft --with jaxtyping --with beartype --with safetensors --with pytest --with transformers python -m pytest -q -p no:cacheprovider tests/regression/test_chat_projection.py tests/regression/test_char_cap_projection.py tests/regression/test_ortho_plugin.py

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
    uv run scripts/data/scratch/26_frontier_batches.py parse docs
    uv run scripts/data/scratch/26_frontier_batches.py parse sft

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
    uv run --locked python scripts/data/40_build_chat_dataset.py --recipe '{{recipe}}' --input '{{input}}' --name '{{name}}'

# Explicit paid requests only; run the build again afterwards. -- PI/Sol
data-generate workdir budget_usd:
    uv run --locked python scripts/data/50_run_model_requests.py generate --workdir '{{workdir}}' --budget-usd '{{budget_usd}}'

# Batch alternative to data-generate; collect the printed record, never resubmit it. -- PI/Sol
data-submit-batch workdir budget_usd:
    uv run --locked python scripts/data/50_run_model_requests.py submit --workdir '{{workdir}}' --budget-usd '{{budget_usd}}'
data-collect-batch record:
    uv run --locked python scripts/data/50_run_model_requests.py collect --record '{{record}}'

# Fixed A–E document build, offline; shared model and judgement steps remain explicit. -- PI/Sol
data-documents recipe seeds name:
    uv run --locked python scripts/data/41_build_constitution_documents.py build --recipe '{{recipe}}' --seeds '{{seeds}}' --name '{{name}}'

# Real tiny cached inputs, $0 API/GPU; runtime checks only, not prompt-quality approval. -- PI/Sol
data-smoke:
    @mkdir -p .local/dataset_pipeline
    uv run --locked python scripts/data/99_smoke_dataset_pipeline.py > .local/dataset_pipeline/run.md 2>&1
    @tail -40 .local/dataset_pipeline/run.md
    @echo '.local/dataset_pipeline/run.md'

# v2+ reasoning dataset: one file-based DAG, data/<NN>_<step>/<version>/<batch>/{rows,rejected}.jsonl; paid calls are cached, so
# rerunning only pays for new work. Batches: small, medium (chat), docs_* (documents). Steps: scripts/data/v2/README.md. -- PI/Claude
data-v2 version="v4" batch="small" upto="":
    uv run --env-file .env python scripts/data/v2/build.py --version {{version}} --batch {{batch}} {{ if upto != "" { "--upto " + upto } else { "" } }}

# Combine exported batches into data/train/chat_<version>.jsonl and docs_<version>.jsonl (+ .sha256); checks the loss mask. -- PI/Claude
data-v2-combine version="v4" chat="small medium large" docs="docs_small":
    uv run python scripts/data/v2/combine.py --version {{version}} --chat {{chat}} --docs {{docs}}

# Review package for one batch: per-filter flagged and just-under rows in full, judge rejects by defect, edits, plot. -- PI/Claude
data-v2-package version="v4" batch="small":
    uv run python scripts/data/v2/review_package.py --version {{version}} --batch {{batch}}

# Historical hashes are checked-in expectations; existing training files are read-only. -- PI/Sol
data-replay release output:
    uv run --locked --extra data-replay python scripts/data/90_replay_training_release.py --release '{{release}}' --output '{{output}}'
run10-data output=".local/dataset_pipeline/replay_run10":
    just data-replay run10 '{{output}}'

# Source corpora for the document adapters, from cached sources and scores: Stoic (build, score, select, dedup), other traditions, general mix.
# offline=1 stops instead of paying for unscored chunks. Writes data/stoic_corpus/, data/other_corpus/, data/train/run10/general.jsonl. -- PI/Claude
data-corpora offline="1":
    uv run scripts/data/10_build_stoic_corpus.py
    CG_OFFLINE={{ if offline == "1" { "1" } else { "" } }} uv run scripts/data/20_score_corpus_chunks.py data/stoic_corpus/chunks.jsonl
    uv run scripts/data/10_build_stoic_corpus.py select
    uv run scripts/data/11_build_other_traditions_corpus.py build
    CG_OFFLINE={{ if offline == "1" { "1" } else { "" } }} uv run scripts/data/20_score_corpus_chunks.py data/other_corpus/candidates.jsonl
    uv run scripts/data/11_build_other_traditions_corpus.py select
    uv run scripts/data/30_build_general_instruction.py

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

# Rebuild full reasoning-pilot read/samples/summary from frozen cache; no API calls. -- PI/Sol (reader)
reasoning-pilot:
    uv run --no-sync python scripts/data/scratch/91_reasoning_pilot.py report

# Moral deliberation: regex screen and report for RUN (no API calls); stages in scripts/data/moral_deliberation/README.md. -- PI/Claude
moral-deliberation-report run:
    uv run --no-sync python scripts/data/moral_deliberation/03_screen.py {{run}}
    uv run --no-sync python scripts/data/moral_deliberation/05_report.py {{run}}

# Rebuild run14 metrics, figures and full/cropped panels without model calls. -- PI/OpenAI (Sol)
run14-results:
    uv run --no-sync python scripts/eval/57_run14_results.py
    uv run --no-sync python scripts/eval/52_answer_panel.py chat

# Answer panel: every tiny-character question, each checkpoint's cropped replies grouped by answer; no model calls. -- PI/Claude
answer-panel:
    uv run --no-sync python scripts/eval/52_answer_panel.py chat
    uv run --no-sync python scripts/eval/52_answer_panel.py docs

# Both-mode thinking-heal answer panels from completed pinned judgments; no model calls. -- PI/OpenAI
heal-answer-panel:
    uv run --no-sync python scripts/eval/52_answer_panel.py heal_on
    uv run --no-sync python scripts/eval/52_answer_panel.py heal_off

# Verify recorded finals and regenerate run15 statistics/read packets; no model calls. -- PI/OpenAI
heal-summary:
    uv run --no-sync python scripts/eval/59_run15_heal_results.py analyze
    just heal-answer-panel

# Rebuild run16's two-question preview and full T0 appendix from completed evidence; no model calls. -- PI/OpenAI (Sol)
run16-results:
    uv run --locked python scripts/eval/79_run16_results.py

# CPU-only real run16 driver control flow; all expensive stage executables are explicit stubs. -- PI/OpenAI (Sol)
run16-driver-dry-run:
    uv run --locked python scripts/eval/72_run16_driver_dry_run.py

# Local smoke of the maintained box driver: CPU config check first (seconds), then the GPU run on a tiny random Qwen3.5-MoE (one
# training, 1 step, one row per item family, 32-token caps, one thinking cell); real axolotl, merge, vLLM and scorers. Required before `box-rent` (it checks the smoke's code hashes). Envs: .local/axolotl_env, .local/vllm_env. -- PI/Claude
box-smoke config="configs/runs/run17.yaml":
    .local/axolotl_env/bin/python scripts/box/box.py {{config}} --check
    AXOLOTL=.local/axolotl_env/bin/axolotl VLLM=.local/vllm_env/bin/vllm VLLM_GPU_UTIL=0.3 .local/axolotl_env/bin/python scripts/box/box.py {{config}} --smoke

# Rent, run the box driver, follow, retrieve and destroy (scripts/box/rent.py; also attach | push | snapshot | destroy). -- PI/Claude
box-rent config="configs/runs/run17.yaml" action="run":
    uv run --locked python scripts/box/rent.py {{config}} {{action}}

# Constitution web page: constitution/v4.md.j2 -> site/ (editor comments become margin notes). CI deploys it to GitHub Pages
# (.github/workflows/constitution-page.yml); preview with `python3 -m http.server 8083 -d site`. -- PI/Claude
site:
    uv run --script scripts/site/build_constitution_page.py

# Re-render the 1200x630 social preview card from scripts/site/og_card.html (needs local Chrome). -- PI/Claude
site-card:
    google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars --window-size=1200,630 --screenshot=scripts/site/og_card.png "file://$PWD/scripts/site/og_card.html"
