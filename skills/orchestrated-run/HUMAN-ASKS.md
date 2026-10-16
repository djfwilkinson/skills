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

Store ask pages under the run. Each open run is registered in the device-level
action ledger:

```text
<run>/asks/
  T-005-DIS.html
  T-006-HUM.html
~/.agent-runs/action-ledger/
  index.html          ask index, copied from templates/ask-index.html
  port, pid           the ledger server's last port and process
  runs/<key>.json     one registration per open run
```

`<key>` is `<project folder name>--<run folder name>`.

The orchestrator writes `asks/` as process work, like `LOG.md`. A subagent must
never create, edit, or delete these files or a registration.

Copy `templates/ask-detail.html` to `asks/<ticket-id>.html` for each human
ticket. Ask pages are static, self-contained HTML with an inline renderer. A
page the ledger serves also polls `/runs` for its unsettled checks. Opened as a
file or a copy, it is not live and shows only the unsettled snapshot written
into its data.

The ask index is shared by every run on the device. Use this skill's
`scripts/ledger.py` with Python 3.9 or later:

- `python3 <skill>/scripts/ledger.py register <run-dir>` registers the run,
  then starts the ledger and prints the index URL. It is safe to repeat.
- `python3 <skill>/scripts/ledger.py complete <run-dir>` removes the
  registration.

Starting the ledger creates its directory and index when missing, replaces the
index when the template's `ledger-version` is higher than the installed one,
and starts the ledger server in the background unless the same or a newer
server is running. It replaces an older server. The server listens on
`127.0.0.1` only, keeps using the port in `port`, and moves to the next free
port in its range when another program holds it. Never edit the device
`index.html` or a registration by hand. Beyond the bundled ledger script and
templates, do not add any other script, network request, build step, server,
dependency, or install.

Ask pages and the ledger are not a prepared human environment. A preview,
service, artifact, or other resource the ask refers to still follows
prepared-human-environment rules.

## Template data

`ask-detail.html` starts with one `ORCHESTRATOR DATA` object. Copy the
template, then edit only that object. Do not regenerate the styles, markup, or
renderer for routine ask changes.

The ledger server derives every registered run's asks from its files; the
orchestrator writes no ask records for it. It reads ticket YAML `presentation`,
`status`, `type`, and `title` from `tickets/`, plus `may_withdraw_on` and the
`status` and `title` of the tickets it names, and `ask.summary`, `ask.why`, and
`presentation.presentedAt` from the ticket's ask page. The index polls every 5
seconds and on Refresh. It:

- makes a live row of each ticket with `presentation: presented` that is not
  `resolved` or `cancelled`;
- lists `upcoming` tickets separately by summary, or title before a page
  exists, without presenting their full ask;
- omits every other ticket;
- derives counts, the oldest-ask age, and links to `asks/<id>.html` and
  `tickets/<id>.md`;
- skips a registered run whose directory no longer exists;
- marks a run as looking complete when every `GOALS.md` status is `achieved` or
  `abandoned` and no ask is open, and offers the user a button that removes its
  registration, as `complete` does. That is the user's choice, not run
  completion; a run still in progress registers again at its next ask;
- shows "May change" with a count on a live row while any ticket in its
  `may_withdraw_on` is not `resolved` or `cancelled`, or cannot be read;
- when the user opts in, raises one browser notification for each newly
  presented ask found while the page is in the background, labelled "May
  change" when the ask is unsettled, and one more when that ask stops being
  unsettled while still presented.

Notifications are a convenience for the user. They never replace the complete
first presentation in chat or count as a successful open in the current client.

`ask-detail.html` has one `askPageData` object. The one-sentence summary,
resources, ordered sections, steps, commands, expected reply, ticket metadata,
and presentation lifecycle all live in that object. `ask.summary` carries that
sentence and `ask.why` why the ask matters to the user. `expectedReply.body`
states what the returned result must contain. Its examples omit the ask ticket
ID because the renderer displays and copies each as `<ask-ticket-id>: <reply>`.
For a finite choice, include one complete reply example per option.
For Human and Agent Task, replace the current ask data rather than appending
earlier turns. `ticket.mayWithdrawOn` mirrors the ticket YAML IDs as history.
`presentation.unsettled` is a snapshot, `{ at, checks }`, recomputed from
current ticket statuses on every page-data write with the ledger's rules: `at`
is the ISO write time and `checks` holds each listed ticket not `resolved` or
`cancelled` as `{ id, title, status }`, with `status: null` when it cannot be
read. It is what a file or copy shows.

