# Ticket contracts

This file is part of the `orchestrated-run` contract. The orchestrator must read
the relevant sections before creating, assigning, presenting, executing, or
recovering a ticket. It is not a skill and must not be invoked.

Subagents do not receive `SKILL.md`. Agent-ticket assignment prompts copy the
persona brief from `PERSONAS.md`, then the shared agent rules and exact type
prompt from this file.

## Ticket identity and types

Store tickets in `tickets/` as Markdown with ticket YAML.

| Type | Suffix | Example |
| --- | --- | --- |
| Research | `RES` | `T-001-RES` |
| Agent Task | `AGT` | `T-002-AGT` |
| Explore Options | `EXP` | `T-003-EXP` |
| Plan | `PLN` | `T-004-PLN` |
| Plan Review | `PLR` | `T-005-PLR` |
| Adversarial Review | `ADV` | `T-006-ADV` |
| Discuss/Gather Inputs | `DIS` | `T-007-DIS` |
| Human Task | `HUM` | `T-008-HUM` |
| Human and Agent Task | `HAT` | `T-009-HAT` |

Use one number sequence across every type. Increment the number for each new
ticket regardless of suffix. The full ID is the stable ID. The numeric prefix,
such as `T-001`, is valid shorthand within the run.

Name the file `<full-id>.md`, and use the full ID in ticket YAML and the H1. The
suffix records the type at creation. Do not change the type after assigning the
ID; cancel or replace the ticket with the next number when a different type is
needed.

Do not rename existing tickets when resuming an older run. Preserve their IDs
and continue the global number sequence.

## Ticket ownership and schema

`status`, `owner`, `persona`, `presentation`, `plans`, and `reviews` are
orchestrator-owned, and so are Objective, Reads, Completion, and Work units.
`execution_result` is worker-owned and unset until execution ends.

While a ticket is active, the worker may update only:

- `execution_result`;
- `Unknowns`;
- `Findings`;
- `Work performed`;
- `Evidence`;
- `Checkpoints`;
- `Inbox responses`;
- `Interaction log`;
- `Blockers / follow-ups`.

A Plan worker may also write its Completion-named change plan; no other type
writes under the run directory. Agent Task and Explore Options may write
project files under their Objective.

The worker must not modify other ticket metadata. When the orchestrator is the
worker for a Human and Agent Task, it still updates orchestrator-owned fields
separately under that type's lifecycle.

The orchestrator never edits an active agent ticket, including while its
session is parked. Everything it sends to an active ticket goes through that
ticket's inbox.

Use this template. Keep the headings so ownership remains visible. A worker may
leave a worker-maintained section empty when it has nothing to record; do not
fill sections with padding.

```md
---
id: T-001-RES
title: Understand the user prompt
type: Research
persona: scout
status: ready
execution_result: null
presentation: null
goals: []
unknowns: []
pillars: []
modules: []
plans: []
reviews: []
depends_on: []
owner: null
---

# T-001-RES - Understand the user prompt

## Objective
<the bounded result this ticket should produce>

## Reads
- <run file and exact ID or heading, ticket, project path, or documentation>

## Completion
<what must be true for the worker to report completed>

## Work units
<orchestrator-owned: agent tickets only; fixed while the ticket is active>

## Interactive reason
<orchestrator-owned: required only for Human and Agent Task>

## Exclusive scope
<orchestrator-owned: required only for Human and Agent Task; project paths,
external state, prepared human environment, and decisions it may affect>

## Presentation
<orchestrator-owned: human-ticket ask source, ask-page path, prepared
environment, presentation and withdrawal times, current client link check, and
inspection freeze when applicable>

## Unknowns
<worker-maintained; leave empty when none>

## Findings
<worker-maintained; leave empty when none>

## Work performed
<worker-maintained; leave empty when none>

## Evidence
<worker-maintained; leave empty when none>

## Checkpoints
<worker-maintained: one entry per finished unit or separately placed fix>

## Inbox responses
<worker-maintained: one entry per inbox item read>

## Interaction log
<worker-maintained: Human and Agent Task only unless otherwise needed>

## Blockers / follow-ups
<worker-maintained: proposals for the orchestrator; leave empty when none>
```

