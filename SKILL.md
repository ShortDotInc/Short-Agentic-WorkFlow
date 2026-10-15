---
name: graffino-agentic-code-setup
description: Set up or update the agentic working rules in a code repository - AGENTS.md, CLAUDE.md, CONTEXT.md, a decisions/patterns/open-questions ledger, /plan and /build skills, planner and builder agents, and for visual apps the design guardrails, design registry and screenshot procedure; optionally a team addon (tickets, PRs, reviews, journals) that it always asks about. Use for a new project, for an existing repo without these files, or to bring a repo up to the current version ("/graffino-agentic-code-setup", "set up agent rules", "add the agentic setup to this repo", "update the project setup").
---

# Graffino Agentic Code Setup

You install a small, self-contained working system into ONE repository: rules the
agent always loads, a knowledge ledger with a gate, a plan-then-build flow with tests
first, and design guardrails for visual apps. The base has no tickets, no PRs and no
reviews; the optional **team addon** (step 3b) adds them. Every file, including all
docs and journals, lives in the repo itself; nothing points to a shared folder or a
separate docs repo.

Templates are in `templates/` next to this file. `{{…}}` marks a value you fill in.
Text between `<!-- graffino-agentic:begin vN -->` and `<!-- graffino-agentic:end -->` is
owned by this skill; text outside the markers belongs to the repo and is never
removed.

Current version: **v1** (release 1.0.0; the markers carry the major version only).

## 0. Preconditions

1. You are in the repo root (`git rev-parse --show-toplevel`). Not a git repo: ask
   whether to `git init`.
2. `git fetch --all --prune`, then `git pull --ff-only`. Report new commits. A
   non-fast-forward pull or uncommitted changes: stop and report.
3. Client repos (under a `Clients/` folder, or the user says so): client material
   stays in that repo. Never copy facts from other repos or from memory about other
   projects into it.

## 1. Detect

Find out, from the files (never guess):

