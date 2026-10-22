---
name: orchestrated-product-run
description: Drive a product problem from discovery, mocks, and wholesale product proposals through minimal implementation and outcome acceptance, using Product Owner review only when judgement is required. Use only when explicitly invoked by the user.
disable-model-invocation: true
argument-hint: "<product problem or outcome>"
---

# Orchestrated product run

This skill is user-invoked. Start it only when the user explicitly invokes
`orchestrated-product-run`.

It requires `/orchestrated-run`, the `grill-to-done` skill, and the
`user-response` skill. Start one orchestrated run and apply this skill as its
Product Owner process. The `orchestrated-run` skill and its references remain
authoritative for ticket types, personas, the roster, grouping, work units,
inboxes, assignment, ownership, planning depth, reconciliation, implementation
coverage, review, human asks, ticket sources, and run completion, except for the
settings under Run settings.

Read these before acting:

- [PERSONAS.md](PERSONAS.md): which `orchestrated-run` personas product work
  goes to, read before building the roster.
- [PROMPTS.md](PROMPTS.md): the unit prompts and assignment extensions to copy
  into assignments.
- the `grill-to-done` skill file, before the first questioning round.
- the `user-response` skill file, before writing any user-facing proposal or
  ask.
- [TICKET-SOURCES.md](../orchestrated-run/TICKET-SOURCES.md) and the active
  ticket-source definition (by default
  [ticket-sources/filesystem.md](../orchestrated-run/ticket-sources/filesystem.md)).

If one cannot be read, report the blocker rather than proceeding from memory.

## Role of the user

The user is the Product Owner. They supply a problem at any altitude, judge
product direction, trade-offs, cross-space knock-on effects, and mocks or
concepts, and accept finished product behaviour that needs their judgement.

They are never asked to write or review technical change plans, code diffs, test
suites, or non-product docs, and they are not interrupted for internal
engineering process choices.

## Run settings

Record these as user-confirmed working hints at the start. Invoking this skill
confirms them.

- **Planning depth is `smart`.** Do not offer the planning-depth question. Under
  `smart`, the orchestrator decides upfront per qualifying change set whether a
  `Plan` ticket is needed and whether it takes `0`, `1` (`consequences` or
  `product`), or `2` `Plan Review` lenses, logging the choice and reason in
  `LOG.md`. Any change set that touches a high-risk surface or carries a
  user-approved large refactor must use a `Plan` and at least the
  `consequences` lens (plus the `product` lens when product criteria are
  non-trivial).
- **Models question.** Run `scripts/model_setup.py --client <name>...`. When the client can choose models per
  subagent, the machine database is current, and every slot gets a model at
  or near its target without missing pins, confirm `ROSTER.md` automatically
  from the machine setup and log it without asking the models question. Ask the
  models question only when a slot is below target, a pin is unavailable, the
  skill's default database is newer than the machine database, or the user
  mentions models.
- **Minimal non-hacky solutions.** Every planner, implementer, and reviewer
  must choose the simplest clean solution that solves the problem without hacks
  or speculative generality. Keep optional extras out of baseline work and
  surface them separately in wholesale proposals for the user to opt into.
  Never default to a large refactor; if a minimal change fails, record why and
  put the choice to the user in `Discuss/Gather Inputs`.
- **First-party mocks and scoped mock contracts.** Use `designer` (for
  fast wireframes and flow concepts) or `prototyper` (for interactive mocks
  that pull in production CSS and tokens for exact sign-off) under
  `<run-dir>/mocks/` before asking the user to commit to a large or complex
  product change, or whenever a UI or flow has multiple viable options. Do not
  force a design system; work within the project's existing UI setup, and
  suggest introducing or formalising a design system only as an opt-in choice
  when the project lacks one and the planned work would clearly benefit. Every
  mock declares a mock contract (`Mock`, `Fidelity: wireframe | sign-off`,
  `Binding`, `Context only`, `Overrides`). Accepted mock contracts are recorded
  on `GOALS.md` or `WORKINGHINTS.md` and placed on `Reads` for downstream
  planning, implementation, inspection, product-check, and review units.
  Downstream agents are bound by `Binding` at the recorded `Fidelity` and must
  never build or reject against `Context only` scaffolding.
