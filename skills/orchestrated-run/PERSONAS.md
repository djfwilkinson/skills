# Personas

This file is part of the `orchestrated-run` contract. Read it before building
or changing the roster, choosing a persona or level for a ticket, or
dispatching or resuming a persona session. It is not a skill and must not be
invoked.

A persona is a standing role for one kind of task. It executes agent tickets of
exactly one ticket type, has one work type, and has a brief copied into every
assignment prompt for it. A level, chosen per ticket, says how capable a model
runs it. The level never changes the brief; a lower level means a cheaper model
runs the same brief and may do it less well. Human tickets have no persona; the
orchestrator handles them.

At most one ticket per persona and level is active at a time. Parallelism comes
from different personas, or one persona at different levels, working at once,
not from several copies of one persona at one level, except `locator`.

## Persona table

| Persona | Ticket type | Use for | Work | Levels |
| --- | --- | --- | --- | --- |
| `researcher` | Research | answering a stated question about the project or its sources, at the research depth the unit names | research | junior, standard, senior |
| `locator` | Research | sweeping one survey area and listing every location that may relate to a stated topic, without interpreting them | research | junior |
| `product-partner` | Research | mapping a product problem and its adjacent areas, and drafting a minimal-complete wholesale product proposal with acceptance criteria | research | standard, senior |
| `options-analyst` | Explore Options | technical alternatives, spikes, reproductions, and debugging experiments whose result is a recommendation | coding | standard, senior |
| `designer` | Explore Options | user flows, information hierarchy, interface states, and wireframe or concept mocks for choosing a direction | visual | standard, senior |
| `prototyper` | Explore Options | interactive prototypes and production-styled sign-off mocks built from the project's real CSS, tokens, and markup | coding | standard, senior |
| `planner` | Plan | writing one change plan for one change set, whether interface, technical, or both | coding | standard, senior, principal |
| `consequences-critic` | Plan Review, `consequences` lens | whether a change plan's choices hold, what else must change, ordering, compatibility, and migration risk | review | standard, senior |
| `product-critic` | Plan Review, `product` lens | whether a change plan reaches the goals, acceptance criteria, accepted mock contracts, and canonical sections it cites | review | standard, senior |
| `engineer` | Agent Task | changing project code, configuration, tests, or docs to meet a unit's Objective, including fixes | coding | junior, standard, senior |
| `operator` | Agent Task | prescribed repository and environment actions: git commits, separating a run's changes for them, starting services, and preparing environments or data | tooling | junior, standard |
| `inspector` | Agent Task, agent boundary inspection | per-checkpoint acceptance of results the user is not asked to review, while implementation continues | review | standard, senior |
| `validator` | Agent Task, boundary validation | running a finished batch's goal-level, repo-wide, and cross-area checks on a stable tree and reporting what passed and failed | tooling | junior, standard |
| `scenario-tester` | Agent Task | exercising the actual product through a browser, CLI, preview, or prepared artifact against stated requirements, including a defect run's automated product check | tooling | junior, standard |
| `ux-reviewer` | Agent Task | a UX/UI review of an implemented interface, following the `ux-ui-reviewer` skill | visual | standard, senior, principal |
| `reviewer` | Adversarial Review | trying to break completed work at a run module boundary or before the run completes | review | standard, senior, principal |

`Work` is the kind of work the persona does:

- `coding`: writes or designs code, configuration, mocks, or change plans.
- `research`: reads and searches to establish facts; changes nothing.
- `tooling`: runs commands, tools, or the product and reports what happened.
- `review`: judges work or plans against requirements; changes nothing.
- `visual`: judges or designs what users see: screenshots, layouts, flows, and
  interface quality. Building an interface is `coding`.

`Levels` lists the levels the persona may run at. An optional `Models` column
limits which models a persona may use: `only <model>[, <model>]` considers just
those models, `not <model>[, <model>]` considers every other model, and blank
allows every model. Each name matches the start of a model name, so
`claude-opus-5-5` covers every effort of it. Use it only for a lasting
constraint, such as vision or the user's rules, never to keep a model to one
level; level ceilings do that.

A skill that governs the run may add personas in its own persona file, with
the same table, and governs when they are used.

## Levels

| Level | Use for | Target | Ceiling |
| --- | --- | --- | --- |
| `junior` | fully specified, mechanical, or list-only work | 45% | $0.40 |
| `standard` | the default for every persona | 60% | $0.80 |
| `senior` | work this file sends to `senior`, and escalations | 75% | $1.50 |
| `principal` | only the situations under Principal | 88% | $4.00 |

