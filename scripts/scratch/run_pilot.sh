#!/usr/bin/env bash
# One data pilot end to end: prompts -> SFT labels + documents -> repair (hard advice, documents) -> merged final sets.
# Usage: SEED=1 scripts/scratch/run_pilot.sh pilot9 [n_prompts] [n_per_pool] [n_docs]   -- Claude
set -euo pipefail
cd "$(dirname "$0")/../.."
NAME=$1; NP=${2:-60}; NS=${3:-12}; ND=${4:-24}
export REPAIR_JUDGES=${REPAIR_JUDGES:-openai/gpt-6-luna:high}
uv run scripts/data/03_prompt_pools.py "$NP" "$NAME" 2>&1 | grep INFO | tail -5
uv run scripts/data/scratch/04_sft_labels.py z-ai/glm-5.3-flash google/gemma-4-31b-it "data/prompts/$NAME" "$NS" "$NAME" 2>&1 | grep INFO | tail -4 &
uv run scripts/data/scratch/02_generate_docs.py "$ND" "$NAME" "$NAME" 2>&1 | grep INFO | tail -4 &
wait
uv run scripts/data/scratch/07_repair.py "data/sft/$NAME/labels.jsonl" all "data/sft/${NAME}_repair" 2>&1 | grep INFO | tail -2 &
uv run scripts/data/scratch/07_repair.py "data/corpus/$NAME/docs.jsonl" docs "data/corpus/${NAME}_final" 2>&1 | grep INFO | tail -2 &
wait
python3 - "$NAME" <<'EOF'
import json, sys
from pathlib import Path
n = sys.argv[1]
S = [json.loads(l) for l in open(f"data/sft/{n}/labels.jsonl")]
R = [json.loads(l) for l in open(f"data/sft/{n}_repair/labels.jsonl")]
out = [r for r in S if not r.get("C")] + R  # repair covers every item that has a label
d = Path(f"data/sft/{n}_final"); d.mkdir(exist_ok=True)
(d / "labels.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
kept = [r for r in out if not r["dropped"]]
(d / "train.jsonl").write_text("".join(json.dumps({"messages": [{"role": "user", "content": r["prompt"]}, {"role": "assistant", "content": r["C"]}], "pool": r["pool"]}) + "\n" for r in kept))
docs = [json.loads(l) for l in open(f"data/corpus/{n}_final/docs.jsonl")]
print(f"{n}: SFT kept {len(kept)}/{len(out)} (hard {sum(1 for r in kept if r['pool']=='hard_advice')}/{sum(1 for r in out if r['pool']=='hard_advice')}); docs kept {sum(1 for r in docs if not r['dropped'])}/{len(docs)}")
EOF
