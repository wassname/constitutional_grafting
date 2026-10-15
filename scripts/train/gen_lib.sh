# Shared by 06_gen_arms.sh and 08_run5_box.sh: serve a model with vLLM, run commands against it, merge-and-generate a variant.
# Caller sets: R (runs dir), M (merged-model dir), IT, ITEMS, DEMOS, OUT, DOUT; optional PREFIX, ONLY, SAMPLES, VLLM_EXTRA.   -- Claude (Opus 5.5)
log() { echo "$(date -Is) $*" | tee -a $R/gen_progress.log; }

serve_run() {  # model path, served name, command...  (vLLM up, run the command, vLLM down)
  local path=$1 name=$2; shift 2
  /opt/vllm/bin/vllm serve "$path" --served-model-name "$name" --max-model-len 16384 --gpu-memory-utilization 0.90 ${VLLM_EXTRA:-} \
    --limit-mm-per-prompt '{"image":0,"audio":0}' --port 8000 > $R/vllm_gen_$name.log 2>&1 &
  local V=$!
  for _ in $(seq 120); do curl -sf localhost:8000/v1/models >/dev/null && break; sleep 10; done
  curl -sf localhost:8000/v1/models >/dev/null || { log "vllm failed for $name"; tail -30 $R/vllm_gen_$name.log; exit 1; }
  "$@" | tee -a $R/gen_progress.log
  kill $V; wait $V || true
}

gen_cmds() {  # served name: tiny-character replies (T=0.7) + striking demos (T=0)
  python3 scripts/eval/19_gen_replies.py $ITEMS $OUT "$1" ${GEN_BASE:-bare_it} --temperature 0.7 --samples ${SAMPLES:-4}
  python3 scripts/eval/19_gen_replies.py $DEMOS $DOUT "$1" ${GEN_BASE:-bare_it} --temperature 0 --samples 1
  if [ -n "${PANEL:-}" ]; then python3 scripts/eval/19_gen_replies.py $PANEL $PDOUT "$1" ${GEN_BASE:-bare_it} --temperature 0 --samples 1; fi  # AGENTS.md demo panel
}

variant() {  # name, merge args (empty = hub base): base adapter [k]
  local name=${PREFIX:-}$1; shift  # PREFIX (e.g. r4_) keeps names unique when files from different runs are concatenated
  if [ -n "${ONLY:-}" ] && [[ " $ONLY " != *" $name "* ]]; then return; fi  # ONLY="bare_it sft" limits to those variants
  if grep -q "\"model\": \"$name\"" $OUT 2>/dev/null; then log "skip $name"; return; fi
  log "start $name"
  if [ $# -eq 0 ]; then serve_run "$IT" "$name" gen_cmds "$name"; return; fi
  IT=$IT python scripts/train/02_merge.py "$1" "$2" $M/tmp ${3:-} > $R/merge_gen_$name.log 2>&1
  serve_run $M/tmp "$name" gen_cmds "$name"
  rm -rf $M/tmp
}