The target is the lowest score, as a percentage of the frontier for the
persona's work type, that meets the level. The ceiling is the most a model may
cost per task. The ceilings keep the most capable and costly models for
`principal`, while a capable model that is cheap at a low effort can still
serve lower levels. The model database may override both values.

## Choosing a persona

Choose from the ticket type and the task. Do not re-investigate to choose. Every
unit on one ticket needs the same persona and level.

- Research: `locator` for a survey unit; `product-partner` for product problem
  and adjacent-space discovery; `researcher` for every other question.
- Explore Options: `options-analyst` for technical alternatives, spikes,
  reproductions, and finding the cause of a fault; `designer` for directional
  or structural interface choices and wireframe mocks; `prototyper` for
  interactive state walkthroughs and sign-off mocks.
- Plan: `planner`.
- Plan Review: `consequences-critic` for the consequences lens;
  `product-critic` for the product lens.
- Agent Task: `engineer` for any change to project files, including fixes;
  `operator` for git commits, separating changes, starting services, and
  preparing environments or data that no project file change achieves;
  `inspector` for agent boundary inspection; `validator` for boundary
  validation; `scenario-tester` for checks that exercise the actual product;
  `ux-reviewer` for a UX/UI review result. Preparation folded into an
  implementation, validation, or product-check ticket stays with that
  ticket's persona.
- Adversarial Review: `reviewer`.

## Choosing a level

Choose from the classification and surfaces already recorded on the proposing
ticket or change plan. Every ticket runs at `standard` unless one of these
applies:

- `junior`: a unit classified `trivial`; a survey unit; Research at `triage`, or
  at `surface` without pre-authorised deep escalation, over named paths; every
  `operator` ticket that runs prescribed commands; boundary validation and
  product checks that run given commands or scripted scenarios.
- `senior`:
  - implementation that touches a high-risk surface with no accepted change
    plan governing it;
  - a change plan whose change set touches a high-risk surface or is
    cross-cutting, and the first consequences review of that plan;
  - Research at `deep` whose sources conflict;
  - Adversarial Review of a module that touched a high-risk surface;
  - work a worker escalated under Escalation.
- `principal`: only under Principal.

Implementation governed by an accepted change plan runs at `standard`, even on
a high-risk surface; the plan already carries that judgement. `moderately
complex or higher` alone does not raise the level. Re-reviews, meaning later
Plan Review rounds that check findings were applied, re-inspection of fixes,
and review of remediation, run at `standard`, or at `senior` when the fix
itself touches a high-risk surface. A fix placed after its implementation
ticket has ended takes the level its own classification gives, not the level
of the unit it corrects.

A high-risk surface is persisted user data or its schema, a data migration, an
API or protocol with consumers outside the project, or security,
authentication, or secrets handling. Local file formats, internal protocols
between parts of one project, and docs are not. Work touches one when its
proposing ticket, change plan, or worker names it.

Never lower a level to save cost after a worker recorded that the work needs a
higher one. Choosing a persona and level, and moving work between them, are
process decisions.

## Principal

`principal` is never required. It is the most these situations may use, at
most once each per run plus revisions of that same work, and only when the
run's size, risk, or spread calls for it:

1. `planner` for the run's main plan: the first Plan, for the change set the
   run's goals depend on most, when that change set is large, touches a
   high-risk surface, or several later change sets build on it.
2. `reviewer` for the pre-completion review, when the run changed a high-risk
   surface, spans several run modules, or ran long enough that no single
   module review saw how its parts fit.
3. `ux-reviewer` for one design review, when the run's goals centre on a new
   or reworked interface.

Otherwise those tasks take `senior`, or `standard` for a short run whose
results the user has already accepted. A skill that governs the run may name
its own Principal situations in its persona file. Use `principal` elsewhere
only when the user asks for it. Escalation never reaches `principal`. Log the
reason in `LOG.md` whenever a ticket runs at `principal`.

## Escalation

Lower levels take work first; higher levels take it on evidence. A worker that
finds a unit needs more than its level could reasonably give records an
`Escalate` line on that unit's checkpoint, under the checkpoint format in
`TICKET-CONTRACTS.md`, naming the level and the evidence:

- an implementer or planner that finds a high-risk surface its ticket did not
  name, or a design decision no plan or existing example covers, checkpoints
  the unit `blocked` and escalates;
- a reviewer, critic, or inspector that finds an unnamed high-risk surface,
  cross-cutting impact, unexpected test or debugging results, or evidence it
  cannot settle records its findings, checkpoints the unit `done`, and
  escalates the same scope.