`persona` names the persona from `PERSONAS.md` that executes an agent ticket;
it is `null` on human tickets. `plans` holds the Plan ticket IDs for change
plans that govern the ticket. `reviews` is used only on a Plan ticket and holds
the current round's Plan Review ticket IDs.

Ticket statuses:

`proposed | ready | active | blocked | resolved | cancelled`

Human-ticket presentation:

`null | upcoming | presented | withdrawn | answered`

Use `null` for agent tickets. Use the other values only under Human involvement
and the Human and Agent Task contract.

Execution results:

`completed | blocked | failed`

A ticket is `ready` when the orchestrator decides its dependencies and required
inputs are available. `depends_on` may name tickets, units, or inbox items; a
unit or inbox-item dependency is met when the checkpoint carrying it is
reconciled `done`. `execution_result: completed` does not imply
`status: resolved`. Reconcile first.

## Work units

Every agent ticket holds one or more work units: ordered pieces of its
Objective, each with its own Objective and Completion, sized like one coherent
change or one research question. A unit usually serves one run module or a
coherent part of one. Plan and Plan Review tickets have exactly one unit.
Human tickets have none.

Unit IDs are scoped to the ticket: `W1`, `W2`, written in full as
`T-004-AGT/W1`. They are never reused on that ticket.

```md
### W1 - <title>
Modules: M-002
Goals: <goal IDs, or none>
Unknowns: <unknown IDs, or none>
Plans: <Plan ticket IDs governing this unit, or none>
Covers: <for inspection, validation, and review units: the unit or ticket IDs
it judges>
Objective: <the bounded result of this unit>
Completion: <what must be true for this unit's checkpoint to be done>
Reads: <paths this unit needs beyond the ticket's Reads, or none>
```

A unit's `Goals`, `Unknowns`, and `Plans` lines count as if they were in the
ticket YAML, so a unit added through the inbox carries its own links.

A unit is finished when it has a `done` checkpoint or a `dropped unit` item
removed it. A `blocked` checkpoint does not finish it: the worker returns to
it when a decision or added Reads arrive and checkpoints it again.

A worker ends each unit, and each fix it places on its own, with a checkpoint
in `## Checkpoints`, then returns so the orchestrator can reconcile it and
resume the session:

```md
### W1 - <title>
Outcome: done | blocked | failed
Snapshot: <tree hash> | none (<reason>)
Changed paths:
- <path>
Checks: <this unit's Completion checks and results>
Includes: <inbox item IDs this checkpoint carries, or none>
For review: <what an inspector or reviewer needs, or none>
Next: <next unit or fix, or none>
```

Label a separately placed fix's checkpoint `Fix I-002` instead of a unit ID.

## Ticket inbox

Each active agent ticket has an inbox at `inbox/<full-id>.md` under the run.
The orchestrator creates it at assignment and appends to it; it never edits or
deletes an item it has sent. To change one, it sends a new item that names the
one it supersedes. The worker reads it and never writes it.

```md
## I-001 - <short title>
Kind: added unit | dropped unit | fix request | decision | hold | stop | closing
Sent: <ISO time>
Urgency: blocking | normal
Source: <finding ID, Discuss ticket, or user steering>
Applies to: <unit IDs on this or an earlier ticket, and paths>
Supersedes: <item ID, or none>
Body: <for an added unit, its full Work units entry; otherwise what to change,
what was decided, or what to leave alone>
```

Item IDs are scoped to the inbox, written in full as `T-004-AGT/I-001`.
`Urgency` applies to fix requests only. `blocking` means the current or later
units build on what the fix changes; the worker must place it `now`.

A streaming ticket is one whose Objective says further units will arrive
through its inbox, such as an inspection or review that follows other
tickets' checkpoints. Its session parks with an empty queue rather than
completing. `closing` tells it no further units will arrive: finish the queue,
then complete.

The worker records each item it has read in `## Inbox responses`, with what it
did and, for a fix request, its placement and reason:

- `now`: stop the current step at a safe point, apply the fix, then continue;
- `with-current`: carry it in the current unit's checkpoint;
- `after-current`: apply it straight after the current unit's checkpoint,
  before the next unit, with its own checkpoint.

When the worker is between units, `now` and `after-current` both mean before
the next unit.

## Readiness

