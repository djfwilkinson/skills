---
name: orchestrated-run
description: Coordinate a substantial project run through one user-facing orchestrator, shared run files, and subagent tickets. The orchestrator owns the process: run state, ticket creation and assignment, user interaction, steering, reconciliation, next work, and goal verification. Subagents execute individual tickets from a type prompt and file references. Use only when explicitly invoked by the user.
disable-model-invocation: true
metadata:
  invocation: user-only
---

# Orchestrated run

This skill is user-invoked. Start it only when the user explicitly invokes `orchestrated-run`.

The skill defines the process. Run files define current state. Tickets define pieces of work and keep their detailed results. Subagents execute tickets. The orchestrator reconciles results and controls the run.

## Roles

The orchestrator owns the process, not the detailed execution of every ticket.

It:

- maintains run state;
- creates and assigns tickets;
- handles user interaction;
- acts on steering immediately;
- reconciles returned ticket results;
- updates goals, non-goals, unknowns, working hints, pillars, modules and the log;
- decides what work should happen next;
- decides when goals have been verified.

Subagents own individual agent tickets while they are active and execute them. The orchestrator owns `Discuss/Gather Inputs`, `Human Task`, and `Human and Agent Task` tickets.

The orchestrator must not:

- perform the bounded work of an agent ticket;
- write worker-maintained ticket sections, except to record `execution_result` and the user response in Evidence for Discuss or Human Task, or while executing a `Human and Agent Task`;
- reconstruct or rewrite a returned ticket record;
- give this skill file to a subagent.

`Human and Agent Task` is the only ticket type that lets the orchestrator perform bounded production or investigation work. Use it only under that type's contract.

Product decisions stay with the user when the product-decision rule below applies. Process decisions stay with the orchestrator: which ticket to create, whom to assign, whether to accept an execution result, whether a goal is verified, whether adversarial review is due, whether the run is complete.

A subagent reports what it found. It does not create run-level plans or tickets. The orchestrator decides how that changes the run. Follow-ups in a ticket are proposals, not a whitelist.

## Required references

This skill keeps the run-level process loop in this file and ticket, run-state,
and human-ask contracts in one-level references stored beside `SKILL.md` in the
same skill folder:

- Read [TICKET-CONTRACTS.md](TICKET-CONTRACTS.md) before creating, assigning,
  presenting, executing, or recovering a ticket. Read the schema, shared rules,
  and exact type contract that apply.
- Read [RUN-STATE.md](RUN-STATE.md) before creating or updating run files and
  after compaction.
- Read [HUMAN-ASKS.md](HUMAN-ASKS.md) and use its templates before every
  human-ticket presentation state change and after compaction with a presented ticket.

These references are mandatory parts of the contract, not optional guidance or
skills to invoke. If a required reference cannot be read, stop and report that
blocker rather than proceeding from memory. Do not put this skill or its
contract references on a subagent's Reads. Agent-ticket assignment prompts copy
the shared rules and exact type prompt from `TICKET-CONTRACTS.md`.

## Run files

Conversation context is temporary. Persistent memory is run files, ticket files, and project files. After compaction or a lost thread, recover the run from those files plus this skill.

Create a new run at:

`<project>/.agent-runs/orchestrated-run/<timestamp>-<short-name>/`

Create these as empty placeholders. Markdown files get a title heading only.
`tickets/` and `asks/` are empty directories.

```text
GOALS.md
NONGOALS.md
UNKNOWNS.md
WORKINGHINTS.md
LOG.md
PILLARS.md
MODULES.md
tickets/
asks/
```

Do not fill the Markdown files during setup. `tickets/` and `asks/` start empty.
Ask pages are orchestrator-owned presentation artifacts derived from human
tickets; they are never a source of truth. Resume a run when the user or
invocation identifies it. Otherwise create a new run.

When creating `<project>/.agent-runs/`, add `.agent-runs/` to the project `.gitignore` if that line is missing. Create `.gitignore` if the project has none. That is setup, not an Agent Task.

