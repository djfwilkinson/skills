# Defect ticket contracts

This file is part of the `defect-capture` and `orchestrated-defect-run`
contracts. Read it before creating, assigning, updating, or recovering a defect
ticket. It is not a skill and must not be invoked.

## Layout and identity

A defect list is one dated folder under:

`<project>/.agent-runs/defect-lists/<timestamp>-<short-name>/`

Store each defect as `D-<number>.md`. Use one number sequence per list. IDs are
stable, are never reused, and do not change when defects are related or marked
as duplicates.

Copied evidence lives under the list's `assets/` directory. Use relative links
from defect tickets so the list remains portable.

## Schema

Use this template. Keep every heading so later capture, triage, implementation,
and review evidence has one stable location.

```md
---
id: D-001
title: "Short description of the observed defect"
status: backlog
capture_state: drafting
capture_owner: null
resolution: null
cycle: 1
resume_status: null
created_at: <RFC 3339 timestamp>
updated_at: <RFC 3339 timestamp>
orchestrated_run: null
duplicate_of: null
duplicates: []
related_defects: []
---

# D-001 - Short description of the observed defect

## Report

### Summary

### Captured context

### Context and environment

### Expected behavior

Authority: unknown

### Actual behavior

### Reproduction

### Impact

### Evidence

### Unknowns

## Additional context

## Triage

## Resolution

## Automated product checks

## User review

## Orchestrated-run links

## History
```

Use `unknown` in prose when the supplied context does not establish a field.
Do not use invented detail to make a report appear complete.

## Defect fields

Defect status is a defect-level projection. It is separate from an
orchestrated-run ticket's `status`, `presentation`, and `execution_result`.
Allowed values are:

`backlog | triaged | in progress | blocked | awaiting automated review | automated reviewing | awaiting user review | surfaced for user review | done | failed review`

Capture state records whether the initial report is ready:

`drafting | ready | failed`

`capture_owner` is `null` when no capture writer owns the file. Before
dispatch, the capture coordinator sets it to a unique assignment identifier.
Apart from the coordinator recording or clearing this ownership field, only
that assignment may edit the file until its return is reconciled. A non-null
owner survives compaction and forbids a second assignment.

Resolution is `null` until the defect reaches `done`. Allowed non-null values
are:

`fixed | duplicate | not-a-defect | cannot-reproduce | wont-fix`

`cycle` starts at 1 and increments once when a failed review starts another
triage cycle. `resume_status` is normally `null`. While status is `blocked`, it
records the prior non-blocked status as context. Recompute defect status from
the current run tickets when the blocker clears; do not restore it
mechanically. Clear `resume_status` whenever status leaves `blocked`.

`orchestrated_run` is the relative path of the run currently handling the
defect. `duplicate_of` appears only on a duplicate and points to its canonical
defect. `duplicates` appears on the canonical defect and contains the inverse
links. `related_defects` contains symmetric links for related defects that are
not duplicate inverses.

Every metadata change updates `updated_at`. Every status, resolution, cycle,
duplicate, and relationship change gets a concise timestamped History entry
with its reason and evidence pointer.

## Section ownership

The capture coordinator owns identity, timestamps, initial `status`,
`capture_owner`, initial `capture_state: drafting`, and durable attachment
import. It may set capture state to `failed` when dispatch never starts or a
return is invalid. It clears `capture_owner` only after reconciling the
assigned writer.

An initial capture writer owns the title and Report while assigned and may set
capture state to `ready` or `failed`. An amendment writer may append under
Additional context without changing defect status or capture state. No two
writers may own the same defect file at once.

During an orchestrated defect run, the orchestrator owns defect status,
resolution, cycle, resume status, run and relationship metadata, Triage,
Resolution, Automated product checks, User review, Orchestrated-run links, and
downstream History entries.

An orchestrated-run subagent writes only its own orchestrated-run ticket. It
must not edit a defect ticket. The orchestrator reconciles returned evidence
into the defect ticket without reconstructing or replacing the subagent's
ticket record.

## Capture rules

Preserve the user's supplied text under Captured context. It may be formatted
for Markdown safety but must not be paraphrased there. Put its lightly rewritten
version in Summary and other synthesis in the remaining Report fields. Keep
ticket YAML valid. Quote a title containing `:` or another YAML-significant
character.

Write Summary as a lightly rewritten version of the user's original prompt for
later defect-related asks. Keep the user's product terms, observed problem, and
requested or implied corrected behavior. Remove chat framing, invocation text,
repetition, and incidental grammar errors. Do not add diagnosis, severity,
implementation detail, or requirements the user did not supply. Summary must
make sense beside the defect ID to a user who has not reopened Captured context.
Use one short paragraph unless that would lose distinct reported conditions.

Start Expected behavior with exactly one authority:

- `Authority: user-stated` when the user directly states the required result;
- `Authority: defect-implied` when the report unambiguously identifies a
  minimum corrected state, such as "the button is missing an icon" meaning the
  button should have an icon;
- `Authority: unknown` when the report does not establish the desired result.

`user-stated` and `defect-implied` are both user-confirmed outcomes for an
orchestrated defect run. Prefer `defect-implied` whenever Captured context,
Actual behavior, or an attachment describes an observable as missing, absent,
broken, incorrect, or unexpectedly different and therefore establishes a
minimum corrected state. An unspecified implementation detail does not make
outcome authority `unknown`. Infer only that minimum outcome.

Separate:

- observations supplied by the user or visible in evidence;
- user expectations;
- writer inferences, labelled as inferences;
- unknowns that later triage may close.

Describe reproduction steps only when the context establishes them. A partial
sequence is useful when marked partial. Link every supplied or copied artifact
under Evidence and explain what it shows. Never claim an image shows something
the writer cannot see.

Capture does not inspect the codebase, diagnose root cause, decide duplicates,
or propose a fix. Those belong to triage.

## Confirmed-outcome run rules

For an orchestrated defect run, a confirmed outcome comes from:

- Expected behavior marked `user-stated` or `defect-implied`;
- Additional context marked `user-stated` or `defect-implied`; or
- Captured context, Actual behavior, or an attachment that establishes the
  same minimum corrected state even when a capture writer conservatively left
  Expected behavior as `unknown`.

The Report remains immutable during amendment capture. Every later reader
treats confirmed Additional context as equal in authority to confirmed Expected
behavior.

Confirmed outcomes specialize orchestrated-run's product-decision and Discuss
rules. They override only an action that would ask whether to deliver that
outcome, treat UX involvement alone as a product decision, or treat an
unspecified implementation detail as an incomplete goal. Apply this override
to discovery Discuss, goal activation, Explore Options, Plan Open decisions,
Plan Review findings, implementation blockers, and Human and Agent Task
product-decision stops.

Do not use the override to suppress a supported non-fix disposition, the
planning-depth offer when its actual conditions are met, a genuinely unresolved
product choice, or post-implementation inspection and acceptance.

### Assignment extension

Copy this block into every agent-ticket assignment in an orchestrated defect
run, after orchestrated-run's shared rules and exact type prompt:

```text
Expected behavior or Additional context marked user-stated or defect-implied
is a confirmed run requirement. Captured context, Actual behavior, or an
attachment that unambiguously establishes the same minimum corrected state is
also confirmed even if Expected behavior says Authority: unknown.

Do not reopen whether the run should deliver a confirmed outcome. Delivering
that minimum outcome, or a project-conventional way to deliver it, is process.
An unspecified implementation detail and UX involvement alone do not make the
outcome incomplete or create a product decision.

A remaining choice is still a product decision when source and project evidence
cannot settle it and reasonable alternatives would materially change the
confirmed outcome or another product, architectural, operational,
compatibility, or scope result. A supported non-fix disposition still follows
the defect-run disposition rules when evidence shows implementation is
inappropriate.

Classify work from actual scope, coupling, and reversibility. Do not classify
work as moderately complex merely because it affects UX.
```

### Pre-implementation decision gate

Do not create Discuss merely to confirm the defect, a confirmed outcome, the
decision to fix it, or acceptance criteria directly implied by Expected versus
Actual behavior. Do not ask the user for facts available from the source
defect, its attachments, the project, or assigned Research. Severity, priority,
scheduling, grouping, review timing, and local implementation choices following
project patterns are process decisions.

Before creating a pre-implementation Discuss, require Research or Explore
Options to record:

- the exact unresolved choice;
- why Captured context, Expected behavior, Actual behavior, Additional context,
  and attachments do not answer it;
- which project paths, canonical docs, components, siblings, or patterns were
  checked and why they do not settle it;
- reasonable alternatives with meaningfully different product,
  architectural, operational, compatibility, or scope outcomes;
- why the choice blocks safe implementation now.

If that record is missing, create or reassign Research instead of Discuss. Ask
only the smallest remaining product choice. For "the button is missing an
icon", adding an icon is confirmed. The exact icon may be asked only when its
action, project patterns, and design system genuinely cannot settle a
materially different remaining choice.

This gate applies before implementation. Boundary inspection after
implementation remains required acceptance and asks whether the implemented
result is acceptable, not whether the confirmed outcome should have been
pursued.

## Initial ticket-writer assignment prompt

Give one background subagent the defect path, supplied context, and attachment
paths, followed by this prompt:

```text
You are writing one defect ticket. You own only the assigned defect file.

Read its placeholder, the supplied context, and every supplied image. Preserve
the original text under Report / Captured context. Write a concise title and
write Report / Summary as the lightly rewritten original prompt defined by the
contract. Turn the remaining evidence into a usable report without diagnosing
the code or inventing missing facts.

You may update only:
- title in ticket metadata and the H1
- capture_state
- Report
- updated_at
- the capture entry in History

Keep status as backlog. Do not update resolution, cycle, resume_status,
capture_owner, orchestrated_run, duplicate_of, duplicates, related_defects,
Triage, Resolution, Automated product checks, User review, or Orchestrated-run
links. Keep ticket YAML valid and quote a title containing a colon or another
YAML-significant character.

Separate observed facts, expectations, labelled inferences, and unknowns. Use
unknown when the context does not establish an answer. Include partial
reproduction steps when useful and mark them partial. Link evidence and state
what each item shows.

Start Expected behavior with `Authority: user-stated`,
`Authority: defect-implied`, or `Authority: unknown` under the contract. Treat
clear defect language as committing its minimum corrected state and prefer
`defect-implied` for a missing, absent, broken, incorrect, or unexpectedly
different observable. "Missing icon" means an icon should be present. Which
icon remains an implementation detail and does not make outcome authority
unknown.

Set capture_state to ready when the report faithfully represents the supplied
context. If the ticket cannot be made usable, retain the original context, set
capture_state to failed, and record the reason in History.

Return with the completed file path and capture_state. Do not create another
ticket or inspect the project.
```

## Amendment-writer assignment prompt

Use this prompt when the user adds context to an existing ready defect:

```text
You are appending context to one existing defect ticket. You own only the
assigned defect file.

Read the existing ticket, the new supplied context, and every new supplied
image. Append a timestamped entry under Additional context. Preserve the new
text without paraphrasing in that entry, link new evidence, and add a concise
synthesis only when it does not replace or contradict the existing Report.
State whether the amendment contains a `user-stated`, `defect-implied`, or
`unknown` expected outcome, using the same minimum-outcome rule as the Report.
Do not change the Report; later run readers treat a confirmed amendment outcome
as equal to confirmed Expected behavior.

You may update only:
- Additional context
- updated_at
- the amendment entry in History

Do not change title, status, capture_state, capture_owner, resolution, cycle,
resume_status, orchestrated_run, duplicate_of, duplicates, related_defects,
Triage, Resolution, Automated product checks, User review, Orchestrated-run
links, or earlier Report content. If the amendment cannot be written, preserve
the existing ticket unchanged and return the reason. The coordinator records
the failed assignment and clears capture_owner.

Return with the file path and whether the amendment was appended. Do not create
another ticket or inspect the project.
```

## Status lifecycle

`backlog` means the defect has not been triaged. It is triage-eligible only
while `capture_state: ready`, `capture_owner: null`, and no unresolved Research
ticket already owns triage for its current cycle.

`triaged` means Research has established an actionable understanding or a
supported non-fix disposition, recorded `duplicate_of`, `duplicates`, and
related-defect evidence where applicable, identified likely project areas, and
drafted and classified the next work.

`in progress` starts only when an implementation Agent Task becomes active.
Plan, Plan Review, Research, and Explore Options do not cause this transition.

`blocked` is a detour, not a required sequential phase. Use it only when no
ready or active path can advance the defect. Record the prior state in
`resume_status`, the blocker, and the orchestrated-run ticket that owns its
resolution. Recompute the appropriate projection from current run tickets and
clear `resume_status` when the blocker closes.

`awaiting automated review` means all implementation work for the current
cycle has resolved and the dedicated automated product check or boundary
validation is queued.

`automated reviewing` means the dedicated product check or boundary validation
is active.

`awaiting user review` means the dedicated product check and boundary
validation have returned without evidence requiring remediation. An
inconclusive product check may advance here when it could not safely create
the required scenario; record and surface that gap.

`surfaced for user review` means the defect's current boundary-inspection
Discuss ticket has `presentation: presented`. When that ask is withdrawn,
recompute the defect status from the withdrawal reason; do not leave it
surfaced.

`failed review` means an automated check observed that the result is absent or
incorrect, boundary validation found a material issue, or the user requested
changes. Keep this status while scheduling it like backlog. After every
in-flight check for the prior cycle returns, start one new Research ticket
using all review evidence and increment `cycle` once. Preserve earlier ticket
evidence and apply orchestrated-run's inspection-invalidation lifecycle to
upcoming or presented inspection.

`done` means the defect has a supported resolution and the orchestrated run has
the evidence required for that resolution. Fixed defects require completed
implementation coverage and user acceptance. A duplicate stays `triaged` until
the canonical defect is done and its goal verification explicitly covers the
duplicate's reported scenario; for a fixed canonical defect, its automated
product check and user inspection both name the duplicate ID and scenario.
Other non-fix dispositions require evidence and use Discuss whenever the normal
product-decision test finds reasonable alternatives. `wont-fix` is a product
decision unless the user already made it.

A later finding may invalidate `done`. Record why, clear resolution when
appropriate, set `failed review`, and start another cycle rather than rewriting
the earlier evidence.