Keep each unit bounded enough for one checkpoint, and group units into tickets
under Grouping in `SKILL.md`. If a unit proves too broad, the worker may
complete a severable part that stays within its Objective, records what
remains, and checkpoints it `blocked` unless its Completion is met. The
orchestrator decides how to split, replace, or reassign the rest. A reassigned
Objective names what earlier checkpoints already cover so the next worker does
not repeat it.

An agent ticket is not `ready` until it names a persona and every unit is
ready by its type's rules. Its ticket-level Objective and Completion state what
the units add up to and that every unit must be finished. A unit added through
the inbox meets the same readiness, dependency, conflict, Exclusive scope, and
planning-depth gates as a unit on a new ticket before it is sent.

An Agent Task unit is not ready until its Objective, Completion, and the Reads
that apply to it name what to change and what done looks like. Vague Research
follow-ups stay Research or unknowns. Agent Task Reads are files Research
already found or an accepted change plan, not the repo.

A Human Task is not `ready` until Objective is a complete ask the user can
perform without inventing the procedure, and Completion names the observable
result or evidence to return. Do not block readiness only because no hint or
recovery step applies.

A human ticket that needs a prepared file, artifact, page, preview, service, or
other environment is not `ready` until a completed preparation Agent Task has:

- Objective and Completion, written before dispatch, requiring the resource to
  remain available after return; and
- Evidence recording the path or URL, persistent process or session when
  relevant, expected state, and known expiry or restart procedure.

An implementation or boundary validation ticket may also be the preparation
ticket only when its Objective and Completion already contain those
requirements. Otherwise create a separate preparation ticket.

A Human and Agent Task is not `ready` until Objective, Completion, and Reads
bound the work; Interactive reason explains why repeated branching interaction
is materially better than the existing ticket types; Exclusive scope names the
directories or modules in which it may branch, external state, prepared human
environment, and decisions it may affect;
and preparation dependencies are complete. Completion is the overall end
condition, not the expected result of one interaction.

Explore Options is the type for deciding what to build when that reasoning
needs investigation. That reasoning does not land on an Agent Task. Local
implementation choices that follow established project patterns are process
decisions and do not require Explore Options. A Plan ticket commits an approach
and sequences the work; an open decision in a change plan that needs
investigation becomes an Explore Options ticket, and no Plan Review starts
until it returns and the plan is revised.

Do not create a Plan or Plan Review, even as `proposed` or `blocked`, unless
`WORKINGHINTS.md` records confirmed planning depth as `reviewed planning`.

A Plan is not `ready` unless that confirmed value is `reviewed planning`. It
also requires an Objective naming its change set and goal outcome; Reads naming
the proposing tickets and drafts, governing run state, end user and canonical
docs when known, and discovered project paths; and Completion requiring every
Plan-prompt section at the change plan path. Objective and Completion permit
only the worker-maintained ticket sections and change plan write, prohibiting
project, external-state, and prepared-environment changes.

A Plan Review is not `ready` unless that confirmed value is `reviewed
planning`. It also requires the Plan to have returned `completed` with no
approach-blocking investigation, its file to exist, its persona to match the
lens, Objective to name the lens,
and Reads to name the plan, governing goals and acceptance criteria, non-goals
and working hints. Product-lens Reads also name the end user and cited
canonical sections or their recorded gaps.

A boundary validation ticket is its own Agent Task for the `validator`. It
checks goal-level, repo-wide, or cross-area requirements for the
implementation tickets it names, on a stable tree. Do not fold wider
validation into those implementation tickets.

An agent boundary inspection is its own Agent Task for the `inspector`,
separate from boundary validation. It has one unit per covered implementation
unit or separately placed fix, and its `Covers` line names that ID. It is a
streaming ticket that follows the implementation tickets its units cover.
A unit is ready once the checkpoint it covers is reconciled `done` with a
snapshot or a recorded reason for none; the ticket is `ready` once its first
unit is. Send `closing` once every implementation ticket it follows has ended
and every covered ID's current verdict is `accepted`. Each
unit's Objective names the parts of the covered result it judges. Completion
requires a verdict for each covered ID. Objective and Completion prohibit
changes to project files, external state, and prepared human environments.
Reads name the covered tickets, the goals and acceptance criteria they serve,
applicable working hints and confirmed decisions, and any governing change
plan; each unit's Reads add the checkpoint it covers. Further units arrive
through the inbox as checkpoints are reconciled.

