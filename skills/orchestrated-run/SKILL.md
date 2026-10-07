---
name: orchestrated-run
description: >-
  Coordinate a substantial project run through one user-facing orchestrator,
  shared run files, and grouped tickets executed by personas on models the
  user confirms. Use only when explicitly invoked by the user.
disable-model-invocation: true
metadata:
  invocation: user-only
---

# Orchestrated run

This skill is user-invoked. Start it only when the user explicitly invokes `orchestrated-run`.

The skill defines the process. Run files define current state. Tickets define pieces of work and keep their detailed results. Personas execute tickets as subagent sessions. The orchestrator reconciles results and controls the run.

## Roles

The orchestrator owns run state, the roster, ticket creation and assignment,
user interaction, steering, reconciliation, next work, and goal verification.
Personas execute and own active agent tickets. Each persona serves one ticket
type, runs on the model the roster gives it, and has at most one active ticket.
The orchestrator owns `Discuss/Gather Inputs`, `Human Task`, and `Human and
Agent Task`. Discovery, planning, implementation, issue resolution, validation,
and human acceptance all happen as tickets.

Work moves in large tickets of several work units. A persona checkpoints each
unit and continues with the next while other personas review the one it just
finished. Their findings reach it through its ticket inbox, and it decides
where in its remaining work to place each fix.

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
  presenting, executing, or recovering a ticket. Read the schema, work units,
  ticket inbox, shared rules, and exact type contract that apply.
- Read [PERSONAS.md](PERSONAS.md) before building or changing the roster,
  choosing a persona, or starting or resuming a persona session.
- Read [RUN-STATE.md](RUN-STATE.md) before creating or updating run files and
  after compaction.
- Read [HUMAN-ASKS.md](HUMAN-ASKS.md) and use its templates before every
  human-ticket presentation state change and after compaction with a presented ticket.

These are required contract references, not skills. If one cannot be read,
report the blocker rather than proceeding from memory. Never put them on a
subagent's Reads; copy its persona brief from `PERSONAS.md` and its shared
rules and type prompt from `TICKET-CONTRACTS.md`.

## Run files

Conversation context is temporary. Recover from this skill, run files, tickets,
ticket inboxes, change plans, and project files.

Create a new run at:

`<project>/.agent-runs/orchestrated-run/<timestamp>-<short-name>/`

Create title-only Markdown placeholders and empty `tickets/`, `inbox/`, and
`asks/`:

```text
GOALS.md
NONGOALS.md
UNKNOWNS.md
WORKINGHINTS.md
LOG.md
PILLARS.md
MODULES.md
ROSTER.md
tickets/
inbox/
asks/
```

Create `plans/` only when planning depth is recorded as reviewed planning.
Ask pages are orchestrator-owned presentation artifacts derived from human
tickets; they are never a source of truth. Resume a run when the user or
invocation identifies it. Otherwise create a new run.

When creating `<project>/.agent-runs/`, add `.agent-runs/` to the project `.gitignore` if that line is missing. Create `.gitignore` if the project has none. That is setup, not an Agent Task.

Use stable IDs: goals `G-001`, non-goals `NG-001`, unknowns `U-001`, pillars `P-001`, modules `M-001`, tickets such as `T-001-RES`, work units such as `T-004-AGT/W1`, and inbox items such as `T-004-AGT/I-001`. IDs remain stable for the lifetime of the run and are not reused.

The orchestrator owns run files, `inbox/`, and `asks/`. A persona session
exclusively owns its active ticket and a Plan worker also owns its change plan;
the orchestrator owns an active `Human and Agent Task`. See `RUN-STATE.md` for
change-plan ownership.

## Start the run

1. Create the placeholder files. Apply the `.agent-runs/` gitignore rule above.
2. Build the recommended roster under Suggesting models in `PERSONAS.md`.
3. Create one bootstrap Research ticket with one unit per separable area. Use
   two tickets, one for the `scout` and one for the `investigator`, only when
   some areas need deep research and others only surface. Put likely project
   paths on Reads; never research in the orchestrator thread. A scout unit
   that cannot meet its Completion requests deep, and the gap becomes an
   investigator unit. Bootstrap also seeks the end user and canonical docs or
   spec when cheap to establish.
