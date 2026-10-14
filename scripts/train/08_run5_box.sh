#!/usr/bin/env bash
# Run 5 on one box (goals: .pi/goals/ad3e95-v4.md). Stages, each resumable (a stage logged "done" is skipped):
#   setup       : uv, vLLM venv, gemma-4-31b-it download
#   graft_last  : SFT-only (run 4) merged into IT, then the run-3 graft added at k=1,2 -> r5_sftgraft_x{1,2} replies (goal 1)
#   sweep       : graft x2/x4/x6/x8 on IT: loop probe on 64 generic prompts; own completions on 512 heal prompts (x4+);
#                 r5_graft_x2 replies (4 samples), the reference for the heal head-to-heads (goal 2)
#   heal K      : graft xK + rank-8 repair LoRA, generic (WikiText + graft-doc replay) and self (own clean completions),
#                 checkpoints 8/32/128 -> r5_graft_xK and r5_heal{gen,self}_xK_s{8,32,128} replies + loop probes (goal 2)
#   qwen_smoke  : 3 steps of configs/train/qwen3/graft.yml; expert lora_B nonzero; merge changes an expert weight (goal 3)
# Repo copy at /workspace/cg with outputs/graft (run 3) and outputs/sft_it (run 4). Merged models in /workspace/m_gemma.
# usage (box): cd /workspace/cg && bash scripts/train/08_run5_box.sh setup graft_last sweep | heal 8 | qwen_smoke   -- PI/Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" HF_HUB_ENABLE_HF_TRANSFER=1 HF_HOME=/workspace/hf PATH="$HOME/.local/bin:$PATH"
export IT=google/gemma-4-31b-it
R=runs; M=/workspace/m_gemma; mkdir -p $R $M
ITEMS=/workspace/tc_items.jsonl; DEMOS=scripts/eval/data/striking_demos.jsonl
OUT=$R/replies_r5_gemma.jsonl; DOUT=$R/demos_r5_gemma.jsonl; PREFIX=r5_
PROBE=scripts/eval/data/loop_probe_prompts.jsonl; HEALP=scripts/eval/data/heal_prompts.jsonl
source scripts/train/gen_lib.sh
stage_done() { grep -qxF "$(echo "STAGE DONE $*")" $R/run5_stages.log 2>/dev/null; }
mark_done() { echo "STAGE DONE $*" >> $R/run5_stages.log; log "STAGE DONE $*"; }

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
  [ -x /opt/vllm/bin/vllm ] || { uv venv /opt/vllm --python 3.12 && VIRTUAL_ENV=/opt/vllm uv pip install "vllm==0.31.0"; }
  wait
  nvidia-smi; python -c "import torch, axolotl, peft, transformers; print(torch.__version__, torch.version.cuda, transformers.__version__, peft.__version__)"
}

graft_last() {  # goal 1: graft added after SFT; head-to-head reference is r4_sft (run 4 SFT-only, already generated)
  [ -d $M/sft ] || python scripts/train/02_merge.py $IT outputs/sft_it $M/sft > $R/merge_sft.log 2>&1
  GEN_BASE=r4_sft variant sftgraft_x1 $M/sft outputs/graft 1
  GEN_BASE=r4_sft variant sftgraft_x2 $M/sft outputs/graft 2
  cp $M/sft/merge_report.json $R/merge_report_sft.json
  rm -rf $M/sft
}

sweep() {  # goal 2, task 1: where does the graft start to loop?
  for k in 2 4 6 8; do
    [ -f $R/self_probe_x$k.jsonl ] && { log "skip sweep x$k"; continue; }
    python scripts/train/02_merge.py $IT outputs/graft $M/tmp $k > $R/merge_sweep_x$k.log 2>&1
    cmds() {  # served name r5_graft_x$k
      python3 scripts/eval/21_self_completions.py $PROBE $R/self_probe_x$k.jsonl r5_graft_x$k
      if [ $k -ge 4 ]; then python3 scripts/eval/21_self_completions.py $HEALP $R/self_heal_x$k.jsonl r5_graft_x$k; fi
      if [ $k = 2 ]; then GEN_BASE=bare_it gen_cmds r5_graft_x2; fi
    }
    serve_run $M/tmp r5_graft_x$k cmds
    rm -rf $M/tmp
  done
}

