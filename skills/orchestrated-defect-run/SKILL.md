---
name: orchestrated-defect-run
description: Resolve a defect list through orchestrated triage, implementation, automated product checks, and user review. Use only when explicitly invoked by the user.
disable-model-invocation: true
argument-hint: "<defect-list-path>"
---

# Orchestrated defect run

This skill is user-invoked. Start it only when the user explicitly invokes
`orchestrated-defect-run`. A request to start it from an active
`defect-capture`, including one started from the `ux-ui-reviewer` handoff, is
an explicit invocation.

It requires `/orchestrated-run` and the defect-ticket contract bundled with
`defect-capture`. Start one orchestrated run and apply this skill as its
defect-specific process. The orchestrated-run skill and its required references
remain authoritative for ticket types, ticket status, assignment, ownership,
planning depth, reconciliation, implementation coverage, review, human asks,
and run completion, except for the confirmed-outcome specialization named
below.

Read
[DEFECT-TICKETS.md](../defect-capture/DEFECT-TICKETS.md) before changing a
defect ticket. It owns the separate defect schema and lifecycle. If this file
or an orchestrated-run required reference cannot be read, report the blocker
rather than proceeding from memory.

## Start

Resolve the defect-list path from the invocation or the active capture
session. If neither identifies one and several lists exist, use
Discuss/Gather Inputs to ask which list to run.

Inspect `orchestrated_run` on the list's defect tickets. If it points to one
incomplete run, resume that run. If different incomplete runs claim the list
or its defects, report the conflict and do not start another. Otherwise start
a new `/orchestrated-run` whose request is to implement each ready defect's
confirmed outcome. Treat those outcomes, including confirmed amendment
outcomes, as part of the user's invocation. Use Research when no outcome is
confirmed. Consider a non-fix disposition only when later evidence shows
implementation is inappropriate. Do not copy the defect files into the
orchestrated-run folder.

Put the source list path, this skill-file path, and the
`DEFECT-TICKETS.md` path in `WORKINGHINTS.md` as required recovery references.
The hint states that a recovering orchestrator must read both referenced
contract files before acting after compaction.
When a ready defect enters the run, set its `orchestrated_run` to the relative
run path and record that link in History.

Record these user-confirmed working hints:

- defect status is a projection onto source defect tickets, not an
  orchestrated-run ticket status;
- confirmed outcomes under `DEFECT-TICKETS.md`, including confirmed Additional
  context, must not be put back to the user as decisions;
- only an active implementation Agent Task moves a defect to `in progress`;
- a dedicated automated product check must run against the actual product or
  prepared artifact before the defect is presented for user review;
- the product check does not replace boundary validation, Adversarial Review,
  Plan Review, or any other orchestrated-run requirement;
- when a product scenario cannot be created with safe test data, the check may
  return `inconclusive` and pass the gap to user review;
- capture may add defects to the list while the run is active, and dispatch
  acknowledgement is permitted defect-capture process work.

This run sequences human inspection more strictly than orchestrated-run's
default parallel presentation. For defect-run human boundary inspections, this
working hint overrides only the base sentences that boundary inspection and
boundary validation run in parallel and that presentation never waits for
validation. When implementation completes, create or attach its coverage
tickets under orchestrated-run's Reconciliation rules and dispatch boundary
validation, but keep the human inspection upcoming until the dedicated product
check and that boundary validation return. Build the ask only from recorded evidence. This is
presentation scheduling, not a substitute for either ticket.

## Bootstrap and goals

The bootstrap Research ticket reads the defect list and enough of the project
to:

- inventory defects with `capture_state: ready`;
- treat `backlog` and `failed review` as triage-eligible only when
  `capture_owner: null` and the current cycle has no unresolved triage Research;
- propose one goal per defect that faithfully carries its confirmed outcome;
  when no outcome is confirmed, propose Research to establish it before
  deciding implementation or disposition;
