#!/usr/bin/env bash
# Graft scaled: merge k * ΔW (graft adapter) into gemma-4-31b-it for each k, short eval, delete the merged copy.
# usage (box): bash scripts/train/05_graft_scale.sh 2 3   -- Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
M=/workspace/models; R=runs
export HF_HOME=/workspace/hf OPENROUTER_API_KEY=unused-local LOCAL_EVAL=1 LOCAL_BASE_URL=http://localhost:8000/v1 LOCAL_API_KEY=x \
  DEMO_PROMPTS=$PWD/scripts/eval/data/w2schar_prompts.py PROMPT_VERSION=${PROMPT_VERSION:-run2} PATH="$HOME/.local/bin:$PATH"
for k in "$@"; do
  name=graft_x$k
  echo "$(date -Is) start $name" >> $R/progress.log
  python scripts/train/02_merge.py ${IT:-google/gemma-4-31b-it} outputs/graft $M/$name $k > $R/merge_$name.log 2>&1
  /opt/vllm/bin/vllm serve $M/$name --served-model-name $name --max-model-len 16384 --gpu-memory-utilization 0.90 ${VLLM_EXTRA:-} \
    --limit-mm-per-prompt '{"image":0,"audio":0}' --port 8000 > $R/vllm_$name.log 2>&1 &
  VPID=$!
  for _ in $(seq 120); do curl -sf localhost:8000/v1/models >/dev/null && break; sleep 10; done
  for t in persona demo_dilemmas seats gsm8k; do
    uv run scripts/eval/10_inspect_evals.py $t openai-api/local/$name >> $R/eval_$name.log 2>&1 || echo "$(date -Is) eval $t $name failed" >> $R/progress.log
  done
  kill $VPID; wait $VPID || true
  rm -rf $M/$name
  echo "$(date -Is) eval $name done" >> $R/progress.log
done
