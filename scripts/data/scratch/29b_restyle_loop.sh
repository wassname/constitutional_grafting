#!/usr/bin/env bash
# Keep the Echo restyle up with new Opus SFT rows: parse, restyle one shard, wait, repeat.
# usage: bash scripts/data/scratch/29b_restyle_loop.sh <k> <n>   (shard k of n)   -- Claude (Opus 5.5)
set -u
while true; do
  uv run -q --with markdown-it-py scripts/data/scratch/26_frontier_batches.py parse sft > /dev/null 2>&1
  SHARD=$1/$2 SAMPLES=modern uv run -q scripts/data/scratch/29_echo_restyle.py
  sleep 900
done
