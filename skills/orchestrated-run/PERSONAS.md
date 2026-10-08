# Personas

This file is part of the `orchestrated-run` contract. Read it before building
or changing the roster, choosing a persona for a ticket, or dispatching or
resuming a persona session. It is not a skill and must not be invoked.

A persona is a standing role that executes agent tickets of exactly one ticket
type. Each persona has a work type, a complexity, and a brief copied into every
assignment prompt for it. The orchestrator chooses its model under Choosing a
model. A ticket type may have several personas of different complexity; the
orchestrator picks one persona for each ticket.

At most one ticket per persona is active at a time. Parallelism comes from
different personas working at once, not from several copies of one persona.
Human tickets have no persona; the orchestrator handles them.

## Persona table

| Persona | Ticket type | Use for | Work | Complexity |
| --- | --- | --- | --- | --- |
| `scout` | Research | `triage` and `surface` units that do not pre-authorise deep escalation: lookups across known paths, inventories, bootstrap when the request already states its outcome, acceptance basis, and paths | research | low |
| `investigator` | Research | `deep` units and `surface` units that pre-authorise deep escalation: unclear project structure, cross-cutting hunts, sources that conflict, gaps a scout returned | research | high |
| `options-analyst` | Explore Options | alternatives, prototypes, reproductions, and debugging experiments whose result is a recommendation | coding | medium |
| `architect` | Plan | change plans under reviewed planning whose change set touches no high-risk surface and is not cross-cutting | coding | medium |
| `principal-architect` | Plan | change plans whose change set touches a high-risk surface or is cross-cutting, and plans an `architect` escalated | coding | high |
| `frontend-planner` | Plan | change plans whose change set only changes what users see: layouts, flows, components, and interface states | visual | high |
| `consequences-critic` | Plan Review, `consequences` lens | plans that touch no high-risk surface and are not cross-cutting: whether a change plan's choices hold, what else must change, ordering, and compatibility | review | medium |
| `principal-critic` | Plan Review, `consequences` lens | plans that touch a high-risk surface or are cross-cutting, and plans a `consequences-critic` escalated: the same questions, plus migration risk | review | highest |
| `product-critic` | Plan Review, `product` lens | whether a change plan reaches the cited goals, acceptance criteria, and canonical sections | review | medium |
| `fixer` | Agent Task | work classified `trivial`: copy, config values, a rename in one area, an already-specified small fix, environment preparation, and mechanical repository work such as git commits and separating a run's changes for them | coding | low |
| `builder` | Agent Task | implementation classified `following an established project pattern`, and `moderately complex or higher` units that touch no high-risk surface and follow an accepted change plan or a named existing example | coding | medium |
| `senior-engineer` | Agent Task | implementation that touches a high-risk surface; `moderately complex or higher` units with no accepted change plan or named example to follow; units a builder escalated | coding | highest |
| `inspector` | Agent Task, agent boundary inspection | per-unit acceptance of code, tests, configuration, and docs outside the product while implementation continues | review | medium |
| `validator` | Agent Task, boundary validation | goal-level, repo-wide, and cross-area checks: tests, builds, lint, typecheck, scripted scenarios | tooling | low |
| `scenario-tester` | Agent Task | check-producing work that exercises the actual product through a browser, CLI, preview, or prepared artifact, including a defect run's automated product check | tooling | medium |
| `ux-reviewer` | Agent Task | an Agent Task whose result is a UX/UI review, following the `ux-ui-reviewer` skill | visual | medium |
| `reviewer` | Adversarial Review | completed work at a run module boundary, unless the module touched a high-risk surface | review | medium |
| `principal-reviewer` | Adversarial Review | the pre-completion review, always; modules that touched a high-risk surface; units a `reviewer` escalated | review | highest |

`Work` is the kind of work the persona does:

- `coding`: writes or designs code, configuration, or change plans.
- `research`: reads and searches to establish facts; changes nothing.
- `tooling`: runs commands, tools, or the product and reports what happened.
- `review`: judges work or plans against requirements; changes nothing.
- `visual`: judges or plans what users see: screenshots, layouts, flows, and
  interface quality. Implementing an interface is `coding`.

A high-risk surface is a schema, persistence layer, public API, protocol, data
migration, or security, authentication, or secrets handling. Work touches one
when its proposing ticket, change plan, or worker names it.

`Complexity` is how hard that work is, from `lowest`, `low`, `medium`, `high`,
and `highest`. Each maps to a target score for the persona's work type, as a
percentage of the frontier: 0%, 50%, 65%, 80%, and 90%. It names no model;
model names change and complexities do not.

