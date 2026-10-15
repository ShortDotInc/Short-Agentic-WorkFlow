<!-- graffino-agentic:team:begin v1 -->
## Team workflow (tickets, PRs, reviews)

This repo runs the team addon. These rules add to "How we work here" and win where
they are stricter. Team settings: `docs/agents/TEAM.md`.

### Tickets
- **No ticket, no code.** Every change needs a `{{PREFIX}}-<id>` ticket in {{TRACKER}}.
  Without one, stop and ask for it. This overrides any "keep working" default.
- Read the ticket, its parent and **every comment** before work; comments change
  requirements more often than descriptions do.
- Routine ticket updates are allowed without asking: comments that start with
  "AI:", the branch and PR link comment, and moving the ticket to in progress,
  blocked or in review.
- **Creating** a ticket needs the user's OK on the exact text. New tickets go to
  {{BACKLOG}}. Never close a ticket or change its scope fields.

### Git
- Branch: `feat|fix|chore/<short-name>-{{PREFIX}}-<id>` from `{{BASE_BRANCH}}`.
- Push the branch and open a **draft PR at once**, then comment both links on the
  ticket before any further work.
- Commits: `{{PREFIX}}-<id> - <type>(<scope>): <what>` with the co-author trailer.
  Never amend, squash or force-push a shared branch.
- PR description: the five sections of `.github/pull_request_template.md`.
- **Never merge or approve a PR**, and never count your own review as the human
  review. Never touch `{{BASE_BRANCH}}`, `master`/`main`, `release/*`, `hotfix/*`.

### Pipeline
`/start {{PREFIX}}-<id>` runs: product owner → **gate A** (you answer) → `/plan`
→ **gate B** (you approve the plan and the knowledge used) → test author (tests
red) → `/build` → reviewer (at most 2 rounds) → **gate C** (you review and merge).
`/start {{PREFIX}}-<id> fast` is for size S: plan → gate B → build (test first) →
reviewer (1 round) → gate C. When the intended behaviour changes, the test author
goes first again.

### Journal
Every session ends written down, finished or not, in
`docs/agents/tasks/{{PREFIX}}-<id>/`: `OVERVIEW.md` ("Resume here", status,
manifest) and `log_YYYY-MM-DD_HHMM.md`. Templates: `docs/agents/tasks/_templates/`.
"What happened on {{PREFIX}}-123?" is answered from that folder alone.
`docs/agents/STATE.md` holds one row per ticket in flight and the last 10 done;
every session that starts, pauses or finishes a ticket updates its row.
{{MANUAL_TESTS_RULE}}
<!-- graffino-agentic:team:end -->
