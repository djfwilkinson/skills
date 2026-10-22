# Rating models

This file is part of the `orchestrated-run` contract. Read it only when the
user asks to rate a model, add one to the model database, re-rate the model
database, or find which models and efforts the client should offer. Runs do not
read it, and it is not a skill.

The model database stores raw results and the frontier, not ratings.
`scripts/model_setup.py` rates every row against the stored frontier each time
it runs, so refreshing the frontier moves older models down as it moves up.

## Sources

Artificial Analysis is the primary source: one lab runs every model, at every
effort level, on the same harnesses. `scripts/model_stats.py` reads its public
leaderboard data once a day into `~/.agent-runs/model-stats/` and writes the
model database.

Use another source only when all of these hold:

- it ran the same benchmark version in the same agent harness as Artificial
  Analysis, checked per result, since a different harness moves scores by as
  much as 20 points;
- it has measured at least five models that Artificial Analysis has also
  measured on that benchmark, so it can be bridged: add the median difference
  between the two sources to its result, and add the spread of those
  differences to the result's uncertainty;
- it is independent of the model's vendor. Vendor-reported scores are never
  used.

Record every result taken from another source, with its link, harness, and
bridge, in the report to the user.

Artificial Analysis has no evaluation of how good frontend and interface work
looks, so `visual` uses the Frontend board of WebDev Arena,
<https://arena.ai/leaderboard/code/webdev/frontend>: blind human votes
between two models' builds of the same web app, independent of the vendors.
The script reads it once a day and matches a row by model and effort, such as
`claude-sonnet-5.5-high`. Report entries that ran in a vendor's harness, such
as `(codex-harness)`, since the harness affects the result.

## Workflow

The scripts edit the default database, `templates/models.json`, unless given
`--db`. Edit the machine database, `~/.agent-runs/models.json`, only when the
user says so.

1. Map each model to an Artificial Analysis row name with
   `scripts/model_stats.py find <name>`, such as `claude-sonnet-5-5` to
   `Claude Sonnet 5.5`. Anthropic rows marked `Default Fallback` are the
   client's models.
2. Add every measured effort of each new model, whether or not the client
   offers it, plus any effort the client offers that needs interpolating:
   `scripts/model_stats.py add <model> <effort> <provider> "<row name>@<effort>"`.
   Add a model Artificial Analysis does not list with `add <model> <effort>
   <provider> --result <key>=<bridged result>... price=<in>/<out>`.
3. Run `scripts/model_stats.py refresh` to re-read every row and recompute the
   frontier from all current Artificial Analysis rows.
4. Run `scripts/model_setup.py --db <database> --ratings` and check each row
   against Scoring below, resolving the cases under Missing and conflicting
   evidence.
5. Report to the user, before keeping anything: every row's score and 90%
   interval per work type, and its cost per task; every score that moved
   across a level's target and why;
   every interpolated, partial, or unrated cell; every conflict between core
   and supporting evaluations; and the setup analysis below.
6. On the user's agreement, keep the database and raise its `version` when it
   is the default database. Otherwise restore it from git.

## Setup analysis

A client usually offers each model at one effort, so the efforts it offers
decide which slots get cheap rows. A slot is one work type at one level, such
as `coding/senior`, shared by the personas that may run at it.
`scripts/model_setup.py` rates the database, builds the slots from the persona
table in `PERSONAS.md`, and reports:

- the best setup: every combination of one effort per model searched for the
  least shortfall below target, then the lowest mean cost per task, with each
  slot assigned as Choosing a model does;
- with `--client <name>...`, the client's model names as it lists them, such
  as `claude-haiku-5-5-thinking-high` or `grok-4.7-high`, the assignment those
  give now, using the user's pins, and the swaps from them to the best setup.
  `--available <model>=<effort>` gives models and efforts directly instead.

Options:

- `--multi <model>` lets a model be offered at several efforts at once, only
  for a client that offers more than one effort of that model. Clients
  usually offer one effort per model, Grok included. The report names the
  efforts chosen.
- `--weight <slot>=<n>` sets how often a slot works relative to the others;
  slots weigh equally otherwise. `scripts/run_usage.py` shows how often each
  persona and level worked in past runs.
