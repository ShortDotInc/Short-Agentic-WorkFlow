---
name: graffino-agentic-code-setup
description: Set up or update the agentic working rules in a code repository - AGENTS.md, CLAUDE.md, CONTEXT.md, a decisions/patterns/contracts/open-questions ledger and ARCHITECTURE.md, filled for existing repos by a backfill that assumes from the code and opens a temporary review UI for clashes only, /plan and /build skills, planner and builder agents, and for visual apps the design guardrails, design registry and screenshot procedure; optionally a team addon (tickets, PRs, reviews, journals) that it always asks about. Use for a new project, for an existing repo without these files, or to bring a repo up to the current version ("/graffino-agentic-code-setup", "set up agent rules", "add the agentic setup to this repo", "update the project setup", "backfill this repo", "review the backfill", "apply the backfill review").
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

Current version: **v1** (release 1.1.0; the markers carry the major version only).

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

## 2. Backfill (existing repos)

A repo with code needs its knowledge written down before the rules mean anything:
without a backfill, decisions, patterns and contracts start empty. Run it on the
first setup of an existing repo, and again when the user asks ("backfill again").
A brand-new, empty repo skips it.

**The principle: assume from the code, review only clashes.** The code is the
strongest evidence of how this repo works. An entry the code consistently follows is
recorded as `approved` with that evidence; nobody needs to confirm it. Only items
where sources disagree go to the user, in one review page.

### 2.1 Mine (parallel agents)
Spawn these as `general-purpose` agents in one message (read-only: they return
findings, they never write). Give each the repo path, the Detect results and the
brief in `templates/backfill/archaeologist.md` with its **lens**:

| Lens | Finds |
|---|---|
| `structure` | parts, entry points, data flow, external services, config, deploy → ARCHITECTURE; layering and module patterns |
| `contracts` | every interface this repo provides or consumes (see 2.3) |
| `rules` | constraints: guards, validations, invariants, "never/must" comments, CI and Makefile gates, generated files, security boundaries |
| `history` | `git log` (full), merge/PR titles (`gh pr list --state merged --limit 200` if a remote exists), fix and revert commits → lessons behind the rules; how practices changed over time |
| `docs` | existing CLAUDE.md / AGENTS.md / README / docs/ / the repo's local Claude memory, each fact checked against the code |

Visual apps run step 4 (design) as one more parallel agent.

Small repo (under ~50 source files): one agent with all lenses is enough.

### 2.2 Classify each finding
| Evidence | Becomes | Status |
|---|---|---|
| The code follows it everywhere it applies (≥ 2 consistent instances, or one enforced guard/test) | D- or PATTERN- | **approved** (assumed) |
| A written rule (docs, memory, comment) that the code follows | D- or PATTERN- | **approved** (assumed) |
| Seen once, nothing contradicts it | PATTERN- | candidate |
| Unknown, and it blocks a decision | Q- | open |
| **A clash** (below) | review item | — |

**A clash** is any of:
1. A written rule (docs, memory, comment, README) that the code does not follow.
2. Two or more ways of doing the same thing in the code, with no clear current one
   (the newest way is not clearly the intended one).
3. Two findings that contradict each other.
4. A contract whose two sides disagree (2.3).
5. A rule that looks deliberately broken somewhere (a guard skipped in one place).

For a clash in group 2, when git history shows the old way is being replaced (newer
commits all use the new way), it is **not** a clash: record the new way as
`approved` and the old as `superseded-by`, with the commits as evidence.

Every entry keeps: one rule, one reason, evidence (`path:line` or commit). The reason
comes from the code, the commit message or the docs; if none states it, write
"Why: inferred — <your reading>" so a reader knows it was not stated.

Stale facts (memory or docs naming a file, function or flag that no longer exists)
are dropped and listed in the report.

### 2.3 Contracts
A contract is a promise across a boundary: an HTTP API (routes, request/response
shapes, status codes, auth), a file or object another program reads (JSON/YAML
schemas, S3 keys, paths), a CLI or script interface (args, exit codes, output), a
queue/event/webhook payload, env vars another system sets, a database another app
reads, a URL scheme, a package or installer identity.