4. Dispatch bootstrap on the model and effort its persona's recommended row
   resolves to, and record that row in `ROSTER.md` as provisional. Then create and present the roster ask
   under `PERSONAS.md`, unless the client cannot choose models per subagent or
   the invocation already settled every persona. Every session started after
   the answer uses the confirmed roster.
5. When bootstrap is two tickets, wait for both before activating goals or
   creating any other ticket; Discuss needed for discovery may start sooner.
   Reconcile them together under `RUN-STATE.md`, subject to step 6.
6. Until planning depth is recorded, create only Discuss and Research tickets
   from bootstrap follow-ups. Do not create any other ticket type from them,
   even as `proposed`; those drafts stay on the proposing ticket.

Keep work that implements or depends on unconfirmed product decisions off
active tickets until the relevant Discuss tickets resolve. A ticket whose
units all depend on them is `blocked` with `depends_on` those tickets; when only
some units do, leave those units out and add them through the inbox once the
decision lands.

**If the invocation contains a request.** Create one Research ticket with one
unit per separable area of the request. Understand the
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

The orchestrator owns all process decisions, including next work, grouping,
persona choice, assignment, result acceptance, verification, review, and
completion. The roster, including roster-change asks when a row cannot be
resolved, and planning depth are the only process decisions this skill puts to
the user; other process decisions are not user tickets.

## Tickets
Read [TICKET-CONTRACTS.md](TICKET-CONTRACTS.md) before creating a ticket.
That reference owns ticket IDs, schema, ownership, readiness, and type
contracts. Every new ticket follows it.

## Grouping

Cost grows with the number of sessions started and with what each one must
read. Group work so each persona takes few, large tickets.

- A unit is one coherent change or one research question with its own
  Completion, the size a ticket used to be.
- Put every ready unit for one persona that shares Reads or run modules on one
  ticket, in dependency order. A coder may take five modules on one ticket.
- Split a ticket only when its units share no Reads, when an early unit
  awaits a decision that later units depend on, when it would need several
  personas, or when it would pass about seven units. Queue the rest as that
  persona's next ticket.
- When a persona already has an active ticket, add fitting new units, fixes,
  and steering changes to it through its inbox instead of creating a ticket.
  Otherwise create a `ready` ticket that waits for that persona.
- Accept that same-persona work runs one ticket at a time. That trades
  elapsed time for cost.
- Batch human asks the same way: one grouped inspection per completed ticket
  or set of tickets, and related decisions in one Discuss.

Choose the persona under Choosing a persona in `PERSONAS.md`. Prefer the
cheapest persona the recorded classification allows, and escalate a unit when
its worker records that it needs more.

## Assignment

Every `ready` agent ticket is assigned to its persona's session before any work
on it starts. That is the only way agent tickets get done. A persona has at most
one active ticket; its other ready tickets wait.

Do not give the subagent this skill. A new session gets:

1. the persona brief from `PERSONAS.md`;
2. the shared agent rules and exact assignment prompt copied from
   `TICKET-CONTRACTS.md`;
3. the absolute paths of the ticket, its inbox, and `scripts/snapshot.py`;
4. the `## Reads` list of paths.

A resumed session gets only what `TICKET-CONTRACTS.md` says to send on resume.

Do not build a large custom context summary. Point at files, naming the exact ID
or heading when only part of a run file applies. Reads may include applicable
working hints, goals, unknowns, pillar or module entries, earlier tickets,
project paths, and documentation. Include every governing entry, but omit run
files that have nothing for the ticket. Repo-wide Reads are for Research, not
Agent Task. Do not dump a repo survey into the ticket.

When assigning a ticket:

1. confirm dependencies using ticket metadata and owned run files;
2. check every unit for file, state, and decision conflicts with active
   tickets, including parked sessions' remaining units, and with every other
   ticket in the same dispatch wave; a conflicting wave member stays `ready`
   and queued;
3. fill `## Reads` and `## Work units`;
4. create its inbox file with a title only;
5. set `status: active` and `owner` to the persona;
6. resume the persona's idle session, or start a new one on the model and
   effort its roster row resolves to under Resolving a row in `PERSONAS.md`,
   and record the session and its state in `ROSTER.md`. When the row's
   fallback is `ask` and nothing resolves, keep the ticket `ready` and present
   the roster-change ask.

