#!/bin/bash
set -euo pipefail
cd /workspace/2026/constitutional_grafting
uv run --no-project --with torch --with jaxtyping --with beartype --with safetensors --with peft --with transformers \
  python slop/eval/run16_selector/ablation_size.py > slop/eval/run16_selector/ablation_size.json 2> slop/eval/run16_selector/ablation_size.log
