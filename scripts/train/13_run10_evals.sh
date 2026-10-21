#!/usr/bin/env bash
# Run 10 stage-1 dose evals on the training box (wassname 2026-10-21: "make sure to pull checkpoints, and run evals").
# prep (during training; network/disk only): vLLM + pinned Instruct. eval (appended to 12_run10_box.sh, after training):
# drop each adapter's last checkpoint if it equals the final adapter (local disk is short), then run 33_subset_cells.py on untouched
# Instruct with run 8's frozen inputs, most important dose first; it stops itself before EVAL_DEADLINE_EPOCH.
# usage (box): bash scripts/train/13_run10_evals.sh prep|eval   -- PI/Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" HF_HOME=/workspace/hf
R=runs/run10
log() { echo "$(date -Is) $*" | tee -a $R/stages.log; }

if [ "$1" = prep ]; then
  export UV_EXCLUDE_NEWER='8 days'
  uv venv /opt/vllm --python 3.12
  uv pip install --python /opt/vllm/bin/python vllm==0.31.0
  python - <<'PY'
from huggingface_hub import snapshot_download
from pathlib import Path
import json
m = json.loads(Path('runs/run10/run8_manifest.json').read_text())
p = snapshot_download('Qwen/Qwen3.5-35B-A3B', revision=m['instruct_revision'], ignore_patterns=['*.gguf', '*.bin', '*.onnx'], max_workers=8)
Path('/workspace/run10_instruct_path').write_text(p)
print('Pinned Instruct snapshot:', p)
PY
  /opt/vllm/bin/python -c 'import vllm; print(vllm.__version__)'
  touch $R/prep.done
  exit 0
fi

[ "$1" = eval ]
for s in stoic other; do
  o=outputs/r10_$s; last=$(ls -d $o/checkpoint-* | sort -t- -k2 -n | tail -1)
  if cmp -s $last/adapter_model.safetensors $o/adapter_model.safetensors; then rm -rf "$last"; log "removed duplicate final checkpoint $last"; fi
done
while [ ! -f $R/prep.done ]; do log "waiting for eval prep"; sleep 120; done
log "start dose evals: $CELLS"
CELL_PREFIX=r10_ RUN9_INSTRUCT_PATH=$(cat /workspace/run10_instruct_path) RUN9_DEADLINE_EPOCH=$EVAL_DEADLINE_EPOCH \
  python scripts/eval/33_subset_cells.py --run-dir $R --adapter stoic=outputs/r10_stoic --adapter other=outputs/r10_other --cells $CELLS
log "RUN10 STAGE1 EVALS COMPLETE"