## Shared agent rules

Copy this block into every agent-ticket assignment prompt, after the persona
brief and followed by the exact type prompt. Give the absolute paths of the
ticket, its inbox, and this skill's `scripts/snapshot.py` with it.

```text
You are executing one ticket as an ordered series of work units. You own that
ticket file while it is active.

Read the ticket file, your inbox, and every entry in the ticket's Reads list,
at the exact ID or heading when one is named. Then work through Work units in
order, together with units your inbox adds, doing only the bounded work each
unit and the ticket Objective allow. If Checkpoints already has entries, take
the first unit or placed fix that is not finished and not waiting on a
decision; do not repeat work with a done checkpoint.

Update the ticket as you go. You may change only execution_result, Unknowns,
Findings, Work performed, Evidence, Checkpoints, Inbox responses, Interaction
log, and Blockers / follow-ups. Do not change other ticket metadata or Work
units. Keep the record proportional to the result: leave worker-maintained
sections empty when they have nothing to record, and use a concise Evidence
pointer when the changed files or checks are the evidence. Do not leave the
detailed record only in chat.

Checkpoints. Before your first change to project files, run the snapshot
script and record its output as Base in Work performed. When a unit ends,
record its checkpoint under Checkpoints using the format in Work units: its
outcome (done, blocked, or failed), a snapshot taken after its last change or
the reason there is none, changed paths, its Completion checks and results,
the inbox items it carries, what a reviewer needs, and what you will do next.
If the project is not a git worktree, record `none (not a git worktree)`.
Then return. You will be resumed to continue.

If a unit blocks, checkpoint it blocked and continue with the next unit only
when that unit does not depend on it. Return to the blocked unit when its
decision or missing input arrives, and checkpoint it again.

Inbox. The orchestrator writes your inbox; never edit it. Read it when you
start or resume, before each unit, and before each new step within a unit,
such as starting another file or running checks. Record every new item in
Inbox responses with what you did. Place each fix request now, with-current,
or after-current, and give the reason: now when it is blocking or the work in
progress builds on what the fix changes; with-current when it touches the same
paths or is small enough for this checkpoint to carry; after-current when
separating it keeps both reviewable. List a fix under Includes in the
checkpoint that carries it. An added unit joins your queue where it says, or
at the end. A decision settles the choice it names. A hold names paths or
choices to leave alone until a later item lifts it. A dropped unit leaves your
queue. A stop means finish at a safe point, record where you are, set
execution_result to blocked, and return. Closing means no further units will
arrive.

Set execution_result to null when you start. Leave it null at a checkpoint
when units or placed fixes remain, or when your Objective says further units
will arrive through the inbox and no closing item has. Before you set a
result, read the inbox one last time and handle anything new. When every unit
and placed fix is finished, or only blocked ones remain, and nothing more can
arrive, set it to completed, or blocked when blocked units remain, or failed,
and return. That is your result, not the
persistent ticket status. The orchestrator owns status, owner, and Work units.

Your return message is one line: the ticket ID, what you just checkpointed,
its outcome, and whether work remains. Everything else belongs on the ticket.

Do not edit run-level files (GOALS.md, NONGOALS.md, UNKNOWNS.md,
WORKINGHINTS.md, LOG.md, PILLARS.md, MODULES.md, ROSTER.md, inbox/, or asks/).
Do not create tickets. Do not plan the run. Record follow-ups on this ticket.
The orchestrator decides what happens next. A Plan ticket also writes the
change plan named in its Completion; no other type writes a file under the run
directory.

Classify proposed or recommended implementation work as `trivial`, `following
an established project pattern`, or `moderately complex or higher`. The last
means it needs decisions beyond an existing pattern, changes several files or
areas together, or is hard to reverse. Name any schema, persistence layer,
public API, protocol, data migration, or canonical doc it changes. Record the
exact label and surfaces with the work in Blockers / follow-ups, or with its
draft under Proposed implementation tickets on a Plan.

Apply this product-decision test: reasonable alternatives produce meaningfully
different product, architectural, operational, compatibility, or scope
outcomes; a local implementation choice following an established pattern is
process. Examples include goals, architecture, public API, persistence, UX,
dependencies, platforms, and scope trade-offs. Unless the type prompt says to
classify and continue, stop before committing a product decision. Complete only
severable work that stays correct under every option. Record the smallest
decision, options, recommendation, completed work, and withheld boundary in
Blockers / follow-ups and checkpoint that unit blocked.

If a unit needs a higher classification than your persona brief covers,
record the label and why, and checkpoint it blocked.
```

