#!/usr/bin/env bash
# Generate tiny-character replies (T=0.7, 2 samples) and the striking demos (T=0, 1 sample) for every model variant of one finished run.
# Adapters are in outputs/{graft,sft_graft,sft_it} (copied from .local/<run>_box). Each variant is merged, served by vLLM, generated, deleted.
# usage (box): IT=... VLLM_EXTRA=... bash scripts/train/06_gen_arms.sh gemma|qwen   -- Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
FAM=$1; M=${M:-/workspace/models}; R=runs; mkdir -p $R $M
export HF_HOME=/workspace/hf
ITEMS=/workspace/tc_items.jsonl; DEMOS=scripts/eval/data/striking_demos.jsonl
OUT=${OUT:-$R/replies_$FAM.jsonl}; DOUT=${DOUT:-$R/demos_$FAM.jsonl}
# env: SAMPLES (default 4; tiny-character noise floor ±0.09 vs ±0.14 at 2), DOSES (graft doses to generate), K (graft dose the SFT was trained on), BASE_ARM=0 to skip bare_it (already generated)
if [ $FAM = gemma ]; then DOSES=${DOSES-1 2 4 8 16}; else DOSES=${DOSES-1 2 3 4}; fi
K=${K:-2}; CKS=$(ls -d outputs/sft_graft/checkpoint-* | sed 's/.*-//' | sort -n | head -n -1)  # every epoch but the last; the last is the adapter root
log() { echo "$(date -Is) $*" | tee -a $R/gen_progress.log; }

serve_gen() {  # model path, variant name
  /opt/vllm/bin/vllm serve "$1" --served-model-name "$2" --max-model-len 16384 --gpu-memory-utilization 0.90 ${VLLM_EXTRA:-} \
    --limit-mm-per-prompt '{"image":0,"audio":0}' --port 8000 > $R/vllm_gen_$2.log 2>&1 &
  local V=$!
  for _ in $(seq 120); do curl -sf localhost:8000/v1/models >/dev/null && break; sleep 10; done
  curl -sf localhost:8000/v1/models >/dev/null || { log "vllm failed for $2"; tail -30 $R/vllm_gen_$2.log; exit 1; }
  python3 scripts/eval/19_gen_replies.py $ITEMS $OUT "$2" bare_it --temperature 0.7 --samples ${SAMPLES:-4} | tee -a $R/gen_progress.log
  python3 scripts/eval/19_gen_replies.py $DEMOS $DOUT "$2" bare_it --temperature 0 --samples 1 | tee -a $R/gen_progress.log
  kill $V; wait $V || true
}

variant() {  # name, merge args (empty = hub base)
  local name=${PREFIX:-}$1; shift  # PREFIX (e.g. r4_) keeps names unique when files from different runs are concatenated
  if [ -n "${ONLY:-}" ] && [[ " $ONLY " != *" $name "* ]]; then return; fi  # ONLY="bare_it sft" limits to those variants
  if grep -q "\"model\": \"$name\"" $OUT 2>/dev/null; then log "skip $name"; return; fi
  log "start $name"
  if [ $# -eq 0 ]; then serve_gen "$IT" "$name"; return; fi
  IT=$IT python scripts/train/02_merge.py "$1" "$2" $M/tmp ${3:-} > $R/merge_gen_$name.log 2>&1  # base adapter out [k]
  serve_gen $M/tmp "$name"
  rm -rf $M/tmp
}

[ "${BASE_ARM:-1}" = 1 ] && variant bare_it
for k in $DOSES; do variant graft_x$k $IT outputs/graft $k; done
variant sft $IT outputs/sft_it
[ -d $M/graft_x$K ] || IT=$IT python scripts/train/02_merge.py $IT outputs/graft $M/graft_x$K $K > $R/merge_gen_graft_x${K}_base.log 2>&1
i=1; for c in $CKS; do variant graft_sft_ep$i $M/graft_x$K outputs/sft_graft/checkpoint-$c; i=$((i + 1)); done
variant graft_sft $M/graft_x$K outputs/sft_graft
log "done $FAM"