- **Run scope (`full delivery` vs `shape and ticket only`).** Run end-to-end
  delivery by default. When the user's request or the active ticket-source
  configuration specifies stopping after problem shaping and ticket creation,
  record `Stop mode: shape and ticket only` in `WORKINGHINTS.md` and complete
  the run at the end of Stage 3 once the proposal is accepted and the shaped
  tickets are written to the ticket source.
- **Writing.** Follow `user-response` for all user-visible text: explain every
  proposal, option, and cross-space knock-on effect fully in as few plain words
  as possible, with `detail <item>` available on demand.
- **Recovery.** Put the paths of this skill file, `PERSONAS.md`, `PROMPTS.md`,
  the `grill-to-done` skill file, the `user-response` skill file, and the
  active ticket-source file in `WORKINGHINTS.md` as required reads after
  compaction.

## Stages

Work through the stages in order. A stage may overlap the next when its inputs
for a coherent slice are settled and tickets allow it.

### 1. Problem and adjacent-space discovery

Start the run under `orchestrated-run` and create `<run-dir>/mocks/`.

- **Adaptive sizing.** For most requests, create one `Research` ticket for
  `product-partner` with the Problem discovery prompt (`surface` depth with
  `deep` escalation pre-authorised). When the codebase or documentation is
  unfamiliar and too large for one discovery pass, first run a fast parallel
  `locator` survey wave (as in `orchestrated-plan`) to inventory locations, then
  hand those survey tickets to `product-partner`.
- **What discovery produces.** `product-partner` inspects both the target area
  and adjacent product areas that share state, data, permissions, or user flows,
  plus the project's existing UI setup, components, and styling. It separates:
  1. **Settled facts:** how the product works today and what UI setup exists,
     with `path:line` evidence.
  2. **Known unknowns (`ready` or `waiting`):** sharp product decisions with 2
     to 4 viable options, a recommended minimal-complete default, observable
     user effects, and cross-space knock-on effects.
  3. **Unknown unknowns (`fog`):** areas where a risk, interaction, or
     capability question is visible, but concrete options cannot be framed until
     an earlier answer, a technical spike, or a visual mock settles what is
     possible.
  4. **Mocks needed:** which decisions or complex changes need a rough wireframe
     concept (`designer`) or a production-styled interactive sign-off
     mock (`prototyper`) before the user is asked to commit.
  5. **Recommended minimal-complete baseline and optional extras:** the
     smallest clean product change that solves the user's problem, separated
     from opt-in extras (including any suggestion to introduce a design system
     when the project lacks one and this work would clearly benefit, or any
     justified refactor where a minimal change would be a hack).

Reconcile the discovery ticket: record `ready`, `waiting`, and `fog` entries in
`UNKNOWNS.md` with their `Node state` lines, propose or activate goals that
already match the user's request, and open any needed Stage 2 mock tickets.

### 2. Mocks and concepts (`Explore Options`)

Before presenting a `Discuss/Gather Inputs` round for a large or complex
product change, or for any decision where a UI, flow, or state model could be
built in meaningfully different ways, create an `Explore Options` ticket to
produce a concrete mock or concept under `<run-dir>/mocks/`:

- Choose `designer` with the Concept and wireframe mock prompt when the
  choice is directional: user flow, information hierarchy, screen structure, or
  comparing 2 to 3 layout approaches quickly.
- Choose `prototyper` with the Production sign-off mock prompt when the user
  needs to see exact form using the project's production CSS/tokens (served via
  `/r/<key>/project/...` on the local action ledger), or needs an interactive
  state/variant walkthrough before signing off.