When resuming a parked or idle session, send only what changed: for a parked
session, `Continue <ticket ID>. Read your inbox first.`; for an idle session
taking a new ticket, the new ticket, inbox, and snapshot script paths and its
Reads. A resumed session already has its brief and rules.

## Research (subagent)

Close knowledge gaps, one per unit, at the `triage`, `surface`, or `deep`
depth each unit's Objective and Completion choose. Prefer `surface` to
standalone triage. Research drafts and classifies follow-up Agent Tasks at
either planning depth. The unit depths decide the persona under `PERSONAS.md`,
so one ticket's units share a depth class.

Assignment prompt, after the shared agent rules:

```text
This ticket is Research. For each unit, use only the depth path its Objective
and Completion allow. Depth is effort on context and hunting.

triage: decide whether investigation is needed. Do not hunt the answer. Return
one next step (no-investigation-required | surface | deep) and a one-line basis.

surface: pull obvious context. Record the answer if it is there. Continue to
deep only when the unit pre-authorizes that escalation; record why you
escalated. If deep is not authorized and surface cannot meet the unit's
Completion, record what you found, request deep on that gap, record new
unknowns, and checkpoint the unit blocked.

deep: get full context and hunt. Close in-scope gaps this unit permits.
Record the answer, remaining unknowns, or a partial answer with evidence.

Record on the ticket, per unit: depth used; findings; evidence; remaining
uncertainty; implications; and follow-ups. Keep the record proportional to the
result.

For every Agent Task follow-up, draft Objective, Completion, and Reads from
what you found, or name which part is missing and which ticket type could close
it. When several drafts must ship together, name them as one change set and say
why. Say which drafts share Reads or run modules and the order they depend on,
so they can be grouped as units of one ticket. These drafts are proposals. Do not create tickets. Propose Human and Agent
Task only when its bounded work and need for repeated branching interaction
are already clear.

Do not implement production changes unless Objective says to.
```

## Agent Task (subagent)

Perform bounded implementation or production work. When Objective is to produce
a UX/UI review, use the `ux-reviewer` persona and put the `ux-ui-reviewer`
skill file on Reads.

Assignment prompt, after the shared agent rules:

```text
This ticket is an Agent Task. Perform the bounded production work in each
unit's Objective. Do not research what to build. Implement from the unit's
Objective, Completion, and Reads. If that is not enough, checkpoint the unit
blocked and record the gap.

Meet each unit's Completion. Check that, and nothing wider. Wider tests, lint,
typecheck, or cross-area review are not this ticket's job unless a unit's
Objective and Completion expressly make them so. An inspector reviews each
checkpoint while you continue, and its findings reach you as fix requests.

Record on the ticket, per unit:
- work performed
- changed files or artifacts
- checks against the unit's Completion
- blockers
- possible follow-up work
```

For an agent boundary inspection, add this after the Agent Task prompt:

```text
This ticket is an agent boundary inspection. It gives the acceptance judgement
for results the user is not asked to review: code, tests, configuration, and
docs outside the product.

For each unit, judge whether the parts of the covered result named in its
Objective deliver what the governing goals and acceptance criteria, the user
request, confirmed decisions, and any accepted change plan require, and
nothing outside them. When a unit names fixes for a covered ID, judge the
current result they form together. Treat recorded check outcomes as evidence;
do not repeat boundary validation.

Judge the checkpoint as recorded, not the live files, which may already hold
later work. Read its change with `git diff <previous> <snapshot> -- <changed
paths>`, where previous is the implementer's prior checkpoint snapshot or its
Base, and read a file as it was with `git show <snapshot>:<path>`. When the
checkpoint has no snapshot, read the live files and record that later work may
have changed them.

Do not change project files, external state, or prepared human environments. Do
not fix findings. Classify each choice you find by the product-decision test and
continue instead of stopping.

Record one verdict for each covered ID in that unit's checkpoint, with its
evidence:
- accepted: the result meets that basis and no finding for it remains open;
- changes needed: name each required change, with a finding ID such as
  `T-006-AGT/F-001`, its location, and whether later work that builds on it
  makes it blocking;
- decision needed: name the choice for the user, its options, and a
  recommendation.
Checkpoint each unit when its verdicts are recorded. Set execution_result to
completed when every unit has a verdict.
```