- identify obvious duplicate or related groups without committing them;
- propose useful pillars or modules based on product areas or likely shared
  causes;
- identify the end user, canonical docs or specification, likely project
  paths, and useful verification surfaces;
- draft the per-defect triage Research tickets.

Do not treat drafting or failed captures as run goals. If a ready defect is
already `done`, include it only when evidence indicates its resolution has
been invalidated.

After bootstrap reconciliation, activate goals that match the user's request
to handle the list. A goal that faithfully restates a confirmed minimum outcome
matches that request, is complete enough to activate, and does not become an
unknown merely because implementation detail is absent. Apply the normal
planning-depth gate before creating implementation work. Triage Research may
proceed while a planning-depth ask is unresolved because it does not implement.

## Defect context in human asks

Every Discuss, Human Task, or Human and Agent Task ask whose decision, action,
or review is scoped to a source defect starts its defect-specific content with
the defect ID and Report / Summary under the label `Original report`. Put both
in the human ticket's Objective, or in the latest Interaction log entry for
Human and Agent Task, so chat and the ask page derive them from the normal ask
source.

Use Summary as written: it is the capture writer's lightly rewritten original
prompt, not a diagnosis or current result. Do not substitute the title, Triage,
or a later implementation summary. In a grouped ask, repeat the ID and Summary
inside each defect's result. If an older defect has no usable Summary, lightly
rewrite Captured context for that ask without changing the source Report.

## Assignment extensions

For every agent ticket, copy the shared agent rules and exact type prompt from
orchestrated-run's `TICKET-CONTRACTS.md`. Then add the applicable extension
below. Also copy the Confirmed-outcome assignment extension from
`DEFECT-TICKETS.md` into every agent ticket in this run, including bootstrap,
Plan, Plan Review, boundary validation, Adversarial Review, and tickets created
through steering. These extensions specialize the product-decision test for
confirmed defect outcomes. They do not relax ticket types, ownership,
implementation coverage, or the ban on subagents editing source defect
tickets.

### Defect triage Research

Create one Research ticket per eligible defect. Related defects may be
dispatched in parallel when their work is read-only. Its Reads include:

- the source defect ticket;
- every other ready defect ticket in the list for duplicate and relationship
  comparison;
- prior triage, implementation, product-check, validation, inspection, and
  review tickets for the current defect when they exist;
- likely project paths from bootstrap;
- applicable goals, unknowns, and working hints.

The Objective and Completion say Research depth `surface` with deep escalation
pre-authorised when meeting Completion requires codebase hunting. Never use
Research depth `triage` for this work. Before dispatch, record the new Research
ticket under Orchestrated-run links for the defect's current cycle. Prepare all
such source updates before activating a parallel dispatch wave.

Add this assignment extension:

```text
This Research ticket triages one source defect for an orchestrated defect run.
Do not edit the source defect ticket.

Establish what is observed, what remains unknown, likely reproduction and
affected paths, the likely cause boundary, and the evidence for any duplicate
or related defects. Search the whole supplied defect list for duplicate or
highly related reports. Distinguish the same symptom from the same likely root
cause.

Apply the Confirmed-outcome run rules and assignment extension from
`DEFECT-TICKETS.md`. Resolve implementation details from project evidence
before proposing a human decision.

Return a concise defect-ticket update proposal for the orchestrator, including
Triage content, duplicate_of, canonical duplicates, symmetric related_defects,
and evidence pointers. Draft and classify the next implementation work under
the normal Research contract. When review previously failed, explain what the
new evidence changes and do not repeat investigation already supported by
prior tickets.
```

On reconciliation, the orchestrator writes the supported proposal into the
source defect's Triage, relationship metadata, Orchestrated-run links, and
History. It updates both sides of a supported relationship. The source moves
to `triaged` when the triage Completion is met.

