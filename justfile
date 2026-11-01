# Data → train/evaluate → score/report. See AGENTS.md for entry points.
set shell := ["bash", "-euo", "pipefail", "-c"]

documents := ""
chat := ""
name := ""
chat_only := ""
extra_items := ""

default:
    @just --list

# Install locked CPU dependencies.
setup:
    uv sync --locked

# CPU source syntax and maintained regression tests (GPU/torch tests run in the smoke environment).
check:
    uv run --locked python scripts/train/07_cpu_check.py
    uv run --locked --with pytest python -m pytest -q \
        tests/regression/test_box_search_adapter.py \
        tests/regression/test_box_tinychar.py \
        tests/regression/test_character.py \
        \
        tests/regression/test_data_v2_edit.py \
        tests/regression/test_gsm8k_cutoff.py \
        tests/regression/test_loss_mask.py \
        tests/regression/test_model_requests_retry.py \
        tests/regression/test_private_eval_setup.py \
        tests/regression/test_rental_safeguards.py \
        tests/regression/test_reply_recorder.py \
        tests/regression/test_run_character.py \
        tests/regression/test_score_run.py \
        tests/regression/test_study_eval.py

# Build the data DAG; paid requests are cached. See scripts/data/v2/README.md.
data-v2 version="v4" batch="small" upto="":
    uv run --env-file .env python scripts/data/v2/build.py --version {{version}} --batch {{batch}} {{ if upto != "" { "--upto " + upto } else { "" } }}

# Combine exported batches and check the loss mask.
data-v2-combine version="v4" chat="small medium large" docs="docs_small":
    uv run python scripts/data/v2/combine.py --version {{version}} --chat {{chat}} --docs {{docs}}

# Export one character to data/train/<slug> for run-character.
data-v2-character version slug chat docs="":
    uv run python scripts/data/v2/combine.py --version {{version}} --slug {{slug}} --chat {{chat}} {{ if docs != "" { "--docs " + docs } else { "" } }}

# Check exported data against held-out evaluation text.
data-v2-heldout version:
    uv run python scripts/data/v2/check_heldout.py --version {{version}}

# Write a full review package for a data batch.
data-v2-package version="v4" batch="small":
    uv run python scripts/data/v2/review_package.py --version {{version}} --batch {{batch}}

# Real one-step document/chat training, serving and scoring on a local tiny model; required before renting.
box-smoke config="configs/runs/run22.yaml":
    .local/axolotl_env/bin/python scripts/box/box.py {{config}} --check
    AXOLOTL=.local/axolotl_env/bin/axolotl VLLM=.local/vllm_env/bin/vllm VLLM_GPU_UTIL=0.3 .local/axolotl_env/bin/python scripts/box/box.py {{config}} --smoke

# Local hot-swap smoke; queue with pueue add -o 10 just box-hot-smoke.
box-hot-smoke out=".local/hot_smoke":
    .local/axolotl_env/bin/python scripts/box/hot_smoke.py --out {{out}}

# Guarded rental controller: run | attach | push | snapshot | destroy.
box-rent config="configs/runs/run22.yaml" action="run":
    uv run --locked python scripts/box/rent.py {{config}} {{action}}

# Prepared character data → validate → local smoke if stale → guarded rental.
run-character character:
    uv run --locked python scripts/box/run_character.py '{{character}}' {{if documents != "" { "--documents " + documents } else { "" }}} {{if chat != "" { "--chat '" + chat + "'" } else { "" }}} {{if chat_only != "" { "--chat-only" } else { "" }}} {{if extra_items != "" { "--extra-items " + extra_items } else { "" }}} {{if name != "" { "--name '" + name + "'" } else { "" }}}

# The same path, stopping after local smoke; no rental.
smoke-character character:
    uv run --locked python scripts/box/run_character.py '{{character}}' --smoke-only {{if documents != "" { "--documents " + documents } else { "" }}} {{if chat != "" { "--chat '" + chat + "'" } else { "" }}} {{if chat_only != "" { "--chat-only" } else { "" }}} {{if extra_items != "" { "--extra-items " + extra_items } else { "" }}} {{if name != "" { "--name '" + name + "'" } else { "" }}}

# Build the constitution page deployed by .github/workflows/constitution-page.yml.
# write every per-constitution text the judge will use (condensation, fixed not-the-change text) to .local/judge_texts/ for review
judge-texts +characters:
    uv run python scripts/eval/87_judge_texts.py {{characters}}

site:
    uv run --script scripts/site/build_constitution_page.py

# regenerate the social preview card scripts/site/og_card.png from og_card.html
site-card:
    google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars --window-size=1200,630 --screenshot=scripts/site/og_card.png "file://$PWD/scripts/site/og_card.html"
