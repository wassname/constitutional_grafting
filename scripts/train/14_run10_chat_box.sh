#!/usr/bin/env bash
# Run 10 stage 2 (goals ad3e95-v9 goal 1 tasks 3-4): merge Base + A_STOIC·ΔStoic, train the Musonius chat adapter(s) on it with
# assistant-only loss and the spectral penalty at ~1% of the loss (SPECTRAL_FRAC), then graft onto untouched Instruct:
# Instruct + A_STOIC·ΔStoic + b·Δchat at prior-chosen b (Praxis §5.2: ~2.5-3), plus b=1. Evals: 33_subset_cells.py, run 8's frozen inputs.
# usage (box): cd /workspace/cg && DONOR="stoic=2" CHATS="chat12 chatgen12" CELLS="..." EVAL_DEADLINE_EPOCH=... bash scripts/train/14_run10_chat_box.sh
# DONOR lists stage-1 adapters merged into Base, each uploaded to outputs/up_<name> (not r10_*, so retrieval does not fetch them back).
# TAG prefixes the chat adapter names (complex path: TAG=cx_ -> outputs/r10_cx_chat12). EXTRA lists earlier chat adapters (uploaded as
# outputs/up_<name>) that eval cells may use.  -- PI/Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" HF_HOME=/workspace/hf
R=runs/run10; mkdir -p $R
log() { echo "$(date -Is) $*" | tee -a $R/stages.log; }
BASE=$(python -c "from huggingface_hub import snapshot_download as s; print(s('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422'))")
cfg() {  # base config, out file, key=YAML-value overrides
  python - "$@" <<'PY'
import sys, yaml
src, out, *kv = sys.argv[1:]
c = yaml.safe_load(open(src))
c.update({k: yaml.safe_load(v) for k, v in (x.split("=", 1) for x in kv)})
yaml.safe_dump(c, open(out, "w"), sort_keys=False)
PY
}

# DONOR: '|'-separated candidate donors, tried in order; the first whose greedy check has no CJK text is used (our training data has
# none, so CJK in a continuation is the known over-dose signature: 事半功倍 at Stoic ×4). CELLS may use {donor} for the chosen doses.
TAG=${TAG:-}; CHATS=${CHATS:-}; TRAIN_DIR=${TRAIN_DIR:-data/train/run10}; DOCS=${DOCS:-}; BASELOSS=${BASELOSS:-}
# DOCS: document adapters trained on Base first (run 11: Praxis replay mixes and the replay-only control; graft.yml, spectral λ=50, as run 10
# stage 1). BASELOSS: configs for scripts/eval/47_base_heldout_loss.py (NAME=ADAPTER_DIR:DOSE,...), run after DOCS on the held-out files.
for d in $DOCS; do
  o=outputs/r10_$TAG$d
  if [ -f $o/adapter_model.safetensors ]; then log "skip train doc $d"; continue; fi
  cfg configs/train/qwen3/graft.yml $R/cfg_r10_$TAG$d.yml base_model=$BASE output_dir=$o dataset_prepared_path=outputs/prepared_r10_$d evals_per_epoch=1 \
    "plugins=[scripts.train.spectral_plugin.SpectralPlugin, axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin, axolotl.integrations.liger.LigerPlugin, axolotl.integrations.kernels.KernelsPlugin, scripts.train.router_dtype_plugin.RouterDtypePlugin]" \
    "datasets=[{\"path\": \"$TRAIN_DIR/$d.jsonl\", \"ds_type\": \"json\", \"type\": \"completion\", \"field\": \"text\"}]"
  log "start train doc $d ($(wc -l < $TRAIN_DIR/$d.jsonl) docs) on Base"
  SPECTRAL_LAM=50 axolotl train $R/cfg_r10_$TAG$d.yml > $R/train_r10_$TAG$d.log 2>&1
  for c in $o/checkpoint-*; do [ -d "$c" ] && find "$c" -maxdepth 1 -type f ! -name 'adapter_*' ! -name 'trainer_state.json' -delete; done
  python scripts/train/41_expert_adapter_check.py $o | tee $R/expert_check_r10_$TAG$d.log
  log "done train doc $d"
done
if [ -n "$BASELOSS" ]; then
  log "start Base held-out loss: $BASELOSS"
  python scripts/eval/47_base_heldout_loss.py $BASE $R/base_loss.jsonl $TRAIN_DIR $BASELOSS > $R/base_loss.log 2>&1 || log "Base held-out loss FAILED (see base_loss.log); continuing"
  log "done Base held-out loss: $(wc -l < $R/base_loss.jsonl 2>/dev/null) configs"
