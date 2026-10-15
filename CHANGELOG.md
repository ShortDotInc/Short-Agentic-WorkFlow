# Changelog

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
