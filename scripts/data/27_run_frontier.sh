#!/usr/bin/env bash
# Run frontier batches one at a time with plain pi (no extensions except the two auth ones, no skills, prompt templates or AGENTS.md),
# paced per provider account by 26_frontier_batches.py next. One lane per account; run lanes in parallel.
# usage: scripts/data/27_run_frontier.sh <sft|docs> <account: openai-codex|openai-codex-2|anthropic> <max batches>  -- Claude (Opus 5.5)
set -euo pipefail
cd "$(dirname "$0")/../.."
kind=$1; acct=$2; max=$3; py="uv run -q scripts/data/26_frontier_batches.py"
# only the two auth extensions: Anthropic subscription and the second OpenAI account (openai-codex-2)
AUTH=(-e "$HOME/.pi/agent/git/github.com/gotgenes/pi-anthropic-auth/src/index.ts" -e "$HOME/.pi/agent/npm/node_modules/pi-codex-multi/extensions/multi-sub.ts")
for ((n=0; n<max; n++)); do
  nxt=$($py next "$kind" "$acct")
  case "$nxt" in DONE*|WAIT*) echo "$nxt"; break;; esac
  batch=$(jq -r .batch <<<"$nxt"); writer=$(jq -r .writer <<<"$nxt"); file=$(jq -r .file <<<"$nxt"); wait_s=$(jq -r .wait_s <<<"$nxt")
  echo "$(date -Is) batch $batch writer $writer wait ${wait_s}s"; sleep "$wait_s"
  $py mark "$kind" "$batch" running
  log="data/frontier/$kind/pi_${batch}.log"
  if pi -ne -nc -ns -np --no-session "${AUTH[@]}" --system-prompt "You are a careful, skilled writer. Do the writing task in the file you are given." -t read,write --model "$writer" -p "Read $file and do exactly what it says. Write only the output file it names." </dev/null >"$log" 2>&1 \
     && [ -s "data/frontier/$kind/out_$(printf %03d "$batch").md" ]; then
    $py mark "$kind" "$batch" done
  else
    if grep -q "Usage Policy\|violate Anthropic\|refused to complete" "$log"; then
      echo "batch $batch refused by the provider's usage policy; splitting (content unchanged)"; mv "$log" "${log%.log}_blocked.log"
      $py split "$kind" "$batch"; continue
    fi
    $py mark "$kind" "$batch" failed; echo "batch $batch failed, see $log"; tail -5 "$log"; break
  fi
done
