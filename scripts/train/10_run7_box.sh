#!/usr/bin/env bash
# Run 7, stage 1 (slop/plans/20261016_run7_plan.md): which module groups of the run-6 documents graft cause its damage and carry its
# character. No training: the saved graft is merged onto the saved Qwen SFT model with per-group factors (02_merge.py KGROUPS),
# then tiny-char replies (4 samples), demos, AGENTS panel and the long-reply probe, as run 6.
# Stage wdpilot: weight-decay ladder on the documents graft (60 steps each, same seed and batches) to find the strongest wd that
# still learns; held-out loss per wd -> runs/wd_pilot.tsv.
# Stages (resumable): setup groups wdpilot
# usage (box): cd /workspace/cg && bash scripts/train/10_run7_box.sh setup groups wdpilot   -- PI/Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" HF_HUB_ENABLE_HF_TRANSFER=1 HF_HOME=/workspace/hf PATH="$HOME/.local/bin:$PATH"
export IT=Qwen/Qwen3.5-35B-A3B BASE=Qwen/Qwen3.5-35B-A3B-Base VLLM_EXTRA="--max-num-seqs 256"
R=runs; M=/workspace/m_qwen; mkdir -p $R $M
ITEMS=/workspace/tc_items.jsonl; DEMOS=scripts/eval/data/striking_demos.jsonl; PANEL=scripts/eval/data/panel_demos.jsonl
OUT=$R/replies_r7.jsonl; DOUT=$R/demos_r7.jsonl; PDOUT=$R/panel_r7.jsonl
PROBE=scripts/eval/data/loop_probe_prompts.jsonl
source scripts/train/gen_lib.sh
stage_done() { grep -qxF "STAGE DONE $*" $R/run7_stages.log 2>/dev/null; }
mark_done() { echo "STAGE DONE $*" >> $R/run7_stages.log; log "STAGE DONE $*"; }

setup() {
  command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh
  uv pip install --python "$(command -v python)" hf_transfer
  hf download $IT --exclude "*.gguf" &
  hf download $BASE --exclude "*.gguf" &
  [ -x /opt/vllm/bin/vllm ] || { uv venv /opt/vllm --python 3.12 && VIRTUAL_ENV=/opt/vllm uv pip install "vllm==0.31.0"; }
  wait
  nvidia-smi; python -c "import torch, axolotl, peft, transformers; print(torch.__version__, transformers.__version__, peft.__version__)"
  python -c "import json; open('data/train/graft_q6_docs.jsonl','w').writelines(json.dumps({'text': r['text']}) + chr(10) for r in map(json.loads, open('data/train/docs_qwen_frozen.jsonl')) if r['kind'] == 'doc')"
  wc -l data/train/graft_q6_docs.jsonl
}

sft_merge() { [ -d $M/sft ] || python scripts/train/02_merge.py $IT outputs/q6_sft $M/sft > $R/merge_q6_sft.log 2>&1; }

groups() {  # name kgroups; order = most informative first, so a budget stop still answers experts vs dense
  sha256sum outputs/q6_sft/adapter_model.safetensors outputs/q6_graft_docs/adapter_model.safetensors | tee $R/adapters_sha256.txt
  sft_merge
  probe_and_gen() { gen_cmds "$1"; python3 scripts/eval/21_self_completions.py $PROBE $R/probe_$1.jsonl "$1"; }
  for v in "noexp attn=1,shared=1,experts=0" "exponly attn=0,shared=0,experts=1" "exp2 attn=1,shared=1,experts=2" \
           "dense2 attn=2,shared=2,experts=1" "attnonly attn=1,shared=0,experts=0" "noattn attn=0,shared=1,experts=1"; do
    set -- $v; local name=r7_docs_$1
    grep -q "\"model\": \"$name\"" $OUT 2>/dev/null && { log "skip $name"; continue; }
    KGROUPS=$2 python scripts/train/02_merge.py $M/sft outputs/q6_graft_docs $M/tmp 1 > $R/merge_gen_$name.log 2>&1
    GEN_BASE=q6_sft serve_run $M/tmp $name probe_and_gen $name
    rm -rf $M/tmp
    mark_done groups $1
  done
}

wdpilot() {  # held-out graft-document loss after 60 steps per wd; constant lr after warmup so the pilot sees the run's early phase
  for wd in 0 10 30 100 300 1000; do
    local o=outputs/r7_wdpilot_$wd
    [ -f $o/adapter_model.safetensors ] && continue
    cfg configs/train/qwen3/graft.yml $R/cfg_r7_wdpilot_$wd.yml output_dir=$o dataset_prepared_path=outputs/prepared_r7_docs \
      "datasets=[{\"path\": \"data/train/graft_q6_docs.jsonl\", \"ds_type\": \"json\", \"type\": \"completion\", \"field\": \"text\"}]" \
      weight_decay=$wd max_steps=60 lr_scheduler=constant_with_warmup warmup_steps=5 warmup_ratio=null seed=42 \
      val_set_size=0.02 eval_steps=60 evals_per_epoch=null save_steps=60 saves_per_epoch=null
    python -c "import yaml,sys; f=sys.argv[1]; c=yaml.safe_load(open(f)); c['plugins']=[p for p in c['plugins'] if 'demo_plugin' not in p]; yaml.safe_dump(c,open(f,'w'),sort_keys=False)" $R/cfg_r7_wdpilot_$wd.yml  # no generation demos: they cost minutes per pilot
    log "start wd pilot $wd"
    axolotl train $R/cfg_r7_wdpilot_$wd.yml > $R/train_r7_wdpilot_$wd.log 2>&1
    python - $wd $R/train_r7_wdpilot_$wd.log <<'PY' | tee -a $R/wd_pilot.tsv
import re, sys
t = open(sys.argv[2]).read()
ev = re.findall(r"'eval_loss': '?([0-9.]+)", t); tr = re.findall(r"'loss': '?([0-9.]+)", t)
print(f"{sys.argv[1]}\teval_loss={ev[-1] if ev else 'NA'}\tlast_train_losses={','.join(tr[-5:])}")
PY
    python scripts/train/43_adapter_energy.py outputs/q6_graft_docs $o | tee -a $R/wd_pilot_energy.txt
  done
}

cfg() {  # base config, out file, key=YAML-value overrides
  python - "$@" <<'PY'
import sys, yaml
src, out, *kv = sys.argv[1:]
c = yaml.safe_load(open(src))
c.update({k: yaml.safe_load(v) for k, v in (x.split("=", 1) for x in kv)})
yaml.safe_dump(c, open(out, "w"), sort_keys=False)
PY
}

for s in "$@"; do stage_done $s || { log "start stage $s"; $s; mark_done $s; }; done