Run every persona session in the background when the client allows it, so each
return wakes the orchestrator, including while a human ask is presented.
Waiting in the foreground on one session stops the others being resumed, and
review no longer overlaps implementation. When the client has no background
subagents, say so in the roster ask.

Send a unit through an inbox only after it passes the same dependency,
conflict, Exclusive scope, and planning-depth checks as a unit on a new ticket.

Different personas may run in parallel. A wave of ready tickets for different
personas may be dependency-checked, conflict-checked, filled, and dispatched in
one pass. Do not dispatch `proposed` or `blocked` tickets. Handle Discuss,
Human Task, and Human and Agent Task in the orchestrator thread.

Outside a selected or active Human and Agent Task, wait for sessions to return.
That wait is not a user prompt. When one returns, reconcile every return
already received at that point; do not wait for more solely to enlarge the
batch. Do not wait for the user to continue the run.

Selecting a ready Human and Agent Task creates an exclusive-scope barrier. Do
not select or start it while another human ticket has
`presentation: presented`; get that response before starting it. Record
selection and Exclusive scope in `LOG.md`.

An agent ticket is safe to run concurrently only when its Objective and
Completion explicitly prohibit changes to project files, external state, and
prepared human environments; its Reads are disjoint from Exclusive scope; and
it shares no unresolved decision with the unfinished interaction. Wait for
every running session on a ticket that does not meet this test to reach a
checkpoint or return before starting the Human and Agent Task, and leave it
parked. While it is active, dispatch, resume, or leave running only sessions
on tickets that meet the same test, and do not present another human ticket.
When independence is uncertain, allow no concurrent agent ticket.

Before expanding Exclusive scope, wait for running sessions that would fail the
expanded test to reach a checkpoint. Check Findings and Evidence from every
ticket that ran concurrently for invalidation of recorded Interaction log
evidence, and record the result in `LOG.md`.

Apart from progress updates, return to the user only when a human ticket needs
a response, or when the run is complete. If sessions are also active, still
reconcile them when they return.

## Checkpoints

A return with a new checkpoint and `execution_result: null` is a checkpoint
return; the ticket stays `active` and its session is `parked`. Handle it in
this order:

1. Record the session `parked` in `ROSTER.md`. Read the new checkpoint, new
   inbox responses, and what the worker recorded for that unit; do not open the
   changed files. Check that every inbox item sent before the worker's last
   read has a response; resend any that does not as a new item that supersedes
   it. A `done` implementation checkpoint in a git worktree without a snapshot
   is incomplete: resume the session asking for the snapshot before routing
   review.
2. Append any inbox items already due, then resume the session at once unless
   its next unit needs a decision the checkpoint asked for, would change
   paths under a presented inspection freeze or a Human and Agent Task's
   Exclusive scope, or would change paths a running boundary validation is
   checking. Record the session `running` in `ROSTER.md`. Continuing is the
   default; never hold a session to batch work. A streaming ticket's session
   with an empty queue stays parked until an added unit or `closing` is sent;
   resume it then.
3. Add a `LOG.md` entry for the checkpoint and update run files where wider
   state changed.
4. Route review work. For a `done` implementation unit or placed fix, add an
   inspection unit covering it to the `inspector`'s active ticket through its
   inbox, or create that inspection ticket. For an inspection or review
   checkpoint, route its findings as below. Treat a Research or Explore
   Options checkpoint's follow-ups like those of a returned ticket.
5. For a `blocked` unit, create the Discuss, Research, or Explore Options
   ticket that settles it, or move the unit to a ticket for the persona its
   worker named. Send the result through the inbox as a decision or added unit
   when it lands.

Route findings to the persona that owns the work. When a review finds changes
needed in a unit whose ticket is still active, decide which findings become
work, then send each as a fix request through that ticket's inbox. Mark it
`blocking` when later units build on what it changes; otherwise leave placement
to the worker. When the ticket has ended, add the fix as a unit with its own
Reads to the same persona's active ticket, or create a ticket for that persona
when it has none. A finding that meets the product-decision test goes to
Discuss first; send a `hold` naming the paths or choices to leave alone until
the decision arrives.

