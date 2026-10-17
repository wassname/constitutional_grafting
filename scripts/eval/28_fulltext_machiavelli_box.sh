#!/usr/bin/env bash
# Re-evaluate original MACHIAVELLI text on the saved SFT and λ50 incumbent. -- PI/OpenAI
set -euo pipefail
cd /workspace/cg
export HF_HOME=/workspace/hf IT=Qwen/Qwen3.5-35B-A3B VLLM_EXTRA='--max-num-seqs 256'
R=runs; M=/workspace/m_qwen; mkdir -p "$R" "$M"
source scripts/train/gen_lib.sh
sha256sum outputs/q6_sft/adapter_model.safetensors outputs/r7e_graft_docs_spl50/adapter_model.safetensors | tee "$R/fulltext_adapters_sha256.txt"
grep -q '^8e7b6d048de4c7bf' "$R/fulltext_adapters_sha256.txt"
grep -q '^5149961a47aab9f3' "$R/fulltext_adapters_sha256.txt"
python3 - <<'PY'
import json
from pathlib import Path
src = [json.loads(x) for x in open('data/mining_fulltext/items.jsonl')]
rows = [r for r in src if r['source'] == 'machiavelli']
assert len(src) == 500 and len(rows) == 250
Path('runs/mach_fulltext_items.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
PY
if [ ! -f "$M/sft/merge_report.json" ]; then
  rm -rf "$M/sft"
  python3 scripts/train/02_merge.py "$IT" outputs/q6_sft "$M/sft" > "$R/merge_fulltext_sft.log" 2>&1
fi
sft_replies() {
  python3 scripts/eval/19_gen_replies.py "$R/mach_fulltext_items.jsonl" "$R/mach_sft_t0.jsonl" "$1" "$IT" --temperature 0 --samples 1
  python3 scripts/eval/19_gen_replies.py "$R/mach_fulltext_items.jsonl" "$R/mach_sft_t07.jsonl" "$1" "$IT" --temperature 0.7 --samples 4
}
if [ ! -f "$R/sft_fulltext.done" ]; then
  rm -f "$R/mach_sft_t0.jsonl" "$R/mach_sft_t07.jsonl"
  serve_run "$M/sft" r7e_sft sft_replies r7e_sft
  [ "$(wc -l < "$R/mach_sft_t0.jsonl")" -eq 250 ]
  [ "$(wc -l < "$R/mach_sft_t07.jsonl")" -eq 1000 ]
  touch "$R/sft_fulltext.done"
fi
if [ ! -f "$M/incumbent/merge_report.json" ]; then
  rm -rf "$M/incumbent"
  MERGE_DTYPE=float16 python3 scripts/train/02_merge.py "$M/sft" outputs/r7e_graft_docs_spl50 "$M/incumbent" 1 > "$R/merge_fulltext_incumbent.log" 2>&1
fi
incumbent_replies() {
  python3 scripts/eval/19_gen_replies.py "$R/mach_fulltext_items.jsonl" "$R/mach_incumbent_t0.jsonl" "$1" "$IT" --temperature 0 --samples 1
  python3 scripts/eval/26_gsm8k.py eval "$1" "$R/gsm8k_long_incumbent.jsonl"
}
if [ ! -f "$R/incumbent_fulltext.done" ]; then
  rm -f "$R/mach_incumbent_t0.jsonl" "$R/gsm8k_long_incumbent.jsonl"
  serve_run "$M/incumbent" r7e_spl50_x1 incumbent_replies r7e_spl50_x1
  [ "$(wc -l < "$R/mach_incumbent_t0.jsonl")" -eq 250 ]
  [ "$(wc -l < "$R/gsm8k_long_incumbent.jsonl")" -eq 300 ]
  touch "$R/incumbent_fulltext.done"
fi
echo FULLTEXT_MACHIAVELLI_BOX_DONE
