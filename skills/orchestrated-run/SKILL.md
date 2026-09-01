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
- write worker-maintained ticket sections, except while executing a `Human and Agent Task`;
- reconstruct or rewrite a returned ticket record;
- give this skill file to a subagent.

`Human and Agent Task` is the only ticket type that lets the orchestrator perform bounded production or investigation work. Use it only under that type's contract.

Product decisions stay with the user when the product-decision rule below applies. Process decisions stay with the orchestrator: which ticket to create, whom to assign, whether to accept an execution result, whether a goal is verified, whether adversarial review is due, whether the run is complete.

A subagent reports what it found. It does not create run-level plans or tickets. The orchestrator decides how that changes the run. Follow-ups in a ticket are proposals, not a whitelist.

## Run files

Conversation context is temporary. Persistent memory is run files, ticket files, and project files. After compaction or a lost thread, recover the run from those files plus this skill.

Create a new run at:

`<project>/.agent-runs/orchestrated-run/<timestamp>-<short-name>/`

Create these as empty placeholders. Markdown files get a title heading only. `tickets/` is an empty directory.

```text
GOALS.md
NONGOALS.md
UNKNOWNS.md
WORKINGHINTS.md
LOG.md
PILLARS.md
MODULES.md
tickets/
```

Do not fill them during setup. Resume a run when the user or invocation identifies it. Otherwise create a new run.

When creating `<project>/.agent-runs/`, add `.agent-runs/` to the project `.gitignore` if that line is missing. Create `.gitignore` if the project has none. That is setup, not an Agent Task.

Use stable IDs: goals `G-001`, non-goals `NG-001`, unknowns `U-001`, pillars `P-001`, modules `M-001`, tickets `T-001`. IDs remain stable for the lifetime of the run and are not reused.

The orchestrator owns and writes all run files except active subagent-owned ticket files.

A subagent owns its agent ticket file while the ticket is active. No other agent edits that ticket until it is returned. The orchestrator owns an active `Human and Agent Task` ticket.

## Start the run

1. Create the placeholder files. Apply the `.agent-runs/` gitignore rule above.
2. Create the bootstrap ticket or short bootstrap set from the invocation. Do not do the research in the orchestrator thread. You may attach a `## Reads` list of likely project paths or directories.
3. Dispatch those tickets with the Research assignment prompt and those references.
4. Reconcile when they return. Copy proposals into run files using the Goals and Non-goals rules. Decide which other follow-ups become tickets.

Mark `Agent Task`, `Explore Options`, and any ticket that implements or depends on unconfirmed product decisions as `blocked` with `depends_on` the relevant Discuss tickets. They become `ready` only after those tickets resolve.

**If the invocation contains a request.** Create one `Research` ticket: understand that request and inspect enough of the project to propose goals, non-goals, unknowns, useful user questions, and likely next tickets. Put the user prompt on the ticket. Point `## Reads` at the repo rather than pasting a survey. The proposed goals should record incompleteness, conflicts, and whether they match the user's original prompt.

**If the invocation contains no useful request.** Create a Research ticket whose objective is to inspect enough of the project to reach a useful question before asking the user. Do not ask for goals with no project context when the project itself can provide useful information first. Do not start implementation in bootstrap.

## Unknowns and decisions

`UNKNOWNS.md` is the run-level log of unknowns. Tickets keep the discovery record. This file is what later tickets reference when their job is to close an unknown.

Subagents should identify unknowns and record them on the ticket, with a suggested classification:

- `Research` if a subagent can close it from the project, environment, or existing evidence;
- `Discuss/Gather Inputs` if the user must supply a fact, preference, or decision;
- `Human Task` if the user must perform an external action;
- `Human and Agent Task` if closing it requires branching, repeated interaction between the user and orchestrator.

The orchestrator decides which of those become entries in `UNKNOWNS.md`, and which become tickets. A gap or an unclassified unknown is an input to that decision, not an automatic Research ticket.

Copy new unknowns into `UNKNOWNS.md` during reconciliation. Give each a stable `U-001` ID. Do not rewrite the ticket's Unknowns section into this file as a second investigation. One entry per unknown.

