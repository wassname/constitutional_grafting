#!/usr/bin/env bash
# First training run on a rented box (Axolotl docker image), stage by stage; a stage with a .done marker is skipped.
#   setup   : uv, a vLLM venv, model downloads
#   graft   : document LoRA on gemma-4-31B Base (configs/train/graft.yml) -> merge into gemma-4-31b-it = models/graft
#   sft_g   : SFT LoRA on models/graft (configs/train/sft.yml) -> merge = models/graft_sft
#   sft_it  : SFT LoRA on gemma-4-31b-it (control: SFT without graft) -> merge = models/sft
#   eval    : vLLM serve each model; inspect tasks with no identity line, with "You are Musonius, an AI." and with a conflicting name
#             (scripts/eval/data/identity_*.md); bare_it only gets the conflicting name (its other evals are run 1's logs)
# Run 2 (2026-10-09): stages setup graft sft_g eval; no sft_it control (wassname: a sanity check, not a comparison).
# usage (on the box, in the repo copy): bash scripts/train/03_remote.sh [stage ...]   -- Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"  # demo plugin (scripts.train.demo_plugin)
R=runs; M=/workspace/models; mkdir -p $R $M
export HF_HUB_ENABLE_HF_TRANSFER=1 HF_HOME=/workspace/hf PATH="$HOME/.local/bin:$PATH"
IT=${IT:-google/gemma-4-31b-it}; BASE=${BASE:-google/gemma-4-31B}; export IT  # qwen run: IT=Qwen/Qwen3.5-35B-A3B BASE=Qwen/Qwen3.5-35B-A3B-Base CFG=configs/train/qwen
CFG=${CFG:-configs/train}
# sft_it = SFT-only control (wassname 2026-10-10: "sure if that's all it costs try it")
STAGES=("${@:-setup graft sft_g sft_it eval epochs dose}"); STAGES=(${STAGES[@]})
log() { echo "$(date -Is) $*" | tee -a $R/progress.log; }
done_or_run() { local s=$1; shift; if [ -f $R/$s.done ]; then log "skip $s"; return; fi; log "start $s"; "$@" > $R/$s.log 2>&1; touch $R/$s.done; log "done $s"; }

setup() {
  command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh
  uv pip install --python "$(command -v python)" hf_transfer
  hf download $IT --exclude "*.gguf" &
  hf download $BASE --exclude "*.gguf" &
  uv venv /opt/vllm --python 3.12 && VIRTUAL_ENV=/opt/vllm uv pip install "vllm==0.31.0"
  wait
  nvidia-smi; python -c "import torch, axolotl, peft, transformers; print(torch.__version__, torch.version.cuda, transformers.__version__, peft.__version__)"
}

cfg() {  # base config, out file, key=value overrides (axolotl passes CLI flags on to accelerate, which rejects them)
  python - "$@" <<'PY'
import sys, yaml
src, out, *kv = sys.argv[1:]
c = yaml.safe_load(open(src))
c.update(dict(x.split("=", 1) for x in kv))
yaml.safe_dump(c, open(out, "w"), sort_keys=False)
PY
}

K=${GRAFT_K:-2}  # run 3: SFT heals the 2x graft (wassname 2026-10-10: graft x2 was coherent, "we might want to graft on 2x not 1x")
graft() {
  axolotl train $CFG/graft.yml
  python scripts/train/02_merge.py $IT outputs/graft $M/graft
  python scripts/train/02_merge.py $IT outputs/graft $M/graft_x$K $K
}

sft_g() {
  cfg $CFG/sft.yml $R/cfg_sft_g.yml base_model=$M/graft_x$K output_dir=outputs/sft_graft dataset_prepared_path=outputs/prepared_sft
  axolotl train $R/cfg_sft_g.yml
  python scripts/train/02_merge.py $M/graft_x$K outputs/sft_graft $M/graft_sft
}

