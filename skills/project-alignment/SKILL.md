---
name: project-alignment
description: Use orchestrated-run to establish a project's shared language, assess structural and agent-facing alignment, update language and project guidance, and write an alignment plan or implement the alignment changes. Use only when explicitly invoked by the user.
disable-model-invocation: true
argument-hint: "[optional project area or concern]"
metadata:
  invocation: user-only
---

# Project alignment

This skill is user-invoked. It requires `/orchestrated-run`.

Use it to analyse an existing project, establish shared language with the user, and identify changes that would make the project easier for humans and agents to understand and change. Write an alignment plan, or implement those changes without a plan, according to the user.

The run may write shared-language documents and update project guidance that needs to point to or consume that language. It does not implement planned code or structural refactors unless the user chose to implement without a plan.

## Start

Start a new `/orchestrated-run` for this work.

After the run folder exists, open `Discuss/Gather Inputs` unless the user already chose how this run should finish.

Ask whether an alignment plan file is required and whether to implement without a plan. Present them as one choice:

- write an alignment plan; do not implement the planned changes;
- implement the alignment changes in this run without a plan file;
- do not write a plan file and do not implement the alignment changes.

If a plan file is required, ask where to put it in a further `Discuss/Gather Inputs` ticket. Before asking, check the repository root and `docs/plans/` for an existing alignment plan. Default to a file in this run's folder:

`.agent-runs/orchestrated-run/<timestamp>-<short-name>/project-alignment-plan.md`

Also offer `docs/plans/project-alignment.md` and the repository root (`project-alignment-plan.md`). Include a found established path when it is not already in that list. Accept another path the user names.

When asking, say that a run-folder plan stays with the run and is usually untracked when `.agent-runs/` is gitignored, while `docs/plans/` and the repository root stay in the project.

Do not wait for language research for these questions. Do not write the alignment plan or start implementing planned changes until those tickets return. Shared-language research may proceed.

Give that run these goals:

1. Establish an agreed shared language for the project.
2. Identify project changes that would improve consistency with that language, conceptual locality, navigability, testability, documentation, and agent/user understanding.
3. Update the shared-language documents and any project guidance needed to make them discoverable and consistently used.

After those tickets return:

- if they chose a plan file, add a goal to write the alignment plan at the agreed path;
- if they chose to implement without a plan, add a goal to implement the recommended alignment changes in this run;
- if they chose neither, do not add a fourth goal.

Give it these non-goals:

- changing product behaviour;
- broad terminology migrations through the codebase;
- unrelated code-quality cleanup;
- introducing new architecture only to make the project look more organised.

If the user did not choose to implement without a plan, also treat implementing code or structural refactors from the analysis as a non-goal.

When the user chose to implement without a plan, still finish shared language and alignment analysis first. Implement only recommended changes the user has accepted, using `Agent Task` tickets.

If the user supplied an area or concern with this invocation, include it in the run goals or working hints without narrowing away relevant project-wide findings.

## Research

Use `Research` tickets to establish the current state before asking the user to make language or project-model decisions.

Inspect enough of the project to understand:

- its purpose and main domains;
- directory and module structure;
- existing terminology in code, tests, UI, docs, schemas and configuration;
- `AGENTS.md`, `CLAUDE.md`, README files, contributor docs, project skills and other agent-facing instructions;
- existing glossaries, context docs, ADRs, architecture docs and plans;
- testing structure and the interfaces through which important behaviour is verified;
- concepts whose implementation is spread across unrelated areas;
- names that describe the same concept differently;
- words that are overloaded or used inconsistently;
- documentation that duplicates context instead of pointing to a canonical source;
- recent change hotspots when git history is available.

For a large project, split research by domain or concern. Keep terminology findings comparable across those tickets so the orchestrator can reconcile them into one language.

Research tickets should separate:

- observed facts;
- terminology candidates;
- inconsistencies;
- unresolved decisions;
- possible alignment changes.

Do not ask the user for facts that the project can answer.

## Shared language

The project should have one canonical language for concepts shared across the project.

Default layout when the project has no established equivalent:

```text
LANGUAGE.md
docs/language/
  <domain>.md
```

Follow an existing project convention when it already provides the same function.

`LANGUAGE.md` contains:

- project-wide terms;
- distinctions that apply across domains;
- links to domain language files.

Create domain files only where a domain has enough distinct language to justify one.

A language entry should define the concept, not its current implementation.

Use a consistent form such as:

```md
### <Term>

<Concise definition>

Related:
- <related term and distinction>

Avoid:
- <ambiguous or superseded term, when useful>
```

Include `Related` or `Avoid` only when they add useful information.

### Terms across domains

When two domains use different words for the same concept, choose one project-wide term and use it in both domains.

When similar words represent genuinely different concepts, keep the distinct terms and define their relationship.

Do not invent a project-wide umbrella term merely to remove a valid domain distinction.

Prefer terms that:

- match the user's understanding of the product or domain;
- describe the concept rather than its implementation;
- remain useful if the implementation changes;
- reduce ambiguity elsewhere in the project.

## User decisions

Use `Discuss/Gather Inputs` tickets for language and project decisions that cannot be settled from project evidence.

Ask one decision at a time when later decisions depend on it.

For each decision:

1. state what the project currently does;
2. explain the inconsistency or choice;
3. give the recommended answer and why;
4. present meaningful alternatives;
5. record the user's decision on the ticket.

Useful discussion topics include:

- which of several terms should become canonical;
- whether apparently similar concepts are actually the same;
- where domain boundaries should be understood to sit;
- whether an existing abstraction represents a real project concept;
- whether a proposed structural change is worth its disruption;
- whether an existing project convention should be preserved or changed.

