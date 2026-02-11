#!/usr/bin/env bash
# Hook: PreToolUse (Edit|Write) → block edits to protected files
# Reads tool input JSON from stdin, checks file_path against protection list
#
# Customize: add your critical files to the PROTECTED_BASENAMES list
# or add path patterns to the case block below.

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

# ── Protected basenames (always blocked) ──
# Add your critical config files here
PROTECTED_BASENAMES="settings.json settings.local.json"

for PROTECTED in $PROTECTED_BASENAMES; do
  if [ "$BASENAME" = "$PROTECTED" ]; then
    echo "BLOCKED: '$BASENAME' is a protected file. Manual edit required."
    exit 2
  fi
done

# ── Protected path patterns ──
# Customize: add patterns for files Claude should not modify
case "$FILE_PATH" in
  # Example: protect core library files
  # *my_sdk/*/core.py|*my_sdk/*/api.py)
  #   echo "BLOCKED: Core library file '$BASENAME' is protected."
  #   exit 2
  #   ;;

  # Example: protect package definitions
  # *my_sdk/setup.py|*my_sdk/pyproject.toml)
  #   echo "BLOCKED: Package definition '$BASENAME' is protected."
  #   exit 2
  #   ;;

  # Published papers are always read-only
  *papers/published/*)
    echo "BLOCKED: Published paper files are read-only. Copy to drafts/ first."
    exit 2
    ;;
esac

exit 0