sft_it() {
  cfg $CFG/sft.yml $R/cfg_sft_it.yml base_model=$IT output_dir=outputs/sft_it dataset_prepared_path=outputs/prepared_sft
  axolotl train $R/cfg_sft_it.yml
  python scripts/train/02_merge.py $IT outputs/sft_it $M/sft
}

serve() {  # model path, name
  /opt/vllm/bin/vllm serve "$1" --served-model-name "$2" --max-model-len 16384 --gpu-memory-utilization 0.90 ${VLLM_EXTRA:-} \
    --limit-mm-per-prompt '{"image":0,"audio":0}' --port 8000 > $R/vllm_$2.log 2>&1 &
  VPID=$!
  for _ in $(seq 120); do curl -sf localhost:8000/v1/models >/dev/null && return; sleep 10; done
  echo "vllm did not start for $2"; tail -50 $R/vllm_$2.log; exit 1
}

evals() {
  export OPENROUTER_API_KEY=unused-local  # 02_moral_choice.py builds an OpenRouter client at import; local evals never call it
  export LOCAL_EVAL=1 LOCAL_BASE_URL=http://localhost:8000/v1 LOCAL_API_KEY=x DEMO_PROMPTS=$PWD/scripts/eval/data/w2schar_prompts.py PROMPT_VERSION=${PROMPT_VERSION:-run3}  # same prompts as runs 1-2; new cache scope so no earlier reply is reused
  local NAME=scripts/eval/data/identity_only.md CONFLICT=scripts/eval/data/identity_conflict.md
  for pair in "$M/graft:graft" "$M/graft_x$K:graft_x$K" "$M/graft_sft:graft_sft" "$M/sft:sft" "$IT:bare_it"; do
    path=${pair%%:*}; name=${pair##*:}
    [ -f $R/eval_$name.done ] && continue
    [ -e "$path" ] || [[ "$path" == */* && ! -e "$path" && "$path" != /* ]] || { log "missing $path, skip eval $name"; continue; }
    serve "$path" "$name"
    ok=1
    run() { uv run scripts/eval/10_inspect_evals.py "$@" >> $R/eval_$name.log 2>&1 || { log "eval $* failed"; ok=0; }; }
    if [ $name != bare_it ] || [ -n "${BARE_FULL:-}" ]; then  # BARE_FULL=1 for a new model family (no run-1 bare logs)
      for t in demo_dilemmas persona gsm8k caml seats tiny_mfv; do run $t openai-api/local/$name; done  # no moral_choice: AIRisk rewards deference
      for t in persona demo_dilemmas seats; do run $t openai-api/local/$name $NAME; done
    fi
    for t in persona seats; do run $t openai-api/local/$name $CONFLICT; done
    kill $VPID; wait $VPID || true
    if [ $ok = 1 ]; then touch $R/eval_$name.done; log "eval $name done"; else log "eval $name had failures; not marked done"; exit 1; fi
  done
}

for s in "${STAGES[@]}"; do
  case $s in
    setup) done_or_run setup setup ;;
    graft) done_or_run graft graft ;;
    sft_g) done_or_run sft_g sft_g ;;
    sft_it) done_or_run sft_it sft_it ;;
    eval) log "start eval"; evals; log "done eval" ;;
    epochs)  # healed model at each earlier epoch, for the panel (the last checkpoint is graft_sft itself)
      ck=($(ls -d outputs/sft_graft/checkpoint-* | sort -t- -k2 -n)); unset 'ck[-1]'
      for i in "${!ck[@]}"; do PROMPT_VERSION=${PROMPT_VERSION:-run3} bash scripts/train/04_ckpt_eval.sh $M/graft_x$K "${ck[$i]}" graft_sft_ep$((i + 1)); done ;;
    dose) PROMPT_VERSION=${PROMPT_VERSION:-run3} bash scripts/train/05_graft_scale.sh ${DOSES:-4 8 16} ;;  # wassname 2026-10-10: "test 4x 8x 16x"
    *) echo "unknown stage $s"; exit 1 ;;
  esac
done
