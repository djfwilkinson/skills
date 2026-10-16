---
name: orchestrated-plan
description: Plan a piece of work through an orchestrated run, ending in a reviewed plan file the user has accepted twice. Use only when explicitly invoked by the user.
disable-model-invocation: true
argument-hint: "<what to plan>"
---

# Orchestrated plan

This skill is user-invoked. Start it only when the user explicitly invokes
`orchestrated-plan`.

It requires `/orchestrated-run`, the `grill-to-done` skill and the
`user-response` skill. Start one orchestrated run and apply this skill as its
planning-specific process. The `orchestrated-run` skill and its references
stay authoritative for ticket types, personas, the roster, grouping, work
units, inboxes, assignment, ownership, reconciliation, human asks and run
completion, except for the settings under Run settings.

Read these before acting:

- [PERSONAS.md](PERSONAS.md): the two personas this skill adds to
  `orchestrated-run`'s and the levels this run uses, read before building the
  roster.
- [PLAN-FILE.md](PLAN-FILE.md): the plan file's two parts and layout.
- [PROMPTS.md](PROMPTS.md): the unit prompts to copy into assignments.
- the `grill-to-done` skill file, before the first question round.
- the `user-response` skill file, before presenting any draft, and put its path
  on the Reads of every unit that writes or reviews the user's part of a plan.

If one cannot be read, report the blocker rather than proceeding from memory.

## What it produces

One plan file with two parts. The first is for the user and explains what the
plan is and why it is that way, in the order a newcomer can follow. The second
is for the agents that will carry the plan out. The user accepts the broad
direction first, then the full plan. Each is adversarially reviewed before the
user sees it. The accepted plan is copied to where the project keeps its plans
and the run ends by giving the command that implements it.

The run does not implement the plan.

## Run settings

Record these as user-confirmed working hints at the start. Invoking this skill
confirms them.

- **Planning depth is `standard`.** Do not offer the planning-depth question.
  The plan file is this run's deliverable, not a change plan, so create no Plan
  or Plan Review ticket.
- **Plan workspace.** Create the workspace under PLAN-FILE.md when the run
  folder is created. Plan-drafting tickets write only there.
- **Not implementation.** The `plan-author` and `plan-reviewer` tickets and the
  publish unit are not implementation tickets or units. Every orchestrated-run
  rule that attaches to implementation does not apply to them: the implementation
  streaming ticket rule in `TICKET-CONTRACTS.md`, the agent boundary inspection
  and boundary validation tickets, the inspection routing under Checkpoints, the
  snapshot requirement, and implementation coverage under Reconciliation. Do
  not copy the Agent Task sentence about an inspector reviewing each checkpoint
  into their assignments, and do not put snapshots on Reads: `.agent-runs/` is
  gitignored, so a snapshot would not contain the plan. Reviewers read the
  workspace files themselves.
- **Coverage.** A draft is covered by a current plan-reviewer verdict with every
  finding routed, and by the user's acceptance. The publish unit is covered by
  its own link check.
- **Review.** The `plan-reviewer`'s rounds are this run's Adversarial Review.
  This replaces the base module-boundary and pre-completion scheduling: use
  no `reviewer` ticket, and treat the last full review
  as the pre-completion review. Each review unit's `Covers` line names the plan
  file and its Reads name workspace paths.
- **Streaming.** The `plan-author` and `plan-reviewer` tickets stay open after
  each unit and take amendments, new draft units and new review units through
  the inbox. Never create a second ticket for either persona; send an added unit
  to the open one. Send `closing` to both once the plan is published.
- **Writing.** The `user-response` skill governs the user's part of the plan
  file, and the draft and ask text built from it, and `public-docs` does not. A
  part for agents is engine text.
- **Personas.** `PERSONAS.md` in this skill adds `plan-author` and
  `plan-reviewer`, with their levels, how to score them (`--personas`) and the
  one parallel-session exception for `locator`.
- **Recovery.** Put the paths of this skill file, `PERSONAS.md`,
  `PLAN-FILE.md`, `PROMPTS.md` and the `grill-to-done` skill file in
  `WORKINGHINTS.md` as required reads. A recovering orchestrator reads all five
  before acting after compaction.

The goal is `G-001`: an accepted plan for the request exists at the project's
plans location, or in place when it has none. Its acceptance criteria are the
first and final acceptance, a full review with every finding routed, and the
published copy's checked links. Its Verification is `defined`, requiring: both
acceptance tickets resolved; the last full review's units each with a verdict
and every finding applied, declined with a reason, or settled; and the publish
unit's link check passing. Non-goals: implementing the plan, and changing
project files other than the published copy.

## Stages

Work through the stages in order. A stage may start before the previous one
finishes when its inputs are ready and tickets allow it.

### 1. Bootstrap

Use the orchestrated-run Start. The bootstrap Research ticket is for the
`researcher` at `junior` and uses the Bootstrap prompt. Its result is the source inventory, the
proposed survey areas, where the project keeps plans, the end user and the
canonical docs. Reconcile it under the normal rules, set `G-001` active and
write the run settings.

### 2. Survey

Confirm or adjust the proposed survey areas. That is a process decision.
Create one Research ticket per survey area for the `locator`, with the Survey
prompt, the request split into topics in each Objective, and `surface` as the
depth with deep escalation not authorised. Dispatch them all at once and in the
background. Locators run in parallel; the rule against two tickets for one
persona does not apply to them under `PERSONAS.md`, and each ticket gets its
own `ROSTER.md` session entry.

Treat each survey ticket's checkpoint as usual: resume that locator at once for
its second unit. Do not hold a locator to batch the wave. Start synthesis only
when every survey ticket in the wave has returned an `execution_result`, then
reconcile them together.

### 3. Synthesis

