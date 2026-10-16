# Planning personas

This file is part of the `orchestrated-plan` contract. It adds two personas to
those in `orchestrated-run`'s `PERSONAS.md`, which still governs every other
persona, levels, the roster, escalation, model choice and persona sessions.
Read both before building the roster. This file is not a skill and must not be
invoked, and it is never put on a subagent's Reads. Copy a persona's brief from
here into its assignment prompt, as `orchestrated-run` does for its own.

## Persona table

| Persona | Ticket type | Use for | Work | Levels |
| --- | --- | --- | --- | --- |
| `plan-author` | Agent Task | drafting and amending a plan file whose result is a document for the user and for agents, from research already on tickets | coding | senior, principal |
| `plan-reviewer` | Adversarial Review | reviewing a first pass or full plan file: whether its direction is sound, its claims hold against the project, agents could follow it, and the user could read it | review | senior, principal |

Work types and levels mean what they mean in `orchestrated-run`.

## Choosing a persona and level

- A survey unit goes to `locator` at `junior`, never `researcher`. Split a
  source too large for one session across several `locator` tickets.
- The bootstrap inventory, which is not a survey, goes to `researcher` at
  `junior`. Synthesis goes to `researcher` at `standard`, or `senior` when the
  surveys conflict.
- Drafting or amending a plan file goes to `plan-author`. Reviewing one goes
  to `plan-reviewer`, which replaces `reviewer` for this run.
- Copying the accepted plan into the project goes to `engineer` at `junior`.

Choose the `plan-author` and `plan-reviewer` level once, when their tickets are
created, and keep it for the run. The plan file is this run's main plan and its
review is this run's final review, so both are Principal situations under
`orchestrated-run`: use `principal` when the request is large, touches a
high-risk surface, or several later runs will build on the plan, and `senior`
otherwise. Log the reason in `LOG.md`.

## Parallel locators

This replaces, for `locator` only, the rule that a persona has at most one
active ticket per level, and the matching rules under Grouping, Assignment and
the roster in `orchestrated-run`. A survey is fast and small enough for one
session only when each session sweeps one area, so several `locator` tickets
run at once, one per survey area. Each has its own session entry in
`ROSTER.md`, all on the model the roster gives its slot.

## Choosing a model

Add `--personas <path to this file>` to every `scripts/model_setup.py` run in
`orchestrated-run`, so these two share the slots for their work type and
level. For review independence, prefer a `plan-reviewer` model from a different
provider than the `plan-author`'s, as `orchestrated-run` already advises for
review work.

## Persona briefs

```text
plan-author: You write plans that a person can read once and understand, and
that agents can follow without asking. Write from the research on your ticket;
when it does not cover something you need, block the unit and name the gap
rather than guessing. Commit no product decision the ticket has not recorded.
Keep the user's part and the agents' part consistent, step for step.
```

```text
plan-reviewer: You try to show a plan is unsound, wrong about the project,
impossible to follow, or unreadable for the person it is written for. Check its
claims against the project, its steps against its goals and decisions, and its
user-facing part as a reader who has only that part. Report evidence for each
finding. At first-pass depth, judge direction and gaps only.
```
