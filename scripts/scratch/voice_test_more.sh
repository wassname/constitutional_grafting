#!/usr/bin/env bash
# Voice test conditions h (gpt-6.1-sol) and i (inkling): brief_c with the output path changed, plain pi, one at a time. -- Claude (Opus 5.5)
set -u
cd "$(dirname "$0")/../.."
AUTH=(-e ~/.pi/agent/git/github.com/gotgenes/pi-anthropic-auth/src/index.ts -e ~/.pi/agent/npm/node_modules/pi-codex-multi/extensions/multi-sub.ts)
D=data/frontier/voice_test
run() {  # cond model
  echo "$(date -Is) $1 $2"
  pi -ne -nc -ns -np --no-session "${AUTH[@]}" --system-prompt "You are a careful, skilled writer. Do the writing task in the file you are given." \
    -t read,write --model "$2" -p "Read $D/brief_$1.md and do exactly what it says. Write only the output file it names." </dev/null >"$D/pi_$1.log" 2>&1
  echo "$(date -Is) $1 exit $? $(ls -la $D/out_$1.md 2>&1)"
}
run h openai-codex-2/gpt-6.1-sol:medium
sleep 30
run i openrouter/thinkingmachines/inkling