Every fix a worker places reaches a checkpoint. Re-inspect it by adding an
inspection unit whose `Covers` line names the original unit and the fix. When
two re-inspections of one ID still find changes needed, move the remaining fix
to the `senior-engineer` unless it is already there. After a third, open a
Discuss on whether to keep, change, or drop that result.

A return with no new checkpoint and `execution_result: null` is malformed.
Resume the session once asking it to record its checkpoint; if the next return
is malformed too, treat the ticket as `failed`.

When the client cannot resume a returned session, start a new session for the
same ticket instead; it continues from the recorded checkpoints. Each module
then pays a fresh start, so say so in the roster ask.

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
presentation, follow the liveness, page, ledger, launch, ticket-state, complete
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

Change requests and feedback become work now. Send them as added units or fix
requests to the matching persona's active ticket when they fit under
Grouping; otherwise create tickets. Assign ready tickets unless they conflict
with active work or a selected or active Human and Agent Task's Exclusive
scope. Never edit an active ticket file; use its inbox. When steering
invalidates work in progress, send a `hold` or `stop`. Block or delay
conflicting assignment until the conflicting session reaches a checkpoint.
Record the steering, inbox items, and tickets created in `LOG.md`.

If the prompt responds to a presented Discuss or Human Task, treat it as that
ticket's return. A response to a withdrawn ask is steering or new evidence,
not ticket completion. If it answers the current presented ask on an active
Human and Agent Task, follow the presented-to-upcoming transition under Human
involvement and treat it as the next interaction, not a ticket return. If the
user stops or replaces the interactive task, end and reconcile it before
proceeding. Then continue the run.

## Reconciliation
A checkpoint return follows Checkpoints. When an agent ticket returns with
`execution_result` set, a Discuss or Human Task returns, or a Human and Agent
Task ends:

1. Read `execution_result`, the checkpoints and inbox responses not yet
   reconciled, and the worker's Unknowns, Findings, and Blockers / follow-ups.
   Leave worker-maintained sections as the worker wrote them. Units added
   through the inbox count as the ticket's units; do not copy them into Work
   units. Handle each checkpoint not yet reconciled under Checkpoints steps 3
   to 5, so the last unit is routed to review like the others. Route every
   inbox item without a response as new work under Grouping.
2. Clear `owner`, and mark the session `idle` or `closed` in `ROSTER.md`.
3. Decide the persistent ticket `status`. `completed` is not automatically `resolved`. After return, set `ready` (reassign the same ticket), `blocked`, `resolved`, or `cancelled`. Keeping it for further work means `ready` and `owner` cleared. When reassigning a blocked ticket, state what its checkpoints already cover so the next worker does not repeat it.
4. Reconcile the result into the run: add a concise `LOG.md` entry; use ticket YAML IDs to limit which existing run entries need refresh, but always inspect worker Unknowns, Findings, and Blockers / follow-ups for new wider-run entries; update run files only where wider state changed; decide next work from follow-ups as proposals; decide whether related verification or review is still required.

Reconcile every ticket already returned at the start of the pass. Decide each
ticket's state, then write each affected run file once. Do not wait for more
returns solely to enlarge the batch. Complete persistent writes, recompute
readiness, and dispatch newly ready non-conflicting work before sending routine
progress.

Do not copy the investigation into the log or re-do the ticket in the
orchestrator thread. If evidence is missing or the result is unacceptable,
create or reassign tickets.

Every implementation unit or placed fix with a `done` checkpoint, and every
Human and Agent Task that performed implementation, needs implementation
coverage before its module or the run completes: for each part of its result,
a current `accepted` verdict from an agent boundary inspection or a resolved
human boundary inspection, and a resolved boundary validation ticket covering
its ticket. The inspections must not be superseded, and validation Evidence
must meet its success conditions. Below, a covered ID is such a unit, fix, or
Human and Agent Task.

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

Name a covered ID on the human inspection when its result has product-facing
parts, on the agent inspection when it has other parts, and on both when it has
both. Each inspection unit's Objective names the parts it covers for each ID,
so every part has exactly one current inspection. Choose from the unit's
Objective and changed paths, and correct the assignment before an inspection
starts when Evidence shows otherwise.

Agent boundary inspection streams. Each `done` checkpoint gets an inspection
unit under Checkpoints while its implementer continues, and its findings reach
the implementer as fix requests.