- **Ownership:** the side that **provides** the interface owns the entry in its
  `docs/agents/CONTRACTS.md` (C- ID). The consuming side lists it under "Consumed"
  with a link `<repo>:docs/agents/CONTRACTS.md#C-0NN` and the exact fields it relies
  on. The text lives in one place only.
- **Other repo on disk** (sibling folders, or a path in README/config): read its side.
  Shapes that disagree are a clash. A provider repo without the agentic setup yet:
  write the full contract as "Consumed (provider not set up yet)" here; the
  provider's own setup later takes ownership and this side becomes a link.
- **External services** (Fleet, Stripe, AWS, Apple…): record what this repo relies
  on under "External", with the version or docs link if known.

### 2.4 The review (only if there are clashes)
No clashes: no review; say so in the report.

Otherwise, one item per clash (`R-001`…), each with the sources side by side, 2–4
options, **your recommendation** and why, and the entries waiting on it:

1. Write the working file `docs/agents/backfill-review.json` (shape in the header of
   `templates/backfill/review-server.py`; `recommendation` is the 0-based option index).
2. Write the record `docs/agents/BACKFILL-REVIEW.md` from `templates/BACKFILL-REVIEW.md`
   (the same items, readable in git).
3. **Open the temporary review UI:** run in the background
   `python3 -I <skill dir>/templates/backfill/review-server.py docs/agents/backfill-review.json`
   (`<skill dir>` = the folder of this SKILL.md). It serves one page on 127.0.0.1
   with a random token, opens the browser, and prints `REVIEW_URL <url>`. Give the
   user that URL. Never push the URL or token anywhere.
4. The user decides each item: keys `1`–`9` pick an option, `R` takes the
   recommendation, `E` an own answer, `X` rejects the finding, `U` undoes, arrows or
   `J`/`K` move, "Accept all recommendations" decides every open item at once.
   Every click saves to the JSON file at once. "Done" stops the server
   (`REVIEW_DONE answered=n/m`); it also stops by itself after 120 idle minutes.
5. Do not wait idle in the meantime: write everything that does not depend on a
   review item. When the server stops (you are notified), run 2.5.

The user can also answer in chat or by editing `Answer:` lines in the .md file; then
run 2.5 from that.

Entries that depend on a pending review item are not written yet. Everything else is
written now.

### 2.5 Apply the review
From the answers in `backfill-review.json` (or chat / the .md file):
- Option or own answer → an `approved` entry (or a supersede of an old one). An
  answer that means "the code is wrong" → a code-fix suggestion in the report, never
  a silent code change.
- `reject` → the item moves to "Rejected" in BACKFILL-REVIEW.md with the reason.
- Move decided items to "Decided" (R-ID · answer · date · resulting entry). Items left
  open stay open; the user can run "review the backfill" later to reopen the UI.
- When no item is open, delete `backfill-review.json` (the UI is temporary); keep
  BACKFILL-REVIEW.md as the record of what was decided at backfill.

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
| `docs/agents/CONTRACTS.md` | `templates/CONTRACTS.md` | provided, consumed and external interfaces (2.3) |
| `docs/agents/ARCHITECTURE.md` | `templates/ARCHITECTURE.md` | from the `structure` lens |
| `docs/agents/BACKFILL-REVIEW.md` | `templates/BACKFILL-REVIEW.md` | only if there are clashes (2.4) |
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
2. Ledger entries added: D-, PATTERN- (approved vs candidate), C- (provided ·
   consumed · external), Q-, with one line each. Counts first; list in full only
   when under ~30 entries, otherwise the index files are the list.
3. **Review page:** the number of clashes, each in one line with your
   recommendation, and how to answer. Or "no clashes".
4. Facts moved from memory, and facts dropped as stale (with why).
5. Visual apps: token summary, number of DS- entries, hard-coded value findings.
6. Commands that failed or were not run.
7. Team addon: added or not; if added, the settings used.

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
superseded entries stay). Add files that are new in this version (for example
CONTRACTS.md and ARCHITECTURE.md in 1.1). Report what changed.

A repo set up **before the backfill existed** (no `CONTRACTS.md`): run step 2 now.
Existing entries keep their IDs; new findings continue the sequences; a new finding
that disagrees with an existing entry is a clash.

"Apply the review": run 2.5 only. "Review the backfill": reopen the UI (2.4 step 3)
for the open items, then 2.5.
