# Product run personas

This file is part of the `orchestrated-product-run` contract. Every persona
this run uses, with its brief, levels and model choice, is in
`orchestrated-run`'s `PERSONAS.md`. This file only says which of them product
work goes to. Read both before building the roster. This file is not a skill
and must not be invoked, and it is never put on a subagent's Reads.

## Choosing a persona and level

- Problem and adjacent-space discovery goes to `product-partner`, at `senior`
  for a new or wide product area and `standard` for a narrow change. When the
  project is unfamiliar and too large for one session, use parallel `locator`
  tickets first to sweep areas, then hand their results to `product-partner`.
- Rough wireframe concepts, user-flow diagrams, and structural layout options
  in `<run-dir>/mocks/` go to `designer`.
- Interactive state walkthroughs and production-styled sign-off mocks in
  `<run-dir>/mocks/` that pull in production CSS or tokens go to `prototyper`.
- Non-UI technical spikes or performance experiments go to `options-analyst`.
- Technical change plans under `smart` or `reviewed planning` go to `planner`,
  and their reviews to `consequences-critic` and `product-critic`.
- Implementation, code inspection, boundary validation, live product checks,
  UX/UI review, and adversarial review go to `engineer`, `inspector`,
  `validator`, `scenario-tester`, `ux-reviewer`, and `reviewer`.

Choose levels under Choosing a level and Principal in `orchestrated-run`. A
design review of the whole run's interface before completion is a Principal
situation for `ux-reviewer` when the run changed several screens or flows.

## Parallel locators

As in `orchestrated-plan`, `locator` is the only persona that may run several
active tickets at once, one per survey area, each with its own session entry in
`ROSTER.md`. No other persona runs in parallel with itself at one level.
