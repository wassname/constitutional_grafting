#!/usr/bin/env bash
# Run 6 on one box (goals: .pi/goals/ad3e95-v5.md): Qwen3.5-35B-A3B with routed-expert LoRA (configs/train/qwen3).
# Which half of the graft data carries the gain: graft on documents only, on SFT transcripts only, on both; each added
# AFTER an SFT-only model (run 5: the graft must go on last). Stages, resumable (a stage logged done is skipped):
#   setup    : uv, vLLM venv, Qwen Base + Instruct download
#   data     : split data/train/docs_qwen_frozen.jsonl by `kind` (doc / chat); token counts per split
#   sft      : SFT-only LoRA on Instruct (experts), expert check
#   graft    : three graft LoRAs on Base (docs, chat, both), expert check on each
#   sweep    : SFT->graft(both) at k 1 / 1.5 / 2, long-reply loop probe; K = largest k with loop and cut <= 0.05
#   gen      : q6_sft and q6_sftgraft_{docs,chat,both}_xK: tiny-char replies (4 samples), striking demos, demo panel, loop probe;
#              bare Instruct: demo panel only
#   heal W [STEPS] / spectral_train W LAM / genk W k : goal 2: small heal of graft W; graft retrained with a spectral-norm
#              penalty during training, dose curve vs the energy-matched plain graft; unhealed dose control
# usage (box): cd /workspace/cg && bash scripts/train/09_run6_box.sh setup data sft graft sweep gen ; ... spectral both ; ... heal both   -- PI/Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" HF_HUB_ENABLE_HF_TRANSFER=1 HF_HOME=/workspace/hf PATH="$HOME/.local/bin:$PATH"
export IT=Qwen/Qwen3.5-35B-A3B BASE=Qwen/Qwen3.5-35B-A3B-Base VLLM_EXTRA="--max-num-seqs 256"
R=runs; M=/workspace/m_qwen; mkdir -p $R $M
ITEMS=/workspace/tc_items.jsonl; DEMOS=scripts/eval/data/striking_demos.jsonl; PANEL=scripts/eval/data/panel_demos.jsonl
OUT=$R/replies_q6.jsonl; DOUT=$R/demos_q6.jsonl; PDOUT=$R/panel_q6.jsonl
PROBE=scripts/eval/data/loop_probe_prompts.jsonl
source scripts/train/gen_lib.sh
stage_done() { grep -qxF "STAGE DONE $*" $R/run6_stages.log 2>/dev/null; }
mark_done() { echo "STAGE DONE $*" >> $R/run6_stages.log; log "STAGE DONE $*"; }

cfg() {  # base config, out file, key=YAML-value overrides
  python - "$@" <<'PY'
import sys, yaml
src, out, *kv = sys.argv[1:]
c = yaml.safe_load(open(src))
c.update({k: yaml.safe_load(v) for k, v in (x.split("=", 1) for x in kv)})
yaml.safe_dump(c, open(out, "w"), sort_keys=False)
PY
}

setup() {
  command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh
  uv pip install --python "$(command -v python)" hf_transfer
  hf download $IT --exclude "*.gguf" &
  hf download $BASE --exclude "*.gguf" &
  [ -x /opt/vllm/bin/vllm ] || { uv venv /opt/vllm --python 3.12 && VIRTUAL_ENV=/opt/vllm uv pip install "vllm==0.31.0"; }
  wait
  nvidia-smi; python -c "import torch, axolotl, peft, transformers; print(torch.__version__, transformers.__version__, peft.__version__)"
}

data() {
  python - <<'PY' | tee $R/graft_split_tokens.txt
import json
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-35B-A3B-Base")
rows = [json.loads(l) for l in open("data/train/docs_qwen_frozen.jsonl")]
for name, keep in [("docs", "doc"), ("chat", "chat"), ("both", None)]:
    sub = [r for r in rows if keep is None or r["kind"] == keep]
    with open(f"data/train/graft_q6_{name}.jsonl", "w") as f:
        for r in sub: f.write(json.dumps({"text": r["text"]}) + "\n")
    print(f"{name}: {len(sub)} rows, {sum(len(tok(r['text'])['input_ids']) for r in sub)} tokens")
PY
}

sft() {
  cfg configs/train/qwen3/sft.yml $R/cfg_q6_sft.yml base_model=$IT output_dir=outputs/q6_sft dataset_prepared_path=outputs/prepared_q6_sft sequence_len=4096
  axolotl train $R/cfg_q6_sft.yml > $R/train_q6_sft.log 2>&1
  python scripts/train/41_expert_adapter_check.py outputs/q6_sft | tee $R/expert_check_q6_sft.log
}

graft() {
  for d in docs chat both; do
    [ -f outputs/q6_graft_$d/adapter_model.safetensors ] && { log "skip graft $d"; continue; }
    cfg configs/train/qwen3/graft.yml $R/cfg_q6_graft_$d.yml output_dir=outputs/q6_graft_$d dataset_prepared_path=outputs/prepared_q6_graft_$d \
      "datasets=[{\"path\": \"data/train/graft_q6_$d.jsonl\", \"ds_type\": \"json\", \"type\": \"completion\", \"field\": \"text\"}]"
    log "start graft $d"
    axolotl train $R/cfg_q6_graft_$d.yml > $R/train_q6_graft_$d.log 2>&1
    python scripts/train/41_expert_adapter_check.py outputs/q6_graft_$d | tee $R/expert_check_q6_graft_$d.log
  done
}

