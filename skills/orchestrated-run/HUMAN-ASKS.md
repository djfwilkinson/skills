# Human ask pages

This file is part of the `orchestrated-run` contract. Read it before every
human-ticket presentation state change and after compaction when any human
ticket is presented. It is not a skill and must not be invoked.

## Purpose

Chat may bury a complete return-to-user ask when the orchestrator continues the
run. Durable ask pages keep every current ask actionable without requiring the
orchestrator to paste the full procedure into every later progress message.

Ask pages do not replace human tickets, presentation state, or first
presentation in chat. They are derived presentation artifacts. Tickets remain
the source of truth.

## Layout and ownership

Store ask pages under the run:

```text
asks/
  index.html
  T-005-DIS.html
  T-006-HUM.html
```

The orchestrator writes `asks/` as process work, like `LOG.md`. A subagent must
never create, edit, or delete these files.

Use static, self-contained HTML with relative links. Do not require a build
step, server, dependency, script, or install. The ask pages themselves are not
a prepared human environment. A preview, service, artifact, or other resource
the ask refers to still follows prepared-human-environment rules.

## Source of truth

Build the page mechanically from:

- Objective for Discuss/Gather Inputs and Human Task;
- the latest Interaction log entry for Human and Agent Task;
- Presentation for prepared-environment evidence, liveness, and ask-page path;
- ticket YAML for ID, type, presentation state, and related goal or module IDs.

Do not add findings, evidence, options, procedures, or conclusions that are not
already on tickets or run files. If an ask page and its ticket disagree, the
ticket is correct. Rewrite the page before the next user-visible message.

The secret-values ban applies to the index and every ask page.

## Per-ticket page

One page represents one human ticket. It contains:

- full ticket ID, type, and ticket path;
- the complete current return-to-user ask for that type;
- why the ask is required, using the ticket's Objective or Interactive reason;
- any prepared resource path or URL and its current state;
- the expected reply, result, or evidence;
- the presentation state and time recorded in Presentation.

For acceptance, include the exact result or path, inspection method, acceptance
basis, and request to accept or describe changes.

For Human and Agent Task, the page contains only the current ask from the latest
Interaction log entry, not previous turns.

## Index

`index.html` has one live table row per ticket with
`presentation: presented`. Include:

- the action and its object in one sentence;
- why the ask is required;
- ticket ID and ticket path;
- type;
- presentation time;
- a link to the per-ticket page.

Do not describe `upcoming` tickets as waiting. The index may list upcoming
human involvement in a separate section, but it must not present the ask or
imply that the user can complete it yet.

## Lifecycle

Immediately before first presentation:

1. perform the allowed liveness check;
2. record the page path, source, liveness result, and presentation time in
   Presentation;
3. write or replace the per-ticket page;
4. set `presentation: presented`;
5. add or update its live index row;
6. when the client supports local files, open the page or index
   non-mutatingly and record success or failure in Presentation;
7. send the complete first ask in chat with links to the page and index.

When a Human and Agent Task produces a new current ask, update its page and
index row before presenting that ask.

Whenever presentation leaves `presented`, remove the live index row. When a
Human and Agent Task changes to `upcoming` while the orchestrator works, mark
the page not awaiting a reply. When presentation becomes `answered`, mark the
page answered and record the answer time in Presentation. When it becomes
`withdrawn`, mark the page withdrawn and record the withdrawal time and reason
in Presentation. Keep those pages as presentation history; a late response to
a withdrawn page cannot complete the ticket. Re-presentation replaces the page
with the new current ask and adds a new live row.

Every withdrawal of a presented ask sets ticket YAML presentation to
`withdrawn`, removes the live row, marks the page withdrawn, records the reason
and time in Presentation and `LOG.md`, and tells the user that the previous ask
is no longer actionable. The cause-specific process also sets ticket status,
owner, and dependencies before new work starts.

Keep `index.html` even when no live rows remain so its path is stable.

## Chat contract

First presentation of an ask remains complete in chat. A link alone is not a
presentation.

Build it from the ticket, not earlier chat:

- Human Task: what to do, applicable steps, commands, URLs and paths, expected
  result, evidence to return, ticket path, and evidence-backed hints or
  recovery steps when they apply.
- Discuss/Gather Inputs: the question or decision, essential context, options
  and recommendation when present, expected reply, and ticket path.
- Acceptance: exact result or path, inspection method, acceptance basis,
  request to accept or describe changes, and ticket path.
- Human and Agent Task: only the current ask from its latest Interaction log
  entry under that type's contract.

Do not add unsupported hints. Do not paste ticket metadata, Reads, related run
IDs, or the process reason. Acceptance is not an options question; present it
directly and wait for the user's reply.

After that same ask has been presented once, later user-visible messages may
replace the full repeat only when Presentation records that the orchestrator
successfully opened the local page or index in the current client. The
condensed line for each presented ticket contains:

- the action and its object;
- the ticket path;
- a working link to the per-ticket page or ask index.

A reader who does not open the link must still know what action is requested
and what it applies to. These are invalid even with an index link:

- `still waiting`;
- `as above`;
- `previously requested`;
- `T-012 is still open for user review`;
- `waiting for user review(s)`.

Present several human tickets together only when their complete first
presentations remain usable. Otherwise present one and leave the others
`upcoming`. For several presented tickets, use one condensed line per ticket
and one index link, or the complete asks when the link check does not permit the
condensed form.

If that client check is absent or fails, repeat the complete ask in chat.

Each Human and Agent Task turn has a new ask. Present that current ask under its
type contract and refresh the page. A later unrelated progress message may use
the condensed line only when that exact ask has already been presented.

## Recovery

After compaction, reload every presented human ticket first. Rebuild or repair
the index and pages from Objective, the latest Interaction log entry, and
Presentation before another user-visible message. Never infer presentation
state or the current ask from HTML alone.