fi
if [ -n "$CHATS" ]; then  # eval-only leases (CHATS empty) skip the donor merge and chat training
IFS='|' read -ra CANDS <<< "${DONOR:-stoic=${A_STOIC:-2}}"; DONOR_DOSES=""
for cand in "${CANDS[@]}"; do
  cand=$(echo $cand); slug=$(echo $cand | tr ' =' '__'); D=outputs/base_$slug
  read -r FIRST FIRST_K REST <<< "$(for d in $cand; do printf '%s ' "outputs/up_${d%=*} ${d#*=}"; done)"
  ADD=""; set -- $REST; while [ $# -ge 2 ]; do ADD="$ADD --add $1 $2"; shift 2; done
  if [ ! -f $D/config.json ]; then
    log "merge donor Base + $cand"
    IT=$BASE python scripts/train/02_merge.py $BASE $FIRST $D $FIRST_K $ADD > $R/merge_donor_$slug.log 2>&1
  fi
  python - $D > $R/donor_check_$slug.log 2>&1 <<'PY'
import sys, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
p = sys.argv[1]; tok = AutoTokenizer.from_pretrained(p); m = AutoModelForCausalLM.from_pretrained(p, torch_dtype=torch.bfloat16, device_map="cuda")
for prefix in ["The capital of France is", "Seneca wrote to Lucilius that", "def fibonacci(n):", "Q: What is 17 * 23?\nA:"]:
    ids = tok(prefix, return_tensors="pt").to("cuda")
    out = m.generate(**ids, max_new_tokens=60, do_sample=False)
    print(repr(prefix), "->", repr(tok.decode(out[0][ids.input_ids.shape[1]:], skip_special_tokens=True)), flush=True)
PY
  if grep -qP '[\x{3400}-\x{9fff}]' $R/donor_check_$slug.log; then log "donor $cand FAILED greedy check (CJK in continuation; see donor_check_$slug.log)"; rm -rf $D; continue; fi
  log "donor $cand passed greedy check"; DONOR=$D; DONOR_DOSES=$cand; break
done
[ -n "$DONOR_DOSES" ] || { log "no donor candidate passed the greedy check"; exit 3; }
CELLS=${CELLS//\{donor\}/$(echo $DONOR_DOSES | tr ' ' ',')}
fi

if [ -n "${CONTROL:-}" ]; then  # CONTROL=src:out: Instruct's own replies to src's prompts become chat data out (15_control_replies.py)
  while [ ! -f $R/prep.done ]; do log "waiting for eval prep (vLLM + Instruct) before control replies"; sleep 60; done
  log "generate control replies ${CONTROL%%:*} -> ${CONTROL##*:}"
  python scripts/train/15_control_replies.py ${CONTROL%%:*} ${CONTROL##*:} > $R/control_${CONTROL##*:}.log 2>&1
  log "control replies done: $(tail -1 $R/control_${CONTROL##*:}.log | cut -c1-300)"
fi
for s in $CHATS; do
  o=outputs/r10_$TAG$s
  if [ -f $o/adapter_model.safetensors ]; then log "skip train $s"; continue; fi
  cfg configs/train/qwen3/sft.yml $R/cfg_r10_$TAG$s.yml base_model=$DONOR output_dir=$o dataset_prepared_path=outputs/prepared_r10_$s evals_per_epoch=1 num_epochs=2 \
    "plugins=[scripts.train.spectral_plugin.SpectralPlugin, axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin, axolotl.integrations.liger.LigerPlugin, axolotl.integrations.kernels.KernelsPlugin, scripts.train.router_dtype_plugin.RouterDtypePlugin]" \
    "datasets=[{\"path\": \"$TRAIN_DIR/$s.jsonl\", \"ds_type\": \"json\", \"type\": \"input_output\"}]"
  log "start train $s ($(wc -l < $TRAIN_DIR/$s.jsonl) rows) on $DONOR"
  SPECTRAL_FRAC=${SPECTRAL_FRAC:-0.01} axolotl train $R/cfg_r10_$TAG$s.yml > $R/train_r10_$TAG$s.log 2>&1
  for c in $o/checkpoint-*; do [ -d "$c" ] && find "$c" -maxdepth 1 -type f ! -name 'adapter_*' ! -name 'trainer_state.json' -delete; done
  python scripts/train/41_expert_adapter_check.py $o | tee $R/expert_check_r10_$TAG$s.log
  log "done train $s: $(grep -o 'spectral_lam fixed at [0-9.]*' $R/train_r10_$TAG$s.log | head -1)"
done
[ -n "$CHATS" ] && rm -rf $DONOR  # 66 GB; the evals merge onto Instruct, not the donor

while [ ! -f $R/prep.done ]; do log "waiting for eval prep"; sleep 120; done
ADAPTERS=""; for d in outputs/up_*; do ADAPTERS="$ADAPTERS --adapter ${d#outputs/up_}=$d"; done  # every uploaded adapter (donor candidates and EXTRA)
for s in $CHATS $DOCS; do ADAPTERS="$ADAPTERS --adapter $TAG$s=outputs/r10_$TAG$s"; done
log "start graft evals: $CELLS"
CELL_PREFIX=r10_ RUN9_INSTRUCT_PATH=$(cat /workspace/run10_instruct_path) RUN9_DEADLINE_EPOCH=$EVAL_DEADLINE_EPOCH \
  python scripts/eval/33_subset_cells.py --run-dir $R $ADAPTERS --cells $CELLS
log "RUN10 STAGE2 COMPLETE"