For a grouped inspection, put every covered implementation ticket or unit in
`ticket.covered`, group each result with its recorded outcomes into ordered
sections, and put useful complete replies in `expectedReply.examples`. The
template makes the ask ID, covered IDs, and each example response individually
copyable.

Keep data as plain text. Do not add HTML, executable values, secret values, or
unsupported information to the detail object. Keep its `ask.summary`, `ask.why`,
and `presentation.presentedAt` values double-quoted strings on one line so the
index can read them. If a template
or renderer itself needs changing, fix the bundled template first, then replace
affected run pages from ticket state. Raise `templateVersion` with every change
to `ask-detail.html`. A change to `ask-index.html` also raises its
`ledger-version` so the next `scripts/ledger.py` run replaces the device
index.

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

The secret-values ban applies to every ask page and ticket title.

## Writing the ask

Write every ask for a reader who has only that ask. Name the thing, describe in
observable terms what it now does for the user, and state what is being decided
or done, without needing the ticket, the module, chat history, or the run.
Restating a name or label as its own purpose describes nothing.

When the ask needs judgement, state exactly what to inspect or compare and
which observable results distinguish the possible replies. Explain every
proposal, option, and consequence in as few plain words as possible while
keeping the picture complete; let the user reply `detail <item>` when they want
deeper evidence or knock-on traces on a specific item before deciding. For a
decision, describe what the user would observe under each option, its known
knock-on effects for other product areas, later development, compatibility, or
scope, and whether it can be deferred to a named later goal, module, or
project-plan step. Say why it must be decided now when deferral is unsafe or
would block current work. When an ask presents a mock or concept from
`<run-dir>/mocks/`, link its served URL (`<index URL>r/<key>/mocks/<file>`) in
`askPageData.resources` and chat, and state its mock contract (`Fidelity:
wireframe | sign-off`, what is `Binding`, and what is `Context only`
scaffolding that will not be built or tested against). Use only recorded
evidence; if these consequences or mocks are not known, prepare them before
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

Put a result to the user only when it is product-facing, as defined under
Reconciliation in SKILL.md. Do not present code, tests, configuration, or docs
outside the product as items to review or judge, and do not offer a diff as an
inspection method; an agent boundary inspection accepts them. When a batch has
no product-facing result, it has no human ask. `Nothing visible changes, so the
judgement is on the code and docs` fails for that reason.

A Human and Agent Task turn after the first is the current observation or step,
what to look at, and the expected reply. It does not restate the task.

## Per-ticket page

One page represents one human ticket. It contains:

- full ticket ID, type, and ticket path;
- every covered implementation ticket ID for a grouped inspection;
- the one-sentence summary of the ask;
- the complete current return-to-user ask for that type;
- why the ask matters to the user, from the ticket's Objective, never the
  process or Interactive reason, except the model ask, whose subject is how
  the run works;
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

The ask index has one section per registered run, each with its own live table
and upcoming list. Each live row shows:

- the ask page's summary sentence;
- why the ask matters to the user;
- ticket ID, linked to the ticket, and type;
- a "May change" tag and check count while the ask is unsettled;
- presentation time;
- a link to the ask page.

Do not describe `upcoming` tickets as waiting. The index may list upcoming
human involvement in a separate section, but it must not present the ask or
imply that the user can complete it yet.

## Lifecycle

Immediately before first presentation:

1. perform the allowed liveness check;
2. record the page path, source, liveness result, and presentation time in
   Presentation;
3. copy the bundled template when the page file is missing or its
   `templateVersion` is lower than the bundled template's, then populate or
   replace its `ORCHESTRATOR DATA` object. Apply the same rule wherever page
   data is updated;
