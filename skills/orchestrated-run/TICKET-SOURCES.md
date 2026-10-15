# Ticket sources

This file is part of the `orchestrated-run` contract. Read it before creating,
updating, reconciling, or recovering tickets. It is not a skill and must not be
invoked. Never put it on a subagent's Reads.

`orchestrated-run` separates its run-engine state from where tickets are stored
or projected. By default, a run uses
[ticket-sources/filesystem.md](ticket-sources/filesystem.md), which stores
tickets only as Markdown files in `<run-dir>/tickets/`. Other ticket-source
definitions under `ticket-sources/` may project product and work tickets into
an external tracker while keeping high-frequency engine state local.

## Selecting and recovering the ticket source

1. If the user's invocation, the governing skill, or a project configuration
   file (`docs/agents/ticket-source.md` or `.agent-runs/ticket-source.md`)
   names a ticket source, read `ticket-sources/<source>.md` and record the
   chosen source and any config path in `WORKINGHINTS.md`.
2. Otherwise use `ticket-sources/filesystem.md` and record `Ticket source:
   filesystem` in `WORKINGHINTS.md`.
3. After compaction, read `TICKET-SOURCES.md` and the active
   `ticket-sources/<source>.md` named in `WORKINGHINTS.md` before acting on
   tickets.

## Engine-local state versus ticket-source items

Regardless of which ticket source is active, the following stay in
`<project>/.agent-runs/`:

- run files (`GOALS.md`, `NONGOALS.md`, `UNKNOWNS.md`, `WORKINGHINTS.md`,
  `LOG.md`, `PILLARS.md`, `MODULES.md`, `ROSTER.md`);
- active agent ticket files, work-unit checkpoints, and `inbox/` files;
- change plans under `plans/`;
- run-local mocks and concepts under `mocks/`;
- derived human ask pages under `asks/` and the device action ledger.

Subagents read and write only their assigned local `.agent-runs/` files under
`TICKET-CONTRACTS.md`. Subagents must never call external tracker CLIs or MCP
tools, and must never start or wait on an interactive login or credential
prompt. Only the orchestrator reads from or writes to an external ticket
source.

## Required sections in a ticket-source definition

Every file in `ticket-sources/<source>.md` must define these five sections:

### 1. Identity and config

- The source identifier (matching the filename stem, such as `filesystem` or
  `jira`).
- Where per-project tracker settings live when needed (`none` for
  `filesystem`; `docs/agents/ticket-source.md` or
  `.agent-runs/ticket-source.md` for external sources).
- Which questions must be settled with the user through `Discuss/Gather Inputs`
  (or `grill-to-done`) when a project selects the source without a complete
  configuration.

### 2. Boundary

- Which run artifacts exist only in `.agent-runs/` and which tickets or goals
  are created or projected in the ticket source.
- How external tracker IDs or URLs are linked on local run files (`GOALS.md`
  and ticket YAML `external_id` or `external_url` when applicable).

### 3. Creation and hierarchy

- When items are created in the source (for example: immediately on ticket
  creation for `filesystem`; after wholesale product proposal acceptance, at
  slice start, or at the end of a shape-only run for external trackers).
- How goals, tickets, work units, and `depends_on` edges map to the source's
  issue types, parent-child hierarchy, and blocking links.

### 4. Status and field projection

- How run ticket statuses (`proposed`, `ready`, `active`, `blocked`,
  `resolved`, `cancelled`), checkpoints, and outcomes map to the source's
  statuses, labels, or fields.
- Which writing skill governs copy written to the source (`engine text` for
  `filesystem`; `public-docs` for human-facing work trackers).

### 5. Steering and reconciliation

- What the orchestrator writes to the source on each reconciliation pass.
- Whether and how the orchestrator checks linked source items during
  reconciliation for external human edits, comments, or status changes, and how
  those are routed as user steering under `SKILL.md`.
