# Product run prompts

This file is part of the `orchestrated-product-run` contract. Read it before
creating or assigning any ticket for this skill. It is not a skill and must not
be invoked. Never put it on a subagent's Reads.

In an assignment, put the persona brief from `orchestrated-run`'s
`PERSONAS.md`, the shared agent rules and exact type prompt from
`TICKET-CONTRACTS.md`, and the applicable block below, in that order.

Add this to every prompt:

```text
Never start or wait on a login, device code, browser authorization, or
credential prompt. If a source or tool needs one, stop that step, record
exactly what needed authorizing on the ticket, checkpoint the unit blocked, and
return.
```

## Problem discovery (`product-partner`, Research)

Use `surface` depth with `deep` escalation pre-authorised. When `locator`
surveys ran first, put the survey tickets on Reads.

```text
This unit discovers the problem space and its adjacent product spaces so the
Product Owner can make high-leverage decisions and approve a wholesale product
proposal.

Inspect the target area and adjacent areas that share data models, permissions,
state, navigation, or user workflows. Also inspect the project's existing UI
setup (components, styling, tokens, and sibling screens). Do not ask the user
for facts the codebase or docs already hold.

Record on the ticket with these headings:
- Settled project facts: how the target and adjacent areas work today, and the
  existing UI setup, with `path:line` evidence.
- Cross-space knock-on map: which other flows, rules, schemas, or screens this
  problem interacts with or could affect.
- Wholesale product proposal (minimal-complete baseline): the simplest clean,
  non-hacky product solution that solves the user's problem end to end, what
  the user will observe, how edge cases behave, and what it assumes (with the
  cost of reversing each assumption).
- Optional extras and refactors: worthwhile additions, or any large refactor
  where a minimal change would be a hack (with evidence of why the minimal
  change fails), kept separate from the baseline so the user can opt in or out.
  Include a design-system suggestion here only when the project lacks one and
  this work would clearly benefit.
- Known unknowns (ready and waiting decisions): a decision tree where each node
  has a short title; what a different answer changes; dependencies on other
  nodes; 2 to 4 viable options, each with observable user behaviour and
  cross-space knock-on effects; a recommended option with its reason; and
  whether it must be settled now or can wait.
- Unknown unknowns (fog): areas where a risk or open territory is visible, why
  options cannot be framed yet, and what earlier answer, technical spike, or
  mock will clear the fog.
- Mocks and concepts needed: which complex changes or multi-option UI/flow
  decisions need a rough wireframe (`designer`) or a production-styled
  sign-off mock / interactive prototype (`prototyper`) in `<run-dir>/mocks/`
  before the user is asked to commit.
- Draft implementation slices: classified under the shared Research rules.

Do not commit product decisions. Do not modify project files.
```

## Concept and wireframe mock (`designer`, Explore Options)

Objective names the `<run-dir>/mocks/<name>.html` path(s), the decision or flow
being explored, and the project UI context from discovery.

```text
This unit builds a fast, clear wireframe or concept mock at the path under
`<run-dir>/mocks/` named in Objective so the Product Owner can judge flow,
information hierarchy, interaction states, or competing layout directions.

Write only under `<run-dir>/mocks/` unless Objective explicitly states the user
requested a project deliverable. Build a self-contained HTML file that opens
cleanly in a browser with no build step. When comparing multiple viable
directions, put 2 to 3 structurally distinct variants in one file with a fixed
bottom switcher bar (and keyboard left/right support) so the user can flip
between them. Cover the relevant states (default, empty, loading, error, and
key edge cases).

Work within the project's existing UI concepts and terminology. Do not invent a
new design system unless Objective specifically asks to mock one as an optional
extra.

At the top of the HTML page (in a visible contract banner) and in your
checkpoint, include this exact mock contract block:
- Mock: mocks/<filename>.html
- Fidelity: wireframe
- Binding: <the exact flow, layout hierarchy, states, copy, or interaction rules this mock obliges if accepted>
- Context only: <surrounding page chrome, placeholder data, rough wireframe styling, or adjacent features shown only for context that must not be built or tested against>
- Overrides: none
```

## Production sign-off mock (`prototyper`, Explore Options)

Objective names the `<run-dir>/mocks/<name>.html` path(s), the project CSS or
token paths discovered in the repo, and the exact feature or state machine to
demonstrate.