Create one deep Research ticket for the `researcher` with the Synthesis
prompt. It reads every survey ticket, ties them together, finds the gaps and
closes what it can. Its result is the planning brief.

Every `overflow` line in a survey is a gap, not a result. The researcher
requests a tighter survey of that area, or records why it is not needed.

If it asks for a targeted survey, run one more `locator` wave for exactly what
it names, splitting any overflowed area into smaller ones, then add a unit to
the researcher's ticket through its inbox, or create a new ticket when it
has ended. After that second wave, record what is still unknown as an unknown
instead of surveying again.

Put the brief's decisions into `UNKNOWNS.md` as the questioning tree, with a
`Node state` line under each entry's Status.

### 4. Settle the questions that shape the plan

Follow `grill-to-done`, with its section for orchestrated runs. Each round is
one `Discuss/Gather Inputs` ticket. Ask only decisions that change the shape of
the plan. Take the brief's recommended default for every process choice and for
every product decision whose answer would not change the shape, and carry those
forward as assumptions the user will see and can veto in the first pass.

When the brief has no decision of that kind, skip the round and say so in the
next progress update.

### 5. First pass and first acceptance

Create a `plan-author` Agent Task with the First pass prompt, writing
`first-pass.md`. When it checkpoints, add a first-pass review unit to a
`plan-reviewer` ticket. Route findings: apply the ones the orchestrator accepts
as fix requests to the `plan-author` through its inbox, decline others with a
reason, and settle any product decision with the user through `grill-to-done`.

When the file offers shapes the user must choose between, settle that choice
first, in its own `grill-to-done` round. Then present the first pass in one
`Discuss/Gather Inputs` ticket that asks for acceptance of the direction. Lead
with the acceptance request in the user's own words, then give the file's
text without rewriting it. Say what accepting commits the plan to, which is the
approach and the order of steps, and what it does not, which is detail. Say
how to judge it: whether it matches what they want and whether the reasons
hold. Do not use a structured form for the acceptance.

- Accepted: continue.
- Changes to detail: amend through the inbox, review the changed parts, and
  present again.
- The direction is rejected: record why, return to stage 3 with the new
  evidence or to stage 4 with new questions, and send the open `plan-author` a
  new first-pass unit through its inbox.

### 6. Full plan and adversarial review

Send the `plan-author` an added unit with the Full plan prompt. When it
checkpoints, send the `plan-reviewer` the Full review units. Route each
finding:

- apply it, as a fix request to the `plan-author`; blocking when later steps
  build on it;
- decline it with a reason recorded in `LOG.md`;
- if it is a product decision under the shared test, settle it with the user
  through `grill-to-done`, grouping every such finding from the review into
  one round.

A gap the `plan-author` blocked on becomes Research, or a `grill-to-done`
round when it is a decision. Review only the changed parts of an amended plan,
unless the change is high-impact or cross-cutting. Cap each finding at two
rounds of amend and review; after the second, either settle it with the user
or decline it with a reason. A reader-test finding is never declined as a
matter of taste. If one is still open after the second round, settle it with
the user; do not decline it.

Continue until the last full review has every finding applied, declined with a
reason, or settled, and the plan has no open product decision.

### 7. Final acceptance

Present the plan in one `Discuss/Gather Inputs` ticket; settle any option
question in an earlier ticket. Lead with the acceptance request in the user's
words. Open the file for them where the client allows it and give its path.
Ask them to read the `For you` part, say what reading it will tell them, and
give the acceptance basis: whether the outcome, the approach, the order of
steps and the reasons are what they want. Accepting adopts that direction and
those steps. Do not ask them to review or accept the `For agents` part; it
exists only for the agents and the reviews checked it. Do not use a structured
form.

On changes, amend, review the changed parts, and present again. A change that
alters the approach or the order of steps repeats stage 5 for that change
before the full plan is amended, using the open `plan-author` ticket.

### 8. Publish

Create an `engineer` Agent Task at `junior` with the Publish prompt. Its Objective names the
plan workspace, the plans location found at bootstrap, and the naming
convention if any. When the project has no plans location, the plan stays in
the workspace and the unit only updates the banner and checks links. If the
unit stops because the name is taken, open a `Discuss/Gather Inputs` ticket
for a new name, then run the unit again. When it returns clean, send `closing`
to the `plan-author` and `plan-reviewer` tickets.

Do not commit or stage the copy.

### 9. Complete

Complete the run under the orchestrated-run completion rules. The completion
message opens with the bold line `**This orchestrated run is complete.**`,
then a short summary. The summary gives the
plan's path, what the plan covers in the user's own words, the decisions made
and the assumptions the user accepted. It then gives this command with the real
path, and says the run to implement it is up to the user:

```text
/orchestrated-run Implement the plan at <plan-path>. Read the whole file first. The "For agents" part is the specification and the "For you" part explains the reasons.
```

If the plan stayed in the workspace, say that it sits in an ignored folder and
give the path.

## Recovery

After compaction, read the five files named in `WORKINGHINTS.md` before acting,
then rebuild from the run files, the plan workspace and the tickets. Take the
stage from the current state, not from the latest milestone reached. The stage
is the earliest one whose work is not finished:

- bootstrap: the bootstrap ticket is not resolved;
- survey: a survey ticket has no `execution_result`;
- synthesis: the planning brief has not returned;
- questions: a decision that shapes the plan is open in `UNKNOWNS.md`;
- first pass: `first-pass.md` is missing, unreviewed with findings unrouted, or
  not accepted, or the direction was rejected after its acceptance;
- full plan: `plan.md` is missing, or the last full review has an unrouted
  finding or an amendment since it that no review has covered;
- final acceptance: the plan is not accepted since its last amendment;
- publish: the publish unit has not returned clean.
