#!/usr/bin/env bash
# Hook: Notification → macOS desktop notification
# Reads JSON from stdin, extracts message, shows via osascript

set -euo pipefail

INPUT=$(cat)
MESSAGE=$(echo "$INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('message', 'Task complete'))
" 2>/dev/null || echo "Task complete")

osascript -e "display notification \"$MESSAGE\" with title \"Claude Code\" sound name \"Glass\"" 2>/dev/null || true