```md
## U-001 - <name>

### Unknown
<what is not known>

### Suggested close
Research | Discuss/Gather Inputs | Human Task | Human and Agent Task

### Status
open | assigned | resolved | abandoned

### Related
- goals: []
- tickets: []

### Resolution tickets
- T-...

### Evidence
- <result when resolved, with ticket ID>
```

When creating a ticket whose objective is to fill an unknown, point `## Reads` at `UNKNOWNS.md` and the `U-...` entry, and list those IDs in the ticket frontmatter `unknowns` field. Closing that unknown is part of Completion.

Update the entry when a ticket returns: set `assigned` while a resolution ticket is active, `resolved` when the unknown is closed, with evidence pointing at the ticket. `abandoned` only when the orchestrator decides it no longer matters, and after user involvement if that is a product decision.

### Product vs process

A product decision requires user involvement when multiple reasonable choices would produce meaningfully different product, architectural, operational, compatibility, or scope outcomes.

Examples:

- changing or abandoning goals;
- meaningful architecture choices;
- public API or persistence choices with meaningful alternatives;
- UX or product behaviour not already specified;
- material technology, dependency or platform choices;
- scope changes or trade-offs that affect goals;
- accepting significant adversarial findings without fixing them.

Local implementation choices that follow established project patterns are process decisions. The orchestrator applies the rule above. It does not default uncertainty to a user interruption.

If a ticket already lists alternatives with meaningfully different outcomes, that is enough evidence for the product-decision rule above. Open `Discuss/Gather Inputs` using those options and the recommendation on the ticket.

A subagent that hits such a choice records it on the ticket and stops short of committing it. The orchestrator must not commit it either.

Process decisions are not user tickets unless they need a product choice. The orchestrator decides next work, assignment, acceptance of results, verification, review scheduling, and run completion.

## Goals

Update `GOALS.md` when reconciled ticket results change the wider run. When research returns goals that match the user's original prompt, set them `active`. Open Discuss when a proposed goal is incomplete, conflicts, or does not match that prompt. Keep other new goals `proposed` until the user confirms them.

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
- T-...

### Status
proposed | active | achieved | blocked | abandoned

### Evidence
- <verification result>
```

`Outcome` is the intended result. `Acceptance criteria` are what must be true for the goal to count as complete. `Verification` is how those criteria will be checked.

A ticket may propose a verification method. The orchestrator decides whether that method is enough, using evidence already in tickets and run files. It must not invent evidence by re-running the work in the orchestrator thread. If evidence is missing, it creates tickets.

Use `deferred` when verification is not yet defined. Keep the goal unachieved until verification is defined and completed.

Verification can use automated tests; build, lint, typecheck or another script; a defined scenario; artifact inspection; a metric or threshold; comparison with a baseline or reference; verification in an external system; agent review against explicit criteria; adversarial review; human acceptance; or not required.

Use `not required` only when the user or a ticket said that completing the work itself proves the outcome. Do not waive verification because the work looks done and the files contain no evidence.

## Non-goals

Update `NONGOALS.md` when reconciled results change scope. Non-goals are not required. Accept simple guards. Keep a non-goal `proposed` and open Discuss only when implementation is likely to struggle without that steering and the user needs to decide it.

```md
## NG-001 - <name>

### Boundary
<what is outside this run>

### Scope check
<what would indicate that work is crossing this boundary>
```

## Working hints

`WORKINGHINTS.md` contains project and user guidance that should affect multiple tickets.

At start the file is empty. Update it from reconciled ticket results and user answers. New hints that require user involvement under the product-decision rule stay `proposed` until the user confirms them.

Common areas: architecture and conventions, UX and UI, terminology, compatibility, performance, security, testing, docs, preferred or avoided techniques, scope, determinism, accessibility, platforms, agent and model preferences.

Use the same agent/model as the orchestrator for subagents by default. Record any user override in `WORKINGHINTS.md`.

Example:

> Keep UX consistent with existing project patterns unless a goal explicitly changes those patterns.

If a working hint conflicts with a goal, the subagent records the conflict on the ticket. The orchestrator decides whether that is a product Discuss ticket or a process change.

Point subagents at `WORKINGHINTS.md` by path. Do not paste it into the ticket as the main context. You may name hint IDs in `## Reads` when only some apply.

## Pillars

`PILLARS.md` lists the main areas of the run. It starts empty. The orchestrator updates it from reconciled results when that changes the wider run.