Use stable IDs: goals `G-001`, non-goals `NG-001`, unknowns `U-001`, pillars `P-001`, modules `M-001`, tickets such as `T-001-RES`. IDs remain stable for the lifetime of the run and are not reused.

The orchestrator owns and writes all run files and `asks/` artifacts except
active subagent-owned ticket files.

A subagent owns its agent ticket file while the ticket is active. No other agent edits that ticket until it is returned. The orchestrator owns an active `Human and Agent Task` ticket.

## Start the run

1. Create the placeholder files. Apply the `.agent-runs/` gitignore rule above.
2. Create the bootstrap ticket or short bootstrap set from the invocation. Use
   a short set when the request names separable areas that can be researched
   independently. Do not do the research in the orchestrator thread. Attach a
   `## Reads` list of likely project paths or directories. A surface bootstrap
   always pre-authorises escalation to deep in the same assignment when surface
   cannot meet Completion.
3. Dispatch those tickets with the Research assignment prompt and those references.
4. When bootstrap is a set, wait for every ticket in that set to return before
   activating goals or creating production, Explore Options, or Human and Agent
   Task tickets. A Discuss needed to continue discovery may be created earlier.
   Reconcile the set together, copy proposals into run files using
   `RUN-STATE.md`, and decide which follow-ups become tickets.

Mark `Agent Task`, `Explore Options`, and any ticket that implements or depends on unconfirmed product decisions as `blocked` with `depends_on` the relevant Discuss tickets. They become `ready` only after those tickets resolve.

**If the invocation contains a request.** Create one Research ticket, or a
short independent set when the request has separable areas. Understand the
request and inspect enough of the project to propose goals, non-goals,
unknowns, useful user questions, and likely next tickets. Put the user prompt
on the ticket. Point Reads at likely project paths or directories rather than
pasting a survey. Use `surface` when the request already states the outcome,
acceptance basis, and useful paths; use `deep` when scope, project structure,
conflicts, or required evidence need discovery. The proposed goals should
record incompleteness, conflicts, and whether they match the user's prompt.

**If the invocation contains no useful request.** Create one `deep` Research
ticket whose Objective is to inspect enough of the project to reach a useful
question before asking the user. Do not ask for goals with no project context
when the project can provide useful information first. Do not start
implementation in bootstrap.

## Run state
Read [RUN-STATE.md](RUN-STATE.md) before creating or updating goals,
non-goals, unknowns, working hints, pillars, modules, or the log. Tickets keep
the detailed discovery and work record. Run files contain only wider-run state.

### Product vs process

A product decision requires user involvement when reasonable choices would produce meaningfully different product, architectural, operational, compatibility, or scope outcomes. Examples include changing goals; architecture, public API, persistence, UX, dependency, or platform choices; scope trade-offs; and accepting significant adversarial findings without fixing them.

Local implementation choices that follow established project patterns are process decisions. The orchestrator applies this test and does not default uncertainty to a user interruption.

When a ticket lists alternatives, apply the same test. Meaningfully different outcomes are enough prepared evidence for Discuss/Gather Inputs; use the existing options and recommendation without another Research or Explore Options ticket. Reconcile local pattern-following alternatives as a process decision and record the option and reason in `LOG.md`.

A subagent that hits such a choice records it on the ticket and stops short of committing it. The orchestrator must not commit it either.

Process decisions are not user tickets unless they need a product choice. The orchestrator decides next work, assignment, acceptance of results, verification, review scheduling, and run completion.

## Tickets
Read [TICKET-CONTRACTS.md](TICKET-CONTRACTS.md) before creating a ticket.
That reference owns ticket IDs, schema, ownership, readiness, and type
contracts. Every new ticket follows it.

## Assignment

Every `ready` agent ticket is assigned to one subagent before any work on it starts. That is the only way agent tickets get done.

Do not give the subagent this skill. Give it:

1. the ticket file path;
2. the shared agent rules and exact assignment prompt copied from
   `TICKET-CONTRACTS.md`;
3. the `## Reads` list of paths.

