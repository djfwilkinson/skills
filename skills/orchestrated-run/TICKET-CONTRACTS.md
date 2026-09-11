# Ticket contracts

This file is part of the `orchestrated-run` contract. The orchestrator must read
the relevant sections before creating, assigning, presenting, executing, or
recovering a ticket. It is not a skill and must not be invoked.

Subagents do not receive `SKILL.md`. Agent-ticket assignment prompts copy the
shared agent rules and exact type prompt from this file.

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

`status`, `owner`, `presentation`, `plans`, and `reviews` are
orchestrator-owned.
`execution_result` is worker-owned and unset until execution ends.

While a ticket is active, the worker may update only:

- `execution_result`;
- `Unknowns`;
- `Findings`;
- `Work performed`;
- `Evidence`;
- `Interaction log`;
- `Blockers / follow-ups`.

A Plan worker may also write its Completion-named change plan; no other type
writes under the run directory. Agent Task and Explore Options may write
project files under their Objective.

The worker must not modify other ticket metadata. When the orchestrator is the
worker for a Human and Agent Task, it still updates orchestrator-owned fields
separately under that type's lifecycle.

Use this template. Keep the headings so ownership remains visible. A worker may
leave a worker-maintained section empty when it has nothing to record; do not
fill sections with padding.

```md
---
id: T-001-RES
title: Understand the user prompt
type: Research
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

## Interaction log
<worker-maintained: Human and Agent Task only unless otherwise needed>

## Blockers / follow-ups
<worker-maintained: proposals for the orchestrator; leave empty when none>
```

`plans` holds the Plan ticket IDs for change plans that govern the ticket.
`reviews` is used only on a Plan ticket and holds the current round's Plan
Review ticket IDs.

Ticket statuses:

`proposed | ready | active | blocked | resolved | cancelled`

Human-ticket presentation:

`null | upcoming | presented | withdrawn | answered`

Use `null` for agent tickets. Use the other values only under Human involvement
and the Human and Agent Task contract.

Execution results:

`completed | blocked | failed`

A ticket is `ready` when the orchestrator decides its dependencies and required
inputs are available. `execution_result: completed` does not imply
`status: resolved`. Reconcile first.

## Readiness

Keep each ticket bounded enough for one assignment. If a ticket proves too
broad, the worker may complete a severable part that stays within Objective,
records what remains, and reports `blocked` unless Completion is met. The
orchestrator decides how to split, replace, or reassign it. A reassigned
Objective names what Work performed already covers so the next worker does not
repeat it.

An Agent Task is not `ready` until Objective, Completion, and Reads name what to
change and what done looks like. Vague Research follow-ups stay Research or
unknowns. Agent Task Reads are files Research already found or an accepted
change plan, not the repo.

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
approach-blocking investigation, its file to exist, Objective to name the lens,
and Reads to name the plan, governing goals and acceptance criteria, non-goals
and working hints. Product-lens Reads also name the end user and cited
canonical sections or their recorded gaps.

A boundary validation ticket is its own Agent Task. It checks goal-level,
repo-wide, or cross-area requirements for the implementation tickets it names.
Do not fold wider validation into those implementation tickets.

## Shared agent rules

Copy this block into every agent-ticket assignment prompt, followed by the
exact type prompt.

```text
You are executing one ticket. You own that ticket file while it is active.

Read the ticket file and every entry in its Reads list, at the exact ID or
heading when one is named. Then do only the bounded work in Objective.

Update the ticket before you return. You may change only execution_result,
Unknowns, Findings, Work performed, Evidence, Interaction log, and Blockers /
follow-ups. Do not change other ticket metadata. Keep the record proportional
to the result: leave worker-maintained sections empty when they have nothing to
record, and use a concise Evidence pointer when the changed files or checks are
the evidence. Do not leave the detailed record only in chat.

Set execution_result to null before starting this assignment. Before you
return, set it to completed, blocked, or failed. That is your result, not the
persistent ticket status. The orchestrator owns status and owner.

Do not edit run-level files (GOALS.md, NONGOALS.md, UNKNOWNS.md,
WORKINGHINTS.md, LOG.md, PILLARS.md, MODULES.md, or asks/). Do not create
tickets. Do not plan the run. Record follow-ups on this ticket. The orchestrator
decides what happens next. A Plan ticket also writes the change plan named in
its Completion; no other type writes a file under the run directory.

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
Blockers / follow-ups; set execution_result to blocked.

Return by finishing the ticket record and execution_result.
```

## Research (subagent)

