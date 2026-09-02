# Language

Canonical terms for this skills library. Each entry defines a concept. Paths are examples, not the definition.

This checkout's **project skills** are checkout-only and not published. They are not the same as a **target project's** project skills in project-alignment (that project's own agent-facing skills).

When naming, describing, or changing project concepts, use these terms.

## Contents

- [Packaging and authoring](#packaging-and-authoring)
- [Writing](#writing)
- [Orchestrated-run and project-alignment](#orchestrated-run-and-project-alignment)
- [UX/UI review](#uxui-review)
- [Git stage and commit](#git-stage-and-commit)
- [Checkout extras](#checkout-extras)

## Packaging and authoring

### Library skill

A skill this library publishes so it can be installed on another machine. It exists as a repo copy and, after install, as a user copy.

Related:
- project skill (checkout-only, not published)

Avoid:
- calling a project skill a library skill
- listing project-skill ids in the changelog of skill ids

### Repo copy

The git-tracked source of a library skill in this repository. Example layout: `skills/<skill-id>/`.

Related:
- user copy (the installed instance of the same skill)

Avoid:
- treating the repo copy as the loader's live skill unless the user copy is a symlink to it

### User copy

The installed instance of a library skill in a user-level skills folder. Same skill id as the repo copy. May be a copied directory or a symlink to the repo copy.

Related:
- user-level skills folder (the destination directory)

Avoid:
- **local copy** / **install local copies** as the canonical name
- **personal skill** (Cursor product term) for this library's installs
- **repository copy** (that phrase is not used here; the source is a repo copy)

### Project skill

A skill that belongs to this checkout only. It is not published, not changelogged, and must not be installed into user-level skills folders. Example layout: `.cursor/skills/<skill-id>/`.

Distinct from **project skills** in project-alignment, which means a target project's agent-facing skills, not this library's checkout-only skills.

Related:
- library skill (the published kind)
- target project

Avoid:
- **workflow skill**
- treating README "Repo management" as a kind name
- installing these into user-level folders
- recording their ids in the changelog of skill ids

### Skill id

The stable identifier of a skill. Folder name, frontmatter `name`, and slash-command id are the same string: one identifier, not three. The changelog of skill ids records added, removed, and renamed **library** skill ids only.

Related:
- skill title (human heading, not the id)

Avoid:
- using `name` as a human title
- treating folder, `name`, and slash-command id as different identifiers

### Skill folder

The directory named with the skill id that contains the skill file. Extra files in that folder are allowed. Example layout in this repo: one folder with one `SKILL.md`.

### Skill file

The required markdown file in a skill folder (`SKILL.md`): YAML frontmatter plus body. Callers of referenced-only skills read this file.

### Skill title

The human heading in the skill file body (H1). Not used for loading or slash-command identity.

Avoid:
- putting the title in frontmatter `name`

### Frontmatter

The YAML header of a skill file. Write each field for the loader job. Only `name` and `description` are in context before activation.

Related:
- loader
- activation
- ticket YAML (ticket metadata; not this)

Avoid:
- calling ticket YAML or ticket metadata **frontmatter** without the ticket qualifier

### Frontmatter name

The loader field `name`. It is the skill id written for the loader, not a second identifier.

### Frontmatter description

The loader field that holds routing text in context before activation. Job depends on invocation kind. Keep descriptions that contain `:` valid YAML.

- Auto-invoked: what it does and when to load it.
- User-invoked: short menu line; no trigger keywords.
- Referenced-only: states it is not invoked; no trigger keywords.

README catalog lines are human summaries, not this field.

### Frontmatter argument-hint

Slash-menu placeholder when the skill takes extra text. Omit when it does not.

### disable-model-invocation

Frontmatter field that stops the loader from auto-invoking the skill from ambient context. Set `true` for user-invoked and referenced-only. Omit for auto-invoked.

Related:
- invocation kinds

Avoid:
- treating `metadata.invocation` as the thing that controls loading

### Invocation kinds

How a skill is allowed to start. Three kinds: user-invoked, auto-invoked, referenced-only. Follow is a usage verb, not a fourth kind.

### User-invoked

Starts only when the user explicitly invokes it. `disable-model-invocation: true`. Description is a short menu line without trigger keywords. Another skill or ticket may still **follow** it by reading the skill file.

### Auto-invoked

The loader may load it from a description match. Omit `disable-model-invocation`. Description says what it does and when to load it.

### Referenced-only

Not started as a skill. Callers read and follow the skill file. `disable-model-invocation: true`. Description states it is not invoked. The loader may still list it as a slash command; agents must not start it that way.

### Invoke, load, follow, read

Usage verbs, not kinds.

- **Invoke**: start the skill as a skill, typically via slash command.
- **Load**: the loader puts the skill in agent context (`name` and `description` first; body on activation).
- **Read** / **follow**: open the skill file and obey it without invoking it. Required for referenced-only; also used for dependencies.

Avoid:
- invoking a referenced-only skill
- treating follow as auto-invoke

### Loader

The client that discovers skill folders, puts `name` and `description` in context before activation, may show a slash menu, and may auto-invoke from `description`. This library targets more than one loader. Write fields only if every target loader parses them.

### Activation

The point at which the skill body is in context. Before that, only `name` and `description` are.

### User-level skills folder

The machine directory where user copies live. Candidates include Cursor `~/.cursor/skills`, Codex/agents `~/.agents/skills`, and Claude Code `~/.claude/skills`. Do not install into `skills-cursor`.

Related:
- user copy
- destination candidate
- Cursor default destination

Avoid:
- **personal skills directory** as this library's canonical name
- **local skills folder** as a synonym for this destination
- installing into `~/.cursor/skills-cursor`

### Local skills folder

The skill id `local-skills-folder`. The destination concept is **user-level skills folder**. Do not use this phrase as a glossary synonym for that destination.

### Changelog of skill ids

The dated list of added, removed, and renamed **library** skill ids. It exists so install can copy this library's skills and ask before deleting obsolete user copies. Project skill ids are not recorded.

Avoid:
- **retired** as a changelog verb
- recording `.cursor/skills/` ids

### Install

The overall act of getting library skills onto a machine as user copies. Manual methods are copy or symlink. Automated procedures follow `local-skills-folder`.

Related:
- copy
- symlink
- publish (checkout procedure that includes install)

Avoid:
- **install local copies** as if "local" were the kind of skill
- suggesting install of project skills
- using **install** for git commit or push steps

### Copy

Write files from each library skill folder into the destination skill folder, overwriting files in that folder only. This is an install method. Do not sync, mirror, replace, or empty the user-level skills folder.

Related:
- additive copy
- symlink (the other method; also the skip condition)

### Additive copy

Only add or overwrite this library's skill folders. Never delete, mirror, or empty the destination as a whole. Deletion is a separate, changelog-driven, user-confirmed step.

### Symlink

An install method in which the user copy is a link to the repo copy, so checkout edits are live. Skip copying when the user copy is already a symlink. If a confirmed deletion path is a symlink, remove the link only; do not follow it.

### Publish

The checkout procedure that commits the publish path set, pushes to origin, then installs library skills. Updates the changelog of skill ids before the commit when library skill ids changed. Publish includes install. It is not a synonym for copy.

Related:
- publish path set
- install

Avoid:
- using **publish** for a manual copy or symlink
- using **install** for the git commit and push steps

### Foreign skill

A folder in a user-level skills folder that this library never shipped. Leave it alone. Changelog deletions apply only to ids this library removed or renamed that are still present locally and are not current library skills.

### Client-only fields

Frontmatter keys this repo does not rely on for loading, including `metadata`, `paths`, `license`, `compatibility`, `icon`, and `color`. Do not add them unless every target loader parses them. Do not set `paths` on these user-level skills. `metadata` does not affect loading, discovery, invoke, or permission. `metadata.invocation` is unused by this repo's loading rules.

## Writing

### public-docs

Auto-invoked library skill that governs **public copy**: human-facing copy whose intended use is a repository, publication, product, or human work tracker.

Related:
- user-response (the other writing skill; different artifact class)
- human-facing copy

Avoid:
- treating it as "the strict writing skill" versus a sloppy chat skill

### user-response

Auto-invoked library skill that shapes **chat replies** and **response-only artifacts** while they are being composed. It is not a separate rewrite or audit step. Chat replies and response-only artifacts are human-facing copy, not public copy.

Avoid:
- using it to restyle public copy
- using it on engine text

### Intended use

The purpose of a piece of text for its eventual reader. This, not file location, chooses the writing skill. If the result is meant to become a repository file, published page, product surface, or work-tracker item, public-docs governs it even if it started as a chat draft. If it is a chat reply or a response-only artifact, user-response governs it even if the harness wrote a file.

Avoid:
- using "it is on disk" as the test

### Human-facing copy

Text written for people outside the agent workflow. It includes public copy, chat replies, and response-only artifacts. public-docs applies to public copy, not to surrounding code, schemas, or identifiers. user-response applies to chat replies and response-only artifacts.

Related:
- public copy (the public-docs subset)
- chat reply
- response-only artifact
- copy (install method; a different concept)

Avoid:
- bare **copy** when both writing and install could be meant
- **repository copy** (collides with repo copy)
- treating chat replies or response-only artifacts as public copy

### Public copy

Human-facing copy whose intended use is a repository, publication, product, or human work tracker. Includes README and published docs, changelogs and release notes, GitHub descriptions, landing pages, marketing, help, emails, work-tracker items written for people, and product strings. Chat replies and response-only artifacts are human-facing copy, not this subset.

Avoid:
- **repository copy**
- repo copy (packaging)

### Product string

User-facing product text stored in source files. Apply public-docs to the string, not the surrounding code.

### Work-tracker item

A Jira, Linear, or GitHub work item written for people. public-docs applies. This is not an orchestrated-run ticket.

Avoid:
- applying public-docs to orchestrated-run tickets because they are "work items"

### Chat reply

User-visible text in the conversation, including final replies and progress updates. Human-facing copy governed by user-response, not public copy.

Avoid:
- treating the chat reply that reports public-docs work as public copy

### Progress update

A user-visible status message in chat, governed by the same chat-reply rules as a final reply.

### Response-only artifact

A standalone user-visible artifact created as part of a response (Canvas, temporary Markdown). Human-facing copy governed by user-response even if the harness stores it in a file. It is not public copy. **Temporary artifact** is the in-skill heading for the same concept.

Related:
- Canvas

Avoid:
- Explore Options **temporary artifacts** (prototypes and experiments)
- verification **artifact inspection**
- throwaway artifact (a file a UX review script created)

### Canvas

A Cursor response-only artifact that may need visual hierarchy that would be excessive in chat. An example of a response-only artifact, not a separate writing skill.

### Harness

The agent environment that may write a response-only artifact to disk. A disk write does not change intended use.

### Nearby copy

Existing prose in the project that is not a style rule unless the project identifies it as a convention.

### Engine text

Text written for agents, not for people outside the workflow: orchestrated-run tickets, run files, internal plans, prompts, skill files, AGENTS.md, `.cursor/rules`. Neither writing skill applies.

Related:
- work-tracker item (human-facing; public-docs does apply)

Avoid:
- **engine ticket** as the canonical name for a ticket
- rewriting tickets or run files to satisfy public-docs or user-response

### AI tell

A writing pattern associated with generic model output that the writing skills require the agent to remove when that skill applies. Each writing skill owns its operational list. The lists overlap and are not identical. This document defines the concept; it is not the runtime catalog. Independent install means a user copy of one writing skill does not load this file.

Avoid:
- treating the two "Remove AI tells" sections as one list
- treating this file as the runtime catalog for installed user copies
- extracting a third library skill to share the lists

### Authority (writing)

User or project copy, tone, format, and terminology rules win where they conflict with the writing skill. Facts, exact required wording, legal obligations, and (for user-response) an explicit output format take priority over style.

## Orchestrated-run and project-alignment

### Orchestrator

The one user-facing agent that owns the process of a run: run state, ticket creation and assignment, user interaction, steering, reconciliation, next work, and goal verification. It does not execute agent tickets or rewrite worker-maintained ticket sections. It may record the user response in Evidence for Discuss or Human Task. The narrow production-work exception is Human and Agent Task, which it executes and records itself.

Related:
- subagent
- orchestrator thread

Avoid:
- treating the orchestrator as the Adversarial Review reviewer
- giving the orchestrated-run skill file to a subagent
- using the Human and Agent Task exception for ordinary agent work

### Subagent

The agent assigned to execute one agent ticket. It owns that ticket file while the ticket is active, does only the bounded Objective, and must not edit run files or create tickets.

Related:
- worker (adjective for ticket sections that this agent may write, not a third role)
- agent ticket
- assignment

Avoid:
- using subagent for Discuss/Gather Inputs, Human Task, or Human and Agent Task (those stay in the orchestrator thread)
- treating **worker** as a synonym that replaces this role name

### Worker

Adjective for ticket ownership of sections: `execution_result` is worker-owned; Unknowns, Findings, Work performed, Evidence, Interaction log, and Blockers / follow-ups are worker-maintained. A subagent is the worker for an agent ticket. The orchestrator may record `execution_result` and the user response in Evidence for Discuss or Human Task, and is the worker for a Human and Agent Task. Worker is not a third role.

### Agent ticket

A ticket executed by a subagent after assignment: Research, Agent Task, Explore Options, or Adversarial Review. The only way those tickets get done.

Related:
- human ticket
- Agent Task (one type, not the class)

Avoid:
- using **agent ticket** to mean Agent Task

### Human ticket

A ticket the orchestrator handles in its own thread because it needs the user: Discuss/Gather Inputs, Human Task, or Human and Agent Task. Every required human interaction must have one. Its orchestrator-owned presentation state distinguishes an upcoming ask from one currently presented to the user or withdrawn.

### Ticket

A bounded piece of work for a run, stored as Markdown with ticket YAML. Its full ID and filename include its globally sequenced ticket number and ticket type suffix, such as `T-001-RES`. It defines Objective, Reads, and Completion, and keeps the detailed result. Follow-ups on a ticket are proposals, not a whitelist.

- **Objective**: the bounded result this ticket should produce.
- **Reads**: the list of paths the ticket worker must read.
- **Completion**: what must be true to report completed. For a Human Task, the observable result or evidence the user should return. For a Human and Agent Task, the overall end condition, not the result of one interaction.
- **Interactive reason**: why repeated branching interaction in one Human and Agent Task is materially better than the existing ticket types.
- **Exclusive scope**: see the canonical definition below.
- **Presentation**: see the canonical definition below.
- **Ticket finding**: a result recorded in Findings (research, adversarial, or implementation notes). Distinct from a UX finding.

Avoid:
- **engine ticket** as the canonical name
- calling ticket YAML **frontmatter** without the ticket qualifier

### Ticket YAML

Ticket metadata at the top of a ticket file (full id, title, type, status, execution_result, presentation, owner, and similar). Not skill-file frontmatter.

Related:
- frontmatter (loader YAML on a skill file)
- owner
- ticket status
- execution result

### Run

One orchestrated-run instance: a coordinated body of work with shared run files, tickets, and an orchestrator. Persistent memory is run files, ticket files, and project files. Conversation context is temporary. Completing the run is a process decision of the orchestrator, not an empty ticket queue.

Avoid:
- using **run** for a ticket execution or a shell command when the process instance is meant

### Run file

A run-level state document the orchestrator writes, except that an active agent ticket file is owned by its subagent. Kinds: goals, non-goals, unknowns, working hints, log, pillars, modules and tickets. Ask pages and the ask index are derived artifacts stored under the run, not run files or recovery sources. Current filenames are the layout, not the concepts.

Avoid:
- treating a ticket's Unknowns or Findings as a second copy of the unknowns run file

### Ticket type

The contract for how a ticket is executed and what it may do. The orchestrator picks the type when creating the ticket. The types and ID suffixes are Research (`RES`), Agent Task (`AGT`), Explore Options (`EXP`), Adversarial Review (`ADV`), Discuss/Gather Inputs (`DIS`), Human Task (`HUM`), and Human and Agent Task (`HAT`).

### Research

Ticket type that closes a knowledge gap. Depth is effort on surrounding context and hunting, not which sources are allowed.

- **triage**: choose no-investigation-required, surface, or deep; do not hunt.
- **surface**: obvious context; return the answer, continue to deep only when Objective and Completion pre-authorise it, otherwise return the partial result and request deep.
- **deep**: full picture; return the answer, unknowns, or a partial answer plus new unknowns.

Bootstrap is surface when the invocation already states the outcome, acceptance basis and useful paths; deep when discovery is needed.

### Agent Task

Ticket type for bounded production work. Implement from Objective, Completion, and Reads. Not ready until those name what to change and what done looks like. Reads are files Research already found, not the repo.

A UX/UI review whose result is the review is this type, with the ux-ui-reviewer skill file on Reads.

### Explore Options

Ticket type for investigating alternatives without committing them to the production solution. Temporary artifacts (prototypes, experiments) are allowed if labelled temporary. Those are not response-only artifacts.

### Adversarial Review

Ticket type that tries to show completed work is incorrect, incomplete, or inconsistent with the run. The orchestrator must not be the reviewer.

When the completed work is UI, the ticket may put the ux-ui-reviewer skill file on Reads. That is follow, not a change of ticket type. Producing a UX/UI review as the ticket result is an Agent Task.

### Discuss/Gather Inputs

Ticket type for information, preference, product decision, review, judgement, or acceptance from the user. Orchestrator-handled. **Discuss** is the shorthand. Its current ask lives in Objective. An acceptance request is returned directly in chat with the result, inspection path and acceptance basis, not presented through a structured questions form.

Related:
- Human Task
- product decision

Avoid:
- using Discuss for process decisions the orchestrator owns

### Human Task

Ticket type whose Objective is an external action the user must perform. Orchestrator-handled. The Objective is a complete ask the user can follow, including the procedure, commands, paths and expected result that apply. Include hints and known recovery steps only when evidence supports them and they are useful. Completion is the observable result or evidence to return. Do not record secret values on the ticket.

### Human and Agent Task

Orchestrator-handled ticket type for one bounded task that needs repeated, branching interaction between the user and orchestrator. The orchestrator may perform production or investigation work and write worker-maintained sections for this type only. Use it only when a single interactive ticket is materially better than separate existing ticket types, such as fast iterative debugging. Its preparation dependencies must complete before selection. Do not start or present another human ticket while one is active. Only agent tickets that pass the skill's explicit read-only, disjoint concurrency test may remain active or start; allow no concurrent agent ticket when uncertain. Each current ask lives in Interaction log, and the overall Completion stays unchanged across turns.

Related:
- Human Task
- orchestrator thread
- Interaction log

Avoid:
- treating it as an agent ticket
- using it for one human action, one decision, ordinary implementation, asynchronous work, or uncertainty alone
- using its Evidence as a substitute for independently required goal verification or Adversarial Review

### Ticket status

Orchestrator-owned persistence of the ticket in the run: `proposed | ready | active | blocked | resolved | cancelled`. `ready` means dependencies and inputs are available. `execution_result: completed` does not imply `status: resolved`.

Avoid:
- reading execution result `blocked` as ticket status `blocked`, or the reverse
- unqualified **status** next to git status, goal status, unknown status, or module status

### Presentation state

Orchestrator-owned ticket YAML field `presentation`: `upcoming` before an ask is shown, `presented` while the current ask awaits a response, `withdrawn` when that ask is no longer actionable, and `answered` after the user responds. Agent tickets use `null`. A withdrawn ask cannot complete the ticket. After preparation resolves, the human ticket returns to `upcoming` and must be presented again.

### Execution result

Worker-owned result of this assignment, unset until the execution ends: `completed | blocked | failed`. On Discuss/Gather Inputs, Human Task, and Human and Agent Task the orchestrator writes it. It is not the persistent ticket status.

Ticket status `blocked` is waiting (often `depends_on`). Execution `blocked` is the subagent stopping (missing input or an uncommitted product choice).

### Product decision

A choice that needs user involvement when multiple reasonable options would produce meaningfully different product, architectural, operational, compatibility, or scope outcomes. A subagent that hits one records options and a recommendation and stops short of committing it. The orchestrator must not commit it either.

Related:
- process decision
- Discuss/Gather Inputs

Avoid:
- defaulting uncertainty to a user interruption
- mixing this with **git commit** or with English "committing to" a decision

### Process decision

A choice that stays with the orchestrator: which ticket to create, whom to assign, whether to accept an execution result, whether a goal is verified, whether adversarial review is due, whether the run is complete, next work, review scheduling. Local implementation that follows established project patterns is process.

### Goal

An intended outcome for the run. It has an outcome (what must become true), acceptance criteria (what must be true to count as complete), verification (how those are checked), and status `proposed | active | achieved | blocked | abandoned`. Stable IDs such as `G-001`. Never abandoned without Discuss.

Related:
- non-goal
- verification

### Non-goal

A stated boundary of what is outside this run, with a scope check for work that would cross it. Not required to exist.

### Unknown

Something not yet known that matters to the run. Tickets keep the discovery record. The unknowns run file is the run-level log: one entry per unknown, stable IDs such as `U-001`, status `open | assigned | resolved | abandoned`, related goal IDs and resolution-ticket IDs. A gap is an input to the orchestrator, not an automatic Research ticket.

### Working hint

Project or user guidance that should affect multiple tickets. Cross-cutting; not a pillar. New hints that need a product decision stay proposed until the user confirms.

### Pillar

A substantial area of the run, not a code package. Contains ID, name, purpose, related goals, and status.

Related:
- module (run)
- working hint (cross-cutting guidance)

### Module (run)

A grouping of related run work into a manageable part. Status `proposed | active | complete | blocked | retired`. It becomes complete only after its implementation coverage and required module review resolve. This is not a source-code module and not a UI module.

Related:
- project module (a target project's code or directory module)
- UI module (a reusable interface building block in a reviewed project)

Avoid:
- unqualified **module**
- calling this library's skill folders run modules or project modules

### Assignment

The act of giving one ready agent ticket to one subagent before work starts: confirm dependencies, check conflicts against active tickets and other tickets in the dispatch wave, fill Reads, set status `active` and owner, dispatch with the type prompt and paths. Selecting a ready Human and Agent Task permits only tickets that pass the explicit read-only, disjoint concurrency test; allow no concurrent agent ticket when uncertain.

### Reconciliation

What the orchestrator does when a ticket returns or a Human and Agent Task ends: read execution result, leave worker sections as written, clear owner, set persistent status, update run files only where the wider run changed, decide next work from follow-ups as proposals, decide whether verification or review is still required. Every ticket already returned at the start of the pass is reconciled together, and persistent state is written before new dispatch. Must not re-do the ticket in the orchestrator thread.

### Boundary inspection

A Discuss/Gather Inputs ticket through which the user inspects one result produced by one or more named implementation tickets. It may also be the human-acceptance ticket when acceptance concerns that same result.

### Boundary validation ticket

An Agent Task that checks goal-level, repo-wide or cross-area requirements for the same named implementation tickets as a boundary inspection. It runs independently of the boundary inspection and is not folded into an implementation ticket.

### Implementation coverage

The requirement that every completed implementation ticket is named by one non-superseded resolved boundary inspection and one resolved boundary validation ticket whose Evidence meets its success conditions before its module or the run completes.

### Inspection freeze

The Presentation record that prevents the result under a presented boundary inspection from changing. It includes changed paths from covered implementation tickets, shared dependencies that can change the result, and prepared environments that could restart, rebuild or reload. It ends when the inspection returns or is withdrawn.

### Verification

How it is established that a goal's acceptance criteria are met. Status `defined | deferred`. Ticket completion, module completion, and goal achievement are separate. **Plan-change verification** is the same idea for a planned alignment change.

Avoid:
- waiving verification because the work looks done

### Shared language

The agreed canonical vocabulary for concepts shared across a project. Terms define concepts, not current implementation. When two domains use different words for one concept, choose one term. When similar words are different concepts, keep both.

### Language document

The artifact that records shared language so agents and contributors can find it. This library uses one project-wide file (`LANGUAGE.md`). A **domain language file** is a separate file for one domain with enough distinct language to justify it; this library does not use that layout.

Avoid:
- treating `LANGUAGE.md` as the concept name
- treating AGENTS.md as the language document

### Alignment plan

The agreed list of recommended project changes, written so a later orchestrated-run can implement it without this conversation. Each change has problem, target, affected areas, benefit, change size, dependencies, and verification. **Implementation plan** describes the same document as input to a later run, not a second artifact. The alignment run writes this document and does not implement the listed changes. The user may skip the document and implement in this run instead.

Related:
- benefit
- change size

Avoid:
- treating alignment plan and implementation plan as two artifacts
- unqualified **plan** next to a commit preview

### Benefit

How much a proposed alignment change would improve understanding, navigation, discussion, testing, or consistency with shared language. Rated Low, Medium, or High, explained in project terms.

### Change size

How large a proposed alignment change would be to carry out. Rated Low, Medium, or High, explained in project terms. Wide terminology changes are migrations, not ordinary local refactors.

### Target project

The project being aligned. In project-alignment, "project skills" means that project's agent-facing skills, not this library's checkout-only project skill.

### Conceptual locality

The alignment property that a concept's implementation lives together rather than spread across unrelated areas.

### Project guidance

Agent-facing or contributor-facing instructions in the target project (`AGENTS.md`, `CLAUDE.md`, that project's skills, contributor docs, and similar). Prefer a pointer to the language document over duplicating terminology.

### Alignment analysis

Assessing the target project against sufficiently clear shared language for changes that improve terminology consistency, conceptual locality, organisation, navigability, understanding, documentation, discoverability of documentation and project decisions, name consistency (user-facing concepts, docs, and implementation names), and testability through meaningful interfaces. Not a generic code-quality review. This library's current alignment run treats testability as out of scope (T-005); that is run scope, not a missing concept.

### Bootstrap

The first Research ticket or tickets of a run. Inspect enough to propose goals and unknowns or reach a useful question. No implementation in bootstrap.

### Steering

A user prompt while other work is still going. Act immediately. Change requests become tickets. Do not edit an active subagent's ticket file.

### Context compaction

Recovering the run from the skill plus run files and tickets after conversation compaction. Not a second planning process; those actions belong to reconciliation.

### Dispatch

Start the subagent with ticket path, type prompt, and Reads.

### Return

The subagent finishing the ticket record, or the user answering a presented Discuss or Human Task. A response to a withdrawn ask is not a ticket return. A user turn in an active Human and Agent Task is an interaction, not a ticket return. Distinct from returning to the user when a human ticket needs a response.

### Owner

Ticket YAML field for who currently executes an active ticket. Orchestrator-owned. Cleared on reconciliation.

### Follow-up

A proposal on a ticket for the orchestrator. Not a whitelist. Agent Tasks only when Objective, Completion, and Reads are already specified. Human and Agent Task only when its bounded work and need for repeated branching interaction are already clear.

### Log

Concise run history of attempts, execution results, status, decisions, evidence pointers, unknowns, blockers, and ticket IDs. Detailed notes stay on tickets.

### Stable ID

IDs such as `G-001`, `NG-001`, `U-001`, `P-001`, `M-001`, and the full ticket ID `T-001-RES` remain for the lifetime of the run and are not reused. A ticket's suffix records its type at creation; replacing it with another type requires a new ticket.

### Ticket number

The globally incremented numeric part of a ticket ID. Every ticket type shares one sequence, so `T-001-RES`, `T-002-DIS`, and `T-003-AGT` cannot collide. The numeric prefix, such as `T-001`, is valid shorthand for the full ticket ID within the run.

### Human involvement

The orchestrator's user-facing handling of Discuss, Human Task, and Human and Agent Task. Each type has its own return-to-user ask contract. Required environment preparation is completed before readiness. The first presentation is complete in chat and copied to an ask page. Later messages repeat the complete ask or, only after a successful local-page open recorded for the current client, give an actionable line and ask-index link; reminder-only text is never enough. Ordinary human involvement does not pause independent agent tickets. Human and Agent Task allows only agent tickets that pass the explicit read-only, disjoint concurrency test and never another presented human ticket.

### Return-to-user ask

The current action, decision, review or acceptance requested from the user. A Human Task includes the applicable procedure, commands, URLs, paths, expected result and evidence to return. Discuss includes the question, essential context, options and expected reply. Acceptance includes the exact result or path, inspection method, acceptance basis and request to accept or describe changes. Human and Agent Task uses only its latest Interaction log ask. Include evidence-backed hints and known recovery steps only when they apply. Every first presentation includes the ticket path, has a derived ask page, and never includes secret values.

### Prepared human environment

The files, artifacts, pages, previews, services and state needed for a return-to-user ask. Bounded preparation is an agent-ticket dependency completed before the human ticket becomes ready; an existing implementation or validation ticket may own it when its Objective and Completion already require that preparation and its Evidence confirms it. Its Completion leaves the resource available after return; its Evidence records the resource, persistent process or session where relevant, expected state, and any known expiry or restart procedure. At presentation, the orchestrator may only open the resource or perform a non-mutating liveness check. An active Human and Agent Task may manage its own environment within Objective. Ask pages are derived artifacts under the run, not a prepared human environment.

### Presented human ticket

A human ticket with `presentation: presented`. Its ask source, ask page and current environment are recorded in Presentation. Only a presented ticket can be described as waiting for the user. After a complete first presentation and a successful local-page open recorded for the current client, later messages may use one actionable line plus the ticket path and ask-index link; otherwise repeat the complete ask. Reminder-only text is invalid. If its environment becomes unusable, the ask is withdrawn and cannot complete the ticket; after preparation, it becomes upcoming and is presented again.

### Human acceptance

The user's explicit confirmation that a result meets its stated acceptance basis. The orchestrator presents the exact result or its path directly in chat and waits for the user to accept it or request changes. It is not a structured questions-form interaction.

### Presentation

Orchestrator-owned human-ticket section that points to the current ask source and ask page and records prepared-environment evidence, non-mutating liveness and client-link checks, presentation and withdrawal times, inspection freeze when applicable, and re-presentation. It is persistent state for compaction recovery, not a worker-maintained result section or the ticket YAML `presentation` field.

### Ask page

An orchestrator-written, static HTML copy of one current return-to-user ask under the run's `asks/` directory. It is a derived artifact, not a run file, and comes from Objective or the latest Interaction log entry plus Presentation. The ticket remains authoritative. First presentation still happens completely in chat. An ask page is not a prepared human environment and never contains secret values.

### Ask index

The orchestrator-written `asks/index.html` table of presented human tickets. Each live row names the requested action and why it exists and links the ticket and ask page. It is a derived artifact, not a run file, presentation state or a source for compaction recovery. Withdrawn, answered and upcoming asks are not live rows.

Avoid:
- **reports folder** or **reviews folder** for `asks/`
- using the ask index instead of a complete first presentation
- **waiting for user review(s)** or another reminder-only line, even with an index link

### Interaction log

Worker-maintained ticket section that records each agent action, user result, branch taken, next ask, and paths changed during a Human and Agent Task.

### Interactive reason

Orchestrator-owned ticket section required for Human and Agent Task. Explains why repeated branching interaction in one ticket is materially better than separate existing ticket types.

### Exclusive scope

Orchestrator-owned ticket section required for Human and Agent Task. Names directories or modules in which interaction may branch, external state, prepared human environment and decisions it may affect. Only agent tickets whose Objective and Completion prohibit mutation, whose Reads are disjoint, and whose decisions do not overlap may run concurrently. On expansion, the orchestrator waits for newly conflicting work and checks concurrent returns for invalidated Interaction log evidence. Allow no concurrency when uncertain.

### Closed ticket

For chat progress updates, a ticket whose ticket status has just become `resolved` or `cancelled`. A resolved summary gives the ticket ID and user-visible result. A cancelled summary says it was cancelled and gives the concise user-relevant reason without implying an execution result. Detailed ticket sections stay off chat.

### Orchestrator thread

The conversation where the orchestrator works. Must not execute agent-ticket work or invent verification evidence there. Human and Agent Task is the narrow exception for bounded orchestrator work.

## UX/UI review

These terms describe a review of a **target project's** implemented interface. This library has no UI of its own.

### UX/UI review

A review of an implemented interface as a user completing a task. Reports concrete usability, consistency, accessibility, and maintainability problems. Does not redesign the product, invent features, or propose large refactors.

Avoid:
- treating taste, animation, or inconsequential optical nits as the review's job
- skipping obvious inconsistency with the project's system or siblings as polish

### Review area

The named screen, flow, or area under review. Nearby flow only when it affects the same user task. Default is the named ticket, diff, or argument, not a whole-product audit, unless the caller asks for one. Optional extra text on the skill. This sense of **scope** is **review scope**.

Avoid:
- inventing an unbounded product-wide redesign
- unqualified **scope** next to commit set, publish path set, or language scope

### Ticket contract

When the ux-ui-reviewer skill file is on an orchestrated-run ticket's Reads, following it is the inspection contract for that review. Still user-invoked; follow is not a fourth invocation kind. The ticket that produces a UX/UI review as its result is an Agent Task. Adversarial Review of completed UI work may also put this skill on Reads; the ticket type stays Adversarial Review.

### Consistency (UX)

The interface uses the project's system and siblings the same way for the same problem: spacing rhythm, density, alignment, control type and placement, component and variant reuse, typography, colour, and interaction. Obvious inconsistency is in scope. Taste and inconsequential optical nits are not.

Related:
- visual polish (out of scope when there is no consistency or user-task problem)
- review sections: interaction consistency, module consistency, layout consistency, visual consistency

Avoid:
- treating missing padding as the only consistency failure
- using a broken sibling as the definition of correct

### Component library

The reviewed app's native UI library (props, variants, slots, layout utilities, configuration, theming). Not a library skill.

Related:
- design system
- theme
- authority order (UX)

Avoid:
- unqualified **library**

### Design system

The reviewed project's established UI rules and patterns (guidelines, components, tokens, layout). A reference for what the interface should already be doing, not a library skill. If it has a UI problem and lives in the project, it is in the review.

Related:
- component library
- theme

### Theme

The reviewed project's visual values (colour, spacing, type, and similar), including light and dark. A reference alongside the design system and component library.

Related:
- semantic token
- component library
- design system

### Authority order (UX)

When recommending a fix: (1) the reviewed project's guidelines, components, UI modules, tokens, layout, and theming; (2) the native component library; (3) custom CSS only when (1) and (2) do not already support the behaviour. (1) outranks (2). Do not recommend a library primitive when the project already wraps an equivalent.

### Semantic token

A project theme value for colour, spacing, or similar, used instead of one-off literals.

### Visual path

An already obvious way to see the implemented UI (documented URL, running app, existing preview command, or a path on the ticket or Reads). Do not invent one. Do not add preview infrastructure to make one.

Related:
- commit preview (a different "preview")

### Throwaway script

A short script on a clear visual path, using tools already installed, deleted before return.

### Throwaway artifact

A file the review's throwaway script created. Delete before return. Distinct from a response-only artifact.

### Evidence source

Where a UX finding came from: `code`, `visual`, `script`, or `mixed`. Extra sense of Evidence versus the orchestrated-run ticket field.

### Review section

One named inspection area. Apply every relevant section. Do not skip a high section because it appears later. Section importance is `high`, `medium`, or `low` and is not finding severity.

Closed list:

- **Task completion**: whether the user can finish the goal without guessing, extra steps, hidden important actions, or recovery failure.
- **Information hierarchy**: whether importance is visible (primary vs secondary, grouping, progressive disclosure, scannable labels).
- **Interaction consistency**: similar actions look and behave similarly.
- **Module consistency**: the same problem uses the same UI module, component, or pattern.
- **Layout consistency**: shared page chrome, grids, spacing, breakpoints, and content width used the same way in the flow.
- **Navigation and context**: the user knows where they are, how to return, and that list position, filtering, or selection is preserved.
- **Forms and data entry**: labels always visible; placeholders are examples; validation beside the field.
- **Feedback and system state**: every user action has understandable feedback; destructive actions confirmed.
- **Error prevention and recovery**: invalid actions prevented rather than rejected later; failed actions retryable.
- **Accessibility**: keyboard, focus, semantics, names, contrast, colour not the only channel, and related barriers. Fix semantics through the project's components before custom accessibility code.
- **Responsive behaviour**: core task remains completable at narrow, medium, and wide widths.
- **Visual consistency**: the project's spacing, type, colour, and similar tokens, not one-off values. Missing or uneven rhythm and other obvious visual drift against the system are in scope.
- **Content and terminology**: labels are user concepts; terminology consistent in the workflow.
- **Implementation maintainability**: in scope only when it affects UX consistency or future UI maintenance.

### Section importance

`high`, `medium`, or `low` on a review section. Weight when findings compete. Not finding severity and not review order.

### UI module

A reusable interface building block in the reviewed project (editors, tables, dialogs, lists, form kits, wrappers). Not a module (run) and not a folder in this skills library.

Avoid:
- unqualified **module**

### UX finding

One reported interface problem. Requires a user problem and a concrete fix. Fields include severity, section, location, user problem, evidence, recommended fix, and preferred implementation.

Related:
- ticket finding (a different concept)

Avoid:
- unqualified **finding**
- vague findings
- repeating the same root problem

### Finding severity

Exactly one per UX finding. Independent of section importance.

- `blocker`: primary task cannot be completed, data may be lost, or a serious accessibility barrier.
- `high`: a common task is confusing, error-prone, or substantially harder than necessary; or obvious inconsistency that harms the primary layout, hierarchy, or trust in the screen.
- `medium`: noticeable friction that does not prevent completion, including obvious inconsistency that makes the screen look unfinished or sloppy while the task still works.
- `low`: tiny optical mismatch or consistency with limited effect on task completion.

Inconsequential optical nits and taste are not `high` or `blocker`. Obvious consistency failures against the project's system or siblings are not `low` by default and must not be dropped as polish.

### Preferred implementation

The UI module, component, token, or pattern to use for the fix; native library only if the project has no equivalent.

### Visual polish

Appearance without a consistency or user-task problem. Taste and inconsequential optical nits are not UX. Not a release blocker when minor. Distinct from consistency (UX), which is in scope.

## Git stage and commit

### Git stage

Add paths to the git index. Not a staging or deployment environment. Not committing to a product decision.

Avoid:
- **stage** without **git**

### Git commit

Create a git commit object from a staged group. Distinct from committing to a product decision and from publish's later push and install steps.

Avoid:
- **commit** without **git** next to orchestrated-run language

### Git index

The staging area git will commit from. Inspect staged vs unstaged vs untracked before changing it.

### Worktree

The checkout's working files, including staged, unstaged, and untracked paths. **Working tree** is a synonym.

### Commit set

The paths a git-stage-commit request may stage or commit. If the user named a set, stay within it. Preserve unrelated work. This is not Conventional Commits scope, review area, publish path set, or language scope.

Avoid:
- unqualified **scope** / **in-scope**

### Unrelated work

Changes outside the commit set. Leave their staging state alone.

### Secrets (git)

Environment files, credentials, private keys, or other secrets. Do not stage unless the user explicitly included them.

### Destructive git operation

Rewrite history, discard work, or other irreversible git. Requires separate user authorisation. Push is not authorised by a stage or commit request.

### Agent-compatible git

Invocation forms an agent can consume: non-interactive commands and messages; no interactive add or rebase.

### Commit group

One reviewable commit's files, grouped by the repository's rules and recent granularity, else by observable cohesion. Do not mix unrelated changes.

### Commit granularity

How finely this repository splits commits, inferred from recent history when rules are silent.

### Commit preview

Report proposed groups and messages, then stop. Do not stage or commit. Distinct from a visual path.

Avoid:
- unqualified **preview**
- unqualified **plan** for this report

### Commit message

Repository-required structure, else Conventional Commits fallback. The optional Conventional Commits scope is not the commit set.

### Hook rejection

A commit hook refused the commit. Fix only a clear in-scope failure and create a new commit attempt. Do not amend the rejected commit.

### Hash and message pair

Report form after execute: created commit hash plus message, whether the commit set is complete, remaining paths, or why user input is required.

## Checkout extras

Procedure concepts used by this checkout's project skills. Packaging umbrellas (install, copy, publish, changelog of skill ids) are defined above.

### Skills library checkout

This repository as the published source: it has library skill folders with skill files. `publish-skill` and `update-local-skills` both start by confirming that.

### Publish path set

The files `publish-skill` may send to git-stage-commit: named library skill folders, or every changed path under `skills/`; related project-skill changes from the same work; changelog and guidance files when those edits belong to the same skill work. Do not commit unrelated files.

Related:
- commit set

### Changelog rename detection

How a library id change is classified before writing the changelog: git rename is `renamed`; else if this publish has exactly one removed id and one added id, record `renamed`; else separate `removed` and `added`. Do not guess across several adds and removes.

### Origin

The git remote these checkout skills push to or pull from.

### Ahead of origin

The branch has commits origin does not. `publish-skill` still pushes in that case even if this invocation created no new commit.

### Force-push

`git push --force` and equivalent. Forbidden in `publish-skill`.

### Uncommitted-changes stop

`update-local-skills` must not pull if the worktree has uncommitted changes. Stop and ask. Distinct from git-stage-commit, which may stage those changes when the user asked to commit.

### Fast-forward pull

Pull from the tracked origin branch only if git can fast-forward. If not, stop and report. Do not rebase or force.

### Destination candidate

A possible user-level skills folder. Prefer a candidate that already contains this library's skill ids; if several match, the most matches; if none, create the Cursor default destination.

Related:
- deletion candidate (a different "candidate")

Avoid:
- unqualified **candidate**

### Cursor default destination

The user-level skills folder this library creates when no destination candidate already contains this library's skill ids. Example path: `~/.cursor/skills` (Windows: `%USERPROFILE%\.cursor\skills`). Not the only possible live destination.

### skills-cursor

Cursor-managed built-in skills directory. Not an install destination.

### Changelog deletion ask

After additive copy, read the changelog of skill ids and ask before deleting obsolete user copies this library removed or renamed. Skip if the id is still a current library skill or is not present locally. Leave foreign skills alone.

### Deletion candidate

A local folder to ask about: a changelog `renamed` old id still present and not a current library skill, or a changelog `removed` id still present and not a current library skill.

Avoid:
- collapsing this with destination candidate under bare **candidate**

### Install report

Facts `local-skills-folder` returns to its caller: install destination, copied skills, skipped symlinks, deletion candidates, what the user confirmed. Callers may add commit hash, push success, or pull result.