Do not build a large custom context summary. Point at files, naming the exact ID
or heading when only part of a run file applies. Reads may include applicable
working hints, goals, unknowns, pillar or module entries, earlier tickets,
project paths, and documentation. Include every governing entry, but omit run
files that have nothing for the ticket. Repo-wide Reads are for Research, not
Agent Task. Do not dump a repo survey into the ticket.

When assigning a ticket:

1. confirm dependencies using ticket metadata and owned run files;
2. check for file, state, and decision conflicts with active tickets and every
   other ticket in the same dispatch wave; a conflicting wave member stays
   `ready` and queued;
3. fill `## Reads`;
4. set `status: active`;
5. set `owner` to the assigned subagent;
6. dispatch the subagent with the type prompt and those paths.

Independent tickets may run in parallel. A wave of independent ready agent
tickets may be dependency-checked, conflict-checked, filled, and dispatched in
one pass. Do not dispatch `proposed` or `blocked` tickets. Handle Discuss,
Human Task, and Human and Agent Task in the orchestrator thread.

Outside a selected or active Human and Agent Task, wait for dispatched agent
tickets to return. That wait is not a user prompt. When one returns, reconcile
every ticket already returned at that point; do not wait for more solely to
enlarge the batch. Do not wait for the user to continue the run.

Selecting a ready Human and Agent Task creates an exclusive-scope barrier. Do
not select or start it while another human ticket has
`presentation: presented`; get that response before starting it. Record
selection and Exclusive scope in `LOG.md`.

An agent ticket is safe to run concurrently only when its Objective and
Completion explicitly prohibit changes to project files, external state, and
prepared human environments; its Reads are disjoint from Exclusive scope; and
it shares no unresolved decision with the unfinished interaction. Wait for
every active ticket that does not meet this test before starting the Human and
Agent Task. While it is active, dispatch or leave active only tickets that meet
the same test, and do not present another human ticket. When independence is
uncertain, allow no concurrent agent ticket.

Before expanding Exclusive scope, wait for agent tickets that would fail the
expanded test. Check Findings and Evidence from every ticket that ran
concurrently for invalidation of recorded Interaction log evidence, and record
the result in `LOG.md`.

Apart from closed-ticket progress updates, return to the user only when a human
ticket needs a response, or when the run is complete. If agent tickets are also
active, still reconcile them when they return.

## Human involvement
Every required human interaction must have a ticket. A product decision that requires user involvement must have a `Discuss/Gather Inputs` ticket.

Use `Discuss/Gather Inputs` when the user needs to provide information, fill in an unknown, make a product decision, review something, make a judgement, or accept a result, including proposed goals and non-goals.

Use `Human Task` when the user needs to perform an external action.

Use `Human and Agent Task` only for the repeated, branching interaction defined by its contract.

Human acceptance used for goal verification must be a Discuss/Gather Inputs
ticket. The human inspection Discuss may also be the acceptance ticket when its
acceptance basis is that same result. Open another Discuss only when acceptance
is a different judgement.

Environment preparation is readiness work. Follow the single preparation gate
in `TICKET-CONTRACTS.md`; record completed preparation ticket pointers and
current evidence in Presentation. Do not select a Human and Agent Task until
its preparation dependencies complete. Once active, it may adjust its own
environment within Objective.

At presentation time, the orchestrator may perform only non-mutating liveness checks on already-prepared resources and open the relevant file or page when the client supports it. Starting, restarting, repairing or changing the environment is agent-ticket work unless an active Human and Agent Task authorises it.

If a human ticket blocks only part of the run, dispatch ready agent tickets
that do not depend on it, then return to the user. During a Human and Agent Task
this applies only to tickets that pass the test in Assignment under its
exclusive-scope barrier. Tickets whose `depends_on` names the answer are
`blocked`. The orchestrator may block others when the missing answer would
invalidate them. Record that decision in `LOG.md`.

Do not keep planning in place of that return, and do not invent the answer.
Follow the complete first-presentation and condensed-repeat chat contract in
`HUMAN-ASKS.md`. Discuss and Human Task asks live in Objective. Human and Agent
Task current asks live in the latest Interaction log entry.

