#!/usr/bin/env bash
# Dead-man's switch for a rented vast.ai box: stops (not destroys) this instance when the controller goes quiet.
# The controller touches /workspace/heartbeat every 30 min (ssh). No heartbeat for MAX_SILENT_H hours -> stop the instance,
# so a dead agent session or a cut connection costs storage only, not GPU hours. Stopping keeps the disk; destroy by hand.
# Uses the per-instance key vast puts in the container env (CONTAINER_API_KEY, CONTAINER_ID).
# usage (box): tmux new -d -s watchdog "MAX_SILENT_H=4 bash scripts/train/box_watchdog.sh"   -- PI/Claude (Opus 5.5)
set -uo pipefail
env_of_pid1() { tr '\0' '\n' < /proc/1/environ | sed -n "s/^$1=//p"; }
ID=$(env_of_pid1 CONTAINER_ID); KEY=$(env_of_pid1 CONTAINER_API_KEY)
[ -n "$ID" ] && [ -n "$KEY" ] || { echo "no CONTAINER_ID/CONTAINER_API_KEY"; exit 1; }
HB=/workspace/heartbeat; MAX=$(( ${MAX_SILENT_H:-4} * 3600 )); touch $HB
api_state() { curl -s -X PUT "https://console.vast.ai/api/v0/instances/$ID/" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d "{\"state\": \"$1\"}"; }
echo "$(date -Is) watchdog on instance $ID, max silence ${MAX}s; auth check (start = no-op): $(api_state running)"
while sleep 300; do
  age=$(( $(date +%s) - $(stat -c %Y $HB) ))
  if [ $age -gt $MAX ]; then
    echo "$(date -Is) no heartbeat for ${age}s: stopping instance $ID: $(api_state stopped)"
    exit 0
  fi
done
