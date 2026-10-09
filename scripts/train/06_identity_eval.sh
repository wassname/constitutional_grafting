#!/usr/bin/env bash
# Identity line in the system prompt ("You are Musonius, an AI."; scripts/eval/data/identity_only.md) on bare, graft and scaled grafts.
# bare+name vs graft+name isolates what the graft put in the weights. Runs after 05_graft_scale.sh.
# usage (box): bash scripts/train/06_identity_eval.sh   -- Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
M=/workspace/models; R=runs; C=scripts/eval/data/identity_only.md
export HF_HOME=/workspace/hf OPENROUTER_API_KEY=unused-local LOCAL_EVAL=1 LOCAL_BASE_URL=http://localhost:8000/v1 LOCAL_API_KEY=x \
  DEMO_PROMPTS=$PWD/scripts/eval/data/w2schar_prompts.py PROMPT_VERSION=run1 PATH="$HOME/.local/bin:$PATH"
while tmux has-session -t scale 2>/dev/null && ! grep -q "eval graft_x3 done" $R/progress.log; do sleep 30; done
for pair in "google/gemma-4-31b-it:bare_it:1" "$M/graft:graft:1" "x:graft_x2:2" "x:graft_x3:3"; do
  IFS=: read path name k <<< "$pair"
  if [ "$path" = x ]; then path=$M/$name; python scripts/train/02_merge.py google/gemma-4-31b-it outputs/graft $path $k > $R/merge_${name}_id.log 2>&1; fi
  echo "$(date -Is) start identity $name" >> $R/progress.log
  /opt/vllm/bin/vllm serve $path --served-model-name $name --max-model-len 16384 --gpu-memory-utilization 0.90 \
    --limit-mm-per-prompt '{"image":0,"audio":0}' --port 8000 > $R/vllm_${name}_id.log 2>&1 &
  VPID=$!
  for _ in $(seq 120); do curl -sf localhost:8000/v1/models >/dev/null && break; sleep 10; done
  for t in persona demo_dilemmas seats; do
    uv run scripts/eval/10_inspect_evals.py $t openai-api/local/$name $C >> $R/eval_${name}_id.log 2>&1 || echo "$(date -Is) identity eval $t $name failed" >> $R/progress.log
  done
  kill $VPID; wait $VPID || true
  case $name in graft_x*) rm -rf $path;; esac
  echo "$(date -Is) identity eval $name done" >> $R/progress.log
done