Create human tickets with `presentation: upcoming`. Immediately before first
presentation, perform the allowed liveness check; record the ask source,
ask-page path, presentation time, and liveness result in Presentation; write
the per-ticket ask page from the bundled template under `asks/`; set ticket
status to `active`, owner to `orchestrator`, and presentation to `presented`;
then update the index template data to add its live row.
At first presentation, best-effort launch the absolute ask-index path in the
default external browser as specified in `HUMAN-ASKS.md`. Do not wait, verify,
retry, or record the launch as a client-link check.
Present the complete type-appropriate ask in chat with the ticket path and
links to its ask page and index. A link alone is not a presentation.

After that exact ask has had one complete presentation, later user-visible
messages follow the single condensed-line contract in `HUMAN-ASKS.md` only
when Presentation records a successful open in the current client. Otherwise
repeat the complete ask. A new or changed ask always gets a complete
presentation first.

If a non-mutating liveness check shows that the prepared environment is
unusable, set ticket status to `blocked`, clear owner, set presentation to
`withdrawn`, remove its live index row and mark its page withdrawn, add the
preparation ticket to `depends_on`, record the withdrawal in Presentation and
`LOG.md`, and tell the user the previous ask is withdrawn. A reply to a
withdrawn ask cannot complete the ticket. After preparation returns, set the
human ticket to `ready` with presentation `upcoming` and present it as a new
ask.

That return does not pause the run. Reconcile any agent ticket that returns while you wait. A return for an active `Human and Agent Task` is different: the run intentionally stays in that ticket's interaction loop.

When the user responds to a presented Discuss or Human Task, set presentation
to `answered`, remove its live index row and mark its page answered, record the
response on the ticket, reconcile it, and continue the run. When the user
responds to a Human and Agent Task, record the interaction, set presentation to
`upcoming` while the orchestrator works, remove its live index row, mark the
page not awaiting a reply, and continue that ticket; reconcile only when its
execution ends. Before its next ask, replace the page, add the row, and make the
complete new presentation.

## Steering

When the user sends a new prompt while other work is still going, act on it immediately. Do not wait for active tickets to return.

Change requests and feedback become tickets. Create them now. Assign ready
agent tickets unless they conflict with active work or a selected or active
Human and Agent Task's Exclusive scope. Do not edit an active subagent's ticket
file. Block or delay conflicting assignment until the active ticket returns.
Record the steering and tickets created in `LOG.md`.

If the prompt responds to a presented Discuss or Human Task, treat it as that
ticket's return. A response to a withdrawn ask is steering or new evidence,
not ticket completion. If it answers the current presented ask on an active
Human and Agent Task, follow the presented-to-upcoming transition under Human
involvement and treat it as the next interaction, not a ticket return. Other
prompts are steering: create resulting tickets and assign only those that pass
current conflict rules. If the user stops or replaces the interactive task,
end and reconcile it before proceeding. Then continue the run.

## Reconciliation
When an agent ticket returns, a Discuss or Human Task returns, or a Human and Agent Task ends:

1. Read the ticket file and `execution_result`. Leave worker-maintained sections as the worker wrote them.
2. Clear `owner`.
3. Decide the persistent ticket `status`. `completed` is not automatically `resolved`. After return, set `ready` (reassign the same ticket), `blocked`, `resolved`, or `cancelled`. Keeping it for further work means `ready` and `owner` cleared. When reassigning a blocked ticket, state what Work performed already covers so the next worker does not repeat it.
4. Reconcile the result into the run: add a concise `LOG.md` entry; use ticket YAML IDs to limit which existing run entries need refresh, but always inspect worker Unknowns, Findings, and Blockers / follow-ups for new wider-run entries; update run files only where wider state changed; decide next work from follow-ups as proposals; decide whether related verification or review is still required.

Reconcile every ticket already returned at the start of the pass. Decide each
ticket's state, then write each affected run file once. Do not wait for more
returns solely to enlarge the batch. Complete persistent writes, recompute
readiness, and dispatch newly ready non-conflicting work before sending routine
progress.