Possible pillars include UX, UI, product behaviour, domain logic, architecture, data, API and integrations, performance, security, accessibility, migration, testing, developer experience, documentation, and infrastructure. Use pillars that are relevant. The list is not exhaustive.

Each pillar should contain ID and name, purpose, related goals, and status.

Use pillars for substantial areas of work. Put cross-cutting guidance in `WORKINGHINTS.md`.

## Modules

`MODULES.md` groups related work into manageable parts. It starts empty. The orchestrator updates it from reconciled results.

Each module should contain ID and name, purpose, related goals and pillars, known dependencies, and status: `proposed | active | complete | blocked | retired`.

Modules may be added, split, merged or retired when reconciliation says the run needs that.

## Tickets

Store tickets in `tickets/` as Markdown with YAML frontmatter.

`status` and `owner` are orchestrator-owned. `execution_result` is worker-owned and unset until the worker's execution ends.

While a ticket is active, the worker may update only:

- `execution_result`;
- `Unknowns`;
- `Findings`;
- `Work performed`;
- `Evidence`;
- `Interaction log`;
- `Blockers / follow-ups`.

The worker must not modify other ticket metadata. When the orchestrator is the worker for a Human and Agent Task, it still updates its orchestrator-owned fields separately under that type's lifecycle.

```md
---
id: T-001
title: Understand the user prompt
type: Research
status: ready
execution_result: null
goals: []
unknowns: []
pillars: []
modules: []
depends_on: []
owner: null
---

# T-001 - Understand the user prompt

## Objective
<the bounded result this ticket should produce>

## Reads
- <run file, goal, unknown, ticket, project file, directory, or doc path>
- WORKINGHINTS.md
- GOALS.md
- UNKNOWNS.md

## Completion
<what must be true for the worker to report completed>

## Interactive reason
<orchestrator-owned: required only for Human and Agent Task; why one interactive ticket is materially better>

## Unknowns
<worker-maintained>

## Findings
<worker-maintained>

## Work performed
<worker-maintained>

## Evidence
<worker-maintained>

## Interaction log
<worker-maintained: used by Human and Agent Task; otherwise optional>

## Blockers / follow-ups
<worker-maintained: proposals for the orchestrator>
```

Ticket statuses:

`proposed | ready | active | blocked | resolved | cancelled`

Execution results:

`completed | blocked | failed`

A ticket is `ready` when the orchestrator decides its dependencies and required inputs are available.

`execution_result: completed` does not mean the orchestrator must set `status: resolved`. Reconcile first.

Keep each ticket bounded enough for one assignment. If it is too broad, the worker reports `blocked` or `failed` with a split proposal. The orchestrator decides how to split or replace it.

An Agent Task is not `ready` until Objective, Completion, and Reads name what to change and what done looks like. Vague Research follow-ups stay Research or unknowns, not ready Agent Tasks. Agent Task `## Reads` are the files Research already found, not the repo.

A Human Task is not `ready` until Objective is a complete ask the user can perform without inventing the procedure, and Completion names the observable result or evidence to return.

A `Human and Agent Task` is not `ready` until Objective, Completion, and Reads bound the work, and Interactive reason explains why repeated branching interaction in one ticket is materially better than using the existing ticket types. Completion is the overall end condition for the ticket, not the expected result of one interaction.

Explore Options is the type for deciding what to build. That reasoning does not land on an Agent Task.

Repo-wide or cross-area validation is its own ticket. That ticket may be an Agent Task created for that purpose. Create it at a module or run boundary, or when several parallel Agent Tasks have touched different areas. Do not fold it into those implementation tickets.

## Assignment

Every `ready` agent ticket is assigned to one subagent before any work on it starts. That is the only way agent tickets get done.

Do not give the subagent this skill. Give it:

1. the ticket file path;
2. the assignment prompt for that ticket type, copied from this skill;
3. the `## Reads` list of paths.

Do not build a large custom context summary. Point at files. A `## Reads` list may include `WORKINGHINTS.md`, `UNKNOWNS.md`, relevant goals, unknown IDs, pillar or module entries, earlier tickets, project files, directories, and documentation. You may name project paths and directories so the worker can read them. Do not dump a repo survey into the ticket.

When assigning a ticket:

1. confirm dependencies using ticket metadata and owned run files;
2. check for file, state and decision conflicts with active tickets;
3. fill `## Reads`;
4. set `status: active`;
5. set `owner` to the assigned subagent;
6. dispatch the subagent with the type prompt and those paths.

Independent tickets may run in parallel. Dispatch `ready` agent tickets unless a ready `Human and Agent Task` has been selected as the next work. Do not dispatch `proposed` or `blocked` tickets. Handle Discuss, Human Task, and Human and Agent Task in the orchestrator thread.

After dispatching agent tickets, wait for those tickets to return. That wait is not a user prompt. Reconcile as soon as a ticket returns. Do not wait for the user to continue the run.

Selecting a ready `Human and Agent Task` as the next work creates a barrier: stop new subagent dispatches, wait for every already-active subagent to return, and reconcile them first. Ready agent tickets may remain queued. Do not start or surface the interactive ticket until no subagent ticket is active. Do not dispatch subagents while it remains active.

Apart from closed-ticket progress updates, return to the user only when a human ticket needs a response, or when the run is complete. If agent tickets are also active, still reconcile them when they return.

### Shared agent rules

Include this block in every agent assignment prompt, then the type contract.

```text
You are executing one ticket. You own that ticket file while it is active.

Read the ticket file and every path in its Reads list. Then do only the bounded work in the Objective.

Update the ticket before you return. You may change only execution_result, Unknowns, Findings, Work performed, Evidence, Interaction log, and Blockers / follow-ups. Do not change other ticket metadata. Do not leave the detailed record only in chat.

Set execution_result to completed, blocked, or failed. That is your result, not the persistent ticket status. The orchestrator owns status and owner.

Do not edit run-level files (GOALS.md, NONGOALS.md, UNKNOWNS.md, WORKINGHINTS.md, LOG.md, PILLARS.md, MODULES.md). Do not create tickets or run-level plans. Record follow-ups on this ticket. The orchestrator decides what happens next.

If multiple reasonable choices would produce meaningfully different product, architectural, operational, compatibility, or scope outcomes, stop short of committing the choice. Record the options and a recommendation on the ticket. Set execution_result to blocked.

Return by finishing the ticket record and execution_result.
```

## Ticket type contracts

The prose here is for the orchestrator choosing a type. The prompt is what the subagent receives.

### Research (subagent)

Close a knowledge gap. Set depth in Objective and Completion. Depth is how much effort goes into surrounding context and hunting the answer, not which sources are allowed.

- `triage`: fast. Decide whether any research is needed, and if so whether `surface` or `deep`. Do not hunt the answer. Returns `no-investigation-required`, `surface`, or `deep`.
- `surface`: pull obvious context. If the answer is there, return it. If not, request `deep` on the same gap, or unknowns for newly uncovered gaps.
- `deep`: get a full picture and hunt. Return the answer, unknowns, or a partial answer plus newly discovered unknowns.

Bootstrap is `deep` unless set otherwise.

Assignment prompt, after the shared agent rules:

```text
This ticket is Research. Do the depth named in the Objective. Depth is effort on context and hunting.

triage: quick decision only. Do not hunt the answer. Return one next step: no-investigation-required | surface | deep.

surface: pull obvious context. Return the answer if it is there. Otherwise request deep on this gap, or unknowns for newly uncovered gaps.

deep: get full context. Hunt. Return the answer, unknowns, or a partial answer plus newly discovered unknowns.

Return on the ticket: depth used; findings (the answer or partial answer); evidence; remaining uncertainty; implications; triage next step if triage; follow-ups.

Follow-ups: Agent Tasks only when Objective, Completion, and Reads are already specified. Propose Human and Agent Task only when its bounded work and need for repeated branching interaction are already clear. Otherwise return unknowns, more Research, Explore Options, or Discuss.

Do not implement production changes unless the Objective says to.
```

### Agent Task (subagent)

Perform the bounded implementation or production task. When the Objective is to produce a UX/UI review, put the `ux-ui-reviewer` skill file on Reads.

Assignment prompt, after the shared agent rules:

```text
This ticket is an Agent Task. Perform the bounded production work in the Objective. Do not research what to build. Implement from Objective, Completion, and Reads. If that is not enough, set execution_result to blocked and record the gap.

Meet this ticket's Completion. Check that, and nothing wider. Wider tests, lint, typecheck, or cross-area review are not this ticket's job unless Objective and Completion expressly make them so.

Return on the ticket:
- work performed
- changed files or artifacts
- checks against this ticket's Completion
- blockers
- possible follow-up work
```

### Explore Options (subagent)

Investigate alternatives without committing them to the production solution.

Assignment prompt, after the shared agent rules:

```text
This ticket is Explore Options. Investigate alternatives. Do not commit them to the production solution.

You may use prototypes, temporary code, temporary tests, instrumentation, reproductions, or debugging experiments. Label any temporary artifacts as temporary.

Return on the ticket:
- options explored
- evidence from each
- trade-offs
- a recommendation where supported
- temporary artifacts created
```

### Adversarial Review (subagent)

Actively try to show that completed work is incorrect, incomplete, or inconsistent with the run. When the completed work is UI, put the `ux-ui-reviewer` skill file on Reads so inspection follows that skill. The ticket type remains Adversarial Review. Do not create a UX/UI review Agent Task for the same completed work.

The orchestrator must not be the reviewer. It decides whether review is due and assigns this type. Typical times: completing a module; after high-impact or cross-cutting changes; after unexpected test or debugging results; when evidence is uncertain; before completing the run. A later review may cover several small related modules. A worker may recommend review; that recommendation is a proposal.

Assignment prompt, after the shared agent rules:

```text
This ticket is Adversarial Review. Try to show that the completed work is incorrect, incomplete, or inconsistent with the run.

Read the listed goals, acceptance criteria, non-goals, working hints, and verification requirements. Check the work against them.

Return on the ticket:
- specific findings
- evidence
- impact or severity
- checks that found no problem
- remaining uncertainty

Do not fix findings unless this ticket's Objective explicitly includes remediation.
```

### Discuss/Gather Inputs (orchestrator)

The orchestrator handles this ticket because it owns the user conversation.

Ask only for the information, decision, review or acceptance required by the ticket. Write that ask on the ticket from evidence already on tickets or run files: the question, and any options, recommendation, or draft that exist. Do not invent those. If a product decision needs prepared options and they are missing, the ticket is not `ready`: open Research or Explore Options first.

For acceptance, return to the user in normal chat. Show or point to the exact result, state the acceptance basis, and ask the user to accept it or describe required changes. Do not use a structured questions form or multiple-choice prompt for acceptance.

Return using Human involvement. On Discuss and Human Task, the orchestrator writes the user record and `execution_result` on the ticket, then reconciles.

### Human Task (orchestrator)

The user performs the actual task.

Objective is a complete ask: what to do, in order, with the commands, paths, URLs, and expected output the user needs. Name an account or secret-store location when required. Do not put secret values (passwords, tokens, keys, recovery codes) in the ask or on the ticket. Do not leave the procedure implied. Do not invent those details. If they are unknown, the ticket is not `ready`: open Research or Discuss first.

Completion is the observable result or evidence the user should return, not the process reason. The ticket is not `ready` until Objective is a complete ask and Completion names that result. Return using Human involvement.

### Human and Agent Task (orchestrator)

The orchestrator and user perform one bounded task through repeated, branching interaction. The orchestrator may inspect, run commands, change project files or external state within Objective, then ask the user for the next observation or action and continue in the same ticket.

Use this type only when keeping the feedback loop in one ticket is a much better user experience. Appropriate cases include:

- branching work where the next agent action depends on a human action or observation;
- fast iterative debugging with many short human and agent turns;
- interactive setup or diagnosis whose steps cannot be usefully specified in advance.

Do not use it for a single human action, one decision, ordinary implementation, work that can proceed asynchronously, or merely because the next step is uncertain. Use the existing ticket types for those. It does not replace `Discuss/Gather Inputs` for product decisions required by the product-decision rule.

Before starting:

1. confirm no subagent ticket is active;
2. check dependencies and file, state and decision conflicts as for Assignment;
3. set ticket status to `active` and owner to `orchestrator`;
4. set `execution_result: null`.

While active:

