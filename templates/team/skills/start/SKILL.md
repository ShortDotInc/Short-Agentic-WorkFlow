---
name: start
description: Run one ticket through the team pipeline in this repo - product owner, gate A, plan, gate B, tests first, build, review, gate C - or resume it from its journal. Use when the user says "/start <TICKET-ID>", "/start <TICKET-ID> fast", "start <ticket>", or "what happened on <ticket>?".
---
<!-- graffino-agentic:team:begin v1 -->

# /start <ticket> [fast]

You are the **conductor**. You run the roles in order, carry their output to the
user and hold the gates. You do not analyse, plan or write code yourself.

## 0. Intake
1. A ticket ID is required (prefix in `docs/agents/TEAM.md`). Missing: stop and ask.
2. `git fetch --all --prune`, `git pull --ff-only`.
3. `docs/agents/tasks/<ticket>/` exists: read OVERVIEW ("Resume here") and the newest
   log, and offer to resume at that phase.
4. "What happened on <ticket>?": answer from that folder alone, then stop.
5. "fast" on a ticket that is not size S: say so and ask whether to use the full lane.

## Full lane
1. **Product owner** (`product-owner` agent) → coverage report.
   **Gate A:** relay it; ask for answers to blocking questions, missing DS- IDs and
   which proposed subtasks to create (exact text). Re-run it with the answers.
2. **Plan** (`/plan`, with the `planner` agent per independent part). Write the plan
   to `docs/agents/tasks/<ticket>/PLAN.md`.
   **Gate B:** show the plan, sizes first, with the knowledge-used table; record each
   call (confirm · wrong · outdated · answered) in PLAN.md. Nothing is built from an
   unapproved plan.
3. **Tests first** (`test-author` agent). Relay its test summary.
4. **Build** (`/build` with the `builder` agent; independent parts in worktrees) on
   the ticket branch with a draft PR, following AGENTS.md → Team workflow.
5. **Review** (`reviewer` agent). Defects → builder, against the existing tests. An
   uncovered case → test author first. **At most 2 rounds**, then bring it to the user.
6. **Gate C:** report what was built, tests (added · passing · assertions changed by
   the builder: must be 0), deviations, the verdict, files, branch and PR, manual
   tests. When the user says so: mark the PR ready (checks green), send the
   ready-for-review notice from TEAM.md, move the ticket to in review. Merging is
   the user's.

## Fast lane (size S)
Plan (with the coverage check; a blocking question → full lane) → **gate B** →
`builder` writes the failing test first, then the code → `reviewer`, 1 round (a
failure → full lane) → **gate C**.

## Always
- When the intended behaviour changes: test author first again, then build, then review.
- Every session ends written down: `log_YYYY-MM-DD_HHMM.md` and OVERVIEW updated,
  even when the pipeline stops at a gate.
- Open questions go to `docs/agents/OPEN-QUESTIONS.md`; new practices become
  candidate patterns; follow-up tickets are drafted for the user's OK.
<!-- graffino-agentic:team:end -->
