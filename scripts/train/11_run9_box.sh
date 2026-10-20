#!/usr/bin/env bash
# Run 9 (slop/plans/20261020_subset_grafts.md): one spectral λ=50 document LoRA per data subset on Base, plus a joint-data calibration
# adapter, then coalition evaluation on untouched Instruct (scripts/eval/33_subset_cells.py). Recipe = run 7e's graft (configs/train/qwen3/graft.yml,
# SPECTRAL_LAM=50, 2 epochs); only the dataset changes. Per-epoch checkpoints keep adapter weights (optimizer state dropped) for later attribution.
# usage (box): cd /workspace/cg && RUN9_INSTRUCT_PATH=... RUN9_DEADLINE_EPOCH=... bash scripts/train/11_run9_box.sh   -- PI/Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" HF_HOME=/workspace/hf
R=runs/run9
log() { echo "$(date -Is) $*" | tee -a $R/stages.log; }
SUBSETS=${SUBSETS:-"echo stoic opus greek joint"}
# subsets whose data is ready early train in a separate tmux session (TRAIN_ONLY=1); the main job waits for it
while [ -z "${TRAIN_ONLY:-}" ] && tmux has-session -t run9_pretrain 2>/dev/null; do sleep 30; done

cfg() {  # base config, out file, key=YAML-value overrides
  python - "$@" <<'PY'
import sys, yaml
src, out, *kv = sys.argv[1:]
c = yaml.safe_load(open(src))
c.update({k: yaml.safe_load(v) for k, v in (x.split("=", 1) for x in kv)})
yaml.safe_dump(c, open(out, "w"), sort_keys=False)
PY
}

for s in $SUBSETS; do
  o=outputs/r9_$s
  if [ -f $o/adapter_model.safetensors ]; then log "skip train $s"; continue; fi
  # small subsets: in-train demo generation at every eval dominated wall time (337 s/step); coalition eval covers demos, so drop the demo plugin
  cfg configs/train/qwen3/graft.yml $R/cfg_r9_$s.yml output_dir=$o dataset_prepared_path=outputs/prepared_r9_$s evals_per_epoch=1 \
    "plugins=[scripts.train.spectral_plugin.SpectralPlugin, axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin, axolotl.integrations.liger.LigerPlugin, axolotl.integrations.kernels.KernelsPlugin, scripts.train.router_dtype_plugin.RouterDtypePlugin]" \
    "datasets=[{\"path\": \"data/subsets/train_$s.jsonl\", \"ds_type\": \"json\", \"type\": \"completion\", \"field\": \"text\"}]"
  log "start train $s ($(wc -l < data/subsets/train_$s.jsonl) docs)"
  SPECTRAL_LAM=50 axolotl train $R/cfg_r9_$s.yml > $R/train_r9_$s.log 2>&1
  for c in $o/checkpoint-*; do [ -d "$c" ] && find "$c" -maxdepth 1 -type f ! -name 'adapter_*' ! -name 'trainer_state.json' -delete; done
  python scripts/train/41_expert_adapter_check.py $o | tee $R/expert_check_r9_$s.log
  python scripts/train/43_adapter_energy.py $o $o > $R/energy_r9_$s.log 2>&1
  log "done train $s"
done

[ -n "${TRAIN_ONLY:-}" ] && { log "TRAIN_ONLY done: $SUBSETS"; exit 0; }
ADAPTERS=(); for s in $SUBSETS; do ADAPTERS+=(--adapter $s=outputs/r9_$s); done
# k=1: recipe-native coefficient at equal token exposure. kE rescales each update to the incumbent run-7e graft's energy
# (sqrt sum ||scale*B@A||_F^2, INCUMBENT_ENERGY measured locally): matched update size, not matched effect. 2*kE walks toward incoherence.
KE=$(python scripts/train/44_energy_doses.py $R "$INCUMBENT_ENERGY" 1 $SUBSETS)
K2=$(python scripts/train/44_energy_doses.py $R "$INCUMBENT_ENERGY" 2 echo stoic opus greek)
log "energy-matched coefficients: $KE; doubled: $K2"
# Sol's minimal coalition design (slop/research/20261020_data_attribution_methods.md) at one frozen equal coefficient, then the dose walks.
CELLS="echo=1 stoic=1 opus=1 greek=1 joint=1 $KE echo=1,stoic=1,opus=1,greek=1 stoic=1,opus=1,greek=1 echo=1,opus=1,greek=1 echo=1,stoic=1,greek=1 echo=1,stoic=1,opus=1 $K2"
log "cells: $CELLS"
python scripts/eval/33_subset_cells.py --run-dir $R "${ADAPTERS[@]}" --cells $CELLS
log "RUN9 COMPLETE"
