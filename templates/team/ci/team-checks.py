#!/usr/bin/env python3
"""Team workflow checks for a pull request (Graffino agentic team addon).

Checks the branch name, every commit title in the PR, the five PR description
sections and the "Fixes / Part of <ticket>" line. Self-contained: reads only the
GitHub event file and the local git history. Exit 1 on any failure.

Local run:  PREFIX=ABC python3 .github/scripts/team-checks.py --branch feat/x-ABC-12 \
              --base origin/develop --body-file pr.md
"""
import argparse, json, os, re, subprocess, sys

PREFIX = os.environ.get("PREFIX", "{{PREFIX}}")
TICKET = rf"{re.escape(PREFIX)}-\d+"
BRANCH_RE = re.compile(rf"^(feat|fix|chore)/[a-z0-9][a-z0-9-]*-{TICKET}$")
COMMIT_RE = re.compile(rf"^{TICKET} - (feat|fix|chore|docs|test|refactor|perf|build|ci|style)(\([^)]+\))?!?: \S")
SECTIONS = ["Summary", "What to review", "Need to know's for reviewing", "Testing done", "Observations"]
LINK_RE = re.compile(rf"^(Fixes|Part of) {TICKET}\b", re.M)


def commit_titles(base, head):
    out = subprocess.run(["git", "log", "--format=%s", "--no-merges", f"{base}..{head}"],
                         capture_output=True, text=True, check=True).stdout
    return [line for line in out.splitlines() if line]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch"); ap.add_argument("--base"); ap.add_argument("--head", default="HEAD")
    ap.add_argument("--body-file")
    a = ap.parse_args()

    branch, base, body = a.branch, a.base, None
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_path and os.path.exists(event_path):
        pr = json.load(open(event_path)).get("pull_request") or {}
        branch = branch or pr.get("head", {}).get("ref")
        base = base or ("origin/" + pr.get("base", {}).get("ref", "develop"))
        body = pr.get("body") or ""
    if a.body_file:
        body = open(a.body_file).read()

    errors = []
    if branch and not BRANCH_RE.match(branch):
        errors.append(f"branch '{branch}' must be feat|fix|chore/<short-name>-{PREFIX}-<id>")
    if base:
        for title in commit_titles(base, a.head):
            if not COMMIT_RE.match(title):
                errors.append(f"commit '{title}' must be '{PREFIX}-<id> - <type>(<scope>): <what>'")
    if body is not None:
        for s in SECTIONS:
            if not re.search(rf"^##\s+{re.escape(s)}\s*$", body, re.M):
                errors.append(f"PR description misses the section '## {s}'")
        if not LINK_RE.search(body):
            errors.append(f"PR Summary needs 'Fixes {PREFIX}-<id>' or 'Part of {PREFIX}-<id>'")

    for e in errors:
        print(f"::error::{e}" if event_path else f"✗ {e}")
    if not errors:
        print("✓ team checks passed")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
