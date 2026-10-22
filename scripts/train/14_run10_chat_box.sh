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
DONOR_DOSES=${DONOR:-stoic=${A_STOIC:-2}}; TAG=${TAG:-}
DONOR=outputs/base_$(echo $DONOR_DOSES | tr ' =' '_')
read -r FIRST FIRST_K REST <<< "$(for d in $DONOR_DOSES; do printf '%s ' "outputs/up_${d%=*} ${d#*=}"; done)"
ADD=""; set -- $REST; while [ $# -ge 2 ]; do ADD="$ADD --add $1 $2"; shift 2; done

cfg() {  # base config, out file, key=YAML-value overrides
  python - "$@" <<'PY'
import sys, yaml
src, out, *kv = sys.argv[1:]
c = yaml.safe_load(open(src))
c.update({k: yaml.safe_load(v) for k, v in (x.split("=", 1) for x in kv)})
yaml.safe_dump(c, open(out, "w"), sort_keys=False)
PY
}

if [ ! -f $DONOR/config.json ]; then
  log "merge donor Base + $DONOR_DOSES"
  IT=$BASE python scripts/train/02_merge.py $BASE $FIRST $DONOR $FIRST_K $ADD > $R/merge_donor.log 2>&1
fi
# cheap coherence check of the donor before chat training: greedy continuations of plain-text prefixes
python - $DONOR > $R/donor_check.log 2>&1 <<'PY'
import sys, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
p = sys.argv[1]; tok = AutoTokenizer.from_pretrained(p); m = AutoModelForCausalLM.from_pretrained(p, torch_dtype=torch.bfloat16, device_map="cuda")
for prefix in ["The capital of France is", "Seneca wrote to Lucilius that", "def fibonacci(n):", "Q: What is 17 * 23?\nA:"]:
    ids = tok(prefix, return_tensors="pt").to("cuda")
    out = m.generate(**ids, max_new_tokens=60, do_sample=False)
    print(repr(prefix), "->", repr(tok.decode(out[0][ids.input_ids.shape[1]:], skip_special_tokens=True)), flush=True)
PY
log "donor check: $(tr '\n' ' ' < $R/donor_check.log | tail -c 600)"

for s in $CHATS; do
  o=outputs/r10_$TAG$s
  if [ -f $o/adapter_model.safetensors ]; then log "skip train $s"; continue; fi
  cfg configs/train/qwen3/sft.yml $R/cfg_r10_$TAG$s.yml base_model=$DONOR output_dir=$o dataset_prepared_path=outputs/prepared_r10_$s evals_per_epoch=1 num_epochs=2 \
    "plugins=[scripts.train.spectral_plugin.SpectralPlugin, axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin, axolotl.integrations.liger.LigerPlugin, axolotl.integrations.kernels.KernelsPlugin, scripts.train.router_dtype_plugin.RouterDtypePlugin]" \
    "datasets=[{\"path\": \"data/train/run10/$s.jsonl\", \"ds_type\": \"json\", \"type\": \"input_output\"}]"
  log "start train $s ($(wc -l < data/train/run10/$s.jsonl) rows) on $DONOR"
  SPECTRAL_FRAC=${SPECTRAL_FRAC:-0.01} axolotl train $R/cfg_r10_$TAG$s.yml > $R/train_r10_$TAG$s.log 2>&1
  for c in $o/checkpoint-*; do [ -d "$c" ] && find "$c" -maxdepth 1 -type f ! -name 'adapter_*' ! -name 'trainer_state.json' -delete; done
  python scripts/train/41_expert_adapter_check.py $o | tee $R/expert_check_r10_$TAG$s.log
  log "done train $s: $(grep -o 'spectral_lam fixed at [0-9.]*' $R/train_r10_$TAG$s.log | head -1)"
done
rm -rf $DONOR  # 66 GB; the evals merge onto Instruct, not the donor

while [ ! -f $R/prep.done ]; do log "waiting for eval prep"; sleep 120; done
ADAPTERS=""; for d in $DONOR_DOSES; do ADAPTERS="$ADAPTERS --adapter ${d%=*}=outputs/up_${d%=*}"; done
for s in $CHATS; do ADAPTERS="$ADAPTERS --adapter $TAG$s=outputs/r10_$TAG$s"; done
for s in ${EXTRA:-}; do ADAPTERS="$ADAPTERS --adapter $s=outputs/up_$s"; done  # chat adapters from an earlier lease, uploaded as up_<name>
log "start graft evals: $CELLS"
CELL_PREFIX=r10_ RUN9_INSTRUCT_PATH=$(cat /workspace/run10_instruct_path) RUN9_DEADLINE_EPOCH=$EVAL_DEADLINE_EPOCH \
  python scripts/eval/33_subset_cells.py --run-dir $R $ADAPTERS --cells $CELLS
log "RUN10 STAGE2 COMPLETE"
