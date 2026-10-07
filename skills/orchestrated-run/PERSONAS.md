# Personas

This file is part of the `orchestrated-run` contract. Read it before building
or changing the roster, choosing a persona for a ticket, or dispatching or
resuming a persona session. It is not a skill and must not be invoked.

A persona is a standing role that executes agent tickets of exactly one ticket
type. Each persona has a model tier, a model the user confirms in the roster,
and a brief copied into every assignment prompt for it. A ticket type may have
several personas of different complexity; the orchestrator picks one persona
for each ticket.

At most one ticket per persona is active at a time. Parallelism comes from
different personas working at once, not from several copies of one persona.
Human tickets have no persona; the orchestrator handles them.

## Persona table

| Persona | Ticket type | Use for | Tier | Model needs |
| --- | --- | --- | --- | --- |
| `scout` | Research | `triage` and `surface` units that do not pre-authorise deep escalation: lookups across known paths, inventories, bootstrap when the request already states its outcome, acceptance basis, and paths | economy | reliable tool use and fast reading; low reasoning |
| `investigator` | Research | `deep` units and `surface` units that pre-authorise deep escalation: unclear project structure, cross-cutting hunts, sources that conflict, gaps a scout returned | balanced | long context, careful reading; medium to high reasoning |
| `options-analyst` | Explore Options | alternatives, prototypes, reproductions, and debugging experiments whose result is a recommendation | balanced | coding and trade-off reasoning |
| `architect` | Plan | change plans under reviewed planning | frontier | strongest reasoning, long context |
| `consequences-critic` | Plan Review, `consequences` lens | whether a change plan's choices hold, what else must change, ordering, compatibility, and migration risk | frontier | strongest reasoning about code and systems |
| `product-critic` | Plan Review, `product` lens | whether a change plan reaches the cited goals, acceptance criteria, and canonical sections | balanced | careful reading against requirements |
| `fixer` | Agent Task | work classified `trivial`: copy, config values, a rename in one area, an already-specified small fix, and environment preparation | economy | reliable tool use and edits; low reasoning |
| `builder` | Agent Task | implementation classified `following an established project pattern` | balanced | strong coding |
| `senior-engineer` | Agent Task | implementation classified `moderately complex or higher`, or naming a schema, persistence layer, public API, protocol, data migration, or canonical doc; units a builder escalated | frontier | strongest coding and design reasoning |
| `inspector` | Agent Task, agent boundary inspection | per-unit acceptance of code, tests, configuration, and docs outside the product while implementation continues | balanced | careful reading of diffs against requirements |
| `validator` | Agent Task, boundary validation | goal-level, repo-wide, and cross-area checks: tests, builds, lint, typecheck, scripted scenarios | economy | reliable command running and result reporting |
| `scenario-tester` | Agent Task | check-producing work that exercises the actual product through a browser, CLI, preview, or prepared artifact, including a defect run's automated product check | balanced | tool use; vision when the product is visual |
| `ux-reviewer` | Agent Task | an Agent Task whose result is a UX/UI review, following the `ux-ui-reviewer` skill | balanced | vision and interface judgement |
| `reviewer` | Adversarial Review | completed work of ordinary risk at a run module boundary | balanced | adversarial reading and reasoning |
| `principal-reviewer` | Adversarial Review | the pre-completion review; high-impact or cross-cutting work; review after unexpected test or debugging results or uncertain evidence | frontier | strongest adversarial reasoning, long context |

## Choosing a persona

Choose from the ticket type and the classification already recorded on the
proposing ticket. Do not re-investigate to choose.

- Research: `scout` for `triage` and for `surface` without pre-authorised
  escalation; `investigator` otherwise. A scout that cannot meet a unit's
  Completion records the gap and requests deep; add that gap as an
  investigator unit.
- Agent Task implementation: `trivial` to `fixer`, `following an established
  project pattern` to `builder`, `moderately complex or higher` or a named
  schema, persistence layer, public API, protocol, data migration, or canonical
  doc to `senior-engineer`. A missing label goes to `builder` and is logged.
- Agent Task check or review work: `inspector` for agent boundary inspection,
  `validator` for boundary validation, `scenario-tester` for exercising the
  actual product, `ux-reviewer` for a UX/UI review result, `fixer` for a
  separate environment-preparation ticket. Preparation folded into an
  implementation, validation, or product-check ticket stays with that
  ticket's persona.
- Plan Review: the persona that matches the lens.
- Adversarial Review: `principal-reviewer` for the pre-completion review and
  for the escalation cases in the table; `reviewer` otherwise.