For boundary validation, add this after the Agent Task prompt:

```text
This ticket is boundary validation. Run the checks named in each unit's
Completion and record each command, its result, and an output pointer. Do not
fix failures. For each failure, say whether the covered work caused it, it was
already present, or it comes from paths outside the covered changes.

Run checks on a stable tree. If a unit's Objective names a snapshot and a
temporary worktree, make a commit from the snapshot tree with
`git commit-tree <snapshot> -m snapshot`, add a detached worktree at that
commit with `git worktree add --detach <dir> <commit>`, do any setup the unit
names, run the checks there, and remove it with `git worktree remove --force
<dir>` before you return. Otherwise run them in the project and record any sign
that files changed while they ran. Record the snapshot or tree you checked in
Evidence.
```

## Explore Options (subagent)

Investigate alternatives without committing them to the production solution.

Assignment prompt, after the shared agent rules:

```text
This ticket is Explore Options. Investigate alternatives. Do not commit them to
the production solution.

You may use prototypes, temporary code, temporary tests, instrumentation,
reproductions, or debugging experiments. Label temporary artifacts temporary.

Record on the ticket, per unit:
- options explored
- evidence from each
- trade-offs
- a recommendation where supported
- temporary artifacts created
```

## Plan (subagent)

Under reviewed planning, write one agent-facing change plan for one change set at
`plans/<plan-ticket-id>.md`. Its path is stable. The active Plan worker owns its
content; otherwise only the orchestrator may change its Status and revisions
banner. A Plan ticket has one unit. The `architect` or `frontend-planner`
session takes the next Plan ticket for that persona while critics review the
last one.

Assignment prompt, after the shared agent rules:

```text
This ticket is Plan. Produce the change plan named in Objective, at the plan
path in Completion. Apart from the worker-maintained sections of this ticket,
that file is the only file you may write, and this instruction is what
authorises you to write it. Do not change project files, external state, or any
prepared human environment. Do not implement any part of the plan. Do not
create tickets.

Write the change plan for the subagent that will implement it and for the
reviewers who will attack it. Keep it mechanical. It has no user-facing copy.

Plan from Objective, Completion, and Reads, including draft implementation
tickets earlier work recorded. Investigate only as far as the plan requires. If
closing a gap needs its own investigation, record that need rather than
guessing.

Write it with these sections:
- Goals and requirements served, by run goal ID, with canonical doc or spec
  sections when available and the recorded gap otherwise
- Approach and the local choices it commits, each marked local, with rejected
  alternatives and why
- Changes by area, in execution order, with paths, each stating the observable
  effect of that change
- Knock-on effects: callers, dependents, tests, docs, config, data, migrations
- Risks and compatibility
- Verification proposals for goal-level and cross-area checks
- Proposed implementation tickets, each with draft Objective, Completion, Reads
- Open decisions, with options, a recommendation, and what is stable under each
- Status and revisions

Classify every choice by the shared product-decision test, but continue instead
of stopping. Put product decisions under Open decisions, keep planning what
stays correct under every option, and put process choices under Approach marked
local. Set execution_result to completed when the rest is usable, or blocked
when the plan depends on an undecided choice or open investigation.

When this ticket is a revision, read the Plan Review tickets and the decisions
named in Objective. Apply every finding the orchestrator accepted, and add a
Status and revisions entry naming what changed and which findings it answers.
Do not drop an accepted finding without recording why it does not apply.

Return on the ticket: the plan path, every Approach commitment so the
orchestrator can check your classification, open decisions, evidence, and
follow-ups. The plan file is the deliverable; do not copy it into the ticket
record.
```

## Plan Review (subagent)

Under reviewed planning, try to show that a change plan will not work or will
not deliver what it claims. One lens per ticket, named in Objective. Exactly
two lenses exist: `consequences` and `product`.