```text
This unit builds an interactive prototype or production-styled sign-off mock at
the path under `<run-dir>/mocks/` named in Objective so the Product Owner can
experience the exact look, feel, or state transitions before signing off.

Write only under `<run-dir>/mocks/` unless Objective explicitly states the user
requested a project deliverable. Reference the project's real production CSS,
tokens, and assets through relative `../project/<repo-relative-path>` links
(which the action ledger serves from the project root) or inline the project's
real token values and component markup so the mock matches the real product's
appearance.

- When the question is visual sign-off or variant choice: render the feature in
  realistic surrounding context using production styles, with a bottom variant
  switcher if multiple options are being compared.
- When the question is business logic or state transitions: isolate the state
  logic in a clean JS module and provide both free-play action buttons and
  guided scenario tabs (happy path, edge cases, blocked/error cases) that show
  state changes in plain domain language.

At the top of the HTML page (in a visible contract banner) and in your
checkpoint, include this exact mock contract block:
- Mock: mocks/<filename>.html
- Fidelity: sign-off (or `wireframe` when only logic/state is binding and visual styling is rough)
- Binding: <the exact visual styling, component structure, states, copy, or state transitions this mock obliges if accepted>
- Context only: <surrounding page chrome, mocked backend data, switcher bar, or adjacent features shown only to situate the mock that must not be built or tested against>
- Overrides: none
```

## Implementation and review extension (all `Plan`, `Plan Review`, `Agent Task`, and `Adversarial Review` tickets)

Copy this block into every planning, review, implementation, and inspection
assignment in an `orchestrated-product-run`:

```text
Simplicity and scope contract:
- Deliver the simplest clean, non-hacky solution that satisfies the unit's
  Objective, Completion, and governing goals.
- Do not bundle optional extras that were not accepted into the active goals.
- Never perform an unrequested large refactor. If you find that a minimal
  change would be a brittle hack, stop short of the refactor, record the
  evidence for why a minimal change fails, and propose the refactor as a
  product decision in Blockers / follow-ups.

Accepted mock contract (when Reads include a mock from `<run-dir>/mocks/`):
- Read the mock's contract block (`Fidelity`, `Binding`, `Context only`, and
  any user `Overrides` recorded on the goal or working hints).
- Treat `Binding` (plus `Overrides`) as a mandatory requirement at the stated
  `Fidelity`: `wireframe` binds flow, hierarchy, layout structure, states, and
  copy while using the project's real components and styling; `sign-off` binds
  the exact visual styling, layout, states, copy, and interactions.
- Treat `Context only` as non-binding scaffolding shown only to situate the
  mock. Do not plan or implement changes for `Context only` elements, and never
  raise review or inspection findings because the built product differs from
  `Context only` details.
```

## Agent boundary inspection extension (`inspector`)

Copy this block into every agent boundary inspection assignment, after the
Implementation and review extension. It overrides the base inspection prompt
where they conflict:

```text
Also judge parts with a subjective acceptance basis, except results Objective
reserves for the Product Owner. Judge them against the accepted proposal, the
covered goals, and the Binding of any accepted mock on Reads. Record
`accepted` or `changes needed`. Record `decision needed` only for a product
choice the proposal leaves open.

On an `inconclusive` check outcome, record `accepted` and the exact
observation gap. Do not record the verdict superseded.
```

## Automated product check (`scenario-tester`, Agent Task)

Use this prompt for the automated product check:

```text
This unit is the automated product check for the completed product slice. Do
not review only the code and do not fix findings.

Exercise the actual running product or prepared preview environment the way the
Product Owner would, checking every acceptance criterion on the covered goals
and every `Binding` obligation (plus user `Overrides`) on any accepted mock on
Reads. Ignore elements marked `Context only` in the mock contract. Use only
safe test data allowed by Objective.

Record in Evidence and the unit's checkpoint:
- outcome: `passed` (every scenario and Binding mock obligation worked as
  specified), `failed` (an observable requirement or Binding mock obligation
  was absent or wrong), or `inconclusive` (a scenario could not be exercised
  safely, stating the exact observation that could not be made);
- for each checked scenario: what you did and what you observed;
- the product URL or path and how to start it again; when this ticket also
  prepares a review the Product Owner asked for, the persistent process or
  session and expected state.
```
