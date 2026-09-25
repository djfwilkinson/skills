---
name: orchestrated-run
description: >-
  Coordinate a substantial project run through one user-facing orchestrator,
  shared run files, and subagent tickets. The orchestrator owns the process:
  run state, ticket creation and assignment, user interaction, steering,
  reconciliation, next work, and goal verification. Subagents execute
  individual tickets from a type prompt and file references. Use only when
  explicitly invoked by the user.
disable-model-invocation: true
metadata:
  invocation: user-only
---

# Orchestrated run

This skill is user-invoked. Start it only when the user explicitly invokes `orchestrated-run`.

The skill defines the process. Run files define current state. Tickets define pieces of work and keep their detailed results. Subagents execute tickets. The orchestrator reconciles results and controls the run.

## Roles

The orchestrator owns run state, ticket creation and assignment, user
interaction, steering, reconciliation, next work, and goal verification.
Subagents execute and own active agent tickets. The orchestrator owns
`Discuss/Gather Inputs`, `Human Task`, and `Human and Agent Task`.
Discovery, planning, implementation, issue resolution, validation, and human
acceptance all happen as tickets.

The orchestrator must not:

- perform the bounded work of an agent ticket;
- write worker-maintained ticket sections, except to record `execution_result` and the user response in Evidence for Discuss or Human Task, or while executing a `Human and Agent Task`;
- reconstruct or rewrite a returned ticket record;
- give this skill file to a subagent.

Only `Human and Agent Task` lets the orchestrator perform bounded production
or investigation. A subagent reports its ticket result; it does not plan the
run or create tickets. A Plan's change plan is its bounded deliverable, not
run-level planning. The orchestrator decides how ticket results and proposed
follow-ups change the run.

## Required references

- Read [TICKET-CONTRACTS.md](TICKET-CONTRACTS.md) before creating, assigning,
  presenting, executing, or recovering a ticket. Read the schema, shared rules,
  and exact type contract that apply.
- Read [RUN-STATE.md](RUN-STATE.md) before creating or updating run files and
  after compaction.
- Read [HUMAN-ASKS.md](HUMAN-ASKS.md) and use its templates before every
  human-ticket presentation state change and after compaction with a presented ticket.

These are required contract references, not skills. If one cannot be read,
report the blocker rather than proceeding from memory. Never put them on a
subagent's Reads; copy its shared rules and type prompt from
`TICKET-CONTRACTS.md`.

## Run files

Conversation context is temporary. Recover from this skill, run files, tickets,
change plans, and project files.

Create a new run at:

`<project>/.agent-runs/orchestrated-run/<timestamp>-<short-name>/`

Create title-only Markdown placeholders and empty `tickets/` and `asks/`:

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

Create `plans/` only when planning depth is recorded as reviewed planning.
Ask pages are orchestrator-owned presentation artifacts derived from human
tickets; they are never a source of truth. Resume a run when the user or
invocation identifies it. Otherwise create a new run.

When creating `<project>/.agent-runs/`, add `.agent-runs/` to the project `.gitignore` if that line is missing. Create `.gitignore` if the project has none. That is setup, not an Agent Task.

Use stable IDs: goals `G-001`, non-goals `NG-001`, unknowns `U-001`, pillars `P-001`, modules `M-001`, tickets such as `T-001-RES`. IDs remain stable for the lifetime of the run and are not reused.

The orchestrator owns run files and `asks/`. A subagent exclusively owns its
active ticket and a Plan worker also owns its change plan; the orchestrator owns
an active `Human and Agent Task`. See `RUN-STATE.md` for change-plan ownership.

## Start the run

1. Create the placeholder files. Apply the `.agent-runs/` gitignore rule above.
2. Create one bootstrap Research ticket, or a short independent set for
   separable areas. Put likely project paths on Reads; never research in the
   orchestrator thread. A surface bootstrap pre-authorises deep escalation when
   needed for Completion. Its Objective also seeks the end user and canonical
   docs or spec when cheap to establish.