Human boundary inspection and boundary validation wait for the batch. A batch
is one implementation ticket by default, or several that complete together
for one user amendment set. When the first ticket of a batch becomes active,
create its human inspection, when it has product-facing parts, and its
boundary validation, record covered tickets in their Objectives, and keep
them blocked on those tickets. Present one grouped human inspection after the
batch ends. Split only when results cannot be inspected coherently or delay
would stall the run; never split merely because the batch has several units,
modules, or check sets, and do not wait for unknown future work.

Boundary validation checks a stable tree. Dispatch it when no running session
has uncheckpointed changes on the paths its checks exercise. When repo-wide
checks would hold another persona for long, name a snapshot and a temporary
worktree in its unit's Objective instead. Validation Evidence records the tree
it checked. It is stale when a later `done` checkpoint changes a path its
checks cover; stale validation gives no coverage until a new validation unit
checks the later tree.

Run the human inspection and boundary validation in parallel; neither depends
on the other. A grouped human ask maps results to covered IDs, says what each
result now does for the user, reports each check a subagent already ran as a
recorded outcome with its source ticket, and asks for one reply accepting all
or naming IDs needing changes; use the same Discuss for acceptance. Take those
outcomes from covered checkpoints and Evidence, and from validation Evidence
once it returns. Never wait for validation or re-run a check in the
orchestrator thread to build the ask.

Immediately before presenting a human boundary inspection, rebuild its ask from
the current covered-ticket record and establish its inspection freeze in
Presentation. The freeze includes changed paths from every covered
implementation, shared dependents that can change the inspected result, and
every prepared environment that could restart, rebuild, or reload. Until the
inspection returns or is withdrawn, do not resume a session onto, send a fix
request for, or ready work that would change that scope. Findings outside it
may become work immediately. An agent boundary inspection gets the same
stability from checkpoint snapshots.

If boundary validation finds issues, record them and decide which become fix
work, routed under Checkpoints. If an issue invalidates an upcoming human
inspection, keep it blocked, add the tickets or inbox items carrying the chosen
fixes to `depends_on`, and do not present it before fixes and a new boundary
validation start. If an issue
invalidates a presented inspection, first set the inspection ticket
`status: blocked`, clear owner, set presentation to `withdrawn` on the ticket
and its ledger record, mark its page withdrawn, record the reason and times in Presentation
and `LOG.md`, and tell the user the ask is withdrawn. Then route the chosen
fixes and add the tickets or inbox items carrying them to `depends_on`. After
the fixes reach `done` checkpoints for an upcoming or withdrawn inspection,
create or ready a new boundary validation ticket, set the existing inspection
`ready` with presentation `upcoming`, and present a new complete ask under the
normal parallel rule.

An agent boundary inspection records `accepted`, `changes needed`, or
`decision needed` for each covered ID in each unit's checkpoint. An ID's latest
non-superseded verdict is the current one; an `accepted` current verdict is
the orchestrator's acceptance of those parts. For `changes needed`, route the
fixes its findings support under Checkpoints; for `decision needed`, open a
Discuss and route its decision. When the fix reaches a `done` checkpoint, add
a re-inspection unit naming the original ID and the fix. It judges the current
result they form together, and rechecks an accepted ID only when remediation
touches its result or shared dependencies. When an issue invalidates a verdict,
record in `LOG.md` that it applies to the superseded result and add a
re-inspection unit after the fixes. Resolve an inspection ticket when every
unit has a verdict and every finding is routed.

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
each names its Plan ID in `plans` and puts the plan on Reads. A governed unit
added to an existing ticket names it on its `Plans` line and its Reads. Block any existing
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

The orchestrator must not be the reviewer. Default to one Adversarial Review
unit at each module boundary, batching several small related modules when
useful, and one before completing the run. A module boundary is reached when
the implementation work for that module has ended. Add each boundary's unit to
the `reviewer`'s active Adversarial Review ticket through its inbox, so review
of one module runs while later modules are built. Name the covered work's
latest snapshots on each unit's Reads. That ticket is a streaming
ticket; send `closing` when no further module boundary is expected before the
pre-completion review. Use the
`principal-reviewer` for the pre-completion review and for earlier review
after high-impact or cross-cutting changes, unexpected test or debugging
results, or uncertain evidence. After remediation, review the changed surface;
repeat a full review only when the remediation is itself high-impact or
cross-cutting. Do not run overlapping reviews of the same completed work. A
pre-completion review may also satisfy the last module boundary when its Reads
cover both scopes. A worker recommendation to review is a proposal. Route
review findings under Checkpoints.

