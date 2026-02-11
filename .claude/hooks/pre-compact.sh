#!/usr/bin/env bash
# Hook: PreCompact → save state before context compression
# Appends timestamp + current context to the latest session log

set -euo pipefail

LOG_DIR="quality_reports/session_logs"
mkdir -p "$LOG_DIR"

# Find latest session log
LATEST_LOG=$(ls -t "$LOG_DIR"/*.md 2>/dev/null | head -1 || echo "")

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Find latest plan
LATEST_PLAN=$(ls -t quality_reports/plans/*.md 2>/dev/null | head -1 || echo "none")

if [ -n "$LATEST_LOG" ]; then
  cat >> "$LATEST_LOG" << EOF

---
## Context Compact @ $TIMESTAMP
- **Latest plan**: $LATEST_PLAN
- **Git HEAD**: $(git log --oneline -1 2>/dev/null || echo "no git")
- **Unstaged changes**: $(git diff --stat 2>/dev/null | tail -1 || echo "none")
EOF
else
  # Create a new log if none exists
  NEW_LOG="$LOG_DIR/$(date '+%Y-%m-%d')_session.md"
  cat > "$NEW_LOG" << EOF
# Session Log — $(date '+%Y-%m-%d')

## Context Compact @ $TIMESTAMP
- **Latest plan**: $LATEST_PLAN
- **Git HEAD**: $(git log --oneline -1 2>/dev/null || echo "no git")
- **Unstaged changes**: $(git diff --stat 2>/dev/null | tail -1 || echo "none")
EOF
fi