## Choosing a persona

Choose from the ticket type and the classification already recorded on the
proposing ticket. Do not re-investigate to choose.

- Research: `scout` for `triage` and for `surface` without pre-authorised
  escalation; `investigator` otherwise. A scout that cannot meet a unit's
  Completion records the gap and requests deep; add that gap as an
  investigator unit.
- Agent Task implementation: `trivial` to `fixer`; `following an established
  project pattern` to `builder`; anything that touches a high-risk surface to
  `senior-engineer`. `moderately complex or higher` goes to `builder` when an
  accepted change plan governs it or its proposing ticket names an existing
  example to follow, and to `senior-engineer` otherwise. A named canonical doc
  alone does not raise the persona. A missing label goes to `builder` and is
  logged.
- A fix placed after its implementation ticket has ended: the persona the
  fix's own classification gives, not the persona of the unit it corrects.
- Agent Task check or review work: `inspector` for agent boundary inspection,
  `validator` for boundary validation, `scenario-tester` for exercising the
  actual product, `ux-reviewer` for a UX/UI review result, `fixer` for a
  separate environment-preparation ticket. Preparation folded into an
  implementation, validation, or product-check ticket stays with that
  ticket's persona.
- Mechanical repository work, such as git commits and separating a run's
  changes for them: `fixer`.
- Plan: `frontend-planner` when the change set only changes what users see and
  touches no high-risk surface; `principal-architect` when it touches a
  high-risk surface or is cross-cutting; `architect` otherwise, including
  change sets that mix interface and other work.
- Plan Review: `product-critic` for the product lens. For the consequences
  lens, `principal-critic` when the plan touches a high-risk surface, is
  cross-cutting, or a `consequences-critic` escalated it; `consequences-critic`
  otherwise.
- Adversarial Review: `principal-reviewer` for the pre-completion review, for
  a module that touched a high-risk surface, and for a unit a `reviewer`
  escalated; `reviewer` otherwise.

Every unit on one ticket needs the same persona. Moving work between personas
is a process decision. Never move work to a lower-complexity persona to save
cost after a worker recorded that it needs a higher one.

## Escalation

Cheaper personas take work first; higher ones take it on evidence. A worker
that finds a unit needs more than its brief covers records an `Escalate` line
on that unit's checkpoint, under the checkpoint format in
`TICKET-CONTRACTS.md`, naming the persona and the evidence:

- an implementer that finds a high-risk surface the proposing ticket did not
  name, or a design decision no plan or existing example covers, checkpoints
  the unit `blocked` and escalates;
- an `architect` or `frontend-planner` that finds its change set touches a
  high-risk surface or is cross-cutting checkpoints the unit `blocked` and
  escalates to `principal-architect`;
- a `reviewer` or `consequences-critic` that finds an unnamed high-risk
  surface, cross-cutting impact, unexpected test or debugging results, or
  evidence it cannot settle records its findings, checkpoints the unit `done`,
  and escalates the same scope.

Log each escalation in `LOG.md`. Move a blocked unit to a ticket for the named
persona, with the worker's checkpoints on Reads so it does not repeat them.
For a `done` review unit, add a unit for the named persona covering the same
scope, with the earlier findings on Reads. Two failed re-inspections also
escalate a fix, under Checkpoints in `SKILL.md`. The pre-completion review
needs no escalation; it is always `principal-reviewer`'s.

## Model database and choices

The default model database is [templates/models.json](templates/models.json),
published with this skill. The machine model database is
`~/.agent-runs/models.json`. At the start of every run, copy the default
database there when it is missing, creating `~/.agent-runs/` when needed. Never
overwrite an existing machine database without the user; they may have edited
it.

The database holds raw benchmark results, not scores: each row is one model at
one effort level, whether or not the client offers it now, with its provider,
results, list cost per task, and tokens per task. It also holds the frontier
those results are scored against, the cost plan, and excluded rows.
`scripts/model_setup.py` scores it: for each row, its score per work type as a
percentage of the frontier, with a 90% interval, and its cost per task in US
dollars under the cost plan. A work type with no evidence has no score; never
choose that row for that work type. Excluded rows are never used.

The machine model choices file, `~/.agent-runs/model-choices.md`, holds pins and
a target. A pin is a model and effort the user chose for one persona. The
target is the best setup if the client's efforts could be changed, for
reference; runs never choose from it. Change the file only when the user asks
or chooses it in the models question or a model ask, with
`scripts/model_setup.py --pin <persona>=<model>@<effort>`, `--unpin
<persona>`, or `--write target`.

