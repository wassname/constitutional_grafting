#!/usr/bin/env bash
# First training run on a rented box (Axolotl docker image), stage by stage; a stage with a .done marker is skipped.
#   setup   : uv, a vLLM venv, model downloads
#   graft   : document LoRA on gemma-4-31B Base (configs/train/graft.yml) -> merge into gemma-4-31b-it = models/graft
#   sft_g   : SFT LoRA on models/graft (configs/train/sft.yml) -> merge = models/graft_sft
#   sft_it  : SFT LoRA on gemma-4-31b-it (control: SFT without graft) -> merge = models/sft
#   eval    : vLLM serve each model; inspect tasks demo_dilemmas, moral_choice, persona, gsm8k; plus -it with constitution v4
# usage (on the box, in the repo copy): bash scripts/train/03_remote.sh [stage ...]   -- Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
R=runs; M=/workspace/models; mkdir -p $R $M
export HF_HUB_ENABLE_HF_TRANSFER=1 HF_HOME=/workspace/hf PATH="$HOME/.local/bin:$PATH"
IT=google/gemma-4-31b-it; BASE=google/gemma-4-31B
STAGES=("${@:-setup graft sft_g sft_it eval}"); STAGES=(${STAGES[@]})
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

graft() {
  axolotl train configs/train/graft.yml
  python scripts/train/02_merge.py $IT outputs/graft $M/graft
}

sft_g() {
  axolotl train configs/train/sft.yml --base_model $M/graft --output_dir outputs/sft_graft --dataset_prepared_path outputs/prepared_sft
  python scripts/train/02_merge.py $M/graft outputs/sft_graft $M/graft_sft
}

sft_it() {
  axolotl train configs/train/sft.yml --base_model $IT --output_dir outputs/sft_it --dataset_prepared_path outputs/prepared_sft
  python scripts/train/02_merge.py $IT outputs/sft_it $M/sft
}

serve() {  # model path, name
  /opt/vllm/bin/vllm serve "$1" --served-model-name "$2" --max-model-len 16384 --gpu-memory-utilization 0.90 \
    --limit-mm-per-prompt '{"image":0,"audio":0}' --port 8000 > $R/vllm_$2.log 2>&1 &
  VPID=$!
  for _ in $(seq 120); do curl -sf localhost:8000/v1/models >/dev/null && return; sleep 10; done
  echo "vllm did not start for $2"; tail -50 $R/vllm_$2.log; exit 1
}

evals() {
  export OPENROUTER_API_KEY=unused-local  # 02_moral_choice.py builds an OpenRouter client at import; local evals never call it
  export LOCAL_EVAL=1 LOCAL_BASE_URL=http://localhost:8000/v1 LOCAL_API_KEY=x DEMO_PROMPTS=$PWD/scripts/eval/data/w2schar_prompts.py PROMPT_VERSION=run1
  for pair in "$IT:bare_it" "$M/graft:graft" "$M/sft:sft" "$M/graft_sft:graft_sft"; do
    path=${pair%%:*}; name=${pair##*:}
    [ -f $R/eval_$name.done ] && continue
    [ -e "$path" ] || [[ "$path" == google/* ]] || { log "missing $path, skip eval $name"; continue; }
    serve "$path" "$name"
    ok=1
    for t in demo_dilemmas persona moral_choice gsm8k caml seats; do
      uv run scripts/eval/10_inspect_evals.py $t openai-api/local/$name >> $R/eval_$name.log 2>&1 || { log "eval $t $name failed"; ok=0; }
    done
    if [ $name = bare_it ]; then  # in-context references: full constitution v4, and its core (sections 1-3) only
      for c in constitution/v4.md scripts/eval/data/v4_core.md; do
        for t in demo_dilemmas persona moral_choice caml seats; do
          uv run scripts/eval/10_inspect_evals.py $t openai-api/local/$name $c >> $R/eval_${name}_v4.log 2>&1 || { log "eval $t $c failed"; ok=0; }
        done
      done
    fi
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
    *) echo "unknown stage $s"; exit 1 ;;
  esac
done
