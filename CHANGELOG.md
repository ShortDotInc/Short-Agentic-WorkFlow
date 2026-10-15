# Changelog

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
