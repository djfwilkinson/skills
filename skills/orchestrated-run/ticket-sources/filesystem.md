# Ticket source: filesystem

This file is the default ticket-source definition for `orchestrated-run`, under
[TICKET-SOURCES.md](../TICKET-SOURCES.md). It stores every ticket as a local
Markdown file inside the run directory.

## Identity and config

- **Source ID:** `filesystem`
- **Per-project config:** none required.
- **Setup questions:** none. Use this source automatically whenever no other
  ticket source is requested or configured.

## Boundary

- Every ticket lives at `<run-dir>/tickets/<full-id>.md` using the schema and
  ownership rules in [TICKET-CONTRACTS.md](../TICKET-CONTRACTS.md).
- No external tracker is read or written. All run files, tickets, `inbox/`
  items, `plans/`, `mocks/`, and `asks/` stay under `<run-dir>/`.

## Creation and hierarchy

- Create `<run-dir>/tickets/<full-id>.md` as soon as the orchestrator creates a
  `proposed`, `ready`, or `blocked` ticket.
- Ticket types, numeric sequence, work units (`W1`, `W2`), and `depends_on`
  links (referencing ticket IDs, unit IDs, or inbox item IDs) follow
  `TICKET-CONTRACTS.md` directly.
- When a run finishes in a shape-only stop mode, the shaped goals, unknowns,
  accepted mock contracts, and `proposed` or `ready` ticket files in
  `<run-dir>/tickets/` are the persistent backlog for a later run to resume.

## Status and field projection

- Ticket status (`proposed | ready | active | blocked | resolved | cancelled`),
  `presentation`, `owner`, and `execution_result` are stored directly in ticket
  YAML on `<run-dir>/tickets/<full-id>.md`.
- Ticket files are engine text written for agents; neither `public-docs` nor
  `user-response` applies to them, except that human-ticket asks in `Objective`
  or `Interaction log` follow `HUMAN-ASKS.md` and `user-response`.

## Steering and reconciliation

- On each checkpoint return or ticket return, reconcile directly against
  `<run-dir>/tickets/<full-id>.md`, `<run-dir>/inbox/<full-id>.md`, and the run
  files under `SKILL.md` and `RUN-STATE.md`.
- User steering arrives through chat prompts and responses to presented human
  tickets; no external tracker polling is needed.