A supported duplicate records `duplicate_of` and the canonical inverse but
stays `triaged` until the canonical defect is done and its goal verification
explicitly covers the duplicate's reported scenario. For a fixed canonical
defect, its automated product check and user inspection both name every
duplicate ID and scenario they cover.

A supported `not-a-defect` or `cannot-reproduce` disposition may move directly
to `done` when evidence settles it without a product decision. Apply the normal
product-decision test case by case and use Discuss when reasonable alternatives
would produce meaningfully different outcomes. `wont-fix` requires Discuss
unless the user already made that product decision.

### Pre-implementation human decisions

Apply the Pre-implementation decision gate in `DEFECT-TICKETS.md` before every
discovery Discuss, goal-confirmation ask, Plan or Plan Review decision,
Explore Options outcome, implementation blocker, or Human and Agent Task
product-decision stop. This gate overrides only a base action that would re-ask
a confirmed outcome or treat UX involvement alone as a product decision.
Planning-depth asks, supported non-fix decisions, genuinely unresolved product
choices, and post-implementation inspection still follow orchestrated-run.

### Implementation

Implementation follows the run's confirmed planning depth. Keep the source
defect `triaged` during Plan, Plan Review, Research, and Explore Options.

An implementation Agent Task names every defect ID it covers. Add this
assignment extension:

```text
This implementation resolves the named source defects. Do not edit their
source defect tickets.

Implement from this ticket's Objective, Completion, and Reads. Map work and
local checks back to each covered defect ID in Evidence. Leave the actual
product or artifact in the prepared state named by Completion when a later
automated product check or user inspection requires it. When this ticket is
also preparation work, Completion requires the resource to remain available
after return and Evidence records its path or URL, persistent process or
session where relevant, expected state, and known expiry or restart procedure.
Do not claim the user-visible scenario passed unless this ticket actually
exercised it.
```

When the task becomes active, move each covered defect to `in progress`. When
several implementation tickets cover one defect, keep it there until all work
for the current cycle resolves. If no ready or active path can advance it, move
it to `blocked`, record `resume_status`, and point to the blocking run ticket.

After implementation reconciliation, summarize changed paths and local checks
under Resolution and link the implementation tickets. Do not mark the defect
done.

### Automated product check

After all current-cycle implementation for a defect or coherent group
resolves, create a dedicated Agent Task. Create it in addition to normal
implementation coverage and review tickets. Move covered defects to
`awaiting automated review` while the check or boundary validation is
queued, and to `automated reviewing` while either is active.

Its Objective and Completion name the actual product path, prepared artifact
or environment, original scenario, safe-data boundary, and expected observable
result. When a canonical defect has duplicates, they also name every covered
duplicate ID and its reported scenario. If no usable surface is established,
the ticket is still ready when Completion explicitly allows an `inconclusive`
result.

This is a check-producing Agent Task, like an Agent Task whose result is a
UX/UI review; it need not change project files. It is not an implementation
ticket, is not a covered implementation ID, and does not require its own
boundary inspection or boundary validation. Its Reads name the source
defects, covering implementation Evidence, prepared surface, and applicable
goals and working hints.

Add this assignment extension:

```text
This is the dedicated automated product check for the named defects. Do not
review only the code and do not fix findings.

Use the actual prepared product or artifact and exercise the user-visible
scenario in Objective. Create or change test data only when Objective expressly
allows it and the environment is safe. Otherwise do not mutate data merely to
force a result.

Record exactly one outcome for each covered defect:
- passed: the scenario ran and produced the expected observable result;
- failed: the scenario ran and showed that the result is absent or incorrect;
- inconclusive: the scenario could not be run safely or the prepared surface
  could not establish the result.

An inconclusive outcome meets this ticket's Completion when it records the
missing capability, attempts made, and the exact observation the user must
make, but only when Completion explicitly allows an inconclusive outcome,
including a scenario found unsafe at runtime. Otherwise set execution_result
to blocked. It is not a passed check.

When you complete the bounded check and record one of those outcomes, set
execution_result to completed even when the product-check outcome is failed or
inconclusive. Use blocked or failed execution_result only when the assignment
itself cannot produce an outcome under Completion. Keep product-check outcome
separate in Evidence.

If the prepared surface is also needed for user inspection, leave its named
inspectable state available after return. Record its path or URL, persistent
process or session where relevant, expected state, and known expiry or restart
procedure. If the check consumes the scenario, restore it only when Objective
allows that safely; otherwise record what durable evidence remains and what
separate preparation is needed.
```