3. Dispatch those tickets with the Research assignment prompt and those references.
4. When bootstrap is a set, wait for all of it before activating goals or
   creating any other ticket; Discuss needed for discovery may start sooner.
   Reconcile the set together under `RUN-STATE.md`, subject to step 5.
5. Until planning depth is recorded, create only Discuss and Research tickets
   from bootstrap follow-ups. Do not create any other ticket type from them,
   even as `proposed`; those drafts stay on the proposing ticket.

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

## Planning depth

Planning depth is `standard`, where Research feeds Agent Tasks directly, or
`reviewed planning`, where qualifying change sets pass through Plan and Plan
Review tickets first.

Never create, ready, or dispatch a Plan or Plan Review unless
`WORKINGHINTS.md` records the confirmed planning depth as `reviewed planning`.
An unset, proposed, recommended, or `standard` value forbids both types.

If either type already exists without that value, do not infer planning depth
from it or use its change plan. Let an active worker return, then clear owner,
set the ticket `blocked` as invalid, create no reviews, and reconcile its
original proposing drafts under the recorded depth.

After goals become `active` and before creating `Agent Task`, `Explore
Options`, or `Human and Agent Task` tickets from bootstrap follow-ups, offer the
choice once when a reconciled bootstrap ticket records:

- a follow-up it classified as moderately complex or higher, or as changing a
  schema, persistence layer, public API, protocol, data migration, or canonical
  doc;
- a conflict between two sources it could not settle.

The condition must name its artifact; an open unknown alone does not qualify.
Do not offer for research-only runs. If the user stated a preference, record it
in `WORKINGHINTS.md` and `LOG.md` without asking. Otherwise use Discuss for the
offer; if no offer is due, record `standard` in `WORKINGHINTS.md` and its basis
in `LOG.md`. Only a stated preference, a returned offer, or that no-offer
default confirms the value. While the ask is unanswered, steering may create
Research to draft and classify requested work. Do not create, ready, or
dispatch Plan, Plan Review, Agent Task, Explore Options, or Human and Agent
Task until planning depth is recorded.

Never ask twice. Under `standard`, report later qualifying conditions in that
pass's progress update and continue. A process decision never overrides a user
answer. User steering may change the depth for undispatched work; record it in
`WORKINGHINTS.md` and `LOG.md`, without retroactively planning implemented work.

When `WORKINGHINTS.md` records confirmed planning depth as `reviewed planning`, a
proposing ticket qualifies a change set by classifying it as moderately complex
or higher or naming a schema, persistence layer, public API, protocol, data
migration, or canonical doc it changes. The orchestrator follows that record,
departing only for a missing or contradictory label and logging why.

- One classified draft is one change set unless the proposing ticket groups
  drafts that share a plan. Use one Plan ticket per change set.
- Put qualifying drafts on Plan Reads; create Agent Tasks directly for the
  rest.
- Tickets created from an accepted plan inherit it and need no new
  classification.
- Put direct user requests through Research before choosing Plan or Agent Task.
- Findings and recommendations retain the proposing ticket's classification;
  no classification is a missing label.
- If nothing qualifies, say so in the next progress update.

Reviewed planning needs the end user and the canonical docs or spec. When
bootstrap did not establish them, open Research to close the gap where the
project can answer it cheaply, and otherwise record the gap as an unknown and
continue; the product lens then reviews against the goals the plan cites.
Missing either blocks neither the offer nor reviewed planning.

## Run state
Read [RUN-STATE.md](RUN-STATE.md) before creating or updating goals,
non-goals, unknowns, working hints, pillars, modules, or the log. Tickets keep
the detailed discovery and work record. Run files contain only wider-run state.

### Product vs process

A product decision has reasonable alternatives with meaningfully different
product, architectural, operational, compatibility, or scope outcomes. This
includes changing goals, architecture, public API, persistence, UX,
dependencies, platforms, scope, or accepting significant adversarial findings.
Local implementation choices following established patterns are process.