4. set `may_withdraw_on` under Unsettled asks, mirror it into
   `ticket.mayWithdrawOn`, and write `presentation.unsettled`;
5. set `presentation: presented`, which makes it a live row;
6. run `scripts/ledger.py register <run-dir>`; the ledger's notifications tell
   the user the ask is waiting. Do not open the ask page or index in a browser,
   wait, verify, retry, or treat a script failure as a blocker;
7. send the complete first ask in chat with links to the page and the ledger
   index, using the served URLs when the script succeeded and the absolute page
   path otherwise.

Every later user-visible message that mentions an open ask, including each
condensed line and every model text output that reports run progress while an
ask is open, repeats a clickable link to the ledger index so the user can open
it when it is not already open.

When a Human and Agent Task produces a new current ask, update its page before
presenting that ask.

Whenever presentation leaves `presented`, the index drops the live row on its
own; the ask page still needs updating. When a Human and Agent Task
changes to `upcoming` while the orchestrator works, update the detail data so
the page says it is not awaiting a reply. When presentation becomes `answered`,
mark the detail data answered and record the answer time in Presentation. When
it becomes `withdrawn`, mark the detail data withdrawn with its time and reason
and record both in Presentation. Keep those pages as presentation history; a
late response to a withdrawn page cannot complete the ticket.
Re-presentation replaces the detail data with the new current ask.

Every withdrawal of a presented ask sets ticket YAML presentation to
`withdrawn`, marks the page withdrawn, records the reason
and time in Presentation and `LOG.md`, and tells the user that the previous ask
is no longer actionable. The cause-specific process also sets ticket status,
owner, and dependencies before new work starts.

Keep the run registered while it is open, even when it has no live rows. Run
`scripts/ledger.py complete <run-dir>` when the run completes.

## Unsettled asks

A presented ask is unsettled while any ticket in its `may_withdraw_on` is not
`resolved` or `cancelled`, or cannot be read. The ledger derives this. It is not
a presentation state, and settling does not withdraw, re-present, or rewrite
anything.

Set the field immediately before first presentation. List only unresolved agent
tickets whose result could withdraw that exact ask, never unrelated running
work, and write full ticket IDs such as `T-011-REV`; the shorthand `T-011` reads
as status unavailable. Write it as a one-line inline list. A block list or a
trailing comment reads as unavailable, never as safe. You may append an ID while
the ask is presented, and must then update the page data, snapshot included,
before the next user-visible message. Remove an ID only to correct a mistaken
entry, and log that in `LOG.md`. A settled link stays listed as presentation
history. On an `upcoming` ticket the field may be prepared but is not shown.

What the user sees: on a ledger-served page, a notice naming each open check
with its ID, name, and status, and a warning above the reply; on the index, the
"May change" tag and two notifications. Only the served page is live. A file or
copy shows the snapshot from when its data was written. An open page whose ask
has left `presented`, or been presented again, hides the notice, the warning,
and the reply, and asks the user to reload. Clearing needs no page or ticket
write.

Reply intake for a presented Discuss or Human Task ask with a non-empty
`may_withdraw_on`, in order:

1. record the raw reply in Evidence;
2. reconcile every return already received for a listed ticket;
3. re-read the ask's presentation and every listed status;
4. if the ask is `withdrawn`, the reply is steering or new evidence and does not
   complete the ticket;
5. if every listed ticket is `resolved` or `cancelled`, handle the reply
   normally;
6. otherwise accept it as a provisional answer: record "provisional pending
   <IDs>" in Evidence, mark the presentation answered, and reconcile.

A return that arrives after this check is late invalidation. It cannot erase
the recorded reply.

Provisional answers:

- They never count as human acceptance, implementation coverage, or goal
  verification until every listed ticket is `resolved` or `cancelled` without
  invalidating the ask.
- Whenever a listed ticket's status changes to `resolved` or `cancelled`, for
  any reason (a reconciled return, or a cancellation without a return), check
  the human ticket. If every listed ticket is now `resolved` or `cancelled` and
  no invalidation is recorded, record `provisional cleared <time>` in the human
  ticket's Evidence and in `LOG.md`.