- do only the bounded Objective;
- put each user ask in the latest `Interaction log` entry, not Objective;
- make each ask complete enough for that turn: include commands and process when the user would otherwise have to invent a procedure, and always name the expected result and follow the secret-handling rules;
- before every user-facing interaction for this ticket, update `Interaction log` with the agent action and result, any user result received, the branch taken and the next ask; also update Work performed and Evidence, including changed paths;
- copy a short ask into chat and include the ticket file path; for a long procedure, give a one-line description and point to its latest `Interaction log` entry in the ticket file;
- keep the ticket active across user turns rather than closing it and creating another ticket;
- do not dispatch subagents.

If the work reaches a product decision covered by the product-decision rule, stop short of that choice, record options and a recommendation, set `execution_result: blocked`, and reconcile. Open Discuss and make this ticket depend on it; it may return to `ready` after that decision resolves.

When Completion is met or the work cannot continue, set `execution_result` to `completed`, `blocked`, or `failed`, then reconcile the ticket normally. If the user explicitly stops the task, record that result, set `execution_result: blocked`, and reconcile it to `cancelled`. This is the only case where the orchestrator is both ticket worker and reconciler.

Commands, inspections and tests performed in this ticket are its Evidence. They may guide the interaction, but do not replace independently required goal verification or Adversarial Review.

## Human involvement

Every required human interaction must have a ticket. A product decision that requires user involvement must have a `Discuss/Gather Inputs` ticket.

Use `Discuss/Gather Inputs` when the user needs to provide information, fill in an unknown, make a product decision, review something, make a judgement, or accept a result, including proposed goals and non-goals.

Use `Human Task` when the user needs to perform an external action.

Use `Human and Agent Task` only for the repeated, branching interaction defined by its contract.

Human acceptance used for goal verification must have its own `Discuss/Gather Inputs` ticket.

If Discuss or Human Task blocks only part of the run, dispatch `ready` agent tickets that do not `depends_on` it, then return to the user for that ticket. This parallel-dispatch rule does not apply after a Human and Agent Task is selected or while it is active. Tickets whose `depends_on` names that answer are `blocked`. The orchestrator may also set others `blocked` when it decides the missing answer would invalidate them. Record that decision in `LOG.md`.

Do not keep planning in place of that return, and do not invent the answer. Return with a well-defined ask: what the user needs to do or say, filled out enough to act. A question is a good form when there are multiple options and those options are easy to understand. It is not the only form. Use a list of needed decisions, a statement of what is missing, a draft to accept or change, or a Human Task description when that is clearer.

Acceptance is not an options question. Present it directly in chat under the Discuss contract, end the turn, and wait for the user's reply.

Write the complete ask on the ticket. Copy it into the message when it is short enough to include in full. When the ask is a procedure or otherwise too long to copy, point to that ticket file instead of summarising it. Do not summarise a filled-out procedure into a vague instruction. Do not paste ticket metadata, Reads, related run IDs, or the process reason. Do not put secret values on the ticket or in the message.

When that return is for an open Human Task, end the message with the ask and the ticket file path: the full Objective if copied, otherwise a one-line description plus the path. Include the expected result only when the user needs it to know they are done.

If several Human Tasks are waiting, end with each of those asks and paths. If the message is already only that ask, do not repeat it.

That return does not pause the run. Reconcile any agent ticket that returns while you wait. A return for an active `Human and Agent Task` is different: the run intentionally stays in that ticket's interaction loop.

When the user responds to Discuss or Human Task, record the response on the relevant ticket, reconcile it, and continue the run. When the user responds to a `Human and Agent Task`, record the interaction and continue that ticket; reconcile only when its execution ends.

## Steering

When the user sends a new prompt while other work is still going, act on it immediately. Do not wait for active tickets to return.

Change requests and feedback become tickets. Create them now. Assign them when they are `ready`, except while a Human and Agent Task barrier is selected or active. Do not edit an active subagent's ticket file. If the new work conflicts with an active ticket, block or delay assignment until that ticket returns. Record the steering and the tickets created in `LOG.md`.

If the prompt is a response to an open Discuss or Human Task ticket, treat it as that ticket's return. If it answers the current ask on an active `Human and Agent Task`, treat it as the next interaction, not a ticket return. Other prompts are steering: create any resulting tickets but leave subagent work unassigned until the interactive ticket ends. If the user explicitly stops or replaces the interactive task, end and reconcile it before proceeding. Then continue the run.