Neither lens depends on the other. Once both are `ready`, dispatch them
together; their shared read is not a conflict. The `consequences-critic` and
`product-critic` personas own the two lenses. A Plan Review ticket has one
unit. The orchestrator does not review, reviewers do not write the plan, and
Adversarial Review does not replace this type.

Assignment prompt, after the shared agent rules:

```text
This ticket is Plan Review. Try to show that the change plan named in Reads
will not work or will not deliver what it claims. Review only through the lens
named in Objective.

consequences: check whether the choices hold, what else must change for the
plan to work, what the plan breaks or leaves inconsistent, and whether the
order, compatibility, and migration handling are safe.

product: check the plan against the goals it cites, including their outcomes
and acceptance criteria, and the canonical doc or spec sections it cites. Use
the observable effect the plan states for each area. Report where the plan
contradicts those requirements, drifts past a non-goal, or would finish without
reaching the cited outcome.

When Objective names parts of the plan, review only those parts through your
lens.

Do not edit the plan. Do not implement any part of it. Do not write your own
plan. Do not change project files, external state, or any prepared human
environment.

Classify each choice you find by the shared product-decision test and finish the
review instead of stopping.

Return on the ticket:
- findings, each with a ticket-scoped ID such as `T-005-PLR/F-001`, its
  location in the plan, evidence, and impact or severity
- for each finding, whether it is a choice the user should take by that test,
  or one the orchestrator can settle
- whether any finding rejects the approach itself rather than its detail
- what the plan should change, as proposals
- checks that found no problem
- remaining uncertainty
```

## Adversarial Review (subagent)

Actively try to show that completed work is incorrect, incomplete, or
inconsistent with the run. Each unit covers completed implementation tickets
or run modules, named on its `Covers` line; units for newly completed work
arrive through the inbox. When completed work is UI, put the
`ux-ui-reviewer` skill file on Reads so inspection follows that skill. The
ticket type remains Adversarial Review. Do not create a UX/UI review Agent Task
for the same completed work.

The orchestrator must not be the reviewer. It decides whether review is due and
assigns this type.

Assignment prompt, after the shared agent rules:

```text
This ticket is Adversarial Review. Try to show that the completed work is
incorrect, incomplete, or inconsistent with the run.

Read the listed goals, acceptance criteria, non-goals, working hints, and
verification requirements. Check the work each unit covers against them.

When a unit's Reads name snapshots for the work it covers, judge the work as
of those snapshots, as the agent boundary inspection prompt describes, and
note anything later work has already changed.

Record on the ticket, per unit:
- specific findings, each with an ID such as `T-009-ADV/F-001`
- evidence
- impact or severity
- checks that found no problem
- remaining uncertainty

Do not fix findings unless Objective explicitly includes remediation.
```

## Discuss/Gather Inputs (orchestrator)

The orchestrator handles this ticket because it owns the user conversation.

Ask only for information, a decision, review, or acceptance required by the
ticket. Write it under Writing the ask in `HUMAN-ASKS.md`, from evidence
already on tickets or run files: the
question and any options, recommendation, or draft that exist. Do not invent
them. If a product decision needs prepared options and they are missing, the
ticket is not `ready`: open Research or Explore Options first.

For each decision option, explain the behavior the user would observe, known
knock-on effects for later development, compatibility, or scope, and whether
the choice can be deferred to a named later goal, module, or project-plan step.
If it cannot, explain what current work it blocks or would make unsafe. The
ticket is not `ready` until evidence supports those explanations; open Research
or Explore Options to prepare what is missing.

For acceptance, present the exact result, how to inspect it, the acceptance
basis, what observations indicate success or required changes, and a request
to accept it or describe required changes. Do not use a structured questions
form or multiple-choice prompt for acceptance.

Ask only for judgement a subagent cannot make. The model ask and the
planning-depth offer are the only Discuss tickets whose subject is process:
they ask for preferences no subagent can supply. Never ask the user to perform or
confirm a check a subagent can run, such as tests, builds, lint, searches, or
doc checks, under any label, including inspection method or expected result;
report it as a recorded outcome from its ticket instead. Asking the user to run
a product workflow and judge whether it still behaves as expected is inspection,
not such a check. Point the user at a file, page, or preview only when the
judgement needs eyes on it, and give a command only as optional reproduction.

Review and acceptance asks present only product-facing results, as defined
under Reconciliation in SKILL.md; an agent boundary inspection accepts the rest.