A Plan Review is not an Adversarial Review. It does not satisfy a run module
boundary or pre-completion review, an Adversarial Review does not satisfy plan
review, and Adversarial Review is never used on a change plan. An Adversarial
Review of completed work may put the accepted change plan on Reads.

## Progress updates

For chat progress, a ticket is closed when its status becomes `resolved` or `cancelled`.

After a reconciliation pass closes one or more tickets, resume and dispatch
work first, then send one short progress update for that pass. Checkpoints get
no progress line of their own; a resolved ticket's line may name how many units
it finished. For `resolved`,
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

1. all returns and checkpoints received have been reconciled;
2. run files, `ROSTER.md`, and inboxes already reflect any wider-run changes
   and messages from them;
3. an active Human and Agent Task has recorded its current work, evidence and next ask on its ticket.

Detailed ticket results stay in their ticket files. Copy into run-level files only what affects the wider state of the run.

Compaction itself must not draw new conclusions, create new tickets, or change planned work.

After compaction, rebuild context from:

1. this skill;
2. `TICKET-CONTRACTS.md`;
3. `RUN-STATE.md`;
4. `PERSONAS.md`;
5. `HUMAN-ASKS.md` when any human ticket is presented;
6. `ROSTER.md`;
7. `GOALS.md`;
8. `NONGOALS.md`;
9. `UNKNOWNS.md`;
10. `WORKINGHINTS.md`;
11. `PILLARS.md`;
12. `MODULES.md`;
13. relevant entries from `LOG.md`;
14. tickets needed for current work, with the inbox of each active one;
15. change plans for any Plan or Plan Review ticket that is active, ready, or
    blocked, and any accepted change plan governing current implementation work.

Reload completed tickets only when their detailed results become relevant.
The roster and persona sessions are recovered from `ROSTER.md`; a session
recorded `running` is still running until its return arrives. For each active
ticket, compare its Checkpoints with `LOG.md`: reconcile any checkpoint the log
lacks under Checkpoints, then resume a `parked` session. When a session
recorded `running` has a newer checkpoint than the log, or the client shows it
ended, treat it as parked.
Planning depth is recovered from `WORKINGHINTS.md`.
Reapply its Plan and Plan Review gate before acting on recovered tickets.

Before acting on any active, ready, or presented ticket, read its schema and
exact type contract in `TICKET-CONTRACTS.md`.

Reload every presented human ticket from Objective or its latest Interaction
log entry and Presentation. Read `HUMAN-ASKS.md`, then rebuild missing or stale
ask pages and the run's ledger file from those tickets and the bundled template before
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
- every covered ID under Reconciliation has implementation coverage: a
  current `accepted` agent verdict or resolved human inspection for each part
  of its result, and a resolved boundary validation ticket;
- no ticket is active and no persona session is `running` or `parked`;
- under reviewed planning, every change plan whose change set is still in the
  run is `resolved` and accepted with every ID in its `reviews` resolved or
  cancelled, and every implementation ticket or unit it governs names it in
  `plans` or its `Plans` line; a
  `cancelled` Plan ticket carries the record its cancellation cited;
- under reviewed planning, no work a ticket record classified as needing a
  change plan was implemented without one, unless `LOG.md` records the
  departure and its reason;
- required human tasks and acceptance are complete;
- significant adversarial findings are resolved or explicitly accepted by the user;
- open entries in `UNKNOWNS.md` required for achieved goals are closed;
- the run files reflect the final state.

An empty ticket queue does not mean the run is complete.

When the run is complete, delete its ledger file under `HUMAN-ASKS.md` if it
exists, then return to the user with a message that opens with the bold line
`**This orchestrated run is complete.**` and a concise summary under it. Use
only what is already in the run files:

- goals achieved;
- important decisions;
- verification results;
- abandoned goals;
- remaining optional follow-up work.
