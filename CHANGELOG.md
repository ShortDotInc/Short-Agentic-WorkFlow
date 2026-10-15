# Changelog

## 1.2.0 — 2026-10-15

- **ClickUp addon** (always asked): `.github/scripts/clickup-sync.py` (stdlib) +
  `clickup.yml`. CI comments the branch and PR links on the ticket (once), comments
  and moves the ticket to the ready status when a PR is ready (never backwards),
  and comments "released in" on every ticket of a tag. `publish-docs` publishes
  `docs/agents` (+ DESIGN.md) to a ClickUp Doc, one page per file, topic files under
  their index page; a page edited in ClickUp is skipped and reported (`--force` to
  overwrite). Dry run until `AUTOMATION_LIVE=true`.
- **Slack addon** (always asked): `.github/scripts/slack-notify.py` (stdlib) +
  `slack.yml`: "<PR> Ready for review." and a release notice with the tickets and
  the manual tests still open, through an incoming webhook. Dry run until
  `AUTOMATION_LIVE=true`.

- **Ledger lint** (`docs/agents/tools/ledger-lint.py`, copied into each repo):
  unique IDs per kind, required fields incl. evidence, valid statuses,
  `superseded-by` targets exist, indexes in sync (`--fix` rebuilds them),
  consumed-contract links resolve against provider repos on disk, `--next D`.
- **Index + topic files:** ledgers above ~150 lines split into
  `docs/agents/<kind>/<topic>.md`; the main file keeps the index, grouped by topic.
- **Confirmed dates:** a user's "confirm" in a plan sets `Confirmed:` on the entry;
  `/plan` collapses unchanged confirmed entries; any edit removes the date.
- **Guide for people:** `docs/agents/README.md`, one page.
- **Design board pull:** "pull the design" copies a Claude Design board into
  `docs/design/board/` and updates the DS- registry.
- **Team addon:** `docs/agents/STATE.md` (tickets in flight, recently done, ≤ 150
  lines; lint-checked), read by `/start`, updated every session.
- **Backfill:** docs that lag behind the code are fixed, not sent to review; only a
  doc that may state the intended behaviour is a clash.
- **Ledger entries:** `Source:` + confidence, `Owner note:`; questions get
  `investigating` and `Recorded as:`.
- **`docs/agents/REJECTED.md`:** rejected proposals and backfill findings, never
  re-proposed without new evidence; PROPOSAL shape names the supersede.
- **Rule:** cite past work as "replicate" (approved patterns only) or "for awareness
  only"; history is not a template.
- **Lint:** references to IDs that do not exist, broken relative links, sibling
  repos found in `../` and `../../*/`.
- **Team addon:** `PLAN.md` ticket template with the gate B record; one ticket folder
  at a time; `git fetch` before taking an ID (base branch wins a collision); full
  manual-test rules (queue + history, statuses, waiver person, baseline, regression
  runs, environments); `.github/manual-test-paths`; onboarding block for people;
  CI runs the ledger lint, checks manual-test paths, and reports each release's
  tickets and open manual tests on a tag.

## 1.1.0 — 2026-10-15

- **Backfill** for existing repos: parallel read-only archaeologist agents
  (structure, contracts, rules, history, docs lenses) mine the code, the full git
  history and merged PRs, the docs and the local Claude memory.
- **Assume from the code:** what the code consistently follows is recorded as
  `approved` with evidence; only clashes go to review.
- **Review UI:** a temporary local page (`templates/backfill/review-server.py` +
  `review.html`, stdlib only, token-protected, 127.0.0.1) with one clash per card,
  keyboard decisions (1–9, R, E, X, U), "Accept all recommendations", instant save,
  auto-stop. `BACKFILL-REVIEW.md` keeps the record (decided, rejected).
- **Contracts** (`C-` IDs) in `docs/agents/CONTRACTS.md`: the provider owns the
  text, consumers link to it; both sides are checked when the other repo is on disk.
- **Architecture** in `docs/agents/ARCHITECTURE.md`, generated from the code.
- `/plan`, the planner and the reviewer load and check contracts.

## 1.0.0 — 2026-10-15

First release.

- Base setup: `AGENTS.md` with the gate and hard rules, `CLAUDE.md`, `CONTEXT.md`,
  decisions / patterns / open-questions ledger, `/plan` and `/build` skills,
  planner and builder agents.
- Existing knowledge: imports `CLAUDE.md`, `AGENTS.md`, `docs/` and the repo's local
  Claude memory into the ledger after a check against the code.
- Visual apps: `docs/design/DESIGN.md` (guardrails, UI procedure, real tokens),
  `registry.yaml` with DS- IDs, screenshot procedure.
- Optional team addon, always asked: tickets, ticket branches and commit titles,
  draft PRs with a five-section template, `/start` pipeline with product owner,
  test author and reviewer agents and three gates, a journal per ticket, manual
  tests, and a self-contained CI check (`team-checks.py`; asks for the runner).
- Piloted on SysOps-Fleet-AppStore.