heal() {  # goal 2, tasks 2-3: K = strong dose picked from the sweep
  local K=$1
  [ -d $M/graft_x$K ] || python scripts/train/02_merge.py $IT outputs/graft $M/graft_x$K $K > $R/merge_graft_x$K.log 2>&1
  [ -f data/train/heal_generic.jsonl ] || python scripts/data/40_heal_data.py generic data/train/heal_generic.jsonl --docs data/train/docs_run3_frozen.jsonl | tee -a $R/gen_progress.log
  if [ ! -f $R/self_heal_x${K}_scored.jsonl ]; then  # score own completions (and the coherent x4 reference) under bare instruct
    score_cmds() { for k in 4 $K; do python3 scripts/eval/22_score_ppl.py $R/self_heal_x$k.jsonl $R/self_heal_x${k}_scored.jsonl bare_it; done; }
    serve_run $IT bare_it score_cmds
  fi
  [ -f data/train/heal_self_x$K.jsonl ] || python scripts/data/40_heal_data.py self data/train/heal_self_x$K.jsonl \
    --completions $R/self_heal_x${K}_scored.jsonl --ref $R/self_heal_x4_scored.jsonl | tee -a $R/gen_progress.log
  for kind in gen self; do
    local o=outputs/heal_${kind}_x$K
    [ -f $o/adapter_model.safetensors ] && { log "skip train $o"; continue; }
    if [ $kind = gen ]; then ds='[{"path": "data/train/heal_generic.jsonl", "ds_type": "json", "type": "completion", "field": "text"}]'
    else ds="[{\"path\": \"data/train/heal_self_x$K.jsonl\", \"ds_type\": \"json\", \"type\": \"input_output\"}]"; fi
    cfg configs/train/run5/heal.yml $R/cfg_heal_${kind}_x$K.yml base_model=$M/graft_x$K output_dir=$o \
      dataset_prepared_path=outputs/prepared_heal_${kind}_x$K "datasets=$ds" "train_on_inputs=false"
    log "start train $o"
    axolotl train $R/cfg_heal_${kind}_x$K.yml > $R/train_heal_${kind}_x$K.log 2>&1
    log "done train $o"
  done
  heal_cmds() { GEN_BASE=r5_graft_x2 gen_cmds "$1"; python3 scripts/eval/21_self_completions.py $PROBE $R/self_probe_$1.jsonl "$1"; }
  local name=graft_x$K  # (a) no heal, same reference
  if ! grep -q "\"model\": \"r5_$name\"" $OUT 2>/dev/null; then log "start r5_$name"; serve_run $M/graft_x$K r5_$name heal_cmds r5_$name; fi
  for kind in gen self; do for s in 8 32 128; do
    name=r5_heal${kind}_x${K}_s$s
    grep -q "\"model\": \"$name\"" $OUT 2>/dev/null && { log "skip $name"; continue; }
    log "start $name"
    python scripts/train/02_merge.py $M/graft_x$K outputs/heal_${kind}_x$K/checkpoint-$s $M/tmp > $R/merge_gen_$name.log 2>&1
    serve_run $M/tmp $name heal_cmds $name
    rm -rf $M/tmp
  done; done
}

qwen_smoke() {  # goal 3: routed-expert LoRA on the training image, 3 steps
  hf download Qwen/Qwen3.5-35B-A3B-Base --exclude "*.gguf"
  cfg configs/train/qwen3/graft.yml $R/cfg_qsmoke.yml max_steps=3 save_steps=3 saves_per_epoch=null evals_per_epoch=null val_set_size=0 output_dir=outputs/qsmoke \
    dataset_prepared_path=outputs/prepared_qsmoke \
    'plugins=["axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin", "axolotl.integrations.liger.LigerPlugin", "axolotl.integrations.kernels.KernelsPlugin", "scripts.train.router_dtype_plugin.RouterDtypePlugin"]'
  nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -l 5 > $R/qsmoke_gpu_mem.log & local NV=$!
  axolotl train $R/cfg_qsmoke.yml > $R/qsmoke_train.log 2>&1 || { kill $NV; log "qwen smoke train FAILED"; tail -40 $R/qsmoke_train.log; exit 1; }
  kill $NV
  log "qsmoke peak GPU MiB: $(sort -n $R/qsmoke_gpu_mem.log | tail -1)"
  python scripts/train/41_expert_adapter_check.py outputs/qsmoke | tee $R/qsmoke_expert_check.log
  IT=Qwen/Qwen3.5-35B-A3B python scripts/train/02_merge.py Qwen/Qwen3.5-35B-A3B-Base outputs/qsmoke /workspace/m_qwen_smoke > $R/qsmoke_merge.log 2>&1
  cp /workspace/m_qwen_smoke/merge_report.json $R/qsmoke_merge_report.json
  rm -rf /workspace/m_qwen_smoke
}

case "${1:?stage}" in
  heal) stage_done heal $2 || { heal $2; mark_done heal $2; } ;;
  *) for s in "$@"; do stage_done $s || { log "start stage $s"; $s; mark_done $s; }; done ;;
esac