- `--write target` saves the best setup as the target in the machine model
  choices, `~/.agent-runs/model-choices.md`, keeping its pins. `--pin
  <slot>=<model>@<effort>` and `--unpin <slot>` change a pin. Run them only when
  the user asks.

Report each suggested swap, its saving, and which slots it moves. Flag a swap
that rests on a score within 3 points of a level's target, which the script
lists, on an interpolated row, or on an estimated cost. The analysis ignores
provider diversity, vision, and long context, which Choosing a model weighs per
ticket; its table shows the cheapest other-provider row for each slot so the
user can judge review independence.

## Usage across runs

`scripts/run_usage.py` shows how runs used personas and models, to check
whether targets and routing send work where they should. It reads every run
registered in the device action ledger, or the runs and projects given as
paths, and reports per run its tickets, human tickets, fix tickets, and units
per agent ticket; and per persona and level and per model, tickets and share of
cost. Each ticket's model comes from the run's `ROSTER.md`, or, with `--client`
or `--available`, from what Choosing a model gives for the client's models now.
Only personas recorded in ticket YAML count; it lists the rest by ticket type.
Persona names from before levels are reported as the persona and level they
became.

## Usage check

`scripts/usage_check.py EXPORT` reads a Cursor token-usage HTML export and the
model database. For each database model it prints event counts, dollars, and
dollar-weighted dollars per million total tokens, for included-in-plan, for
on-demand, and pooled, beside the plan addend. The rate is total dollars
divided by total tokens, times one million. Included-in-plan is the export's
`Included` kind and on-demand is `On-Demand`. Free, errored, and aborted rows
stay out. A usage name matches a database model when it is that model plus an
effort, with an optional `-thinking` before the effort and an optional `-fast`
at the end.

The plan addend is `tokenRatePerMillion` per million tokens, or zero when the
model name starts with an entry in `exempt`. The database defaults to
`~/.agent-runs/models.json`, or `templates/models.json` when that file is
missing. `--db` selects another file. The command does not write the database
or the model choices.

A row with no `tokensPerTask` needs `--guess MODEL@EFFORT=COUNT`. The report
uses that count, says it is a guess, and shows the fee the plan addend
produces from it.

## Scoring

Each work type averages these core evaluations, equally weighted:

| Work type | Core evaluations | Supporting evaluations |
| --- | --- | --- |
| `coding` | Terminal-Bench 4.0, SciCode | Terminal-Bench 2.1 |
| `research` | AA-LCR, AA-Omniscience accuracy, Humanity's Last Exam | |
| `tooling` | Terminal-Bench 4.0, GDPval-AA | τ²-Bench, τ³-Banking, IFBench, Terminal-Bench 2.1 |
| `review` | Humanity's Last Exam, CritPt, AA-Omniscience accuracy | |
| `visual` | WebDev Arena Frontend | MMMU-Pro |

Core evaluations are the ones Artificial Analysis runs on almost every current
model, or, for `visual`, the only source that measures the work. Supporting
evaluations are reported beside the score but do not set it. They cover too few
models to compare everything on, or, for MMMU-Pro, are so near saturation that
frontier models score within a few points of each other; MMMU-Pro shows that a
model reads images, not how good its interfaces are.

A score is a percentage of the frontier. Each evaluation is divided by the best
current row's result on it, the work type averages those, and the result is
divided again by the best current row's average, so the frontier for each work
type is exactly 100%. Every evaluation is on a scale with a true zero:
GDPval-AA is used as Artificial Analysis scales it in the Intelligence Index,
Elo above 500, and AA-Omniscience uses accuracy, not its index, which can be
negative. A WebDev Arena rating is used as its expected win rate against the
board's median model, from its Elo; the frontier is the top model's win rate.
`visual` has no single best row across sources, so its frontier is that top
model.

The uncertainty of each evaluation is the binomial standard error over its
task count, from the Artificial Analysis methodology page, scaled the same
way. A WebDev Arena rating's uncertainty comes from its published 95%
interval. A work type's 90% interval is its score ± 1.645 combined standard errors.
Compare the score, not the interval's lower end, with a level's target, and
report the interval so the user can see which targets the evidence cannot
separate.

