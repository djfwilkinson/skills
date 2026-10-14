# Plan file

This file is part of the `orchestrated-plan` contract. Read it before creating
a plan-drafting or plan-review ticket and before presenting a draft. It is not
a skill and must not be invoked. Never put it on a subagent's Reads. Where
`PROMPTS.md` says to include a section of this file, copy that section's text
into the assignment prompt.

A plan file has two parts in one Markdown file. The first is for the user and
the second is for the agents that will carry the plan out. They describe the
same plan, step for step, and must never disagree.

## Where it lives

The orchestrator creates the plan workspace at the start of the run:

`<project>/.agent-runs/orchestrated-plan/<same timestamp-short-name as the run>/`

```text
first-pass.md        the broad ideas, for the first acceptance
plan.md              the full plan
files/               data and other files the plan depends on
```

The workspace is outside the run folder because an Agent Task may write
project files but not run files, and only a Plan ticket may add other files
under the run folder. Plan-drafting tickets write only here. Every
file in `files/` is named in the plan's attachments list. `.agent-runs/` is
already gitignored.

## Banner

The top of `plan.md`, above both parts, so a later reader can tell what they
hold:

```md
# <Plan title, in the user's words>

Status: draft | in review | accepted <date>
Request: <the user's request, in one or two sentences>
Plan home: <where this file was published, or "left in place">
Run: <run folder, for provenance; it may be gone>
Attachments: <paths relative to this file, or none>
Revisions: <one line per revision: what changed and which findings it answers>
```

## Part one: for you

Heading `## For you`. This part is written for the user, who has read nothing
else, and the `user-response` skill governs it. That includes its rule that no
concept is named before it is explained. The reader should be able to stop at
any section with a complete, correct picture so far.

Write these sections in this order. Each depends on the one before:

1. **What this plan is for.** The outcome, in the words the user uses for
   their own work. One short paragraph, then what is out of scope for it.
2. **How things stand today.** Only what the reader needs to follow the rest,
   in the terms they already use. Introduce each new term by describing it
   first.
3. **The approach, and why.** The idea in a few sentences. Then why it beats
   the alternatives that were weighed, each alternative in a line with why it
   lost. Then the decisions the user made and the defaults they accepted,
   each with the choice and the reason.
4. **The steps, in order.** Each step has an ID, `S1`, `S2` and so on, which
   Part two reuses. For each step: what it does in plain terms, why it comes
   where it does, and what the reader will be able to see or check when it is
   done. Steps that do not depend on each other say so.
5. **What could go wrong.** Each risk with what it would cost and how it would
   show up.
6. **How we will know it worked.** The checks, in terms of what the user
   observes.
7. **What happens next.** How the plan is carried out, and anything it will
   ask of the user and when.

Do not use agent terms, ticket IDs, file paths for their own sake, or
orchestration vocabulary here. Name a path or a file only when the user needs
to find or open it.

## Part two: for agents

Heading `## For agents`. This is engine text. Neither writing skill applies.
Keep it complete and terse, so an implementer can follow it mechanically
without this file's first part or any conversation.

Sections, in this order:

1. **Reading order and authority.** Part two is the specification. Part one
   explains intent; where they seem to differ, the plan is wrong. Report it.
2. **Goals and acceptance criteria.** Plan goals `PG-1`, `PG-2`, each with an
   outcome and observable acceptance criteria.
3. **Decisions.** `D-1`, `D-2`: the choice, who made it (user, or default the
   user accepted, or evidence), and where it came from. Product decisions
   still open are listed with options and what is safe under each. At
   acceptance there are none.
4. **Constraints and conventions.** Project conventions the work must follow,
   with `path:line` evidence: code style and structure, testing, docs,
   language or terminology files, and where plans live.
5. **Steps.** One entry per step, using the same IDs as part one, each with:
   Objective; Completion; Reads (exact paths, with lines where useful);
   Changes (paths and what changes in each); Depends on (step IDs);
   Classification (`trivial`, `following an established project pattern`, or
   `moderately complex or higher`) and any schema, persistence layer, public
   API, protocol, data migration, canonical doc, or security, authentication
   or secrets handling it touches; Verification; Rollback.
6. **Interfaces and data.** Contracts, schemas, formats and sample data the
   steps share, or a pointer to the attachment that holds them.
7. **Verification.** Goal-level and cross-area checks: the command or
   scenario and the success condition, for each `PG`.
8. **Risks.** Each risk, its detection, and its mitigation.
9. **Facts relied on.** What the plan assumes about the project, each with
   `path:line` evidence from the surveys and research, so a reader does not
   need the run folder.
10. **For the implementing run.** Suggested goals, non-goals and modules for
    an `orchestrated-run`, the order steps can run in parallel, and whether
    extra planning before implementation is worthwhile given that this plan
    already is one.
11. **Attachments.** Each file under `files/`, what it holds, and which steps
    use it.

## First-pass file

`first-pass.md` is quick and short, because it exists for the user to accept
a direction before the full plan is written. It has no part two and no
banner beyond a title, `Status: first pass` and a `Revisions:` line. It follows
the `user-response` skill and the same order of part one, shortened:

1. What this plan is for.
2. How things stand today, only what is needed.
3. The shape of the plan: the recommended approach and why. When there are
   real alternatives the user must choose between, two or three, each with
   what it would mean for them.
4. The steps at a glance, in order, with why that order.
5. What we assumed, as a list the user can veto, each with what reversing it
   would cost.
6. What still needs the user, as few questions as can be, in the
   `grill-to-done` round format.
7. What this plan does not do.

First-pass checklist, which the author checks before checkpointing:

- the sections are in this order;
- no term, label or ID is named before the sentence that explains it;
- every default taken is listed as an assumption with its reversal cost;
- alternatives shown are real ones, each with what it means for the user;
- no product decision is committed that a settled ticket does not record.

## Consistency rules

These apply to the full plan only.

- Every part-one step has exactly one part-two step with the same ID, and the
  reverse.
- Every decision in part one appears in the decisions list in part two, and
  every step in part two that rests on a decision cites it.
- Every goal's acceptance criteria are covered by at least one step's
  verification.
- Part one's outcome matches the `PG` goals, and every acceptance criterion
  can be traced to something the reader will observe.
- Part one's risks match part two's risks, part one's checks match part two's
  verification, and part one's "what happens next" matches "For the
  implementing run".
- Every file in `files/` is listed under Attachments and used by a step, and
  every attachment exists.
- Nothing in part one names a concept, label or ID before the sentence that
  explains it.
- No part-two step relies on a fact that is not in Facts relied on or in its
  own Reads.
