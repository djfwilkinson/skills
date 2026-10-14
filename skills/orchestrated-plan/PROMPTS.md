# Prompts

This file is part of the `orchestrated-plan` contract. Read it before creating
or assigning any ticket for this skill. It is not a skill and must not be
invoked. Never put it on a subagent's Reads.

Each block is a unit prompt. In an assignment, put it after the persona brief
(from this skill's `PERSONAS.md` for `locator`, `plan-author` and
`plan-reviewer`, otherwise from `orchestrated-run`),
the shared agent rules and the type prompt from `TICKET-CONTRACTS.md`, in that
order. Put the unit's own Objective, Completion and Reads in the ticket as
usual. Where a block says to include a section of `PLAN-FILE.md`, copy that
section's text into the prompt.

Add this to every prompt, because a source may be behind a login:

```text
Never start or wait on a login, device code, browser authorization or
credential prompt. If a source needs one, stop that source, record exactly
what needed authorizing on the ticket, checkpoint the unit blocked, and return.
```

## Bootstrap (scout, Research)

Objective for the bootstrap ticket: inventory the sources the request touches
and propose how to survey them.

```text
This unit is surface depth and does not escalate to deep. It inventories
sources. Do not research the request itself.

Find every source that may hold information relevant to the request on your
ticket: each codebase or repository, each directory tree large enough to
survey separately, documentation sets (README files, docs folders, decision
records, wikis, specs), trackers, and any material the user named. For each,
record its kind, its location, and its rough size (file or page count).

Propose survey areas: one source, or one part of a large source, per area. Size
an area so one session can sweep it without summarising from memory, which is
roughly no more than 150 files or one module's worth of documents. Split a
larger source by directory or domain. Give each area a name, its paths or
location, its size, and why it may matter.

Also find: where this project keeps its plans (a plans folder, an existing
plan with a naming convention, or an instruction in AGENTS.md or contributor
docs), the project's end user, and canonical docs or specs. Record the evidence
for each; record "none found" when there is none.
```

## Survey (locator, Research)

One ticket per survey area, two units each. Name the topics in the Objective:
the request, split into the things to look for.

```text
This ticket surveys one source for the topics in its Objective. You do not
need to understand what you find. You need to find all of it. Do not explain
how anything works, judge it, or recommend anything.

These units are surface depth. Do not escalate to deep, whatever the Research
instructions above say. If something needs deeper reading to judge, list it
under Could not judge.

Stay inside your area. When you see something relevant outside it, record it
under Pointers and move on.

Unit 1, sweep: for each topic, search by the topic's words, their variants
and likely synonyms, related identifiers, file and directory names, and the
kinds of file that would hold it: code, tests, configuration, schemas,
documents, tickets. Read enough of each hit to tell whether it matches.

Unit 2, follow the names: take the identifiers, file names, callers, tests,
configuration keys and documents that unit 1 turned up, and sweep again for
what refers to them or sits beside them.

Record on the ticket, per unit, with these headings:
- Locations: one line per location, in the form
  `<path or URL>[:lines] | <kind> | <why it may be relevant, at most fifteen
  words, naming the matched term or symbol> | strong or maybe`. `strong` means
  the topic's own term or symbol appears in code, configuration, a schema, a
  heading or a title there; anything else is `maybe`. Order strong first. List
  at most sixty. If there are more, record the rest as
  `overflow: <count> more in <directory or section>`; the investigator treats
  every overflow line as a gap to re-sweep.
- Search record: the terms and patterns used, the places swept, and the places
  skipped and why.
- No hits: each topic that found nothing, with what you tried.
- Pointers: relevant things outside your area, with where they are.
- Could not judge: anything you could not tell was relevant, with where it is.
```

## Synthesis (investigator, Research)

One ticket, after every survey ticket in the wave has returned.

```text
This ticket ties the surveys together and closes what they could not.

Unit 1, tie together: read every survey ticket on Reads. Merge the locations
into one picture of what the request touches. Read the strong locations and
as many of the maybes as you need. Work out what is missing: topics with no
hits, areas nobody surveyed, pointers nobody followed, locations nobody could
judge, every `overflow` line, and a large set of `maybe` locations in one
area. List each gap.

Unit 2, close gaps: research each gap deeply enough to settle it, or record
precisely why it cannot be settled from the project. If a gap needs a sweep of
a source nobody surveyed, request a targeted survey, naming the source and
topics, rather than sweeping it yourself.

Record on the ticket a planning brief with these headings:
- What the request touches: areas and key locations, with `path:line`.
- How it works today, only where the plan depends on it, with evidence.
- Conventions and constraints: code, testing, documentation, terminology,
  where plans live, with evidence.
- Candidate approaches: each with what it needs, what it risks, and the
  evidence for both.
- Decisions: a tree. Each decision has a short title; what a different answer
  would change; the decisions it depends on; two to four options, each with
  the effect the user would see or the cost it carries, and its knock-on
  effects for later work, compatibility or scope; a recommended option with a
  reason; whether the decision can wait until a named later step, or why it
  must be made now; and whether it is a product decision under the shared test
  or a process choice. Fill every field before the decision is marked ready.
- Facts settled: everything research answered that a reader might otherwise
  ask the user.
- Unknowns: what is still open, with a suggested way to close each.

Do not make product decisions. Do not write the plan.
```

## First pass (plan-author, Agent Task)