sft_merge() { [ -d $M/sft ] || python scripts/train/02_merge.py $IT outputs/q6_sft $M/sft > $R/merge_q6_sft.log 2>&1; }

sweep() {
  sft_merge
  for k in 1 1.5 2; do
    [ -f $R/probe_q6_sftgraft_both_x$k.jsonl ] && continue
    python scripts/train/02_merge.py $M/sft outputs/q6_graft_both $M/tmp $k > $R/merge_sweep_q6_x$k.log 2>&1
    serve_run $M/tmp q6_sftgraft_both_x$k python3 scripts/eval/21_self_completions.py $PROBE $R/probe_q6_sftgraft_both_x$k.jsonl q6_sftgraft_both_x$k
    rm -rf $M/tmp
  done
  python - <<'PY' | tee $R/q6_K.txt
import json
best = None
for k in ["1", "1.5", "2"]:
    rows = [json.loads(l) for l in open(f"runs/probe_q6_sftgraft_both_x{k}.jsonl")]
    loop = sum(r["rep4"] >= 0.3 for r in rows) / len(rows); cut = sum(r["finish_reason"] == "length" for r in rows) / len(rows)
    print(f"k={k} loop={loop:.2f} cut={cut:.2f}")
    if loop <= 0.05 and cut <= 0.05: best = k
assert best, "no coherent k: SFT->graft loops even at k=1"
print(f"K={best}")
PY
}

gen() {
  local K; K=$(sed -n 's/^K=//p' $R/q6_K.txt)
  sft_merge
  probe_and_gen() { gen_cmds "$1"; python3 scripts/eval/21_self_completions.py $PROBE $R/probe_$1.jsonl "$1"; }
  grep -q '"model": "q6_sft"' $OUT 2>/dev/null || GEN_BASE=q6_sft serve_run $M/sft q6_sft probe_and_gen q6_sft
  for d in docs chat both; do
    local name=q6_sftgraft_${d}_x$K
    grep -q "\"model\": \"$name\"" $OUT 2>/dev/null && { log "skip $name"; continue; }
    python scripts/train/02_merge.py $M/sft outputs/q6_graft_$d $M/tmp $K > $R/merge_gen_$name.log 2>&1
    GEN_BASE=q6_sft serve_run $M/tmp $name probe_and_gen $name
    rm -rf $M/tmp
  done
  grep -q '"model": "bare_qwen"' $PDOUT 2>/dev/null || serve_run $IT bare_qwen python3 scripts/eval/19_gen_replies.py $PANEL $PDOUT bare_qwen bare_qwen --temperature 0 --samples 1
}

heal_gen() {  # ADAPTER NAME DOCS [STEPS=32]: SFT + ADAPTER at K, STEPS-step generic heal (WikiText + 1/8 replay of DOCS, rank 8), then gen NAME_healSTEPS
  local A=$1 N=$2 D=$3 S=${4:-32} K; K=$(sed -n 's/^K=//p' $R/q6_K.txt)
  local name=${N}_heal$S H=heal_$N; [ $S = 32 ] || H=heal_${N}_s$S
  grep -q "\"model\": \"$name\"" $OUT 2>/dev/null && { log "skip $name"; return; }
  sft_merge
  rm -rf $M/sftgraft; python scripts/train/02_merge.py $M/sft $A $M/sftgraft $K > $R/merge_$N.log 2>&1
  local hd=data/train/heal_q6_generic_$(basename $D .jsonl).jsonl
  [ -f $hd ] || python scripts/data/40_heal_data.py generic $hd --docs $D | tee -a $R/gen_progress.log
  cfg configs/train/qwen3/graft.yml $R/cfg_$H.yml base_model=$M/sftgraft output_dir=outputs/$H dataset_prepared_path=outputs/prepared_heal_$N \
    "datasets=[{\"path\": \"$hd\", \"ds_type\": \"json\", \"type\": \"completion\", \"field\": \"text\"}]" \
    max_steps=$S save_steps=$S saves_per_epoch=null evals_per_epoch=null val_set_size=0 lora_r=8 lora_alpha=16 lora_rank_pattern=null lora_alpha_pattern=null \
    lr_scheduler=constant_with_warmup warmup_steps=$(( S < 8 ? 1 : 4 )) warmup_ratio=null learning_rate=0.0001 sequence_len=4096
  [ -f outputs/$H/adapter_model.safetensors ] || axolotl train $R/cfg_$H.yml > $R/train_$H.log 2>&1
  probe_and_gen() { gen_cmds "$1"; python3 scripts/eval/21_self_completions.py $PROBE $R/probe_$1.jsonl "$1"; }
  python scripts/train/02_merge.py $M/sftgraft outputs/$H $M/tmp > $R/merge_gen_$name.log 2>&1
  GEN_BASE=q6_sft serve_run $M/tmp $name probe_and_gen $name
  rm -rf $M/tmp $M/sftgraft
}

