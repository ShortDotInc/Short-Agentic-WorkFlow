# Graffino Agentic Code Setup (Claude Code skill)

A Claude Code skill that installs a small, self-contained agentic working system into
any code repository, new or existing. Every file it writes lives in that repository;
there is no shared rules folder and no separate docs repo.

Adapted from the FiscalLink-Docs system, simplified: no tickets, no PRs, no reviews
by default. An optional **team addon** brings them back.

## What it adds to a repo

| Part | Files |
|---|---|
| Rules the agent always loads | `AGENTS.md` (+ `CLAUDE.md` = `@AGENTS.md`), `CONTEXT.md` (project vocabulary) |
| Knowledge ledger with a gate | `docs/agents/DECISIONS.md`, `PATTERNS.md`, `OPEN-QUESTIONS.md` |
| Plan, then build (tests first) | `.claude/skills/plan`, `.claude/skills/build`, `.claude/agents/planner.md`, `builder.md` |
| Visual apps: design guardrails | `docs/design/DESIGN.md` (rules, procedure, real tokens), `registry.yaml` (DS- IDs), `screens/` |
| Optional team addon | ticket-first work, ticket branches and commit titles, draft PRs (5-section template), `/start <ticket>` pipeline (product owner → plan → test author → build → reviewer, 3 user gates), a journal per ticket, manual tests, a self-contained CI check |

The skill asks every time whether to add the team addon. For the CI check it asks
which runner to use.

### The gate
*Does this change something already approved?* Additive work (a candidate pattern,
an open question, code that follows approved entries) is done, then reported. A
change to an approved decision or pattern is a written PROPOSAL, and the agent waits.

### Existing repos
The skill reads the existing `CLAUDE.md` / `AGENTS.md`, `docs/`, and the local Claude
memory for that repo. It turns each fact into a ledger entry after it checks the fact
against the code, and drops stale facts with a reason. It never drops a rule.

## Install

```bash
git clone git@github.com:Graffino/Graffino-Agentic-Coding-Setup-Skill.git \
  ~/Work/Graffino/Internal/Graffino-Agentic-Coding-Setup-Skill
ln -s ~/Work/Graffino/Internal/Graffino-Agentic-Coding-Setup-Skill \
  ~/.claude/skills/graffino-agentic-code-setup
```

Update: `git -C ~/Work/Graffino/Internal/Graffino-Agentic-Coding-Setup-Skill pull`.

## Use

In a repo, in Claude Code:

```text
/graffino-agentic-code-setup
```

The skill detects the stack, commands and layout, writes the files, shows a report
(files, ledger entries, facts moved or dropped, design findings, failed commands), and
commits only on your go: branch `chore/agentic-code-setup`, merged into the default
branch locally. It never pushes.

Then, day to day in that repo: `/plan` → approve → `/build`. With the team addon:
`/start ABC-123` (or `/start ABC-123 fast` for a size-S ticket).

## Re-run and versions

Text between `<!-- graffino-agentic:begin vN -->` and `<!-- graffino-agentic:end -->`
(and the `graffino-agentic:team` markers) belongs to the skill. A re-run replaces those
blocks with the current templates, and keeps all repo text and all ledger entries.
The marker carries the major version; releases follow semver (`VERSION`,
`CHANGELOG.md`).

## Layout

```text
SKILL.md                  the procedure Claude follows
templates/                base files (AGENTS, CLAUDE, CONTEXT, ledger, plan/build, agents)
templates/design/         DESIGN.md + registry.yaml for visual apps
templates/team/           the optional team addon (rules, agents, /start, journal, PR template, CI)
```
