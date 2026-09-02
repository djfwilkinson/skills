# Run-state contracts

This file is part of the `orchestrated-run` contract. Read it before creating or
updating run files and after compaction. It is not a skill and must not be
invoked.

Conversation context is temporary. Run files, tickets, and project files are
persistent memory. The orchestrator owns every run file. Subagents may identify
changes on their tickets but must not write run files.

## Unknowns

`UNKNOWNS.md` is the run-level log of unknowns. Tickets keep the discovery
record. Later tickets reference this file when their Objective is to close an
unknown.

Subagents record unknowns on their tickets with a suggested close:

- Research when a subagent can close it from project or existing evidence;
- Discuss/Gather Inputs when the user must provide a fact or decision;
- Human Task when the user must perform an external action;
- Human and Agent Task when closing it needs repeated branching interaction.

The orchestrator decides which gaps become run-level unknowns and which become
tickets. A gap is not an automatic Research ticket.

Use stable IDs:

```md
## U-001 - <name>

### Unknown
<what is not known>

### Suggested close
Research | Discuss/Gather Inputs | Human Task | Human and Agent Task

### Status
open | assigned | resolved | abandoned

### Related goals
- G-001

### Resolution tickets
- T-002-RES

### Evidence
- <result when resolved, with ticket ID>
```

Copy new unknowns during reconciliation without re-investigating them. When
creating a resolution ticket, list its ID under Resolution tickets, name the
unknown in ticket YAML, and put the exact `UNKNOWNS.md` entry on Reads. Closing
the unknown is part of Completion.

Set the unknown `assigned` while a resolution ticket is active, and `resolved`
only from evidence on a returned ticket. An unknown opened and closed in one
reconciliation pass may be written once as `resolved`. `abandoned` applies only
when the orchestrator decides it no longer matters, after Discuss when that is
a product decision.

## Goals

Update `GOALS.md` when reconciled results change the wider run. When Research
returns goals that match the user's prompt, set them `active`. Open Discuss
when a proposed goal is incomplete, conflicts, or does not match that prompt.
Keep other new goals `proposed` until the user confirms them.

```md
## G-001 - <name>

### Outcome
<what must become true>

### Acceptance criteria
- <observable condition>

### Verification
Status: defined | deferred

Required:
- <method and success condition>

Optional:
- <additional verification>

Deferred because:
<reason, when deferred>

Resolution tickets:
- T-003-AGT

### Status
proposed | active | achieved | blocked | abandoned

### Evidence
- <verification result>
```

Outcome is the intended result. Acceptance criteria are what must be true for
the goal to count as complete. Verification is how those criteria are checked.

A ticket may propose a verification method. The orchestrator decides whether
it is enough from evidence already in tickets and run files. Implementation
Completion contains only that ticket's local done-checks. Put required
goal-level, repo-wide, and cross-area methods and success conditions in
Completion of the boundary validation ticket that covers implementation. For a
goal with no implementation ticket, put them on a dedicated verification or
human-acceptance ticket.

Use `deferred` when verification is not defined. Keep the goal unachieved until
verification is defined and completed.

Verification may use automated tests; build, lint, typecheck, or another
script; a defined scenario; artifact inspection; a metric; comparison with a
baseline; an external system; agent review; Adversarial Review; human
acceptance; or `not required`.

Use `not required` only when the user or a ticket said completion itself proves
the outcome. Do not waive verification because the work looks done.

## Non-goals

Update `NONGOALS.md` when reconciled results change scope. Non-goals are not
required. Accept simple guards. Keep a non-goal `proposed` and open Discuss only
when implementation is likely to struggle without that steering and the user
needs to decide it.

```md
## NG-001 - <name>

### Boundary
<what is outside this run>

### Scope check
<what would indicate that work is crossing this boundary>
```

## Working hints

`WORKINGHINTS.md` contains project and user guidance that should affect
multiple tickets. It starts empty. Update it from reconciled ticket results and
user answers. New hints that need a product decision stay `proposed` until the
user confirms them.

Use the same model as the orchestrator for subagents by default. Record a user
override in `WORKINGHINTS.md`.

If a working hint conflicts with a goal, the subagent records the conflict on
its ticket. The orchestrator decides whether it needs Discuss or a process
change.

Put `WORKINGHINTS.md` on Reads when it has entries that apply. Do not paste it
as the ticket's main context. Name exact hint, goal, and unknown IDs or headings
when only those entries apply. Do not add growing run files by default.

## Pillars

`PILLARS.md` lists substantial areas of the run. Each pillar has stable ID,
name, purpose, related goals, and status. Put cross-cutting guidance in
`WORKINGHINTS.md`, not a pillar.

## Modules

`MODULES.md` groups related run work. Each module has stable ID, name, purpose,
related goals and pillars, known dependencies, and status:

`proposed | active | complete | blocked | retired`

Modules may be added, split, merged, or retired when reconciliation says the
run needs that. Set a module `complete` only when every completed
implementation ticket in it has implementation coverage and required module
review is resolved.

## Log

`LOG.md` records concise run history. For each reconciled ticket, record:

- what was attempted;
- execution result;
- persistent ticket status;
- important decisions;
- evidence pointers;
- unknown IDs opened or closed;
- blockers;
- ticket ID.

Detailed investigation and implementation notes stay on tickets.