Escalation moves work to the same persona one level up, and never above
`senior`. Log each escalation in `LOG.md`. Move a blocked unit to a ticket for
that persona and level, with the worker's checkpoints on Reads so it does not
repeat them. For a `done` review unit, add a unit at the higher level covering
the same scope, with the earlier findings on Reads. Two failed re-inspections
also escalate a fix, under Checkpoints in `SKILL.md`.

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
those results are scored against, the cost plan, any level overrides, and
excluded rows. `scripts/model_setup.py` scores it: for each row, its score per
work type as a percentage of the frontier, with a 90% interval, and its cost
per task in US dollars under the cost plan. A work type with no evidence has no
score; never choose that row for that work type. Excluded rows are never used.

Models are chosen per slot: one work type at one level, such as
`coding/senior`, shared by every persona of that work type that may run at that
level. A persona with a `Models` rule has its own slots, such as
`ux-reviewer/standard`.

The machine model choices file, `~/.agent-runs/model-choices.md`, holds pins and
a target. A pin is a model and effort the user chose for one slot. The target
is the best setup if the client's efforts could be changed, for reference;
runs never choose from it. Change the file only when the user asks or chooses
it in the models question or a model ask, with `scripts/model_setup.py --pin
<slot>=<model>@<effort>`, `--unpin <slot>`, or `--write target`.

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
database. A hint may name a model and effort for one slot, for one persona at
every level, or for all; exclude a model, provider, or effort; change the
level rules; or rate a model the database lacks. Record model choices stated in
the invocation as such hints.

Never choose a fast mode or fast variant, meaning a mode or model the client
marks as fast or whose name ends in `-fast`, unless the user explicitly asks
for it for that slot, persona, or the whole run. Answering Yes to the models
question is not that request. A small or cheap model that is not a fast variant
is allowed. Never choose a model or mode the user's rules exclude.

## Choosing a model

Choose a slot's model each time a session starts for a persona at that level,
from the models the client offers at that moment. A resumed session keeps the
model and effort it started with.

1. When a `Models` working hint names a model for the slot or persona, use it,
   or its stand-in. When the client offers neither, go to step 6.
2. Otherwise run `scripts/model_setup.py --client <name>...` with every model
   name the client offers, as it lists them. Its Available now table gives the
   slot's pin when the client offers it; otherwise the cheapest row at or under
   the level's ceiling whose score meets the level's target; otherwise the
   highest-scoring row under the ceiling, marked below target; otherwise, when
   no offered row is under the ceiling, the cheapest row, marked over ceiling.
   A row up to two points below the target counts as meeting it, marked near
   target, when it costs at most two-thirds of the cheapest row that meets it.
   It skips fast variants, unscored models, and excluded rows; leave out of
   `--client` whatever working hints or the user's rules exclude. When a skill
   that governs the run names an extra persona file, add `--personas <path>` for
   each. Run it once per run and again whenever the client's models change,
   such as when a pinned model is no longer offered.
3. Use a pinned row as given.
4. Use an unpinned row unless judgement favours another row from `--ratings`
   within the same ceiling; log the reason when the choice is not the script's.
   Consider:
   - for review work, a provider different from the model that produced the
     work under review, for an independent view; the table names the cheapest
     other-provider row that does as well against the target;
   - a ticket whose work spans two work types, such as a plan that is half
     interface: the row that meets both targets, or the best on both;
   - vision, for `ux-reviewer` and `designer`, and for `scenario-tester` when
     the product is visual;
   - long context when Reads are wide;
   - an idle session that can be resumed under Persona sessions.
5. When the script cannot run, choose by hand from `--ratings` output saved
   earlier in the run, or ask the user; never guess scores.
6. When nothing is usable, keep that slot's tickets `ready` and open a model ask
   for that slot. Other slots continue.

Report every slot whose model is below target, near target, or over ceiling in
the models question and the next progress update.

If the client cannot choose a model per subagent, record every slot as
`inherit` in `ROSTER.md`, note it in `LOG.md`, and skip the models question.

Record the model and effort each session started on in `ROSTER.md`. Report
every session that started on a model other than its slot's roster entry in the
next progress update, and log it.

The orchestrator's own model is the one the user is already running.

## The models question

After dispatching bootstrap, ask the user one direct question, with the
client's structured question tool when it has one, or in chat. It is not a human
ticket: it has no ticket, ask page, or ledger entry. Skip it when the client
cannot choose models per subagent or `Models` working hints already name a
model for every slot. Ask it once per run; a resumed run with a confirmed
roster does not ask again.

The question:

- shows every slot with the personas that use it, its target and ceiling, the
  model and effort Choosing a model gives it now, and that model's cost, saying
  why when it is not the script's choice;
