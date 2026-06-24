#!/usr/bin/env bash
# Log subagent start to .run-logs/subagent-debug.log

input=$(cat)
agent_type=$(echo "$input" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("agent_type","unknown"))' 2>/dev/null)
agent_id=$(echo "$input" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("agent_id","unknown"))' 2>/dev/null)
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

logdir="$(git -C "${PWD}" rev-parse --show-toplevel 2>/dev/null || echo "${PWD}")/.run-logs"
mkdir -p "$logdir"
echo "[$timestamp] START agent_type=$agent_type agent_id=$agent_id" >> "$logdir/subagent-debug.log"

exit 0