Do not copy the investigation into the log or re-do the ticket in the
orchestrator thread. If evidence is missing or the result is unacceptable,
create or reassign tickets.

Every completed implementation ticket, including a Human and Agent Task that
performed implementation, needs implementation coverage: a boundary inspection
Discuss and a boundary validation Agent Task that both name its ID and both
resolve before its module or the run completes. The inspection must not be
superseded, and validation Evidence must meet its success conditions.

When an implementation ticket completes, attach it to an open non-active
boundary-inspection and boundary-validation pair for a coherent inspection
batch, or create the pair immediately. One user amendment set is one batch by
default: record all covered IDs on both tickets and keep them blocked on its
known active or ready implementation tickets. Present one grouped inspection
after the batch returns. Split only when results cannot be inspected coherently
or delay would stall the run; never split merely because the batch has several
tickets, modules, or check sets, and do not wait for unknown future work.

Run boundary inspection and boundary validation in parallel; neither depends on the other.
A grouped ask maps results and checks to covered IDs and asks for one reply accepting all
or naming IDs needing changes; use the same Discuss for acceptance of that batch.

Immediately before presenting a boundary inspection, rebuild its ask from the
current covered-ticket record and establish its inspection freeze in
Presentation. The freeze includes changed paths from every covered
implementation, shared dependents that can change the inspected result, and
every prepared environment that could restart, rebuild, or reload. Until the
inspection returns or is withdrawn, do not patch or ready a ticket that would
change that scope. Findings outside it may become ready immediately.

If boundary validation finds issues, record them and let the orchestrator
decide which become tickets. If an issue invalidates an upcoming inspection,
keep it blocked, create the chosen fix tickets, and add them to `depends_on`;
do not present it before fixes and a new boundary validation start. If an issue
invalidates a presented inspection, first set the inspection ticket
`status: blocked`, clear owner, set presentation to `withdrawn`, remove its live
index row, mark its page withdrawn, record the reason and times in Presentation
and `LOG.md`, and tell the user the ask is withdrawn. Then create the chosen fix
tickets and add them to `depends_on`. After fixes return for an upcoming or
withdrawn inspection, create or ready a new boundary validation ticket, set the
existing inspection `ready` with presentation `upcoming`, and present a new
complete ask under the normal parallel rule.

If invalidation arrives after inspection was answered or resolved, mark that
inspection and any acceptance evidence superseded, move any affected goal out
of `achieved` to `active` or `blocked` as the remaining work requires, and
create a new boundary inspection after fixes. A reply or acceptance for an
invalidated result never verifies the fixed result.

## Adversarial Review scheduling

The orchestrator must not be the reviewer. Default to one Adversarial Review at
each module boundary, batching several small related modules when useful, and
one before completing the run. Review earlier after high-impact or
cross-cutting changes, unexpected test or debugging results, or uncertain
evidence. After remediation, review the changed surface; repeat a full review
only when the remediation is itself high-impact or cross-cutting. Do not run
overlapping reviews of the same completed work. A pre-completion review may
also satisfy the last module boundary when its Reads cover both scopes. A
worker recommendation to review is a proposal.

## Progress updates

For chat progress, a ticket is closed when its status becomes `resolved` or `cancelled`.

After a reconciliation pass closes one or more tickets, dispatch newly ready
work first, then send one short progress update for that pass. For `resolved`,
give the ticket ID and one sentence with the user-visible result. For
`cancelled`, give the ticket ID and concise user-relevant reason in `LOG.md`;
do not imply an execution result. A ticket cancelled before it was dispatched
or presented needs no progress line unless the user was told it was upcoming.
Do not paste ticket YAML, Reads, Findings, Interaction log, or detailed
evidence. Do not ask the user to approve routine progress.

If known human tickets are coming but are not being presented yet, the update may briefly say what user involvement will be requested later. Do not include the full ask until that ticket is presented under Human involvement or the Human and Agent Task contract.