On return, write the outcome and evidence pointer under Automated product
checks. A `failed` outcome or material boundary-validation issue marks each
affected defect `failed review`, but do not start the new triage cycle until
every in-flight product check and boundary validation for the current cycle
returns. If the defect is already marked failed for that cycle, append further
findings without incrementing its cycle or creating another triage ticket.

A boundary-validation issue that requires remediation but is not material does
not start a new cycle. Create the bounded fix ticket, project the defect to
`in progress` only when that implementation becomes active, and run the
automated gate again afterward.

`passed` or `inconclusive` may proceed after boundary validation returns
without an issue requiring remediation. Include every inconclusive gap in the
user inspection ask.

The dedicated product check does not satisfy an Adversarial Review. Schedule
Adversarial Review under the normal module and pre-completion rules. A later
material finding that invalidates a defect's result moves it to
`failed review`.

## User review

Once the product check is `passed` or `inconclusive` and boundary validation
has no issue requiring remediation, set the defect to
`awaiting user review`. Keep its boundary-inspection Discuss ticket
`presentation: upcoming` until that point.

A fixed defect's reported scenario is product-facing, so its implementation
always has a human boundary inspection for that scenario. The ask presents the
scenario and its observable result, never code or docs outside the product;
other parts of the implementation follow orchestrated-run's agent boundary
inspection rule.

Apply orchestrated-run's prepared-human-environment gate before the inspection
becomes ready. The implementation or automated product-check Agent Task may
serve as preparation only when its Objective and Completion, written before
dispatch, require the resource to remain available after return and its
Evidence records the path or URL, persistent process or session where
relevant, expected state, and known expiry or restart procedure. Otherwise
create a separate preparation Agent Task.

Present coherent defects as one grouped boundary inspection when the results
can be judged together. This inspection asks whether the implemented result is
acceptable, not whether the confirmed outcome should have been pursued. The
ask:

- opens each defect's result with its ID and Report / Summary as the original
  report;
- maps each result and recorded automated outcome to its defect ID;
- names each duplicate separately and asks the user to inspect its reported
  scenario even when one canonical implementation covers it;
- links the prepared product or artifact and explains how to inspect it;
- discloses every inconclusive automated scenario;
- asks the user to accept all results or name the defect IDs needing changes.

When the Discuss ticket becomes presented, set each covered defect to
`surfaced for user review`.

When an inspection is withdrawn because its prepared environment became
unusable, move each covered defect to `blocked` with
`resume_status: awaiting user review`. After preparation returns, recompute the
projection, clear `resume_status`, and return it to `awaiting user review`.
When validation or another finding invalidates the result, use `failed review`
and the failed-cycle rules instead.

User-requested changes move the named defects to `failed review`. For a grouped
reply that accepts some defects and rejects others, do not resolve the
inspection or give any covered implementation ticket inspection coverage.
Record the accepted IDs as evidence, move them back to
`awaiting user review`, remediate the rejected IDs, rebuild the grouped result,
and present one current non-superseded inspection again. Move fixed defects to
`done` with `resolution: fixed` only after that inspection resolves and their
implementation coverage and goal evidence satisfy orchestrated-run.
When a canonical defect reaches done, move each linked duplicate whose named
scenario was covered and accepted to `done` with `resolution: duplicate`.

If later evidence invalidates acceptance, supersede it under the base contract
and reopen the defect through `failed review`.

