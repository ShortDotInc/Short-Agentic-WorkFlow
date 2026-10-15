<!-- graffino-agentic:team:begin v1 -->
## Team workflow (for people)

**First day:** connect the tracker to Claude Code (TEAM.md → "Tracker access for
agents"), then check it with "get ticket {{PREFIX}}-1". Read AGENTS.md → Team workflow
and `STATE.md`.

| You want to | Do |
|---|---|
| Run a ticket | `/start {{PREFIX}}-123` (full lane) or `/start {{PREFIX}}-123 fast` (size S) |
| Your 3 decisions | **Gate A** answer the questions · **Gate B** approve the plan and its knowledge · **Gate C** review and merge |
| Resume a ticket | `/start {{PREFIX}}-123` again; it resumes from `tasks/{{PREFIX}}-123/OVERVIEW.md` |
| Know what happened | "What happened on {{PREFIX}}-123?" |
| See what is in flight | `STATE.md` |
| See what needs a manual test | `MANUAL-TESTS.md` → Queue |

**Traceability:** ticket `{{PREFIX}}-123` → branch `feat/<short-name>-{{PREFIX}}-123`
(links commented on the ticket) → commits `{{PREFIX}}-123 - <type>(<scope>): …` → PR
"Fixes {{PREFIX}}-123" → journal `docs/agents/tasks/{{PREFIX}}-123/`.

Agents never merge, approve, close tickets, or mark a manual test passed.
<!-- graffino-agentic:team:end -->