For ticketed alternatives, use existing options and recommendations as Discuss
evidence; do not investigate again. The orchestrator selects and logs process
choices. Do not treat uncertainty alone as a product choice. Neither it nor a
subagent commits a product choice; Plan records one under Open decisions.

The orchestrator owns all process decisions, including next work, assignment,
result acceptance, verification, review, and completion. Planning depth is the
only process decision this skill puts to the user; other process decisions are
not user tickets.

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
presentation, follow the liveness, page, index, launch, ticket-state, complete
chat ask, and later-repeat lifecycle in `HUMAN-ASKS.md`. Set a presented ticket
`active` with owner `orchestrator`; a link alone is not presentation.

If a non-mutating liveness check shows that the prepared environment is
unusable, block the ticket on preparation, clear owner, withdraw its
presentation under `HUMAN-ASKS.md`, log it, and tell the user. After preparation
returns, set it `ready` and `upcoming`, then present a new ask.

That return does not pause the run. Reconcile any agent ticket that returns while you wait. A return for an active `Human and Agent Task` is different: the run intentionally stays in that ticket's interaction loop.

On a presented Discuss or Human Task response, mark the presentation answered
under `HUMAN-ASKS.md`, record the response, and reconcile. On a Human and Agent
Task response, record the interaction, return presentation to `upcoming`, and
continue the ticket; reconcile only when execution ends. Present each next ask
through the same contract.

## Steering

When the user sends a new prompt while other work is still going, act on it immediately. Do not wait for active tickets to return.

Classify the prompt first. When any part of it answers, stops, or replaces a
presented ask, use the return and interaction rules below. When it only asks
for information already explicit in the presented ticket, run files, or this
contract, answer it in the next message, leaving every presented ask
`presented` with its required repeat: change no ticket, run file, or
presentation, do not inspect the project, and do not review, verify, decide, or
invent a missing answer. Such a prompt is neither a ticket return nor a Human
and Agent Task interaction. Anything else follows the steering rules below:
create the tickets it needs.

Change requests and feedback become tickets. Create them now. Assign ready
agent tickets unless they conflict with active work or a selected or active
Human and Agent Task's Exclusive scope. Do not edit an active subagent's ticket
file. Block or delay conflicting assignment until the active ticket returns.
Record the steering and tickets created in `LOG.md`.

If the prompt responds to a presented Discuss or Human Task, treat it as that
ticket's return. A response to a withdrawn ask is steering or new evidence,
not ticket completion. If it answers the current presented ask on an active
Human and Agent Task, follow the presented-to-upcoming transition under Human
involvement and treat it as the next interaction, not a ticket return. If the
user stops or replaces the interactive task, end and reconcile it before
proceeding. Then continue the run.

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
performed implementation, needs implementation coverage before its module or
the run completes: the boundary inspections its result needs and a boundary
validation Agent Task, each naming its ID and resolved. The inspections must
not be superseded, and validation Evidence must meet its success conditions.

A boundary inspection is human or agent. A human boundary inspection is a
Discuss covering product-facing results: user-observable behaviour, interaction,
or delivered content, including docs that are part of the product. A workflow
the user runs to confirm it still behaves as expected qualifies only when the
ticket changes how that workflow runs and the ask names the scenario and the
expected observation. Code, contracts, and tests are not product-facing because
a workflow later uses them. An agent boundary inspection, the Agent Task defined
in `TICKET-CONTRACTS.md`, covers everything else: code, tests, configuration,
and docs outside the product, such as contributor docs, canonical specs, change
plans, and agent-facing files. Never ask the user to review or accept those
unless the user asked to; record that request, with the results it covers, as a
working hint.

Name a ticket on the human inspection when its result has product-facing parts,
on the agent inspection when it has other parts, and on both when it has both.
Each inspection's Objective names the parts it covers for each ID, so every
part has exactly one current inspection. Choose from the ticket's Objective and
changed surfaces, and correct the assignment before an inspection starts when
Evidence shows otherwise.