- Unless the user explicitly asked for a mock or prototype as a project
  deliverable, mock tickets write only under `<run-dir>/mocks/` and never modify
  project files.
- Every mock file and checkpoint must include its mock contract (`Mock`,
  `Fidelity: wireframe | sign-off`, `Binding`, `Context only`, `Overrides`).

Wait for the mock ticket to checkpoint `done` before presenting the `Discuss`
round that relies on it, so the ask links the live mock URL from the action
ledger.

### 3. Wholesale proposal and grilling rounds (`Discuss/Gather Inputs`)

Follow `grill-to-done` using one `Discuss/Gather Inputs` ticket per round and
the combined **Proposal + Decisions** structure:

1. **Where we are:** round number, estimated rounds left, settled vs total
   decisions, the tree with `ready`, `waiting`, and `fog` branches, and what
   will clear each `fog` branch.
2. **Wholesale product proposal:** the recommended minimal-complete product
   package in concise plain words:
   - what it does for the user and how edge cases behave;
   - where it knocks on other product areas, data, or workflows;
   - any prepared mock link (`<index URL>r/<key>/mocks/<file>`) together with
     its `Fidelity`, what is `Binding`, and what is `Context only` scaffolding;
   - what it assumes (with the cost of reversing each assumption).
3. **Decisions and optional extras:**
   - numbered sub-decisions for the current frontier, each with 2 to 4 options,
     observable user effects, cross-space knock-on effects, and the recommended
     choice;
   - separated opt-in extras (and any justified large refactor option, stating
     why a smaller change fails) so the user can accept the minimal baseline
     alone or opt into specific extras (`+E1`, `+E2`).
4. **Fast reply:** one copyable line showing how to accept the whole package
   (`accept` or `recs`), accept with overrides or extras (`accept, except 2b
   +E1`), answer individual items (`1a 2b`), or drill down for more detail
   (`detail 2` or `detail proposal`).

**Handling replies:**

- **`detail <item>`:** Do not resolve the `Discuss` ticket. Expand the requested
  item with deeper evidence, edge-case walkthroughs, or knock-on traces from
  the ticket record (or withdraw the ask and run a quick `Research` or `Explore
  Options` unit if missing), record any decisions the user also answered, and
  re-present only the remaining open items.
- **Answers that unblock `fog`:** Mark settled decisions `resolved` in
  `UNKNOWNS.md`, update `GOALS.md`, `NONGOALS.md`, and `WORKINGHINTS.md`
  (including any accepted mock contract and user `Overrides`), and immediately
  dispatch `Research` or `Explore Options` (mock) units to turn unblocked `fog`
  entries into concrete options for the next round.
- **Stop mode (`shape and ticket only`):** Once no open product decision or
  `fog` entry remains for the requested scope, if `WORKINGHINTS.md` records
  `Stop mode: shape and ticket only`, create or update the shaped tickets and
  acceptance criteria in the active ticket source under `TICKET-SOURCES.md`,
  verify that every settled decision and accepted mock contract is recorded on
  them, and complete the run under Stage 6.

### 4. Minimal build, smart planning, and automated product checks

When the wholesale proposal (or a coherent module of it) is accepted and the
run is in full-delivery mode:

1. **Record accepted contracts:** Write the confirmed goals, acceptance
   criteria, non-goals (including declined optional extras), and accepted mock
   contracts (`Mock`, `Fidelity`, `Binding`, `Context only`, `Overrides`) into
   `GOALS.md`, `NONGOALS.md`, and `WORKINGHINTS.md`. Create or project the work
   tickets in the active ticket source under `TICKET-SOURCES.md`.