Include the section `First-pass file`, with its checklist, of `PLAN-FILE.md`.
Do not include `Consistency rules`; they apply to the full plan. Reads include the `user-response` skill file, the planning brief, the settled
Discuss tickets and the working hints.

```text
This unit writes first-pass.md at the path in its Completion. It is a quick
first draft of the broad ideas, so the user can accept a direction before
a full plan is written. Do not polish it and do not write the agents' part.

Write it from the research and decisions on Reads. If you need a fact they do
not hold, block the unit and name the gap; do not guess. Commit no product
decision the Discuss tickets have not settled. List defaults you took as
assumptions the user can veto, each with the cost of reversing it.

Follow the user-response skill file on Reads for all of it, including its rule
that no concept, label or term is named before it has been explained.

Record on the ticket: the path, the assumptions, the questions left for the
user, and any gap you blocked on.
```

## Full plan (plan-author, Agent Task)

Include the sections `Banner`, `Part one: for you`, `Part two: for agents` and
`Consistency rules` of `PLAN-FILE.md`. Reads include the `user-response` skill
file, the accepted first pass, the planning brief, and every settled Discuss
ticket. Do not put the survey tickets on Reads: the brief carries their
evidence as `path:line`, and the author needs only that.

```text
This unit writes plan.md at the path in its Completion, with the banner, the
user's part and the agents' part. The user accepted the first pass on Reads as
the direction; the plan fills it in and may change it only where evidence
requires, and says so in Revisions.

Write the user's part for a reader who has only that part. Follow the
user-response skill file on Reads for it: plain words, nothing named before it
is explained, and each step with the reason it sits where it does. Write the
agents' part so an implementer can follow it without the first part or any
conversation. Cite evidence as path:line.

Copy no product decision the settled tickets do not record. Where one is open,
list it under Decisions with options, and finish the rest.

Put every file the plan depends on under the files folder in the workspace,
and list it under Attachments.

Before you checkpoint, check the consistency rules yourself and fix every
break. Record on the ticket: the path, open decisions, any gap you blocked on,
and the classification of each step.
```

## Amend (plan-author, Agent Task)

Sent through the inbox as an added unit or fix request. Reads name the review
tickets and finding IDs, or the user's change request.

```text
Apply every finding and change request named in the inbox item. Change only
what they require and what must follow from it for the two parts to stay
consistent. Add a line to Revisions, in plan.md or first-pass.md, naming what
changed and which findings it answers. If you do not apply a finding, record why on the ticket. If applying
it needs a fact or decision you do not have, block and name it.
```

## First-pass review (plan-reviewer, Adversarial Review)

```text
This unit is a first-pass review of first-pass.md. It is a quick check of
direction, not a full review. Do not edit the file. Judge:
- whether the recommended approach fits the request and the evidence on Reads,
  and whether a materially better one was missed;
- whether something material is absent: a goal, a constraint, a decision;
- whether an assumption should have been a question, or a question should have
  been an assumption;
- whether a reader with only this file would understand it, and whether any
  term or label is named before it is explained.

Record each finding with a ticket-scoped ID such as <ticket ID>/F-001, its
location, the evidence, and whether it needs a user decision. Record the
checks that found nothing.
```

## Full review (plan-reviewer, Adversarial Review)

One ticket, three units, one lens each. Reads include the plan, the accepted
first pass, the survey and research tickets, every settled Discuss ticket,
the goals and working hints, and for the third unit the `user-response` skill
file.

```text
This ticket is a full review of plan.md. Do not edit the plan. Try to show it
is wrong. Each unit has one lens.

Correctness: check every fact under Facts relied on, and every path and
line a step cites, against the project. Check each step against its goal:
does finishing it move the goal's acceptance criteria. Check order and
dependencies: what a step needs that an earlier step does not provide. Look
for what the plan breaks, callers and data it does not mention, and
compatibility. Check each classification, and any high-risk surface that is
not named. Check that each verification could fail.

Coverage and followability: check that every user decision and accepted
assumption is carried into the steps, that every goal criterion has a
verification, and that nothing goes beyond the stated scope. Read the agents'
part as a builder who has only it: where would they have to guess, ask, or
make a product decision? Check the consistency rules in the order they are
given.

Reader test: read only the user's part, as the user. Find every term, label
or ID named before it is explained, every step whose reason is missing, every
place the order forces the reader to wait for an explanation, and every claim
the reader could not check. Check the part against the user-response skill
file on Reads. Then check it matches the agents' part, step for step.

Record each finding with a ticket-scoped ID such as <ticket ID>/F-001, its
location, evidence, severity, and whether it needs a user decision under the
shared test. Record the checks that found nothing and the remaining
uncertainty.
```

## Publish (fixer, Agent Task)

Objective names the plan workspace path, the plans location found at
bootstrap or `none`, and the project's naming convention if any.

```text
This unit copies the accepted plan into the project and checks the copy. It
changes nothing else and does not commit.

If the Objective names a plans location, copy there; otherwise leave the files
where they are. Name the copy by the project's convention. Without one, use
the plan's short name. If the plan has attachments, make a folder for it
named the same way and put plan.md and the attachments in it, keeping their
relative layout; otherwise copy the single file. Never overwrite an existing
file: if the name is taken, stop and record it.

Edit the banner of the copy, or of the workspace file when you leave it in
place: set Status to accepted with today's date and Plan home to the final
path, or to "left in place". When you copied, rewrite any relative links so
they work from the new location.

Check that every relative link and attachment in the copy resolves. Record the
final path, each file written, and the check results as Evidence.
```