The user decides non-trivial product and project-model choices. The orchestrator decides how to organise the analysis and plan.

## Project alignment analysis

Once the language is sufficiently clear, use `Research`, `Explore Options`, and `Adversarial Review` tickets to assess the project against it.

Look for changes that improve one or more of:

- terminology consistency;
- conceptual locality;
- module and directory organisation;
- agent navigability;
- developer understanding;
- testability through meaningful interfaces;
- discoverability of documentation and project decisions;
- consistency between user-facing concepts, docs and implementation names.

Relevant findings can include:

- one concept spread across many unrelated modules;
- several names for the same concept;
- one name used for several different concepts;
- folders or modules named after implementation details instead of domain concepts;
- shallow pass-through abstractions that add navigation without hiding complexity;
- important behaviour that is difficult to verify through its current interface;
- project guidance that duplicates or contradicts other guidance;
- agent instructions that contain large copied context instead of a pointer to the canonical document;
- obsolete names that remain after the project model changed;
- domain boundaries that exist in the product but are not visible in the project structure.

Do not turn this into a generic code-quality review. A finding belongs in this run when changing it would improve how the project is understood, navigated, discussed, tested, or aligned with the shared language.

## Value and change size

Assess each significant proposed change by:

- **Benefit:** low, medium or high;
- **Change size:** low, medium or high.

Explain both in project terms.

Examples:

- High benefit, low change size: recommend early.
- High benefit, high change size: recommend with sequencing and verification.
- Low benefit, high change size: normally do not recommend, and record why.
- Low benefit, low change size: include only when it removes a recurring source of confusion.

Use recent change frequency as supporting evidence when it helps estimate benefit. A confusing area that changes often usually has more value to improve than an isolated stable area.

## Agent and project guidance

Make the shared language easy for future agents and contributors to find.

Inspect existing project guidance before changing it.

When the project has `AGENTS.md`, `CLAUDE.md`, project skills, contributor docs, or similar agent-facing material:

- add or update a concise pointer to the shared-language documents where relevant;
- state when the reader should consult them;
- replace duplicated terminology guidance with a pointer when the canonical language now covers it;
- update terminology in the guidance when an agreed language decision makes the old wording incorrect.

Prefer a pointer such as:

> When naming, describing, or changing project concepts, read `LANGUAGE.md` and the relevant domain language file.

Use the project's existing entry-point file rather than creating a competing one.

This run may make these documentation and guidance changes. Broader code, folder and architecture changes belong in the alignment plan, or in this run when the user chose to implement without a plan.

## Plan

Write the alignment plan only when the user required a plan file.

Write it to the agreed path. Default:

`.agent-runs/orchestrated-run/<timestamp>-<short-name>/project-alignment-plan.md`

The plan is the input to a later `/orchestrated-run`, so it should be understandable without this conversation.

Start with:

```md
# Project Alignment Plan

## Purpose

<what this alignment work is intended to improve>

## Shared language

- <canonical language documents and how they are organised>

## Current state

<short summary of the relevant project structure and main alignment problems>
```

Then describe recommended changes in implementation order.

For each change include:

```md
## <Change name>

### Problem
<what is currently difficult or inconsistent>

### Target
<what should be true afterwards>

### Affected areas
<modules, directories, docs, concepts or systems involved>

### Benefit
Low | Medium | High

<why>

### Change size
Low | Medium | High

<why>

### Dependencies
<earlier changes or decisions this relies on>

### Verification
<how an implementation run can establish that the change succeeded>
```

Use paths where they identify stable project areas. Do not fill the plan with line-level edits that are likely to change before implementation.

Flag wide terminology changes as migrations rather than pretending they are ordinary local refactors. The alignment plan should allow old and new forms to coexist temporarily when that is needed to keep the project working while callers are moved.

A plan can include language changes, structural refactors, module changes, documentation changes, testability improvements and agent-context changes when they serve the alignment goals.

Do not add implementation work solely because it is conventional cleanup.

### Changes not recommended

Record a rejected candidate when the reason is useful for a later implementation or future alignment review.

Use:

```md
## Changes not recommended

### <Candidate>

Benefit: <Low | Medium | High>
Change size: <Low | Medium | High>

<why this is not recommended>
```

Do not turn this section into a list of every possible improvement.

## Review

Before completing the alignment run, use `Adversarial Review` tickets to check:

1. the shared language for contradictions, duplicate concepts and unnecessary domain-specific synonyms;
2. project guidance for stale or duplicated terminology;
3. when a plan was written, the plan for changes that do not serve the stated alignment goals;
4. each recommended change for a clear benefit, change-size assessment and verification method;
5. whether a high-impact project area was missed because its terminology or structure made it hard to discover;
6. when this run implemented changes, the implemented work for mismatch with the agreed language and the user's decision.

Resolve material findings through the normal orchestrated-run process.

## Completion

The alignment run is complete when:

- the user has confirmed the non-trivial shared-language decisions;
- the canonical shared-language documents exist;
- relevant project guidance points to and uses that language;
- if a plan file was required, the agreed path contains the alignment plan, it uses the agreed language consistently, and recommended changes state their benefit, change size, dependencies and verification;
- adversarial review has no unresolved finding that materially changes the plan or the implemented work;
- if the user did not choose to implement without a plan, no planned code or structural refactor has been implemented;
- if the user chose to implement without a plan, the recommended alignment changes that this run accepted have been implemented.

Finish by summarising the documents written or changed and the highest-value recommendations.

If a plan was written, give the user one exact command for starting a new implementation run, using the actual plan path:

```text
/orchestrated-run Implement the project alignment plan at <plan-path>. Treat the shared-language documents and project guidance referenced by the plan as required context.
```

Do not continue into implementation in the current run unless the user chose to implement without a plan.