One Discuss may inspect or accept several named implementation tickets when
their results form one usable review. Group each result with its recorded
evidence and acceptance basis, then request one response that accepts all or
names the ticket or unit IDs needing changes. Do not create one Discuss per
amendment by default.

One Discuss may also carry several decisions that are ready in the same
reconciliation pass and concern the same tickets or run modules. Number them
and request one reply that answers each by number.

The current Discuss ask lives in Objective. On Discuss and Human Task, the
orchestrator records the user response in Evidence, writes
`execution_result`, then reconciles.

## Human Task (orchestrator)

The user performs the actual task. Use this type only for an external action the
run must not automate, including one needing the user's authority, credentials,
access, or presence.

Objective is a complete ask under Writing the ask in `HUMAN-ASKS.md`: what to
do, how to do it, in order, with the commands, paths, URLs, and expected output
the user needs. Include hints and
known recovery steps only when supported by ticket or run-file evidence. Name
an account or secret-store location when required. Never put secret values in
the ask or ticket. If procedure details are unknown, the ticket is not `ready`:
open Research or Discuss first. Do not block readiness only because no hint or
recovery step applies.

Completion is the observable result or evidence the user should return, not the
process reason.

## Human and Agent Task (orchestrator)

The orchestrator and user perform one bounded task through repeated, branching
interaction. The orchestrator may inspect, run commands, change project files,
or change external state within Objective.

Use this type only when one interaction loop is materially better, such as:

- branching work whose next agent action depends on a human observation;
- fast iterative debugging with many short human and agent turns;
- interactive setup or diagnosis whose steps cannot be specified usefully in
  advance.

Do not use it for one human action, one decision, ordinary implementation,
asynchronous work, or uncertainty alone. It does not replace Discuss for a
product decision.

Before starting:

1. apply the exact concurrent-ticket test in SKILL.md and wait for every active
   agent ticket that does not pass it; a parked session on such a ticket stays
   parked and is not resumed until this ticket ends;
2. check dependencies and file, state, and decision conflicts as for Assignment;
3. confirm no other human ticket has `presentation: presented`;
4. set ticket status to `active`, owner to `orchestrator`, and presentation to
   `upcoming`;
5. set `execution_result: null`.

While active:

- do only the bounded Objective;
- put each current ask in the latest Interaction log entry, not Objective;
- make each ask complete for that turn, including procedure, expected result,
  evidence-backed hints, and secret handling when applicable;
- before every user-facing interaction, append one Interaction log entry with
  the agent action and result, user result received, branch taken, next ask,
  and paths changed in that turn;
- update Work performed and Evidence on any turn that changes project files or
  external state, and before execution ends;
- set presentation to `presented` immediately before returning with the ask;
  when the user replies, set it to `upcoming` while the orchestrator works;
- on `presented` to `upcoming`, mark the ask page not awaiting a reply; before
  the next ask, replace the page;
- keep the ticket active across user turns;
- do not present another human ticket;
- dispatch or leave active only agent tickets that pass the exact
  concurrent-ticket test in SKILL.md.

Before expanding Exclusive scope, wait for newly conflicting active agent
tickets to return and reconcile them. Check Findings and Evidence from tickets
that ran concurrently for invalidation of Interaction log evidence and record
the result in `LOG.md`.

If work reaches a product decision, stop short of the choice, record options
and a recommendation, set presentation to `withdrawn` and execution result to
`blocked`, update its ask page under `HUMAN-ASKS.md`, then reconcile.
Open Discuss and make this ticket depend on it. After Discuss resolves, restore
Exclusive scope, set this ticket `ready` with presentation `upcoming`, and
present its next ask as a new complete presentation.

When Completion is met, set presentation to `answered` and execution result to
`completed`, update its ask page, then reconcile. If work cannot
continue, set presentation to `withdrawn`, update its ask page, set
execution result to `blocked` or `failed`, then reconcile. If the user stops the
task, record that result, withdraw it, update its ask page, set
execution result to `blocked`, and reconcile it to `cancelled`. This is the only
case where the orchestrator performs production work and then reconciles it.

Commands, inspections, and tests performed in this ticket are its Evidence.
They do not replace independently required goal verification or Adversarial
Review.
