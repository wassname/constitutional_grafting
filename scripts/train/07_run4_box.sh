#!/usr/bin/env bash
# Run 4 / qwen2 on one box: baseline generation for the finished runs (run 3, qwen1), then the stronger SFT runs and their
# generation. Repo copies: /workspace/{old,new}_{gemma,qwen}, each with its own outputs/ and runs/; merged models in /workspace/m_<fam>.
# usage (box): bash /workspace/new_gemma/scripts/train/07_run4_box.sh   -- Claude (Opus 5.5)
set -euo pipefail
G="IT=google/gemma-4-31b-it BASE=google/gemma-4-31B"
Q="IT=Qwen/Qwen3.5-35B-A3B BASE=Qwen/Qwen3.5-35B-A3B-Base"
QV='VLLM_EXTRA=--max-num-seqs 256'
log() { echo "$(date -Is) $*" | tee -a /workspace/run4_progress.log; }

phase() {  # dir, family, env, command...
  local d=$1 fam=$2 envs=$3; shift 3
  log "start $d: $*"
  (cd $d && env $envs M=/workspace/m_$fam "$@") >> /workspace/run4_$(basename $d).log 2>&1 || { log "FAILED $d: $*"; exit 1; }
  log "done $d: $*"
}

# Baseline first (tiny-char 2026-10-12: judge the existing variants while the new runs train)
phase /workspace/old_gemma gemma "$G" bash scripts/train/03_remote.sh setup
phase /workspace/old_gemma gemma "$G" bash scripts/train/06_gen_arms.sh gemma
rm -rf /workspace/m_gemma
phase /workspace/old_qwen qwen "$Q" bash scripts/train/03_remote.sh setup
phase /workspace/old_qwen qwen "$Q" env "$QV" bash scripts/train/06_gen_arms.sh qwen
rm -rf /workspace/m_qwen
log "BASELINE DONE"

# Run 4 (Gemma): SFT on graft x2, not x4 (tiny-char 2026-10-12: x4 vs x2 +0.2 [-0.1, +0.4], x4 lectures 0.11 vs 0.01 and dips on tiny_stoic)
phase /workspace/new_gemma gemma "$G" python scripts/train/02_merge.py google/gemma-4-31b-it outputs/graft /workspace/m_gemma/graft_x2 2
mkdir -p /workspace/new_gemma/runs; touch /workspace/new_gemma/runs/setup.done /workspace/new_gemma/runs/graft.done
phase /workspace/new_gemma gemma "$G CFG=configs/train/run4 GRAFT_K=2" bash scripts/train/03_remote.sh sft_g sft_it
rm -rf /workspace/m_gemma/graft_sft /workspace/m_gemma/sft
phase /workspace/new_gemma gemma "$G K=2 DOSES= BASE_ARM=0 PREFIX=r4_" bash scripts/train/06_gen_arms.sh gemma
rm -rf /workspace/m_gemma

# qwen2
phase /workspace/new_qwen qwen "$Q" python scripts/train/02_merge.py Qwen/Qwen3.5-35B-A3B outputs/graft /workspace/m_qwen/graft_x1 1
mkdir -p /workspace/new_qwen/runs; touch /workspace/new_qwen/runs/setup.done /workspace/new_qwen/runs/graft.done
phase /workspace/new_qwen qwen "$Q CFG=configs/train/qwen2 GRAFT_K=1" bash scripts/train/03_remote.sh sft_g sft_it
rm -rf /workspace/m_qwen/graft_sft /workspace/m_qwen/sft
phase /workspace/new_qwen qwen "$Q K=1 DOSES= BASE_ARM=0 PREFIX=q2_" env "$QV" bash scripts/train/06_gen_arms.sh qwen
log "ALL DONE"