Every unit on one ticket needs the same persona. When a worker reclassifies a
unit above its persona, it records the new label and blocks that unit; move the
unit to a ticket for the matching persona. Moving work between personas is a
process decision. Never move work to a lower tier to save cost after a worker
recorded that it needs a higher one.

## Model tiers

A tier describes the capability a persona needs, not a model name. Model names
change; tiers do not.

- `economy`: the cheapest models that still use tools reliably and follow a
  structured prompt. Small, fast, or speed-tuned models, or a mid-size model
  at low reasoning.
- `balanced`: strong general coding and reasoning at moderate cost. A
  family's mid-size model, or its flagship at default reasoning.
- `frontier`: the strongest reasoning available. A family's flagship at high
  reasoning.

## Roster rows

Each roster row names a model family and version, an effort range, a preferred
effort, and a fallback. Availability changes between clients and over time,
so a row states what is acceptable rather than one exact variant.

Effort levels, lowest to highest: `low`, `medium`, `high`, `xhigh`. Use the
client's own level names when it has others, in its order. An effort range
such as `medium-xhigh` accepts every level from the first to the last. A single
level such as `high` accepts only that level. A client that offers a model
with no effort choice satisfies any range at that model's default; record the
effort as `default`.

The fallback says what to do when nothing in the range is available:

- a model and range, such as `<model> medium-high`: use it, resolved the same
  way;
- `suggest`: use the best available match under Resolving a row and report it;
- `ask`: hold that persona's work and ask the user.

`ROSTER.md` holds one default fallback for the whole roster. A row may override
it. The default is `suggest` unless the user chooses otherwise.

## Resolving a row

Resolve a persona's row each time a session starts for it, from the models the
client offers at that moment. A resumed session keeps the model and effort it
started with.

1. Take the row's model. If it offers the preferred effort, use it. Otherwise
   use the available level in the range nearest the preferred one; on a tie,
   take the higher level.
2. If the model is unavailable or offers no level in the range, apply the
   row's fallback, or the roster's default when the row has none.
3. For a fallback model and range, resolve it by step 1. If it also fails, ask.
4. For `suggest`, choose another model in the same tier, then the nearest
   tier above, using the same effort range, or the nearest level above it
   when none is in range. Never choose a lower tier or a level below the range
   without the user; ask instead.
5. For `ask`, open a roster-change Discuss for that persona. Its tickets wait;
   other personas continue. The ask names the row, what the client offers now,
   and a recommendation from step 4.

Record the model and effort each session started on in `ROSTER.md`. Report
every resolution that departs from the preferred model or effort in the next
progress update, and log it.

## Suggesting models

Build the recommended roster mechanically:

1. List the models the client lets the orchestrator choose for a subagent. If
   the client cannot choose a model per subagent, record every persona as
   `inherit` in `ROSTER.md`, note it in `LOG.md`, and skip the roster ask.
2. Remove models and modes the user's rules or the invocation exclude, such as
   modes the user has forbidden. Keep the latest version of each family unless
   the user named an older one.
3. Place each remaining model in a tier using what the client says about it:
   its description, its position in its family, and its reasoning level. When
   the client gives only names, place each by its family's naming (flagship,
   mid-size, small, or speed-tuned) and its reasoning suffix, and mark every
   such placement as inferred in the ask. Do not invent capabilities. When the
   placement is uncertain, say so in the ask.
4. For each persona, recommend the cheapest model in its tier that meets its
   model needs. If its tier has no model, use the nearest tier above and say
   so; never recommend a lower tier. Give it a preferred effort that matches
   the tier, and an effort range one level either side where the model's
   family usually offers those levels: for example, preferred `high` and range
   `medium-xhigh` for a frontier coder. Recommend `suggest` as the default
   fallback.
5. When `~/.agent-runs/persona-roster.md` exists, recommend each of its rows
   and its default fallback, show what each row resolves to on this client
   now, and apply steps 3 and 4 only to personas it lacks.

User-stated model choices always win. When the invocation already names
models for personas or one model for all, record them in `ROSTER.md` and ask
only about personas it left open.

The roster does not choose the orchestrator's model. That is the model the user
is already running.

## The roster ask

The roster is a process decision put to the user, like planning depth. Use one
Discuss ticket. Its ask, under Writing the ask in `HUMAN-ASKS.md`:

- says the run will use these personas and models, and that each later
  subagent uses its persona's model;
- shows every persona with what it is used for, its tier, and the recommended
  model, preferred effort, and effort range, from this file and step 4, and
  what each row resolves to on this client now;
- names the other available models and effort levels in each tier;
- asks for the default fallback, `suggest`, `ask`, or one fallback model and
  range, and says that any row may name its own;