2. **Apply `smart` planning depth:**
   - If a change set is straightforward or already fully specified by the
     settled proposal and accepted mock, create implementation `Agent Task`
     tickets directly for the `engineer` and log the
     `smart` routing in `LOG.md`.
   - If a change set spans multiple areas, needs interface/state design, touches
     a high-risk surface, or carries a user-approved refactor, create a `Plan`
     ticket for the `planner` and choose `0`, `1` (`consequences` or
     `product`), or `2` `Plan Review` lenses upfront. Always include the
     `consequences` lens for high-risk surfaces or approved large refactors,
     and the `product` lens when product criteria or
     mock contracts are non-trivial. Never ask the user to review or accept a
     change plan.
3. **Bind downstream units:** Put the governing goals, working hints, and
   accepted mock paths (with their `Binding` vs `Context only` contracts) on
   `Reads` for every `Plan`, `Plan Review`, implementation `Agent Task`,
   `inspector`, `scenario-tester`, `ux-reviewer`, and `Adversarial Review`
   unit, and include the Implementation and review extension from `PROMPTS.md`.
4. **Run automated coverage before any human review:**
   - Stream `inspector` (`agent boundary inspection`) across implementation
     checkpoints for code, tests, configuration, non-product docs, and
     deterministically checkable product-facing parts.
   - Run `validator` (`boundary validation`) on a stable tree for tests, build,
     lint, and typecheck.
   - When the batch changes user-observable product behaviour or UI, run a
     dedicated `scenario-tester` `Agent Task` (with the Automated product check
     prompt from `PROMPTS.md`) against the actual running product or prepared
     preview, checking both the goal's acceptance criteria and any accepted
     mock's `Binding` obligations. When UI changed substantially, also include
     `ux-ui-reviewer` on the module's `Adversarial Review` Reads.
   - Apply orchestrated-run's deterministic-check gate before creating or
     presenting a human boundary inspection. Exact requested copy, presence,
     absence, placement, and other fully specified product observables are
     accepted from `inspector`, `validator`, and `scenario-tester` evidence.
     Do not ask the Product Owner to repeat or accept a successful deterministic
     check.
   - When a result needs Product Owner judgement, hold its human boundary
     inspection `upcoming` until implementation, `validator`, and
     `scenario-tester` return with no material issue requiring remediation.
     `may_withdraw_on` never shortens this hold. List only tickets still open
     after it, and handle provisional acceptance under orchestrated-run.

### 5. Product outcome acceptance

Use recorded agent evidence to accept every fully specified outcome. Present
one grouped human boundary inspection (`Discuss/Gather Inputs`) only for
outcomes whose acceptance basis remains subjective or underspecified, whose
automated product check is inconclusive and no further agent check can close
the gap, which embody an unconfirmed choice meeting the product-decision test,
or which the Product Owner asked to review:

- Open with what the product now does for the user in plain, concise words.
- Link the prepared live product or preview environment (and any accepted mock
  from `<run-dir>/mocks/` for side-by-side comparison of its `Binding` scope).
- Report the recorded `scenario-tester` product-check outcome (`passed` or
  `inconclusive` with the exact observation gap) and `validator` check summary
  from their tickets.
- State the judgement-based acceptance basis and ask the user to accept the result or
  describe what product behaviour needs to change. Never ask the user to inspect
  code diffs, tests, or internal files.

If no result meets that gate, create no acceptance ask. Use the successful
deterministic checks to finalize any `accepted pending check` inspection
verdicts; implementation coverage remains the accepted inspection plus boundary
validation under orchestrated-run.

If the user requests product changes, route them as fix requests or new units
through the normal `orchestrated-run` steering and invalidation rules, re-run
the automated checks, and apply the deterministic-check gate again before
deciding whether to present the updated result for acceptance.

### 6. Complete

Complete the run under `orchestrated-run`'s completion rules (and project final
ticket statuses to the active ticket source under `TICKET-SOURCES.md`). Open the
completion message with `**This orchestrated run is complete.**` followed by a
concise summary of the product outcomes delivered (or tickets shaped, in
shape-only mode), the key Product Owner decisions and accepted mocks, and any
optional extras left parked for future runs.