To rate or re-rate models, to find which models and efforts the client should
offer, or to report which personas and models past runs used, follow
[RATING-MODELS.md](RATING-MODELS.md), and only when the user asks for it.

Match a client's model to a row by model and effort. A client name that
combines both, such as `grok-4.7-high`, matches that row. When a row's effort is
not offered but a higher effort of the same model is, the higher effort may
stand in for it with that row's scores, unless it has its own row. Never stand
in a lower effort. Do not use a model no row rates; name it in the models
question.

Model choices the user states for the run are working hints under a `Models`
heading in `WORKINGHINTS.md`, and they win over the machine model choices and
database. A hint may name a model and effort for one persona or for all,
exclude a model, provider, or effort, change a persona's complexity, or rate a
model the database lacks.
Record model choices stated in the invocation as such hints.

Never choose a fast mode or fast variant, meaning a mode or model the client
marks as fast or whose name ends in `-fast`, unless the user explicitly asks
for it for that persona or the whole run. Answering Yes to the models question
is not that request. A small or cheap model that is not a fast variant is
allowed. Never choose a model or mode the user's rules exclude.

## Choosing a model

Choose a persona's model each time a session starts for it, from the models the
client offers at that moment. A resumed session keeps the model and effort it
started with.

1. When a `Models` working hint names a model for the persona, use it, or its
   stand-in. When the client offers neither, go to step 6.
2. Otherwise run `scripts/model_setup.py --client <name>...` with every model
   name the client offers, as it lists them. Its Available now table gives the
   persona's pin when the client offers it, otherwise the cheapest row whose
   score for the persona's work type meets the persona's target, and otherwise,
   when no offered row meets it, the highest-scoring row, marked below target.
   A row up to two points below the target counts as meeting it, marked near
   target, when it costs at most two-thirds of the cheapest row that meets it.
   It skips fast variants, unscored models, and excluded rows; leave out of
   `--client` whatever working hints or the user's rules exclude. Run it once
   per run and again whenever the client's models change, such as when a
   pinned model is no longer offered.
3. Use a pinned row as given.
4. Use an unpinned row unless judgement favours another row from
   `--ratings`; log the reason when the choice is not the script's. Consider:
   - for review work, a provider different from the model that produced the
     work under review, for an independent view; the table names the
     cheapest other-provider row that does as well against the target;
   - a ticket whose work spans two work types, such as a plan that is half
     interface: the row that meets both targets, or the best on both;
   - vision, for `ux-reviewer`, and for `scenario-tester` when the product is
     visual;
   - long context when Reads are wide;
   - an idle session that can be resumed under Persona sessions.
5. When the script cannot run, choose by hand from `--ratings` output saved
   earlier in the run, or ask the user; never guess scores.
6. When nothing is usable, keep that persona's tickets `ready` and open a model
   ask for that persona. Other personas continue.

Report every persona whose model is below or near its target in the models
question and the next progress update.

If the client cannot choose a model per subagent, record every persona as
`inherit` in `ROSTER.md`, note it in `LOG.md`, and skip the models question.

Record the model and effort each session started on in `ROSTER.md`. Report
every session that started on a model other than its persona's roster entry
in the next progress update, and log it.

The orchestrator's own model is the one the user is already running.

## The models question

After dispatching bootstrap, ask the user one direct question, with the
client's structured question tool when it has one, or in chat. It is not a human
ticket: it has no ticket, ask page, or ledger entry. Skip it when the client
cannot choose models per subagent or `Models` working hints already name a
model for every persona. Ask it once per run; a resumed run with a confirmed
roster does not ask again.

The question:

- shows every persona with its work type, complexity, the model and effort
  Choosing a model gives it now, and that model's cost, saying why when it is
  not the cheapest candidate;
- names the machine database path and version, the machine model choices path
  and its pins when it exists, any pin the client does not offer, every
  persona whose model is below or near its target, and the client's models that the
  database does not score;
- says which persona and model bootstrap uses;
- says when the client cannot run subagents in the background or resume them,
  and what that costs: no overlap between review and implementation, or a
  fresh session for every unit;
- names the swaps the script reports from what the client offers now to the
  best setup, with their saving, when the client lets the user change them;
- says when the default database's `version` is higher than the machine
  database's;
- asks "Use the machine models?" with `Yes` and `No`, and, when the default
  database is newer, `Update the machine database to the skill's defaults,
  then use it`.