If any human ticket is presented, append the repeat required by the chat
contract in `HUMAN-ASKS.md`. Describe an `upcoming` ticket as upcoming, never
waiting; do not append a withdrawn ask.

## Log

Follow the concise `LOG.md` contract in `RUN-STATE.md`. Detailed investigation
and implementation notes stay on tickets.

## Context compaction

Compaction is not a second planning process. Those actions belong to reconciliation.

Before compacting:

1. all returned tickets have been reconciled;
2. run files already reflect any wider-run changes from those tickets;
3. an active Human and Agent Task has recorded its current work, evidence and next ask on its ticket.

Detailed ticket results stay in their ticket files. Copy into run-level files only what affects the wider state of the run.

Compaction itself must not draw new conclusions, create new tickets, or modify the plan.

After compaction, rebuild context from:

1. this skill;
2. `TICKET-CONTRACTS.md`;
3. `RUN-STATE.md`;
4. `HUMAN-ASKS.md` when any human ticket is presented;
5. `GOALS.md`;
6. `NONGOALS.md`;
7. `UNKNOWNS.md`;
8. `WORKINGHINTS.md`;
9. `PILLARS.md`;
10. `MODULES.md`;
11. relevant entries from `LOG.md`;
12. tickets needed for current work.

Reload completed tickets only when their detailed results become relevant.

Before acting on any active, ready, or presented ticket, read its schema and
exact type contract in `TICKET-CONTRACTS.md`.

Reload every presented human ticket from Objective or its latest Interaction
log entry and Presentation. Read `HUMAN-ASKS.md`, then rebuild missing or stale
ask pages and the index from those tickets and the bundled templates before
another user-visible message. Tickets, not HTML, determine current presentation
state and ask content.

If a Human and Agent Task has status `active` and owner `orchestrator`, reload
it and resume from its latest Interaction log entry. Do not repeat recorded
actions.

If `LOG.md` records a selected Human and Agent Task that is still `ready`,
restore its exclusive-scope barrier before dispatching any agent ticket.

## Process

Discovery, planning, implementation, issue resolution, validation and human acceptance happen as tickets. The orchestrator does not execute agent tickets. It executes `Human and Agent Task` only under that type's narrow exception. It picks ticket type when it creates a ticket.

## Goal verification

Ticket completion, module completion and goal achievement are separate.

The orchestrator marks a goal `achieved` when it decides verification is satisfied, using evidence already in tickets and run files: accepted criteria, defined verification, completed verification work, required human acceptance, and disposition of adversarial findings.

Outside an active Human and Agent Task, it must not re-run tests, inspect artifacts, or otherwise execute verification in the orchestrator thread. A non-mutating liveness check used only to present an already-prepared human environment is process work, not goal-verification evidence. Checks performed inside Human and Agent Task remain ticket Evidence and do not replace independently required verification. If verification evidence is missing, create tickets.

Agent judgement used as verification is an `Agent Task` or `Adversarial Review`. Human judgement is `Discuss/Gather Inputs`.

If verification fails, decide next work from the record. Mark a goal `blocked` when the run cannot proceed on it. Never mark a goal `abandoned` until the user confirms abandonment through `Discuss/Gather Inputs`.

## Completing the run

The orchestrator decides when the run is complete. An Adversarial Review can inform that decision. It does not own it.

The run is complete when:

- every goal is `achieved` or `abandoned`;
- achieved goals contain verification evidence;
- no required verification is deferred;
- no unresolved ticket is required for an achieved goal;
- every resolved implementation ticket has implementation coverage from a
  resolved boundary inspection and resolved boundary validation ticket;
- required human tasks and acceptance are complete;
- significant adversarial findings are resolved or explicitly accepted by the user;
- open entries in `UNKNOWNS.md` required for achieved goals are closed;
- the run files reflect the final state.

An empty ticket queue does not mean the run is complete.

When the run is complete, return to the user with a concise summary. Use only what is already in the run files:

- goals achieved;
- important decisions;
- verification results;
- abandoned goals;
- remaining optional follow-up work.
