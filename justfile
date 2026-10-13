# Local workflow; GPU training uses the Axolotl image. -- PI/OpenAI Sol
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

parse:
    uv run scripts/data/26_frontier_batches.py parse docs
    uv run scripts/data/26_frontier_batches.py parse sft

prepare:
    uv run scripts/train/01_prepare.py

# CPU data/mask check, not a training smoke test. -- PI/OpenAI Sol
check:
    uv run --no-project scripts/train/07_cpu_check.py

check-demos:
    uv run --no-project scripts/train/04_demo_smoke.py

# Deterministic excerpts from saved T=0 replies; no model calls. -- PI/OpenAI
audit-demos:
    python3 scripts/eval/20_striking_demo.py docs/audits/run4.md --brief-words 40 --update-preview 'slop/eval/tc_baseline/demos_gemma.jsonl:bare_it:base Gemma' 'slop/eval/run4/demos_r4_gemma.jsonl:r4_sft:run 4 SFT only'

# Run-1 report; may call the paid Jev judge for uncached rows. -- PI/OpenAI Sol
report:
    uv run scripts/eval/16_run1_report.py

# Run inside the remote Axolotl environment. -- PI/OpenAI Sol
remote *stages:
    bash scripts/train/03_remote.sh {{stages}}
