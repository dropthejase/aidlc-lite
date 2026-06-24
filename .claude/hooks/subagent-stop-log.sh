#!/usr/bin/env bash
# Log subagent stop + excerpt key lines from its transcript to .run-logs/subagent-debug.log

input=$(cat)
agent_type=$(echo "$input" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("agent_type","unknown"))' 2>/dev/null)
agent_id=$(echo "$input" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("agent_id","unknown"))' 2>/dev/null)
transcript=$(echo "$input" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("agent_transcript_path",""))' 2>/dev/null)
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

logdir="$(git -C "${PWD}" rev-parse --show-toplevel 2>/dev/null || echo "${PWD}")/.run-logs"
mkdir -p "$logdir"
logfile="$logdir/subagent-debug.log"

echo "[$timestamp] STOP  agent_type=$agent_type agent_id=$agent_id" >> "$logfile"

# Extract tool calls and text from transcript
if [ -f "$transcript" ]; then
    echo "  transcript: $transcript" >> "$logfile"
    python3 - "$transcript" >> "$logfile" 2>/dev/null <<'PYEOF'
import json, sys

path = sys.argv[1]
with open(path) as f:
    for line in f:
        try:
            entry = json.loads(line)
            # subagent JSONL wraps the message under a "message" key
            msg = entry.get("message", entry)
            role = msg.get("role", "")
            content = msg.get("content", [])
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    name = block.get("name", "")
                    inp = block.get("input", {})
                    arg = (inp.get("command") or inp.get("file_path") or
                           inp.get("path") or inp.get("pattern") or "")
                    arg = str(arg).replace("\n", " ")[:100]
                    print(f"  [TOOL] {name}{(': ' + arg) if arg else ''}")
                elif block.get("type") == "text" and role == "assistant":
                    text = block.get("text", "").strip().replace("\n", " ")[:200]
                    if text:
                        print(f"  [TEXT] {text}")
        except Exception:
            pass
PYEOF
    echo "  ---" >> "$logfile"
else
    echo "  (no transcript found)" >> "$logfile"
fi

exit 0