- Before coverage, goal verification, or run completion uses a provisional
  answer that has no `provisional cleared` record, check the same condition and
  write the record first when it holds.
- Supersession follows the late-invalidation rule in SKILL.md for a provisional
  answer. A superseded provisional decision is steering that invalidates work in progress: send
  `hold` or `stop` to the active dependents built on it, apply accepted-plan
  supersession where a change plan used it, and re-ask in a new Discuss.

Withdrawal precedence: a listed result that invalidates a presented ask uses the
existing withdrawal flow and the cause-specific process. `withdrawn` hides the
notice, the reply, and the row.

Inspection freeze: listing a ticket does not exempt it from a presented
inspection's freeze. Findings follow the existing withdraw-then-fix order.

Specializations: listing a ticket never permits presenting earlier than a
governing skill's stricter gate.

Human and Agent Task: the field drives the display and the withdrawn re-check
only. A turn is an interaction, not a return, so it is never marked provisional
and needs no `provisional pending` or `provisional cleared` record.

## Chat contract

First presentation of an ask remains complete in chat. A link alone is not a
presentation.

Build it from the ticket, not earlier chat. Writing the ask governs every type
below; each list is the extra payload that type carries, not a substitute:

- Human Task: what to do, applicable steps, commands, URLs and paths, expected
  result, evidence to return, ticket path, and evidence-backed hints or
  recovery steps when they apply.
- Discuss/Gather Inputs: the question or decision (and any wholesale product
  proposal), essential context, options and recommendation when present, each
  option's observable behavior, known knock-on effects and deferral point or
  reason it must be decided now, any linked mock URL with its `Fidelity` and
  `Binding` versus `Context only` boundary, expected reply (including `accept`
  / `recs` and `detail <item>` where applicable), and ticket path.
- Model ask: the payload under The model ask in `PERSONAS.md`, with the
  personas as one ordered section, one complete reply example each for `lean`,
  `quality`, naming a model and effort for a persona, and excluding a model,
  and the ticket path.
- Acceptance: exact result or path, inspection method, successful and
  change-needed observations, acceptance basis, request to accept or describe
  changes, and ticket path.
- Grouped acceptance: group each product-facing result and its recorded
  evidence under its covered ticket or unit IDs, then request one reply
  accepting all or naming IDs needing changes.
- Grouped decisions: number each decision, give each its own options,
  observable behaviour, knock-on effects, and recommendation, then request one
  reply answering each by number. Do not list checks a subagent can run for the
  user to perform; a product workflow the user runs to judge behaviour is the
  inspection method, not such a check.
- Human and Agent Task: only the current ask from its latest Interaction log
  entry under that type's contract.

For an unsettled ask:

- First presentation adds one sentence: the ask can be answered now and may be
  withdrawn if a named check (ID and title) finds a problem. For a Discuss or
  Human Task it also says a reply given now is provisional. A Human and Agent
  Task turn does not.
- The condensed line adds that it may change and names the open IDs.
- Each message re-derives this from current ticket statuses, because chat cannot
  clear itself.
- Acknowledging a provisional reply to a Discuss or Human Task says it is
  provisional until the named checks finish.
- Send no all-clear message.

Do not add unsupported hints. Do not paste ticket metadata, Reads, related run
IDs, or the process reason. The model ask is the only exception. Acceptance is not an options question; present it directly and
wait for the user's reply.

After that same ask has been presented once, later user-visible messages may
replace the full repeat. The condensed line for each presented ticket
contains:

- the action and its object;
- the ticket path;
- a working link to the per-ticket page, and the ledger index link.

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
and one index link.

Each Human and Agent Task turn has a new ask. Present that current ask under its
type contract and refresh the page. A later unrelated progress message may use
the condensed line only when that exact ask has already been presented.

## Recovery

After compaction, reload every presented human ticket first. Rebuild or repair
its pages from the bundled template using Objective, the latest Interaction log
entry, Presentation, and `may_withdraw_on` before another user-visible message.
A page whose `templateVersion` is lower than the bundled one counts as stale. Never infer
presentation state or the current ask from HTML or the index alone.