Close a knowledge gap at the `triage`, `surface`, or `deep` depth chosen in
Objective and Completion. Prefer `surface` to standalone triage. Research
drafts and classifies follow-up Agent Tasks at either planning depth.

Assignment prompt, after the shared agent rules:

```text
This ticket is Research. Use only the depth path allowed by Objective and
Completion. Depth is effort on context and hunting.

triage: decide whether investigation is needed. Do not hunt the answer. Return
one next step (no-investigation-required | surface | deep) and a one-line basis.

surface: pull obvious context. Return the answer if it is there. Continue to
deep only when Objective and Completion pre-authorize that escalation; record
why you escalated. If deep is not authorized and surface cannot meet
Completion, return what you found, request deep on that gap, record new
unknowns, and set execution_result to blocked.

deep: get full context and hunt. Close in-scope gaps this assignment permits.
Return the answer, remaining unknowns, or a partial answer with evidence.

Return on the ticket: depth used; findings; evidence; remaining uncertainty;
implications; and follow-ups. Keep the record proportional to the result.

For every Agent Task follow-up, draft Objective, Completion, and Reads from
what you found, or name which part is missing and which ticket type could close
it. When several drafts must ship together, name them as one change set and say
why. These drafts are proposals. Do not create tickets. Propose Human and Agent
Task only when its bounded work and need for repeated branching interaction
are already clear.

Do not implement production changes unless Objective says to.
```

## Agent Task (subagent)

Perform bounded implementation or production work. When Objective is to produce
a UX/UI review, put the `ux-ui-reviewer` skill file on Reads.

Assignment prompt, after the shared agent rules:

```text
This ticket is an Agent Task. Perform the bounded production work in Objective.
Do not research what to build. Implement from Objective, Completion, and Reads.
If that is not enough, set execution_result to blocked and record the gap.

Meet this ticket's Completion. Check that, and nothing wider. Wider tests, lint,
typecheck, or cross-area review are not this ticket's job unless Objective and
Completion expressly make them so.

Return on the ticket:
- work performed
- changed files or artifacts
- checks against this ticket's Completion
- blockers
- possible follow-up work
```

## Explore Options (subagent)

Investigate alternatives without committing them to the production solution.

Assignment prompt, after the shared agent rules:

```text
This ticket is Explore Options. Investigate alternatives. Do not commit them to
the production solution.

You may use prototypes, temporary code, temporary tests, instrumentation,
reproductions, or debugging experiments. Label temporary artifacts temporary.

Return on the ticket:
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
banner.

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
together; their shared read is not a conflict. The orchestrator does not review,
reviewers do not write the plan, and Adversarial Review does not replace this
type.

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
inconsistent with the run. When completed work is UI, put the
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
verification requirements. Check the work against them.

Return on the ticket:
- specific findings
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

For acceptance, present the exact result, how to inspect it, the acceptance
basis, and a request to accept it or describe required changes. Do not use a
structured questions form or multiple-choice prompt for acceptance.

Ask only for judgement a subagent cannot make. The planning-depth offer is the
one Discuss whose subject is process: it asks for a preference no subagent can
supply. Never ask the user to perform or
confirm a check a subagent can run, under any label, including inspection
method or expected result; report it as a recorded outcome from its ticket
instead. Point the user at a file, page, or preview only when the judgement
needs eyes on it, and give a command only as optional reproduction.

One Discuss may inspect or accept several named implementation tickets when
their results form one usable review. Group each result with its recorded
evidence and acceptance basis, then request one response that accepts all or
names the ticket IDs needing changes. Do not create one Discuss per amendment
by default.

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
   agent ticket that does not pass it;
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
- on `presented` to `upcoming`, remove the live ask-index row and mark the ask
  page not awaiting a reply; before the next ask, replace the page and row;
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
`blocked`, update its ask page and index under `HUMAN-ASKS.md`, then reconcile.
Open Discuss and make this ticket depend on it. After Discuss resolves, restore
Exclusive scope, set this ticket `ready` with presentation `upcoming`, and
present its next ask as a new complete presentation.

When Completion is met, set presentation to `answered` and execution result to
`completed`, update its ask page and index, then reconcile. If work cannot
continue, set presentation to `withdrawn`, update its ask page and index, set
execution result to `blocked` or `failed`, then reconcile. If the user stops the
task, record that result, withdraw it, update its ask page and index, set
execution result to `blocked`, and reconcile it to `cancelled`. This is the only
case where the orchestrator performs production work and then reconciles it.

Commands, inspections, and tests performed in this ticket are its Evidence.
They do not replace independently required goal verification or Adversarial
Review.
