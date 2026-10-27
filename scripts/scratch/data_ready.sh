#!/usr/bin/env bash
# Prints valid Opus SFT rows and docs every 5 min; prints READY once both reach the run-1 minimum. -- Claude (Opus 5.5)
cd "$(dirname "$0")/../.."
MIN=${MIN:-300}
while true; do
  uv run -q scripts/data/scratch/26_frontier_batches.py parse sft >/dev/null 2>&1
  uv run -q scripts/data/scratch/26_frontier_batches.py parse docs >/dev/null 2>&1
  read s d < <(python3 -c "
import json
c=lambda k: sum(1 for l in open(f'data/frontier/{k}/items.jsonl') if (r:=json.loads(l))['meta']['valid'] and 'opus' in r['meta']['writer'])
print(c('sft'), c('docs'))")
  echo "$(date +%H:%M) sft=$s docs=$d"
  if [ "$s" -ge "$MIN" ] && [ "$d" -ge "$MIN" ]; then echo READY; exit 0; fi
  sleep 300
done