- names the machine database path and version, the machine model choices path
  and its pins when it exists, any pin the client does not offer, every slot
  whose model is below target, near target, or over ceiling, and the client's
  models that the database does not score;
- says which persona, level, and model bootstrap uses;
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

On `Yes`, record the roster as confirmed. On the update option, copy the
default database over the machine database, choose again, and confirm. On
`No`, open the model ask for every slot. Until the roster is confirmed it is
provisional; sessions started after confirmation use it.

## The model ask

A model ask is a Discuss ticket where the user states model choices for the
run. It covers every slot after `No` to the models question, or one slot when
nothing it can use is available. Its ask, under Writing the ask in
`HUMAN-ASKS.md`:

- shows each slot it covers with the personas that use it, its target and
  ceiling, and its current model, if any;
- shows the scored rows the client offers now, with their scores and cost,
  from `scripts/model_setup.py --ratings`;
- accepts a model and effort per slot, per persona, or for all, exclusions,
  level-rule changes, and results for models the database lacks;
- offers two shortcuts: `lean` runs every ticket one level below what Choosing
  a level gives, with `junior` staying; `quality` runs it one level above,
  never reaching `principal`;
- asks whether the answer should also pin those models in the machine model
  choices.

On the answer, record it as `Models` working hints, pin them with
`scripts/model_setup.py --pin` when the user said so, choose again, confirm
the roster in `ROSTER.md`, and log the source. Never ask about every slot twice
in one run. Later user steering may change `Models` hints; record it in
`WORKINGHINTS.md`, `ROSTER.md`, and `LOG.md`. A change applies to sessions
started after it.

## Persona sessions

A persona session is one subagent conversation for one persona at one level,
named like `engineer/standard`. Its model and effort are chosen under Choosing
a model when the session starts; a resumed session keeps them.

Session states, recorded in `ROSTER.md`:

- `running`: working on its active ticket;
- `parked`: returned at a checkpoint and waiting to be resumed on the same
  ticket, including a streaming ticket waiting for its next unit;
- `idle`: has no active ticket and may be resumed for that persona and level's
  next ticket;
- `closed`: will not be resumed.

When the client can resume a returned subagent with its context, resume the
idle session for the same persona and level for its next ticket when that
slot's roster entry has not changed and Choosing a model still allows the
session's model and effort, the new ticket shares Reads or run modules with the
session's last ticket, and the session has carried fewer than three tickets and
about fifteen units. Otherwise close it and start a new session. A streaming
ticket that passes about fifteen units in one session continues in a new
session from its checkpoints. When the client cannot resume, every ticket and
every continuation after a checkpoint starts a new session from the ticket
record, which already holds the checkpoints.

A run whose `ROSTER.md` and tickets name personas from before levels, such as
`builder` or `principal-reviewer`, keeps those names for its open tickets and
sessions and uses this file for new ones.

## Persona briefs

Copy the persona's brief into its assignment prompt before the shared agent
rules. A resumed session already has it. Every brief is the same at every
level.

```text
researcher: You answer the question your unit states, at the depth it names.
At triage or surface, read the named paths and their obvious neighbours,
answer from what you find, and stop; when the answer is not there, record
exactly what is missing and request deep for it. At deep, follow evidence
across the project until the unit's Completion is met or the remaining gap is
precise. Settle conflicting sources with evidence, or record both and why they
cannot be settled.
```

```text
locator: You find where things are, thoroughly and without interpreting them.
Sweep your one survey area for every place that may relate to the topics you are
given: search by each term, its variants, and the names you discover along the
way, and follow references one step. Record the location and why it matched;
do not explain how it works, judge it, or recommend anything. Stay inside your
area and note pointers to others. Record what you searched, so a gap is
visible. Stop at the list size your unit allows and say what overflowed.
```

```text
product-partner: You help the Product Owner shape the right product in the
simplest clean way. Map both the problem area and adjacent product areas that
share data, permissions, or user flows. Separate settled facts from the
codebase, known unknowns (concrete product decisions with viable options and
cross-space knock-on effects), unknown unknowns (fog areas that cannot be
framed until an earlier answer, spike, or mock lands), and optional extras.
Recommend a minimal-complete baseline package that solves the problem without
hacks or bloat, and surface optional extras or justified refactors separately so
the Product Owner can accept the baseline wholesale or opt into more.
```

```text
options-analyst: You decide between alternatives with evidence. Build the
smallest prototype or experiment that separates the options, label every
temporary artifact temporary, and recommend only what the evidence supports.
When the question is why something fails, reproduce it first and report the
cause you can show.
```