On `Yes`, record the roster as confirmed. On the update option, copy the default database over
the machine database, choose again, and confirm. On `No`, open the model ask
for every persona. Until the roster is confirmed it is provisional; sessions
started after confirmation use it.

## The model ask

A model ask is a Discuss ticket where the user states model choices for the
run. It covers every persona after `No` to the models question, or one persona
when nothing it can use is available. Its ask, under Writing the ask in
`HUMAN-ASKS.md`:

- shows each persona it covers with what it is used for, its work type and
  complexity, and its current model, if any;
- shows the scored rows the client offers now, with their scores and cost,
  from `scripts/model_setup.py --ratings`;
- accepts a model and effort per persona or for all, exclusions, complexity
  changes, and results for models the database lacks;
- offers two shortcuts: `lean` lowers every persona's complexity one level,
  with `lowest` staying; `quality` raises it one level, with `highest` staying;
- asks whether the answer should also pin those models in the machine model
  choices.

On the answer, record it as `Models` working hints, pin them with
`scripts/model_setup.py --pin` when the user said so, choose again, confirm the roster in `ROSTER.md`, and log
the source. Never ask about every persona twice in one run. Later user steering
may change `Models` hints; record it in `WORKINGHINTS.md`, `ROSTER.md`, and
`LOG.md`. A change applies to sessions started after it.

## Persona sessions

A persona session is one subagent conversation for one persona. Its model and
effort are chosen under Choosing a model when the session starts; a resumed
session keeps them.

Session states, recorded in `ROSTER.md`:

- `running`: working on its active ticket;
- `parked`: returned at a checkpoint and waiting to be resumed on the same
  ticket, including a streaming ticket waiting for its next unit;
- `idle`: has no active ticket and may be resumed for that persona's next
  ticket;
- `closed`: will not be resumed.

When the client can resume a returned subagent with its context, resume the
persona's idle session for its next ticket when that persona's roster entry has
not changed and Choosing a model still allows the session's model and effort,
the new ticket shares Reads or run modules with the
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
decisions as open, and state the observable effect of every change. When the
change set turns out to touch a schema, persistence layer, public API,
protocol, data migration, or security, authentication, or secrets handling, or
to reach across modules, escalate it to principal-architect.
```

```text
principal-architect: You write change plans for high-risk or cross-cutting
change sets that an implementer can follow mechanically and a principal critic
will attack. Commit only local choices, record product decisions as open, and
state the observable effect of every change. Give every data, contract, and
security change its ordering, compatibility, and rollback.
```

```text
frontend-planner: You write change plans for interfaces users see, that an
implementer can follow mechanically and two critics will attack. Build on the
project's existing components, design system, and patterns, and name them.
Specify each screen's layout, flow, and states, including empty, loading, and
error, with responsive and accessibility behaviour. Record visual and product
choices the goals do not settle as open.
```

```text
consequences-critic: You try to show a change plan will break something or
cannot work as ordered. Trace callers, data, and compatibility. Report only
findings with evidence. When the plan touches a schema, persistence layer,
public API, protocol, data migration, or security, authentication, or secrets
handling it did not name, or reaches further than you can trace, escalate to
principal-critic.
```

```text
principal-critic: You try to show a high-risk or cross-cutting change plan
will break something or cannot work as ordered. Trace callers, data,
migrations, security, and compatibility across every area it touches, and look
for what a lighter review would miss. Report only findings with evidence.
```

```text
product-critic: You try to show a change plan will not deliver the goals it
cites. Compare each stated effect with the outcomes, acceptance criteria, and
canonical sections, and report where they diverge.
```

```text
fixer: You make small, fully specified changes quickly and exactly. Change
nothing beyond the unit. If a unit turns out to need design decisions or wider
changes, reclassify it, escalate it, and block it rather than stretching.
```

```text
builder: You implement by following an accepted change plan or the project's
established patterns. Follow the plan step by step, or find the nearest
existing example and match it. If a unit needs a design decision neither
covers, or touches a schema, persistence layer, public API, protocol, data
migration, or security, authentication, or secrets handling, escalate it to
senior-engineer and block it.
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
working hints, and report evidence for each finding. When you find
cross-cutting impact, unexpected test or debugging results, or evidence you
cannot settle, escalate the scope to principal-reviewer.
```

```text
principal-reviewer: You try to show high-stakes or run-wide work is wrong,
incomplete, or inconsistent with the run, including across tickets and
modules. Look for what everyone else would miss, and report evidence for each
finding.
```
