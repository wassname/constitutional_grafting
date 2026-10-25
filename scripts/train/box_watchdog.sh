#!/usr/bin/env bash
# PI/OpenAI: per-instance dead-man switch; the independent host timer enforces the absolute lease deadline.
set -uo pipefail
env_of_pid1() { tr '\0' '\n' < /proc/1/environ | sed -n "s/^$1=//p"; }
ID=$(env_of_pid1 CONTAINER_ID); KEY=$(env_of_pid1 CONTAINER_API_KEY)
[ -n "$ID" ] && [ -n "$KEY" ] || { echo "no CONTAINER_ID/CONTAINER_API_KEY"; exit 1; }
HB=/workspace/heartbeat; MAX=$(( ${MAX_SILENT_H:-4} * 3600 )); touch "$HB"
api_get() { curl -fsS --connect-timeout 10 --max-time 30 "https://console.vast.ai/api/v0/instances/$ID/" -H "Authorization: Bearer $KEY"; }
api_stop() { curl -fsS --connect-timeout 10 --max-time 30 -X PUT "https://console.vast.ai/api/v0/instances/$ID/" -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' -d '{"state":"stopped"}'; }
auth=$(api_get) || exit 1
printf '%s' "$auth" | python -c 'import json,sys; assert json.load(sys.stdin)["instances"]["id"] == int(sys.argv[1])' "$ID" || exit 1
echo "$(date -Is) watchdog on instance $ID, max silence ${MAX}s; auth check GET: 200"
while sleep 300; do
  age=$(( $(date +%s) - $(stat -c %Y "$HB") ))
  if [ "$age" -gt "$MAX" ]; then
    # PI/OpenAI: rejected/time-limited stop calls never retire the guard as a success.
    while true; do
      echo "$(date -Is) no heartbeat for ${age}s: request stop instance $ID"
      if result=$(api_stop) && printf '%s' "$result" | python -c 'import json,sys; assert json.load(sys.stdin)["success"] is True'; then
        if state=$(api_get) && printf '%s' "$state" | python -c 'import json,sys; r=json.load(sys.stdin)["instances"]; assert r["id"]==int(sys.argv[1]) and r["actual_status"] in ("stopped","exited")' "$ID"; then
          echo "$(date -Is) stopped state confirmed for $ID"
          exit 0
        fi
      fi
      echo "$(date -Is) stop unconfirmed for $ID; retrying; independent absolute guard remains armed" >&2
      sleep 15
    done
  fi
done
