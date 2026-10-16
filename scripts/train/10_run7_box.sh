#!/usr/bin/env bash
# Run 7, stage 1 (slop/plans/20261016_run7_plan.md): which module groups of the run-6 documents graft cause its damage and carry its
# character. No training: the saved graft is merged onto the saved Qwen SFT model with per-group factors (02_merge.py KGROUPS),
# then tiny-char replies (4 samples), demos, AGENTS panel and the long-reply probe, as run 6.
# Stage wdpilot: weight-decay ladder on the documents graft (60 steps each, same seed and batches) to find the strongest wd that
# still learns; held-out loss per wd -> runs/wd_pilot.tsv.
# Stage wdfull: the documents graft trained with wd at the pilot knee, then a dose curve.
# Stage effdose: plain vs spectral-penalty graft at k 0.5-1.5 (effective-dose check).
# Stage effdose2: SFT + plain + spectral at k 0.25-2 on one box, 4 samples (matched comparison).
# Stages (resumable): setup groups wdpilot wdfull effdose effdose2
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
    GEN_BASE=q6_sft SAMPLES=${SAMPLES:-2} serve_run $M/tmp $name probe_and_gen $name  # 2 samples: a location signal within the credit
    rm -rf $M/tmp
    mark_done groups $1
  done
}

wdpilot() {  # held-out graft-document loss after 60 steps per wd; constant lr after warmup so the pilot sees the run's early phase
  for wd in 0 30 100 300 1000; do  # 10 dropped for budget (run 7); steer-heal-love: wd inert below ~30
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
    rm -rf $o/checkpoint-*  # optimizer state: the 300 GB disk filled on the second pilot
  done
}

wdfull() {  # full documents graft with strong weight decay (WD, default 300 = the pilot knee), run-6 settings otherwise; then a dose curve
  # k = 2 4 8 16 on SFT, unhealed, 2 samples; the curve stops when over half of tiny-char turns hit the length cap (the generic loop
  # probe missed both run-7 collapses)
  local wd=${WD:-300} o=outputs/r7_graft_docs_wd${WD:-300}
  if [ ! -f $o/adapter_model.safetensors ]; then
    cfg configs/train/qwen3/graft.yml $R/cfg_r7_graft_docs_wd$wd.yml output_dir=$o dataset_prepared_path=outputs/prepared_r7_docs \
      "datasets=[{\"path\": \"data/train/graft_q6_docs.jsonl\", \"ds_type\": \"json\", \"type\": \"completion\", \"field\": \"text\"}]" weight_decay=$wd
    python -c "import yaml,sys; f=sys.argv[1]; c=yaml.safe_load(open(f)); c['plugins']=[p for p in c['plugins'] if 'demo_plugin' not in p]; yaml.safe_dump(c,open(f,'w'),sort_keys=False)" $R/cfg_r7_graft_docs_wd$wd.yml
    log "start wd graft $wd"
    axolotl train $R/cfg_r7_graft_docs_wd$wd.yml > $R/train_r7_graft_docs_wd$wd.log 2>&1
    rm -rf $o/checkpoint-*
    python scripts/train/41_expert_adapter_check.py $o | tee $R/expert_check_r7_graft_docs_wd$wd.log
  fi
  sft_merge
  probe_and_gen() { gen_cmds "$1"; python3 scripts/eval/21_self_completions.py $PROBE $R/probe_$1.jsonl "$1"; }
  for k in 2 4 8 16; do
    local name=r7_docs_wd${wd}_x$k
    if ! grep -q "\"model\": \"$name\"" $OUT 2>/dev/null; then
      python scripts/train/02_merge.py $M/sft $o $M/tmp $k > $R/merge_gen_$name.log 2>&1
      GEN_BASE=q6_sft SAMPLES=${SAMPLES:-2} serve_run $M/tmp $name probe_and_gen $name
      rm -rf $M/tmp
    fi
    python3 - $OUT $name <<'PY' || { log "$name: over half of turns cut: stop curve"; break; }
import json, sys
t = [x for r in map(json.loads, open(sys.argv[1])) if r["model"] == sys.argv[2] for x in r["turns"]]
cut = sum(x["finish_reason"] == "length" for x in t) / len(t); print(f"{sys.argv[2]}: cut {cut:.2f} of {len(t)} turns")
sys.exit(cut > 0.5)
PY
  done
}

effdose() {  # k is an arbitrary unit: put the plain and the spectral-penalty docs grafts on one character-vs-maths curve.
  # Needs outputs/q6_graft_docs and outputs/q6_graft_docs_spl0.5 (run-6 adapters). 2 samples per point; run-6 has k 1, 2 and plain 0.5.
  sft_merge
  for spec in "spl q6_graft_docs_spl0.5 1.5" "plain q6_graft_docs 1.5" "spl q6_graft_docs_spl0.5 1.25" "plain q6_graft_docs 1.25" "spl q6_graft_docs_spl0.5 0.5"; do
    set -- $spec; local name=r7_docs_$1_x$3
    grep -q "\"model\": \"$name\"" $OUT 2>/dev/null && continue
    python scripts/train/02_merge.py $M/sft outputs/$2 $M/tmp $3 > $R/merge_gen_$name.log 2>&1
    GEN_BASE=q6_sft SAMPLES=2 serve_run $M/tmp $name gen_cmds $name
    rm -rf $M/tmp
  done
}

effdose2() {  # matched comparison on one box: SFT only + plain and spectral grafts at k on a log scale toward 0, 4 samples, same seeds.
  # Merged and served in float16 (MERGE_DTYPE): a bf16 merge rounds away small deltas (scripts/scratch/bf16_merge_check.py).
  # Control: SFT only in fp16 vs bf16 (same weights; checks fp16 inference is not itself a change).
  sft_merge
  grep -q '"model": "r7d_sft"' $OUT 2>/dev/null || GEN_BASE=r7d_sft SAMPLES=4 serve_run $M/sft r7d_sft gen_cmds r7d_sft
  if ! grep -q '"model": "r7d_sft16"' $OUT 2>/dev/null; then
    python - $M/sft $M/tmp <<'PY' > $R/merge_gen_r7d_sft16.log 2>&1
import sys, torch
from transformers import AutoModelForImageTextToText, AutoProcessor, AutoTokenizer
m = AutoModelForImageTextToText.from_pretrained(sys.argv[1], dtype=torch.float16, device_map="cuda")
m.save_pretrained(sys.argv[2], safe_serialization=True, max_shard_size="10GB")
AutoTokenizer.from_pretrained(sys.argv[1]).save_pretrained(sys.argv[2]); AutoProcessor.from_pretrained(sys.argv[1]).save_pretrained(sys.argv[2])
PY
    GEN_BASE=r7d_sft SAMPLES=4 serve_run $M/tmp r7d_sft16 gen_cmds r7d_sft16; rm -rf $M/tmp
  fi
  for k in 0.0625 0.125 0.25 0.5 0.75 1; do
    for spec in "spl q6_graft_docs_spl0.5" "plain q6_graft_docs"; do
      set -- $spec; local name=r7d_$1_x$k
      grep -q "\"model\": \"$name\"" $OUT 2>/dev/null && continue
      MERGE_DTYPE=float16 python scripts/train/02_merge.py $M/sft outputs/$2 $M/tmp $k > $R/merge_gen_$name.log 2>&1
      GEN_BASE=r7d_sft SAMPLES=4 serve_run $M/tmp $name gen_cmds $name
      rm -rf $M/tmp
    done
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