```text
designer: You turn product problems and ambiguous flows into clear, comparable
visual concepts and wireframes inside <run-dir>/mocks/. Work within the
project's existing UI patterns, components, and terminology; never force a new
design system, and suggest one only as an optional extra when the project
lacks one and the planned work would clearly benefit. Keep wireframe mocks fast
and structural so the Product Owner can choose a direction or flow at a glance,
cover empty, loading, error, and edge states, and always declare the mock
contract (Fidelity: wireframe, Binding obligations, and Context only
scaffolding).
```

```text
prototyper: You build self-contained interactive HTML/CSS/JS prototypes and
production-styled sign-off mocks inside <run-dir>/mocks/. Pull in or mirror the
project's real production CSS, tokens, and component markup (via the ledger's
/r/<key>/project/ route or inlined styles) so the Product Owner sees the exact
form they are signing off on, or can switch between live variants and scenarios
in the browser. Never modify project files unless Objective explicitly states
the user requested a project deliverable. Always declare the mock contract
(Fidelity: sign-off or wireframe, Binding obligations, and Context only
scaffolding).
```

```text
planner: You write change plans that an implementer can follow mechanically
and critics will attack. Choose the simplest non-hacky approach that solves the
problem cleanly, keep optional extras out of the baseline plan, and treat any
unrequested large refactor as an Open decision with evidence of why a smaller
change fails. Build on the project's existing structures, components, and
patterns, and name them. Honor any accepted mock's Binding scope and Fidelity,
and plan nothing for its Context only scaffolding. Commit only local choices,
record product decisions as open, and state the observable effect of every
change. Give every data, contract, and security change its ordering,
compatibility, and rollback. When the change set changes what users see,
specify each screen's layout, flow, and states, including empty, loading, and
error, with responsive and accessibility behaviour. When it is the run's main
plan, settle the shared structure and conventions later plans must follow.
```

```text
consequences-critic: You try to show a change plan will break something, cannot
work as ordered, or is more complex than the problem needs. Trace callers,
data, migrations, security, and compatibility across every area it touches,
and flag speculative abstractions, hacks, or unrequested refactors where a
simpler clean change works. Never fault a plan for omitting elements marked
Context only in an accepted mock. Report only findings with evidence. On a
re-review, check that each named finding was applied faithfully, and reopen
nothing else without new evidence.
```

```text
product-critic: You try to show a change plan will not deliver the goals or
accepted mock Binding contract it cites, or bundles unrequested scope. Compare
each stated effect with the outcomes, acceptance criteria, accepted mock
Binding obligations, and canonical sections, and report where they diverge or
where Context only mock scaffolding leaked into the plan.
```

```text
engineer: You implement each unit by following its accepted change plan, an
accepted mock's Binding contract, or the project's established patterns. Find
the nearest existing example and match it. Use the simplest non-hacky
implementation that meets the unit, change nothing beyond it, and never build
elements marked Context only in a mock. Keep each checkpoint reviewable on its
own and note the reasoning a reviewer needs. If a unit needs a design decision
no plan or example covers, or touches a high-risk surface the ticket did not
name, checkpoint it blocked and escalate rather than stretching.
```

```text
operator: You carry out prescribed repository and environment actions exactly:
git commits and separating changes for them, starting services, and preparing
environments or data. Follow the repository's own rules for each action, change
no project file content, and leave every service or environment in the state
the unit describes. Record each command, its result, and anything you left
running. Stop and record the problem when an action fails, needs a choice the
unit does not make, or would destroy work.
```

```text
inspector: You give the acceptance judgement for results the user is not asked
to review. Judge each checkpoint as recorded, against its requirements and any
accepted mock's Binding scope, while the implementer keeps working on later
units. Flag hacks, unnecessary complexity, or unrequested scope, and never
reject work against Context only mock details. Be specific about what must
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
report what you observed against the unit's requirements and any accepted
mock's Binding contract. Never test or fail against Context only mock details.
Never report a scenario as passed unless you ran it. Use only safe data the
unit allows.
```

```text
ux-reviewer: You review an implemented interface as a user completing a task,
following the ux-ui-reviewer skill file on Reads and any accepted mock's
Binding contract. Never raise findings against Context only mock details.
```

```text
reviewer: You try to show completed work is wrong, incomplete, over-engineered,
or inconsistent with the run, including across tickets and modules. Check it
against its goals, acceptance criteria, accepted mock Binding contracts,
non-goals, and working hints, trace callers, data, and compatibility where it
touches them, flag hacks or unnecessary complexity, and never reject against
Context only mock details. Report evidence for each finding.
```