## Failed review cycle

Keep `failed review` as the visible source status. It is backlog-eligible but
does not erase the failed evidence.

For each failed defect:

1. record the finding or user response and its run-ticket pointer;
2. apply orchestrated-run's inspection-invalidation path: keep an upcoming
   inspection blocked on remediation, or withdraw a presented inspection;
3. wait for every in-flight product check and boundary validation for this
   cycle to return, appending their evidence to the same failure record;
4. when no unresolved triage Research already exists for the failed cycle,
   increment `cycle` once and create one new defect-triage Research ticket whose
   Reads include all failed evidence and the prior cycle;
5. record that ticket under Orchestrated-run links before dispatch;
6. add the new-cycle remediation tickets to the blocked inspection's
   dependencies and follow the base rules for new boundary validation and
   re-presentation after fixes;
7. move to `triaged` only after the new triage resolves.

Do not reopen a resolved implementation ticket.

## Reconciliation and steering

After every relevant return, update the orchestrated run first under its
contract, then update each affected source defect from that persistent
evidence. Append concise pointers rather than copying full ticket findings.

Before a source update, conflict-check `capture_owner` and every active agent
ticket whose Reads include that defect or its evidence. If a capture writer or
active reader owns the path, record the pending projection and evidence pointer
in `LOG.md`, leave the source unchanged, and apply it after the conflict
returns. This deferral changes only the source projection; reconcile the
orchestrated-run ticket immediately under the base contract.

Before dispatching a run ticket whose Reads include source defect files,
conflict-check every non-null `capture_owner`. Do not dispatch against a file
being captured or amended.

When capture adds a ready defect to this list during the run, treat it as
steering:

- open Research to understand it and propose its goal;
- compare it with all current defects and clusters;
- activate a matching goal without asking again when resolving new ready
  defects is already in the run request;
- conflict-check it against active implementation and human inspection
  freezes before dispatch.

When capture amends an existing defect past `backlog`, treat the amendment as
steering without incrementing `cycle`. Create defect-triage Research that names
the amendment and prior evidence. If it invalidates active implementation,
upcoming inspection, a presented ask, or acceptance, apply the corresponding
steering and invalidation rules before further work. Do not edit or research
the source until its amendment writer clears `capture_owner`.

One implementation or review ticket may cover several defects with the same
root cause. Keep each defect's metadata, evidence, status, acceptance, and
resolution independently attributable.

## Recovery

After context compaction, first follow orchestrated-run's recovery contract.
Then read the defect-run skill and `DEFECT-TICKETS.md` from the required paths
in `WORKINGHINTS.md` before acting on another ticket or source defect.

Reload every defect whose `orchestrated_run` points to this run, its current
cycle's Orchestrated-run links, active or unresolved linked tickets, and any
pending source projections recorded in `LOG.md`. Recompute defect status from
that persistent record. Do not infer ownership or state from earlier chat.

A non-null `capture_owner` remains an ownership claim after compaction. Do not
edit that source or dispatch conflicting work until the capture assignment
returns or is known not to exist.

## Completion

This defect run is complete only when:

- every ready defect included in the run is `done`;
- every `done` defect has a supported resolution and evidence pointers;
- no included defect remains in backlog, failed review, triaged, in progress,
  blocked, awaiting automated review, automated reviewing, awaiting user
  review, or surfaced for user review;
- no capture assignment for this list still has a non-null `capture_owner`;
- no pending source projection for an included defect remains in `LOG.md`;
- every `duplicate_of` has a matching canonical `duplicates` entry, and every
  related-defect link is symmetric and evidence-backed;
- every done duplicate's canonical goal verification names the duplicate ID
  and scenario;
- all goals and tickets also satisfy the normal orchestrated-run completion
  contract.

Summarize fixed and non-fix resolutions by defect ID, disclose inconclusive
product checks, report drafting or failed captures that were excluded from the
run, and give the defect-list path.
