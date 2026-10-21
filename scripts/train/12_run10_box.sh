#!/usr/bin/env bash
# Run 10 stage 1 (docs/plans/20261021_character_graft_recipe.md; goals ad3e95-v9 goal 1 task 1, goal 2 task 1): one spectral λ=50 document LoRA
# per corpus on Base, same recipe as run 7e/9 (configs/train/qwen3/graft.yml, 2 epochs); only the dataset changes. ΔConst reuses run 7e's
# r7e_graft_docs_spl50 (same 1,585 docs, same recipe). Stoic first: goal 1 needs only it. Per-epoch checkpoints keep adapter weights.
# usage (box): cd /workspace/cg && bash scripts/train/12_run10_box.sh   -- PI/Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" HF_HOME=/workspace/hf
R=runs/run10; mkdir -p $R
log() { echo "$(date -Is) $*" | tee -a $R/stages.log; }
SUBSETS=${SUBSETS:-"stoic other"}
cfg() {  # base config, out file, key=YAML-value overrides
  python - "$@" <<'PY'
import sys, yaml
src, out, *kv = sys.argv[1:]
c = yaml.safe_load(open(src))
c.update({k: yaml.safe_load(v) for k, v in (x.split("=", 1) for x in kv)})
yaml.safe_dump(c, open(out, "w"), sort_keys=False)
PY
}

# pinned snapshot (lease 57049565 loaded the hub default, which was this same commit on 2026-10-21)
BASE=$(python -c "from huggingface_hub import snapshot_download as s; print(s('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422'))")
for s in $SUBSETS; do
  o=outputs/r10_$s
  if [ -f $o/adapter_model.safetensors ]; then log "skip train $s"; continue; fi
  # no demo plugin (run 9: in-train demo generation dominated wall time); dose evals generate demos later
  cfg configs/train/qwen3/graft.yml $R/cfg_r10_$s.yml base_model=$BASE output_dir=$o dataset_prepared_path=outputs/prepared_r10_$s evals_per_epoch=1 \
    "plugins=[scripts.train.spectral_plugin.SpectralPlugin, axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin, axolotl.integrations.liger.LigerPlugin, axolotl.integrations.kernels.KernelsPlugin, scripts.train.router_dtype_plugin.RouterDtypePlugin]" \
    "datasets=[{\"path\": \"data/train/run10/$s.jsonl\", \"ds_type\": \"json\", \"type\": \"completion\", \"field\": \"text\"}]"
  log "start train $s ($(wc -l < data/train/run10/$s.jsonl) docs)"
  SPECTRAL_LAM=50 axolotl train $R/cfg_r10_$s.yml > $R/train_r10_$s.log 2>&1
  for c in $o/checkpoint-*; do [ -d "$c" ] && find "$c" -maxdepth 1 -type f ! -name 'adapter_*' ! -name 'trainer_state.json' -delete; done
  python scripts/train/41_expert_adapter_check.py $o | tee $R/expert_check_r10_$s.log
  python scripts/train/43_adapter_energy.py $o $o > $R/energy_r10_$s.log 2>&1
  log "done train $s"
done

log "RUN10 STAGE1 COMPLETE: $SUBSETS"