Each level has a target score and a cost ceiling per task, set in
`scripts/model_setup.py` and overridable under `levels` in the model database:

| Level | Target, percentage of the frontier | Ceiling, cost per task |
| --- | --- | --- |
| `principal` | 88% | $4.00 |
| `senior` | 75% | $1.50 |
| `standard` | 60% | $0.80 |
| `junior` | 45% | $0.40 |

`principal` starts about the frontier's own 90% interval below it, so a row
that meets it cannot be told apart from the frontier. The lower targets are
wide enough apart that neighbouring levels are separable and cheaper models can
meet them.

The ceiling, not the target, keeps the most capable and costly rows for
`principal`: such models are often cheaper at a medium or high effort than a
weaker model at its highest, so a target alone would hand them every level they
can meet. A slot takes the cheapest offered row under its ceiling that meets the
target; otherwise the highest-scoring row under the ceiling, marked below
target; otherwise, when no row is under the ceiling, the cheapest row, marked
over ceiling. Ceilings are in the same unit as cost per task, so check them when
a refresh moves costs as a whole, such as when Artificial Analysis changes its
index.

A row up to two points below a target counts as meeting it, marked near
target, when it costs at most two-thirds of the cheapest offered row that meets
the target. Two points is well inside every score's interval, so paying half as
much again or more for that difference is not worth it. The script ranks such a
row as meeting the target at one and a half times its cost, so it wins only
under that condition.

Cost is the Artificial Analysis cost per Intelligence Index task, in US
dollars. It measures tokens used as well as price, so a cheap-per-token model
that thinks at length can cost more per task than a dearer one.

Adjust cost for the plan the user's client bills under, in the database's
`plan`:

- Cursor Teams and Enterprise add a token rate to every input, output, and
  cached token on third-party models. Grok, Composer, and Auto are exempt.
  From 2026-10-20, so are Claude Haiku 5.5, Gemini 2.5 Flash, Gemini 3 Flash,
  Gemini 3.1 Flash Lite, Gemini 3.5 Flash Lite, Gemini 3.7 Flash, Gemini 3.8
  Flash, GLM 5.3 Flash, GPT-4.1 Nano, GPT-4o Mini, GPT-5 Mini, GPT-5.1 Codex
  Mini, GPT-5.4 Mini, GPT-5.4 Nano, and GPT-5.6 Luna. The list can grow; check
  Cursor's Models and Pricing page before a refresh. Set `tokenRatePerMillion`
  and `exempt`. Each entry matches the start of a model id, so `grok-` covers
  every Grok and `claude-haiku-5-5` covers that model. `model_setup.py` adds
  the rate using each row's tokens per task.
- A contract discount the user states, such as included Cursor model usage on
  an Enterprise plan, goes in `discounts` as a model prefix and the fraction
  taken off. Never guess a discount that is not published or stated by the
  user.
- Cursor does not publish Enterprise Grok pricing. The default plan applies no
  Grok discount; add one under `discounts` only when the user gives a figure.

## Missing and conflicting evidence

- An effort Artificial Analysis has not measured is interpolated linearly
  between the nearest measured efforts below and above it on `low`, `medium`,
  `high`, `xhigh`, `max`. Never extrapolate beyond the measured range. Mark
  the cell interpolated in the report.
- WebDev Arena lists most models at one high effort. A lower effort of the same
  model without its own entry is `scaled`: the nearest higher measured
  effort's score times the ratio of the two efforts' `coding` scores, with
  both coding uncertainties added to its interval. Never scale up to a higher
  effort, and report every scaled cell.
- A work type missing some core evaluations is `partial`: rate it from what
  exists and report it. With none, rate `coding` or `tooling` from bridged
  supporting results only when they exist, and report it as resting on
  supporting evidence; `visual` is never rated from MMMU-Pro alone.
  Otherwise the cell is `-`, and the model is not chosen for that work type.
- When cost per task is missing, the script estimates it from per-token prices
  using the median ratio of cost per task to price across current rows, without
  the plan's token rate. Report it as estimated.
- Leave out a row that has both partial core evidence and an estimated cost,
  and report it.
- When a supporting evaluation differs from the core score by more than 30
  percentage points, report the conflict and the likely cause, such as a
  different harness, and keep the core score.
