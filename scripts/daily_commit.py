#!/usr/bin/env python3
"""Keeps the repo active with a random 5-9 commits per UTC day."""

import json
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path(".state/commit-count.json")
LOG_FILE = Path("activity-log.md")


def run(*args):
    subprocess.run(args, check=True)


def load_state(today):
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())
        if state.get("date") == today:
            return state
    return {"date": today, "target": random.randint(5, 9), "count": 0}


def save_state(state):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def main():
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    state = load_state(today)
    print(f"Target for {today}: {state['target']}, committed so far: {state['count']}")

    if state["count"] >= state["target"]:
        print("Daily quota reached, skipping.")
        return

    with LOG_FILE.open("a") as f:
        f.write(f"- {timestamp}\n")

    state["count"] += 1
    save_state(state)

    run("git", "add", str(LOG_FILE), str(STATE_FILE))
    run(
        "git",
        "commit",
        "-m",
        f"chore: activity update ({timestamp}) [{state['count']}/{state['target']} today]",
    )
    run("git", "pull", "--rebase", "origin", "main")
    run("git", "push", "origin", "HEAD:main")


if __name__ == "__main__":
    main()