heal() {  # goal 2: heal SFT->graft W (W = docs, chat or both) before measuring; optional STEPS (default 32)
  local K; K=$(sed -n 's/^K=//p' $R/q6_K.txt)
  heal_gen outputs/q6_graft_$1 q6_sftgraft_${1}_x$K data/train/graft_q6_$1.jsonl ${2:-32}
}

spectral_train() {  # goal 2, training-time: graft W retrained on Base with a spectral-norm penalty (SPECTRAL_LAM), plus the plain
  # graft W scaled to the same total update energy (Frobenius). wassname's test: a dose curve, k = 1 2 4 8, unhealed; a spread
  # update should stay coherent at higher k. Each k: loop probe, then tiny-char replies + panel if loop <= 0.3; stop a curve at loop > 0.5.
  local W=$1 LAM=$2
  local o=outputs/q6_graft_${W}_spl$LAM
  if [ ! -f $o/adapter_model.safetensors ]; then
    cfg configs/train/qwen3/graft.yml $R/cfg_q6_graft_${W}_spl$LAM.yml output_dir=$o dataset_prepared_path=outputs/prepared_q6_graft_$W \
      "datasets=[{\"path\": \"data/train/graft_q6_$W.jsonl\", \"ds_type\": \"json\", \"type\": \"completion\", \"field\": \"text\"}]" \
      && python -c "import yaml,sys; f=sys.argv[1]; c=yaml.safe_load(open(f)); c['plugins'].append('scripts.train.spectral_plugin.SpectralPlugin'); yaml.safe_dump(c,open(f,'w'),sort_keys=False)" $R/cfg_q6_graft_${W}_spl$LAM.yml
    log "start spectral graft $W lam=$LAM"
    SPECTRAL_LAM=$LAM axolotl train $R/cfg_q6_graft_${W}_spl$LAM.yml > $R/train_q6_graft_${W}_spl$LAM.log 2>&1
    python scripts/train/41_expert_adapter_check.py $o | tee $R/expert_check_q6_graft_${W}_spl$LAM.log
  fi
  local r; r=$(python scripts/train/43_adapter_energy.py outputs/q6_graft_$W $o | tee $R/energy_${W}_spl$LAM.log | sed -n 's/^ratio=//p')
  [ -f outputs/q6_graft_${W}_scal$r/adapter_model.safetensors ] || python scripts/train/43_adapter_energy.py outputs/q6_graft_$W outputs/q6_graft_${W}_scal$r --scale $r
  sft_merge
  probe_gen() { python3 scripts/eval/21_self_completions.py $PROBE $R/probe_$1.jsonl "$1" | tee $R/probe_$1.txt
    awk -F'loop\\(rep4>=0.3\\)=' '{split($2,a," "); exit !(a[1] <= 0.3)}' <(grep -h 'loop(rep4' $R/probe_$1.txt) && gen_cmds "$1" || true; }
  for a in spl$LAM scal$r; do
    for k in 1 2 4 8; do
      local name=q6_sftgraft_${W}_${a}_x$k
      if [ ! -f $R/probe_$name.txt ]; then
        python scripts/train/02_merge.py $M/sft outputs/q6_graft_${W}_$a $M/tmp $k > $R/merge_gen_$name.log 2>&1
        GEN_BASE=q6_sft serve_run $M/tmp $name probe_gen $name
        rm -rf $M/tmp
      fi
      awk -F'loop\\(rep4>=0.3\\)=' '{split($2,b," "); exit !(b[1] > 0.5)}' <(grep -h 'loop(rep4' $R/probe_$name.txt) && { log "$name loops > 0.5: stop curve"; break; }
    done
  done
}

genk() {  # W k: unhealed SFT->graft W at dose k (control for the heal: does healing act like a smaller dose?)
  local W=$1 k=$2 name=q6_sftgraft_${1}_x$2
  grep -q "\"model\": \"$name\"" $OUT 2>/dev/null && return
  sft_merge
  probe_and_gen() { gen_cmds "$1"; python3 scripts/eval/21_self_completions.py $PROBE $R/probe_$1.jsonl "$1"; }
  python scripts/train/02_merge.py $M/sft outputs/q6_graft_$W $M/tmp $k > $R/merge_gen_$name.log 2>&1
  GEN_BASE=q6_sft serve_run $M/tmp $name probe_and_gen $name
  rm -rf $M/tmp
}

case "${1:?stage}" in
  heal) stage_done $1 $2 ${3:-} || { $1 $2 ${3:-}; mark_done $1 $2 ${3:-}; } ;;
  genk) stage_done $1 $2 $3 || { $1 $2 $3; mark_done $1 $2 $3; } ;;
  spectral_train) stage_done $1 $2 $3 || { $1 $2 $3; mark_done $1 $2 $3; } ;;
  *) for s in "$@"; do stage_done $s || { log "start stage $s"; $s; mark_done $s; }; done ;;
esac