- offers two shortcuts: `lean` moves every persona one tier down, with
  economy personas staying economy; `quality` moves every persona one tier
  up, with frontier personas staying frontier;
- says which persona and model any already-dispatched bootstrap uses;
- says when the client cannot run subagents in the background or resume them,
  and what that costs: no overlap between review and implementation, or a
  fresh session for every unit;
- asks for one reply: accept, a shortcut, or the persona rows to change.

On the answer, write the confirmed roster to `ROSTER.md` and to
`~/.agent-runs/persona-roster.md`, creating `~/.agent-runs/` when missing, and
log the source. Never ask for the whole roster twice in one run; the only later
roster asks are roster-change asks under Resolving a row. Later user steering
may change rows; record it in `ROSTER.md` and `LOG.md`. A change applies to
sessions started after it. A roster-change answer updates that row, and the
device default when the user says so.

## Persona sessions

A persona session is one subagent conversation for one persona. Its model and
effort are resolved from the roster row when the session starts; a resumed
session keeps them.

Session states, recorded in `ROSTER.md`:

- `running`: working on its active ticket;
- `parked`: returned at a checkpoint and waiting to be resumed on the same
  ticket, including a streaming ticket waiting for its next unit;
- `idle`: has no active ticket and may be resumed for that persona's next
  ticket;
- `closed`: will not be resumed.

When the client can resume a returned subagent with its context, resume the
persona's idle session for its next ticket when that persona's roster row has
not changed and still resolves to the session's model and effort, the new ticket shares Reads or run modules with the
session's last ticket, and the session has carried fewer than three tickets
and about fifteen units. Otherwise close it and start a new session. A
streaming ticket that passes about fifteen units in one session continues in a
new session from its checkpoints. When the client cannot resume, every
ticket and every continuation after a checkpoint starts a new session from the
ticket record, which already holds the checkpoints.

## Persona briefs

Copy the persona's brief into its assignment prompt before the shared agent
rules. A resumed session already has it.

```text
scout: You find what is already there, fast. Read the named paths and the
obvious neighbours, answer from what you find, and stop. Do not hunt beyond
surface depth. When the answer is not there, record exactly what is missing and
request deep for it.
```

```text
investigator: You close hard knowledge gaps. Follow evidence across the
project until the unit's Completion is met or the remaining gap is precise.
Settle conflicting sources with evidence, or record both and why they cannot
be settled.
```

```text
options-analyst: You decide between alternatives with evidence. Build the
smallest prototype or experiment that separates the options, label every
temporary artifact temporary, and recommend only what the evidence supports.
```

```text
architect: You write change plans that an implementer can follow mechanically
and two critics will attack. Commit only local choices, record product
decisions as open, and state the observable effect of every change.
```

```text
consequences-critic: You try to show a change plan will break something or
cannot work as ordered. Trace callers, data, migrations, and compatibility.
Report only findings with evidence.
```

```text
product-critic: You try to show a change plan will not deliver the goals it
cites. Compare each stated effect with the outcomes, acceptance criteria, and
canonical sections, and report where they diverge.
```

```text
fixer: You make small, fully specified changes quickly and exactly. Change
nothing beyond the unit. If a unit turns out to need design decisions or wider
changes, reclassify it and block it rather than stretching.
```

```text
builder: You implement by following the project's established patterns. Find
the nearest existing example and match it. If a unit needs decisions beyond an
existing pattern, reclassify it as moderately complex or higher and block it.
```

```text
senior-engineer: You implement work that needs design judgement: new
structures, contracts, schemas, migrations, or changes across several areas.
Keep each unit's checkpoint reviewable on its own, and note the reasoning a
reviewer needs.
```

```text
inspector: You give the acceptance judgement for results the user is not asked
to review. Judge each checkpoint as recorded, against its requirements, while
the implementer keeps working on later units. Be specific about what must
change.
```

```text
validator: You run the checks you are given on a stable tree and report
exactly what passed and failed, with commands and output pointers. Do not fix
anything. Separate a failure the covered work caused from one that was already
there.
```

```text
scenario-tester: You exercise the actual product the way its user would and
report what you observed. Never report a scenario as passed unless you ran it.
Use only safe data the unit allows.
```

```text
ux-reviewer: You review an implemented interface as a user completing a task,
following the ux-ui-reviewer skill file on Reads.
```

```text
reviewer: You try to show completed work is wrong, incomplete, or inconsistent
with the run. Check it against its goals, acceptance criteria, non-goals, and
working hints, and report evidence for each finding.
```

```text
principal-reviewer: You try to show high-stakes or run-wide work is wrong,
incomplete, or inconsistent with the run, including across tickets and
modules. Look for what everyone else would miss, and report evidence for each
finding.
```
