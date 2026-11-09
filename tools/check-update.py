#!/usr/bin/env python3
"""Auto update check for the Graffino agentic code setup (Claude Code SessionStart hook).

1. Pulls this skill repo (fast-forward only, clean tree only, at most once per
   THROTTLE_HOURS) so the skill on disk follows its upstream branch.
2. When the session's repo carries the setup (AGENTS.md has the graffino-agentic
   marker) and its stamp `docs/agents/.setup-version` is older than VERSION, it prints
   SessionStart context that tells Claude to run the skill's re-run before the task.

It never writes into the session's repo and never fails the session: every error
ends in a silent exit 0.

Install (~/.claude/settings.json):
  "SessionStart": [{"matcher": "startup|clear", "hooks": [{"type": "command",
    "command": "python3 ~/.claude/skills/graffino-agentic-code-setup/tools/check-update.py",
    "timeout": 20}]}]

Manual run:  echo '{"cwd": "/path/to/repo"}' | python3 tools/check-update.py
Force a pull now:  GRAFFINO_AGENTIC_FORCE_PULL=1 ... (ignores the throttle)
"""
import json
import os
import re
import subprocess
import sys
import time

SKILL = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
STAMP = os.path.join("docs", "agents", ".setup-version")
MARKER = "graffino-agentic:begin v"
THROTTLE_HOURS = 6
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "graffino-agentic")
LAST_PULL = os.path.join(CACHE, "last-pull")


def git(cwd, *args, timeout=10):
    r = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip()


def semver(text):
    m = re.match(r"\s*v?(\d+)\.(\d+)\.(\d+)", text or "")
    return tuple(int(x) for x in m.groups()) if m else None


def read_version():
    with open(os.path.join(SKILL, "VERSION"), encoding="utf-8") as f:
        return f.read().strip()


def pull_skill():
    """Fast-forward the skill repo. Returns 'old -> new' when VERSION changed, else None."""
    force = os.environ.get("GRAFFINO_AGENTIC_FORCE_PULL") == "1"
    try:
        if not force and time.time() - os.path.getmtime(LAST_PULL) < THROTTLE_HOURS * 3600:
            return None
    except OSError:
        pass
    os.makedirs(CACHE, exist_ok=True)
    with open(LAST_PULL, "w") as f:
        f.write(time.strftime("%Y-%m-%dT%H:%M:%S\n"))
    code, dirty = git(SKILL, "status", "--porcelain")
    if code or dirty:
        return None  # local work in the skill repo: never touch it
    if git(SKILL, "rev-parse", "--abbrev-ref", "@{u}")[0]:
        return None  # no upstream (feature branch): nothing to follow
    before = read_version()
    if git(SKILL, "fetch", "--quiet", "--prune", timeout=12)[0]:
        return None  # offline: try again after the throttle
    if git(SKILL, "merge", "--ff-only", "--quiet", "@{u}")[0]:
        return None  # diverged: a person decides
    after = read_version()
    return f"{before} -> {after}" if after != before else None


def changelog_since(stamp):
    """Headings of the CHANGELOG releases newer than the stamp."""
    try:
        text = open(os.path.join(SKILL, "CHANGELOG.md"), encoding="utf-8").read()
    except OSError:
        return []
    out = []
    for line in text.splitlines():
        if line.startswith("## "):
            v = semver(line[3:])
            if v and (stamp is None or v > stamp):
                out.append(line[3:].strip())
    return out


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    cwd = data.get("cwd") or os.getcwd()

    skill_update = None
    try:
        skill_update = pull_skill()
    except Exception:
        pass

    code, root = git(cwd, "rev-parse", "--show-toplevel")
    if code or not root or os.path.realpath(root) == SKILL:
        return
    try:
        agents = open(os.path.join(root, "AGENTS.md"), encoding="utf-8").read()
    except OSError:
        return
    if MARKER not in agents:
        return  # not set up: offering the setup is a separate rule

    current = read_version()
    stamp_text = None
    try:
        for line in open(os.path.join(root, STAMP), encoding="utf-8"):
            if line.startswith("release:"):
                stamp_text = line.split(":", 1)[1].strip()
    except OSError:
        pass
    stamp = semver(stamp_text)
    if stamp and stamp >= semver(current):
        return

    have = stamp_text or "an unknown release (no docs/agents/.setup-version; read the markers and files)"
    notes = changelog_since(stamp)
    lines = [
        "[graffino-agentic auto update]",
        f"This repo carries the Graffino agentic code setup at {have}. The skill on disk is at {current}"
        + (f" (just pulled: {skill_update})." if skill_update else "."),
        "Before the user's task, and after the global fetch/pull step, run the "
        "graffino-agentic-code-setup skill in re-run (update) mode for this repo. "
        "Follow its 'Re-run (update)' section for every release after the stamp.",
        "Rules: tell the user in one line that the update runs; ask only the questions the "
        "re-run needs; commit only on the user's go; never push.",
        "Do not run it when the repo has uncommitted changes or is not on its default "
        "branch: report that the repo is behind and continue with the task.",
        "If the user declines, do the task and do not offer the update again in this session.",
    ]
    if notes:
        lines.append("Releases to apply: " + "; ".join(notes) + ". Details: " + os.path.join(SKILL, "CHANGELOG.md"))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                             "additionalContext": "\n".join(lines)}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
