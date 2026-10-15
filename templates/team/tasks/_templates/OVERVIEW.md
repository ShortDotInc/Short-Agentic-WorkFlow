---
ticket: {{PREFIX}}-XXX
type: task | bug | investigation
parent:
title: "<ticket title>"
status: not-started | in-progress | blocked | in-review | done
lane: full | fast
branch:
pr:
design_refs: []
summary: "<one line>"
created: YYYY-MM-DD HH:MM
updated: YYYY-MM-DD HH:MM     # bump on every session
---

# {{PREFIX}}-XXX — <title>

## Goal
<1–3 sentences: why this ticket exists. Link the ticket.>

## Resume here ⏯
<The very next action, what is in flight, which branch and files, any half-done
state, what to verify first. Done: "Nothing to resume — completed on <date>.">

## Summary of work so far
- YYYY-MM-DD — <what happened> ([log](log_YYYY-MM-DD_HHMM.md))

## Approach
<How it is built; links to PLAN.md and TESTS.md.>

## Cumulative file manifest 📁
| Action | Path | Purpose / what changed |
|---|---|---|

## Manual verification 🔧
<MT- IDs, steps, where, status — or "none: <reason>".>

## Decisions log 🧭
- **YYYY-MM-DD — <decision>** — Why: <reason>. Rejected: <alternative + why not>. (D-0NN if it became a standing decision)

## Open questions / blockers
- [ ] <question — or "none">

## Links
- Ticket: <URL>
- PR: <URL>