## Reconciliation

When an agent ticket returns, a Discuss or Human Task returns, or a Human and Agent Task ends:

1. Read the ticket file and `execution_result`. Leave worker-maintained sections as the worker wrote them.
2. Clear `owner`.
3. Decide the persistent ticket `status`. `completed` is not automatically `resolved`. After return, set `ready` (reassign the same ticket), `blocked`, `resolved`, or `cancelled`. Keeping it for further work means `ready` and `owner` cleared.
4. Reconcile the result into the run: add a concise `LOG.md` entry; update goals, non-goals, unknowns, working hints, pillars or modules only where the result changes wider run state; decide what work happens next, using follow-ups as proposals; decide whether any goal is now verified, or what verification or review work is still required.

Do not copy the investigation into the log. Do not re-do the ticket in the orchestrator thread. If evidence is missing or the result is not acceptable, create or reassign tickets.

After implementation returns, or a Human and Agent Task that performed implementation ends with `execution_result: completed`, open the human inspection `Discuss/Gather Inputs` and the validation-suite ticket in parallel. Neither `depends_on` the other. Do not wait for the suite before asking the user, and do not wait for the user before starting the suite.

If the validation ticket finds issues, record them. Do not patch, and do not create ready fix tickets that would change files or trigger reloads, until that Discuss has returned. Then the orchestrator decides which findings become tickets.

## Progress updates

For chat progress, a ticket is closed when its status becomes `resolved` or `cancelled`.

After reconciling one or more tickets to a closed status, send a short progress update. Batch tickets closed in the same reconciliation pass. For `resolved`, give the ticket ID and one sentence with the user-visible result. For `cancelled`, give the ticket ID, say it was cancelled, and give the concise user-relevant reason already recorded in `LOG.md`; do not imply an execution result. Do not paste ticket YAML, Reads, Findings, Interaction log or detailed evidence. Continue the run without asking the user to reply to or approve routine progress.

If known human tickets are coming but are not being presented yet, the update may briefly say what user involvement will be requested later. Do not include the full ask until that ticket is presented under Human involvement or the Human and Agent Task contract.

## Log

`LOG.md` records the important history of the run.

For each reconciled ticket, record what was attempted, the execution result, the status you set, important decisions, evidence pointers, unknown IDs opened or closed, blockers, and the ticket ID.

Keep detailed investigation and implementation notes in the ticket. Keep `LOG.md` concise.

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
2. `GOALS.md`
3. `NONGOALS.md`
4. `UNKNOWNS.md`
5. `WORKINGHINTS.md`
6. `PILLARS.md`
7. `MODULES.md`
8. relevant entries from `LOG.md`
9. tickets needed for current work

Reload completed tickets only when their detailed results become relevant.

If a `Human and Agent Task` has status `active` and owner `orchestrator`, reload it and resume from its latest `Interaction log` entry. Do not repeat actions already recorded there.

## Process

Discovery, planning, implementation, issue resolution, validation and human acceptance happen as tickets. The orchestrator does not execute agent tickets. It executes `Human and Agent Task` only under that type's narrow exception. It picks ticket type when it creates a ticket.

## Goal verification

Ticket completion, module completion and goal achievement are separate.

The orchestrator marks a goal `achieved` when it decides verification is satisfied, using evidence already in tickets and run files: accepted criteria, defined verification, completed verification work, required human acceptance, and disposition of adversarial findings.

Outside an active Human and Agent Task, it must not re-run tests, inspect artifacts, or otherwise execute verification in the orchestrator thread. Checks performed inside that type remain ticket Evidence and do not replace independently required verification. If verification evidence is missing, create tickets.

Agent judgement used as verification is an `Agent Task` or `Adversarial Review`. Human judgement is `Discuss/Gather Inputs`.

If verification fails, decide next work from the record. Mark a goal `blocked` when the run cannot proceed on it. Never mark a goal `abandoned` until the user confirms abandonment through `Discuss/Gather Inputs`.

## Completing the run

The orchestrator decides when the run is complete. An Adversarial Review can inform that decision. It does not own it.

The run is complete when:

- every goal is `achieved` or `abandoned`;
- achieved goals contain verification evidence;
- no required verification is deferred;
- no unresolved ticket is required for an achieved goal;
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
