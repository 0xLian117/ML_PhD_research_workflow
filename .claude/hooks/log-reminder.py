#!/usr/bin/env python3
"""Hook: Stop → remind to update research journal.

Counts assistant responses since last session log update.
If >= 20 responses without a log update, outputs a blocking reminder.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("quality_reports/session_logs")
COUNTER_FILE = Path(".claude/hooks/.response_counter")


def get_latest_log_mtime() -> float:
    """Get modification time of most recent session log."""
    if not LOG_DIR.exists():
        return 0.0
    logs = sorted(LOG_DIR.glob("*.md"), key=os.path.getmtime, reverse=True)
    if not logs:
        return 0.0
    return os.path.getmtime(logs[0])


def read_counter() -> dict:
    """Read response counter state."""
    if COUNTER_FILE.exists():
        try:
            return json.loads(COUNTER_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"count": 0, "last_log_mtime": 0.0}


def write_counter(state: dict) -> None:
    """Write response counter state."""
    COUNTER_FILE.parent.mkdir(parents=True, exist_ok=True)
    COUNTER_FILE.write_text(json.dumps(state))


def main():
    state = read_counter()
    current_log_mtime = get_latest_log_mtime()

    # Reset counter if log was updated since last check
    if current_log_mtime > state.get("last_log_mtime", 0.0):
        state = {"count": 0, "last_log_mtime": current_log_mtime}
        write_counter(state)
        return

    # Increment counter
    state["count"] = state.get("count", 0) + 1
    write_counter(state)

    # Block if threshold reached
    if state["count"] >= 20:
        today = datetime.now().strftime("%Y-%m-%d")
        print(
            f"RESEARCH LOG REMINDER: {state['count']} responses since last log update.\n"
            f"Please update or create a session log in {LOG_DIR}/\n"
            f"Suggested filename: {LOG_DIR}/{today}_session.md\n"
            f"Include: progress, decisions, findings, next steps."
        )
        # Reset counter after reminder
        state["count"] = 0
        write_counter(state)
        # Exit 2 = block (show message to user)
        sys.exit(2)


if __name__ == "__main__":
    main()