When an implementation ticket completes, attach it to the open non-active
boundary inspections it needs and the boundary validation for a coherent
inspection batch, or create them immediately. A batch has one boundary
validation covering every ID in its inspections. One user amendment set is one
batch by default: record covered IDs in each ticket's Objective and keep them
blocked on their known active or ready implementation tickets. Present one
grouped human inspection after the batch returns. Split only when results
cannot be inspected coherently or delay would stall the run; never split merely
because the batch has several tickets, modules, or check sets, and do not wait
for unknown future work.

Run boundary inspections and boundary validation in parallel; none depends on
another. A grouped human ask maps results to covered IDs, says what each result
now does for the user, reports each check a subagent already ran as a recorded
outcome with its source ticket, and asks for one reply accepting all or naming
IDs needing changes; use the same Discuss for acceptance. Take those outcomes
from covered implementation Evidence, and from validation Evidence once it
returns. Never wait for validation or re-run a check in the orchestrator thread
to build the ask.

Immediately before presenting a human boundary inspection, rebuild its ask from
the current covered-ticket record and establish its inspection freeze in
Presentation. The freeze includes changed paths from every covered
implementation, shared dependents that can change the inspected result, and
every prepared environment that could restart, rebuild, or reload. Until the
inspection returns or is withdrawn, do not patch or ready a ticket that would
change that scope. Findings outside it may become ready immediately. An agent
boundary inspection gets the same stability from assignment conflict checks.

If boundary validation finds issues, record them and let the orchestrator
decide which become tickets. If an issue invalidates an upcoming human inspection,
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

An agent boundary inspection records `accepted`, `changes needed`, or
`decision needed` for each covered ID. Resolve it only when every ID is
`accepted`; that resolution is the orchestrator's acceptance. Otherwise create
the fix tickets its findings support and a Discuss for each `decision needed`,
block it on them, add fix IDs to its covered IDs, and after they return reassign
it with Reads naming the fixes and decisions. The reassignment judges each ID
against its current result including linked fixes, and rechecks an accepted ID
only when remediation touches its result or shared dependencies. When an issue
invalidates an agent inspection that has not started, block it on the fixes;
when it is active or has returned, let it return, record in `LOG.md` that its
verdicts apply to the superseded result, then handle it the same way.

If invalidation arrives after inspection was answered or resolved, mark that
inspection and any acceptance evidence superseded, move any affected goal out
of `achieved` to `active` or `blocked` as the remaining work requires, and
create a new boundary inspection after fixes. A reply or acceptance for an
invalidated result never verifies the fixed result.

### Change plans

Follow this section only while `WORKINGHINTS.md` records confirmed planning
depth as `reviewed planning`. Otherwise take none of its create, ready,
assignment, or dispatch actions.

Reconcile a Plan return by result:

- `completed`: create the round's Plan Review tickets, replace `reviews` and
  `depends_on` with their IDs, and set the Plan `blocked`;
- `blocked` on a choice or required investigation: block it on the Discuss,
  Research, or Explore Options ticket that settles it; create no review;
- first `failed`: reassign it; second `failed`: block it on Discuss asking
  whether to keep the change set.

Never leave a Plan `ready` during review. On acceptance, set it `resolved`;
that status is the acceptance record. Each round uses new Plan Review IDs so
Findings survive. Resolve a review only after `execution_result: completed`;
otherwise reassign or block it. Cancel it only if superseded before return.
Record earlier rounds in `LOG.md`.

Accept only after every finding is applied or declined with a reason and the
plan has no live Open decision. Use Discuss first when an Open decision, a
finding from either lens, a declined finding, or an Approach commitment meets
the product-decision test; treat the last as a plan fault. Discuss may overlap
reviews, but acceptance waits. Write the settled choice through a reassigned
Plan ticket, then review that change. Record acceptance, reclassifications, and
declined findings in `LOG.md` and the plan banner.
If the user asks to see plans, record that working hint and give the path in
that pass's progress update; the plan is reading material, not an ask.

Review only revised parts unless the revision is high-impact or cross-cutting.
Settle contradictory findings through Discuss when they require a product
decision. Cap each finding at two revision-and-review rounds against the same
plan part. After round two, use Discuss for an approach rejection or product
decision; apply or decline a process finding with a reason. Review the resulting
revision through both lenses only for faithful application, reopening the
finding only on new evidence.

