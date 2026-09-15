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

Create pages from the bundled templates:

- copy `templates/ask-index.html` to `asks/index.html` when the run first needs
  an ask page;
- copy `templates/ask-detail.html` to `asks/<ticket-id>.html` for each human
  ticket.

Both are static, self-contained HTML with relative links. Their local inline
renderer is part of the template. Do not add an external script, network
request, build step, server, dependency, or install. The ask pages themselves
are not a prepared human environment. A preview, service, artifact, or other
resource the ask refers to still follows prepared-human-environment rules.

## Template data

Each template starts with one `ORCHESTRATOR DATA` object. Copy the template,
then edit only that object. Do not regenerate the styles, markup, or renderer
for routine ask changes.

`ask-index.html` has one `ledgerData.asks` array. Keep one record per relevant
human ticket and change its `presentation` value as the ticket moves through
`presented`, `upcoming`, `answered`, or `withdrawn`. The renderer:

- makes only `presented` records live table rows;
- lists `upcoming` records separately without presenting their full ask;
- omits `answered` and `withdrawn` records from the index;
- derives counts and the oldest-ask age;
- shows the run-complete line when `run.complete` is `true`.

`ask-detail.html` has one `askPageData` object. The one-sentence summary,
resources, ordered sections, steps, commands, expected reply, ticket metadata,
and presentation lifecycle all live in that object. `ask.summary` carries that
sentence and `ask.why` why the ask matters to the user. `expectedReply.body`
states what the returned result must contain. Its examples omit the ask ticket
ID because the renderer displays and copies each as `<ask-ticket-id>: <reply>`.
For a finite choice, include one complete reply example per option.
For Human and Agent Task, replace the current ask data rather than appending
earlier turns.

For a grouped inspection, put every covered implementation ticket in
`ticket.covered`, group each result with its recorded outcomes into ordered
sections, and put useful complete replies in `expectedReply.examples`. The
template makes the ask ID, covered IDs, and each example response individually
copyable.

Keep data as plain text. Do not add HTML, executable values, secret values, or
unsupported information to either object. If the template or renderer itself
needs changing, fix the bundled template first and then replace affected run
pages from ticket state.

## Source of truth

Build the page mechanically from:

- Objective for Discuss/Gather Inputs and Human Task;
- the latest Interaction log entry for Human and Agent Task;
- Presentation for prepared-environment evidence, liveness, and ask-page path;
- ticket YAML for ID, type, presentation state, and related goal or module IDs.

Do not add findings, evidence, options, procedures, or conclusions that are not
already on tickets or run files. If an ask page and its ticket disagree, the
ticket is correct. Update its template data before the next user-visible
message.

The secret-values ban applies to the index and every ask page.

## Writing the ask

Write every ask for a reader who has only that ask. Name the thing, describe in
observable terms what it now does for the user, and state what is being decided
or done, without needing the ticket, the module, chat history, or the run.
Restating a name or label as its own purpose describes nothing.

When the ask needs judgement, state exactly what to inspect or compare and
which observable results distinguish the possible replies. For a decision,
describe what the user would observe under each option, its known knock-on
effects for later development, compatibility, or scope, and whether it can be
deferred to a named later goal, module, or project-plan step. Say why it must be
decided now when deferral is unsafe or would block current work. Use only
recorded evidence; if these consequences are not known, prepare them before
making the ticket `ready`.

Lead with one sentence stating the ask in the words the user uses for their own
product, then give the detail under it. Technical terms belong in an ask whose
product or judgement is technical; say what one means for the product when that
is not already plain.

Do not ask the user to judge an aggregate from its name. `Accept module 04 is
complete` fails because it says nothing about what that module was meant to
deliver. Name the aggregate when it helps, then state each result being judged.

Never ask the user to accept an artifact that exists only for agents, such as an
evidence file or a change plan. When a document, report, design, or prepared environment is
itself the deliverable, ask about what it gives the user: say what it holds, why
it exists, and when it will matter.

A Human and Agent Task turn after the first is the current observation or step,
what to look at, and the expected reply. It does not restate the task.

## Per-ticket page

One page represents one human ticket. It contains:

- full ticket ID, type, and ticket path;
- every covered implementation ticket ID for a grouped inspection;
- the one-sentence summary of the ask;
- the complete current return-to-user ask for that type;
- why the ask matters to the user, from the ticket's Objective, never the
  process or Interactive reason, except the planning-depth offer, whose subject
  is how the run works;
- what to inspect or compare and which results distinguish the available
  replies;
- any prepared resource path or URL and its current state;
- the expected reply, result, or evidence;
- the presentation state and time recorded in Presentation.

For acceptance, include the exact result or path, inspection method, what
successful and change-needed results look like, acceptance basis, and request
to accept or describe changes.

For Human and Agent Task, the page contains only the current ask from the latest
Interaction log entry, not previous turns.

## Index

`index.html` has one live table row per ticket with
`presentation: presented`. Include:

- `action`, holding a presented ask page's summary sentence verbatim, or a
  short involvement label for an upcoming record;
- why the ask matters to the user;
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
3. copy the bundled template only when the page file is missing, then populate
   or replace its `ORCHESTRATOR DATA` object;
4. set `presentation: presented`;
5. add or update its record in the index data so it becomes a live row;
6. best-effort launch the absolute `asks/<ticket-id>.html` path, or
   `asks/index.html` when presenting several asks at once, in the default
   external browser with `open` on macOS, `Start-Process` on Windows, or
   `xdg-open` on Linux; do not use Cursor's file opener for HTML, wait, verify,
   retry, or treat launch failure as a blocker. Launch again when a withdrawn
   ask is re-presented. Do not record this external launch as a successful open
   in the current client. Do not launch again for each Human and Agent Task turn;
7. send the complete first ask in chat with links to the page and index.

When a Human and Agent Task produces a new current ask, update its page and
index row before presenting that ask.

Whenever presentation leaves `presented`, change the index record's
`presentation`; the renderer removes its live row. When a Human and Agent Task
changes to `upcoming` while the orchestrator works, update the detail data so
the page says it is not awaiting a reply. When presentation becomes `answered`,
mark the detail data answered and record the answer time in Presentation. When
it becomes `withdrawn`, mark the detail data withdrawn with its time and reason
and record both in Presentation. Keep those pages as presentation history; a
late response to a withdrawn page cannot complete the ticket.
Re-presentation replaces the detail data with the new current ask and changes
the index record to `presented`.

Every withdrawal of a presented ask sets ticket YAML presentation to
`withdrawn`, removes the live row, marks the page withdrawn, records the reason
and time in Presentation and `LOG.md`, and tells the user that the previous ask
is no longer actionable. The cause-specific process also sets ticket status,
owner, and dependencies before new work starts.

Keep `index.html` even when no live rows remain so its path is stable.

## Chat contract

First presentation of an ask remains complete in chat. A link alone is not a
presentation.

Build it from the ticket, not earlier chat. Writing the ask governs every type
below; each list is the extra payload that type carries, not a substitute:

- Human Task: what to do, applicable steps, commands, URLs and paths, expected
  result, evidence to return, ticket path, and evidence-backed hints or
  recovery steps when they apply.
- Discuss/Gather Inputs: the question or decision, essential context, options
  and recommendation when present, each option's observable behavior, known
  knock-on effects and deferral point or reason it must be decided now,
  expected reply, and ticket path.
- Planning depth offer: what reviewed planning changes about how the run
  reaches the user's result, the recorded conditions this run met, the cost as
  the planning and review work it adds before implementation, that change
  plans are agent-facing and require no user sign-off, the recommendation, and
  the ticket path.
- Acceptance: exact result or path, inspection method, successful and
  change-needed observations, acceptance basis, request to accept or describe
  changes, and ticket path.
- Grouped acceptance: group each result and its recorded evidence under its
  covered ticket IDs, then request one reply accepting all or naming IDs
  needing changes. Do not list checks for the user to perform.
- Human and Agent Task: only the current ask from its latest Interaction log
  entry under that type's contract.

Do not add unsupported hints. Do not paste ticket metadata, Reads, related run
IDs, or the process reason. The planning-depth offer is the single exception. Acceptance is not an options question; present it
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
the index and pages from the bundled templates using Objective, the latest
Interaction log entry, and Presentation before another user-visible message.
Never infer presentation state or the current ask from HTML alone.
