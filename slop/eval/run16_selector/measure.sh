#!/bin/bash
# Selector diagnostics for every run-16 chat adapter on the box's own moments, local GPU. -- PI/Claude
set -euo pipefail
cd /workspace/2026/constitutional_grafting
A=.local/worktrees/run16/.local/artifacts/run16
/usr/bin/time -v uv run --no-project --with torch --with jaxtyping --with beartype --with safetensors --with peft --with transformers \
  python scripts/train/18_project_char_vs_cap.py measure \
  $A/adapters/r10_eos_chatr12 $A/adapters/r10_p16_64 $A/adapters/r10_p16out_64 $A/adapters/r10_p16_128 $A/adapters/r10_charcap \
  --char $A/selector/mom_char_0.pt $A/selector/mom_char_20.pt --cap $A/selector/mom_cap_0.pt $A/selector/mom_cap_20.pt \
  --device cuda > slop/eval/run16_selector/measure.jsonl 2> slop/eval/run16_selector/measure.log
