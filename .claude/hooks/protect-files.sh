#!/usr/bin/env bash
# Hook: PreToolUse (Edit|Write) → block edits to protected files
# Reads tool input JSON from stdin, checks file_path against protection list

set -euo pipefail

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
# tool_input contains the parameters passed to Edit/Write
tool_input = data.get('tool_input', {})
print(tool_input.get('file_path', ''))
" 2>/dev/null || echo "")

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

BASENAME=$(basename "$FILE_PATH")

# Protected basenames (settings, SDK core, package definitions)
PROTECTED_BASENAMES="settings.json settings.local.json"

# Check basename match
for PROTECTED in $PROTECTED_BASENAMES; do
  if [ "$BASENAME" = "$PROTECTED" ]; then
    echo "BLOCKED: '$BASENAME' is a protected file. Manual edit required."
    exit 2
  fi
done

# Check SDK core files (only under delta_data_sdk/)
case "$FILE_PATH" in
  *delta_data_sdk/*/api.py|*delta_data_sdk/*/store.py|*delta_data_sdk/*/schema.py)
    echo "BLOCKED: SDK core file '$BASENAME' is protected. Manual edit required."
    exit 2
    ;;
  *delta_data_sdk/setup.py|*delta_data_sdk/pyproject.toml)
    echo "BLOCKED: SDK package definition '$BASENAME' is protected. Manual edit required."
    exit 2
    ;;
esac

# Check published papers
case "$FILE_PATH" in
  *papers/published/*)
    echo "BLOCKED: Published paper files are read-only. Copy to drafts/ first."
    exit 2
    ;;
esac

exit 0
