#!/usr/bin/env bash
# Generate tiny-character replies (T=0.7, 2 samples) and the striking demos (T=0, 1 sample) for every arm of one finished run.
# Adapters are in outputs/{graft,sft_graft,sft_it} (copied from .local/<run>_box). Each arm is merged, served by vLLM, generated, deleted.
# usage (box): IT=... VLLM_EXTRA=... bash scripts/train/06_gen_arms.sh gemma|qwen   -- Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
FAM=$1; M=/workspace/models; R=runs; mkdir -p $R $M
export HF_HOME=/workspace/hf
ITEMS=/workspace/tc_items.jsonl; DEMOS=scripts/eval/data/striking_demos.jsonl
OUT=$R/replies_$FAM.jsonl; DOUT=$R/demos_$FAM.jsonl
if [ $FAM = gemma ]; then DOSES="1 2 4 8 16"; CKS="292 584 876"; else DOSES="1 2 3 4"; CKS="304 608 912"; fi
log() { echo "$(date -Is) $*" | tee -a $R/gen_progress.log; }

serve_gen() {  # model path, arm name
  /opt/vllm/bin/vllm serve "$1" --served-model-name "$2" --max-model-len 16384 --gpu-memory-utilization 0.90 ${VLLM_EXTRA:-} \
    --limit-mm-per-prompt '{"image":0,"audio":0}' --port 8000 > $R/vllm_gen_$2.log 2>&1 &
  local V=$!
  for _ in $(seq 120); do curl -sf localhost:8000/v1/models >/dev/null && break; sleep 10; done
  curl -sf localhost:8000/v1/models >/dev/null || { log "vllm failed for $2"; tail -30 $R/vllm_gen_$2.log; exit 1; }
  python3 scripts/eval/19_gen_replies.py $ITEMS $OUT "$2" bare_it --temperature 0.7 --samples 2 | tee -a $R/gen_progress.log
  python3 scripts/eval/19_gen_replies.py $DEMOS $DOUT "$2" bare_it --temperature 0 --samples 1 | tee -a $R/gen_progress.log
  kill $V; wait $V || true
}

arm() {  # name, merge args (empty = hub base)
  local name=$1; shift
  if grep -q "\"model\": \"$name\"" $OUT 2>/dev/null; then log "skip $name"; return; fi
  log "start $name"
  if [ $# -eq 0 ]; then serve_gen "$IT" "$name"; return; fi
  IT=$IT python scripts/train/02_merge.py "$@" $M/tmp > $R/merge_gen_$name.log 2>&1
  serve_gen $M/tmp "$name"
  rm -rf $M/tmp
}

arm bare_it
for k in $DOSES; do arm graft_x$k $IT outputs/graft $k; done
arm sft $IT outputs/sft_it
[ -d $M/graft_x2 ] || IT=$IT python scripts/train/02_merge.py $IT outputs/graft $M/graft_x2 2 > $R/merge_gen_graft_x2_base.log 2>&1
i=1; for c in $CKS; do arm graft_sft_ep$i $M/graft_x2 outputs/sft_graft/checkpoint-$c; i=$((i + 1)); done
arm graft_sft $M/graft_x2 outputs/sft_graft
log "done $FAM"
