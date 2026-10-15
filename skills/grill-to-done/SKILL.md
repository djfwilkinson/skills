---
name: grill-to-done
description: Question me in grouped rounds, with quick-pick defaults, until a plan or design is settled. Use only when explicitly invoked by the user.
disable-model-invocation: true
argument-hint: "<plan, design or decision to settle>"
---

# Grill to done

This skill is user-invoked. Start it only when the user explicitly invokes
`grill-to-done`. Another skill may follow it by reading this file; the user
sees the same rounds either way.

It is a variation on the grilling skill in
[Matt Pocock's skills library](https://github.com/mattpocock/skills). It keeps
the design tree, the rounds, the recommended answer on every question, and the
rule that facts are the agent's job and decisions are the user's. It changes
five things:

1. every round says where it is in the tree;
2. the session is built to end, and says when;
3. a blocked path gets unblocked, not replaced by more questions;
4. questions are grouped, not listed;
5. every question offers a few good defaults the user can pick in one reply.

## Map the tree first

Before the first round, build the design tree for what is being settled: each
decision, and the decisions that hang off it. Mark each node as one of:

- `settled`: decided, by the user or by evidence;
- `ready`: its prerequisites are settled, so it can be asked now;
- `waiting`: needs another node first;
- `fog`: an unknown unknown or open area where a risk or dependency is visible,
  but real options cannot be framed until an earlier answer, lookup or mock
  clears what is possible;
- `blocked`: cannot be settled yet for a stated reason (see Unblock);
- `parked`: deliberately left for later, with the trigger that reopens it.

Look up every fact you can before asking. Search the project, read the docs,
or dispatch a subagent for a slow lookup. Check both the target area and
adjacent areas that share data, state or flows so knock-on effects and `fog`
areas are visible early. Ask only for decisions and for facts nobody but the
user holds. A lookup in flight does not stop other `ready` questions from being
asked; only the nodes below it wait.

Then fix the finish line. Say what the session must produce and when it is
done: "done when I can write the plan without guessing at anything that would
change it". Everything after this is measured against that line.

## Keep the session finite

A question is worth asking only if a different answer would change what gets
built, decided or written. Test every candidate with that. When the answer
would not change the outcome, or the cost of being wrong is small and easy to
undo, take the recommended default and list it as an assumption instead of
asking.

- Estimate the rounds remaining at the start and restate the estimate every
  round.
- A round should close more branches than it opens. When answers open more than
  they close, say so and say why the new branches are material.
- Open a new branch only when it passes the test above. Prefer folding a small
  follow-up into the question it hangs off, as a conditional ("if you pick a,
  also choose x or y"), so it does not cost a round.
- Stop when no `ready` node remains that passes the test. Do not keep going to
  be exhaustive.

## Run a round

Open every round with where it stands, then ask, then give the fast reply.

**Where we are.** Keep it to a few lines:

- the round number and the current estimate of rounds left;
- how many decisions are settled out of the total, and what this round closes;
- the tree, one line per branch with its state, the branches asked this round
  marked;
- each `fog` branch and what earlier answer, lookup or mock will clear it;
- each blocked path and what is unblocking it.

**Wholesale proposal (when a coherent recommendation exists).** When the
settled facts and ready decisions support a recommended end-to-end package for
the problem or slice, open the round with that package in concise plain words:
what it does for the user, any mock or concept it uses (with what the mock
binds versus what is context only), and where it knocks on other parts of the
product or plan. Separate optional extras from the minimal baseline package so
the user can opt into them without bloating the baseline.

**Questions.** Group by topic. Give each group a one-sentence frame saying what
the group decides and why it comes now. Within a group, ask together every
question that does not depend on another open question. A question that
depends on one asked in the same round is folded in as a conditional or waits
for the next round.

For each question:

- a short title and the question, with one line on what a different answer
  would change;
- two to four options, each lettered, each stating in as few plain words as
  possible what the user would see, the cost it carries, and where it knocks on
  other parts of the product or plan;
- the recommended option marked, with one line on why;
- always room for a free-text answer.

Make the options real alternatives, not a recommended answer with weak
decoys. When the answers tend to move together, offer a preset for the group,
such as "lean", "balanced" or "thorough", that picks an option for each
question in it.

Word each question so "yes" or "recommended" accepts the recommendation.

**Fast reply.** End with one line the user can copy. It shows the shortest
useful reply, such as `accept` or `recs` to take the wholesale package and
every recommendation, `accept, except 2b` to take the package with specific
overrides, `1b 2a 3 ok` to pick by number and letter (with `ok` or a bare
number meaning the recommended option), or `detail <item>` to ask for deeper
evidence, edge cases, or knock-on traces on an item before deciding. A question
the reply does not answer stays open; it takes its recommendation only if the
user says so.

When the user replies with `detail <item>` (or asks a follow-up question about
an item), give the fuller explanation, evidence and knock-on trace for that
item, record any decisions the reply also settled, and re-present only the
unanswered items from the round without counting it as a new round.

Write the round for a reader who has only the round. Follow the
`user-response` skill's rules for the text when it is available: no decorative
emojis, no term before it is explained, plain words.

## Unblock, do not widen

An answer of "don't know", "you decide", a conflict between two answers, or a
fact nobody can supply blocks a path. Handle it before opening any new branch:

1. Take the recommended default and mark the node `settled` as an assumption,
   recording what it would cost to reverse. Do this when the default is safe.
2. Otherwise dispatch the lookup that would settle it, and mark the node
   `blocked` on that lookup. Ask the rest of the tree meanwhile.
3. Otherwise `park` the node: name the event that reopens it, such as a later
   decision or a reply from a named person, and state what is safe to do
   without it.
4. When two nodes block each other, settle the one whose default is cheaper to
   reverse, and let the other follow from it.

While a lookup runs, keep asking every `ready` question that does not hang
off it; only the nodes below it wait. Start each round with the blocked paths:
what is blocking each, and what unblocks it. Do not spawn sub-questions from a node that has no answer yet. A
blocked path gets a way forward, not a deeper branch.

## Finish

The session is done when no `ready` node passes the worth-asking test. Close
with:

- the decisions made, grouped as the tree was;
- the assumptions taken, each with what it would cost to reverse, so the user
  can veto any;
- the parked nodes, each with its reopening trigger, and any node still
  blocked, with what it is waiting on;
- what the session produced, measured against the finish line.

Do not act on the result until the user confirms it. If the user vetoes an
assumption, reopen only that node and what hangs off it.

## Inside an orchestrated run

When an orchestrated skill such as `orchestrated-plan` or
`orchestrated-product-run` follows this file, the tree, rounds and options are
the same, and these differences apply:

- Each round is one `Discuss/Gather Inputs` ticket, written under Writing the
  ask in `HUMAN-ASKS.md`. The where-we-are block, any wholesale proposal, and
  the fast reply go in the ask, and the fast replies are its expected-reply
  examples.
- When the user replies `detail <item>`, keep that `Discuss/Gather Inputs`
  ticket active: record the partial response and the expanded detail in the
  ticket and updated ask page, and re-present the remaining open items of the
  round. If answering `detail <item>` needs project facts not yet on a ticket,
  withdraw the ask while a quick Research ticket fetches them, then re-present.
- A node is an entry in `UNKNOWNS.md`. The orchestrator owns that file, so it
  adds a `Node state` line under Status holding `settled`, `ready`, `waiting`,
  `fog`, `blocked` or `parked`, with the trigger or blocker when there is one.
  The base statuses map as: `open` for `ready`, `waiting` and `fog`; `assigned`
  for `blocked` on a lookup or `fog` with an active Research or Explore Options
  ticket clearing it; `resolved` for `settled`. A settled node cites the ticket
  that settled it. When an earlier answer unblocks a `fog` node, open the
  Research or Explore Options ticket needed to frame its options before marking
  it `ready`. The orchestrator rebuilds the tree from those entries and the
  Discuss tickets after compaction.
- The orchestrator does not invent options or recommendations. They come from
  the Research, Explore Options or planning ticket that prepared the question.
  A question with no prepared options is not ready; open Research or Explore
  Options first.
- A fact lookup is a Research ticket, not an orchestrator search.
- Only product decisions are asked. Process choices take their recommended
  default and are logged, under Product vs process in `SKILL.md` of
  `orchestrated-run`.