| Fact | Where to look |
|---|---|
| Purpose | README, existing CLAUDE.md / AGENTS.md, docs/ |
| Stack | package.json, composer.json, Package.swift, *.csproj, pyproject/requirements, go.mod, Gemfile, Dockerfile |
| Commands (build, run, test, lint, type-check, release) | Makefile targets, package.json scripts, composer scripts, CI workflows |
| Layout | top-level folders, one line each |
| Tests | test folders, test runner config; run the test command once and record pass/fail |
| Release flow | Makefile/CI, CHANGELOG, tags (`git tag --sort=-v:refname \| head`), branches (develop/master) |
| Visual app? | views, templates, CSS/Tailwind, .svelte/.vue/.tsx/.blade.php/.html, SwiftUI/AppKit, Filament |
| Existing rules | CLAUDE.md, AGENTS.md, .cursorrules, CONTRIBUTING, docs/*.md |
| Repo facts in memory | the auto-memory folder of this repo (`~/.claude/projects/<path-slug>/memory/`) |

A fact you cannot find becomes an open question, not a value.

## 2. Collect existing knowledge

Turn every rule or fact that has a reason behind it into a ledger entry:

- **Decision (D-NNN):** a constraint the code must obey ("teams/*.yml are generated;
  change the generator"). Status `approved` if the code already follows it.
- **Pattern (PATTERN-NNN):** how we build a kind of thing here, with the file that
  shows it. Status `approved` if the existing code consistently follows it,
  otherwise `candidate`.
- **Open question (Q-NNN):** something unknown that blocks a decision.

Sources: existing CLAUDE.md/AGENTS.md, docs/, repo memory files, comments that state
a rule (`NEVER`, `must`, `do not`), the git log of fixes that encode a lesson.

**Check each fact against the code before you record it.** A memory fact that names
a file, function or flag that no longer exists is dropped (say so in the summary).
Keep entries short: one rule, one reason, the evidence (`path:line` or commit hash).

Existing CLAUDE.md content: move it into AGENTS.md (section 4 or the ledger) and leave
CLAUDE.md as `@AGENTS.md`. Never drop a rule; if you can't place it, keep it in
AGENTS.md section 4 verbatim.

## 3. Write the files

| File | Template | Notes |
|---|---|---|
| `AGENTS.md` | `templates/AGENTS.md` | fill sections 1–6 from Detect |
| `CLAUDE.md` | `templates/CLAUDE.md` | exactly `@AGENTS.md` (plus any `@` imports the repo already had) |
| `CONTEXT.md` | `templates/CONTEXT.md` | project vocabulary: 5–20 domain terms with one-line definitions and `_Avoid_` synonyms |
| `docs/agents/DECISIONS.md` | `templates/DECISIONS.md` | entries from step 2 |
| `docs/agents/PATTERNS.md` | `templates/PATTERNS.md` | entries from step 2 |
| `docs/agents/OPEN-QUESTIONS.md` | `templates/OPEN-QUESTIONS.md` | facts you could not find |
| `.claude/skills/plan/SKILL.md` | `templates/skills/plan/SKILL.md` | as is |
| `.claude/skills/build/SKILL.md` | `templates/skills/build/SKILL.md` | as is; remove the visual step if not visual |
| `.claude/agents/planner.md` | `templates/agents/planner.md` | as is |
| `.claude/agents/builder.md` | `templates/agents/builder.md` | as is |

**Visual apps also get:**

| File | Template | Notes |
|---|---|---|
| `docs/design/DESIGN.md` | `templates/design/DESIGN.md` | fill the token tables from the real CSS / Tailwind config / Swift constants (step 4) |
| `docs/design/registry.yaml` | `templates/design/registry.yaml` | one `DS-` entry per screen and per shared component |
| `docs/design/screens/` | — | screenshots taken in step 4 (`<DS-id>.<light\|dark>.png`) |

Existing file: merge. Replace only the marked block; keep everything outside it. A
file without markers: add the marked block at the top and keep the old content
below it, reorganized only where it duplicates the block.

Write every file in plain, short English: active voice, one rule per bullet, at most
~20 words per sentence. AGENTS.md stays under ~150 lines; detail goes in the ledger.

## 3b. Team addon (optional — always ask)

The base setup has no tickets, no PRs and no reviews. The **team addon** adds them:
ticket-first work, ticket branches and commit titles, draft PRs with a five-section
description, a product owner → plan → tests → build → reviewer pipeline with three
user gates (`/start <ticket>`), a journal per ticket, and optional manual tests and
CI checks. Everything is stored in this repo; there is no separate docs repo.

**Ask the user every time** (AskUserQuestion), before writing files: "Add the team
addon (tickets, PRs, reviews) to this repo?" Default: no. A re-run on a repo that
already has the `graffino-agentic:team` block updates it without asking again.

If yes, ask in one go for the settings in `templates/team/TEAM.md`: ticket prefix,
tracker (e.g. a ClickUp list), backlog for new tickets, ticket URL pattern, base
branch, who merges, ready-for-review notice, team rules doc (optional), manual tests
(yes/no), CI checks (yes/no). **CI checks: ask which runner** (a Graffino
self-hosted runner or a GitHub-hosted runner); never pick one.

Then write, filling `{{…}}` from the answers:

| File | Template |
|---|---|
| `AGENTS.md` | append `templates/team/AGENTS.team.md` (its own marked block) after the base block; `{{MANUAL_TESTS_RULE}}` = "Manual tests: anything only a person can prove gets an entry in `docs/agents/MANUAL-TESTS.md`; only the person who ran it reports the result." or empty |
| `docs/agents/TEAM.md` | `templates/team/TEAM.md` |
| `docs/agents/tasks/_templates/` | `OVERVIEW.md`, `log.md`, `TESTS.md` |
| `docs/agents/MANUAL-TESTS.md` | `templates/team/MANUAL-TESTS.md` (only if manual tests = yes) |
| `.github/pull_request_template.md` | `templates/team/pull_request_template.md` (merge with an existing one: keep its extra sections) |
| `.claude/agents/` | `product-owner.md`, `test-author.md`, `reviewer.md` |
| `.claude/skills/start/SKILL.md` | `templates/team/skills/start/SKILL.md` |
| `.github/scripts/team-checks.py` + `.github/workflows/team-checks.yml` | `templates/team/ci/` (only if CI = yes; runner from the answer) |

Test the CI script once locally on the current branch before the commit
(`PREFIX=<prefix> python3 .github/scripts/team-checks.py --branch <name> --base <base>`).

## 4. Visual apps: extract the design

1. Find the token source: CSS custom properties (`:root { --… }`), Tailwind config,
   a theme file, SwiftUI `Color`/`Font` extensions, Filament panel colors.
2. Record the **actual** values: colors (light and dark), font families and sizes,
   spacing scale, radii, shadows, breakpoints, motion durations. Note every
   hard-coded value outside the token source as a finding (`path:line`), don't fix it.
3. List screens and shared components with their source file; give each a DS- ID
   `DS-<repo-short>-<name>` in `registry.yaml`, `status: implemented`.
4. Write the screenshot command for this stack into AGENTS.md section 2 (for
   example a headless browser for a web UI, `screencapture -l <window id>` for a Mac
   app, a Playwright script for a Laravel/Filament panel). If none can run here, add
   Q- "how do we screenshot this app" instead of inventing one.

## 5. Verify

- Every command written into AGENTS.md section 2 was run once, or is marked
  "not run: <reason>".
- Every ledger entry has evidence.
- The `.claude/` files parse (frontmatter present, names unique).
- `git status` shows only the files this skill created or changed.

## 6. Report, then commit

Show the user, before any commit:
1. Files created / merged (path, one line each).
2. Ledger entries added: D-, PATTERN- (approved vs candidate), Q-, with one line each.
3. Facts moved from memory, and facts dropped as stale (with why).
4. Visual apps: token summary, number of DS- entries, hard-coded value findings.
5. Commands that failed or were not run.
6. Team addon: added or not; if added, the settings used.

On the user's go:
- Branch `chore/agentic-code-setup` from the default branch (develop if present).
- Commit `chore(agents): Graffino agentic code setup v1` with the session's co-author trailer.
- Merge into the default branch locally with `--no-ff`. Do not push unless the
  user says so. Do not tag or release.
- Memory facts that now live in the repo: remove them from the memory folder and
  its MEMORY.md index (they are shared now; the memory copy would drift).

## Re-run (update)

Read the version in the markers. Replace each marked block with the current
template, keep repo text, keep all ledger entries (never renumber, never delete;
superseded entries stay). Report what changed.