Never cancel a change plan because of a review. A review that rejects the
approach itself is evidence of an unresolved unknown or an undecided choice:
create Research for an unknown or Discuss or Explore Options for a choice,
using the review's classification, and block the Plan on it. Reassignment
Objective names the remaining change set, accepted and declined finding IDs,
and any Discuss decision; Reads name the reviews and parts to re-review.

Cancel a Plan only when its change set leaves the run, citing a goal abandoned
through Discuss, a covering non-goal, or a retired module. Splitting revises the
original Plan to its remaining set and creates another Plan for the rest.

Only after acceptance, create governed implementation tickets from the plan;
each names its Plan ID in `plans` and puts the plan on Reads. Block any existing
unresolved ticket for the set on the Plan, then revise or cancel it from the
accepted plan; surviving tickets name the Plan. Never reopen a resolved
implementation ticket.

When later research, steering, or a returned ticket invalidates an accepted
change plan, let any active reviews return first, then record in `LOG.md` that
their findings apply to a superseded plan. Mark the plan superseded in its
banner and `LOG.md`, set its Plan ticket `ready` or `blocked` on the ticket that
settles the change, block governed tickets that have not started, and reconcile
active returns against the revision. Revise, re-review, and re-accept the plan
before implementation becomes `ready` again. Already implemented work follows
implementation coverage and boundary inspection. Non-invalidating returns
propose newly classified work.

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

A Plan Review is not an Adversarial Review. It does not satisfy a run module
boundary or pre-completion review, an Adversarial Review does not satisfy plan
review, and Adversarial Review is never used on a change plan. An Adversarial
Review of completed work may put the accepted change plan on Reads.

## Progress updates

For chat progress, a ticket is closed when its status becomes `resolved` or `cancelled`.

After a reconciliation pass closes one or more tickets, dispatch newly ready
work first, then send one short progress update for that pass. For `resolved`,
give the ticket ID and one sentence with the user-visible result. For
`cancelled`, give the ticket ID and concise user-relevant reason in `LOG.md`;
do not imply an execution result. A ticket cancelled before it was dispatched
or presented needs no progress line unless the user was told it was upcoming.
For a resolved Plan ticket, name the change set that now has a reviewed
approach and what it will produce, from the goals that plan cites. For a
resolved Plan Review, name the plan reviewed and whether it needs changes.
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

Compaction itself must not draw new conclusions, create new tickets, or change planned work.

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
12. tickets needed for current work;
13. change plans for any Plan or Plan Review ticket that is active, ready, or
    blocked, and any accepted change plan governing current implementation work.

Reload completed tickets only when their detailed results become relevant.
Planning depth is recovered from `WORKINGHINTS.md`.
Reapply its Plan and Plan Review gate before acting on recovered tickets.

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
- every resolved implementation ticket has implementation coverage from the
  resolved boundary inspections it needs and a resolved boundary validation
  ticket;
- under reviewed planning, every change plan whose change set is still in the
  run is `resolved` and accepted with every ID in its `reviews` resolved or
  cancelled, and every implementation ticket it governs names it in `plans`; a
  `cancelled` Plan ticket carries the record its cancellation cited;
- under reviewed planning, no work a ticket record classified as needing a
  change plan was implemented without one, unless `LOG.md` records the
  departure and its reason;
- required human tasks and acceptance are complete;
- significant adversarial findings are resolved or explicitly accepted by the user;
- open entries in `UNKNOWNS.md` required for achieved goals are closed;
- the run files reflect the final state.

An empty ticket queue does not mean the run is complete.

When the run is complete, set `run.complete` in the index template data if that
index exists, then
return to the user with a message that opens with the bold line
`**This orchestrated run is complete.**` and a concise summary under it. Use
only what is already in the run files:

- goals achieved;
- important decisions;
- verification results;
- abandoned goals;
- remaining optional follow-up work.
