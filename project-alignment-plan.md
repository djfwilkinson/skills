# Project Alignment Plan

## Purpose

Make this skills library easier for humans and agents to name, find, and change the same concepts. The remaining work is leftover wording drift against the language document, not a folder or runtime redesign.

This file is the **alignment plan**. It is the input to a later orchestrated-run. This alignment run does not implement the remaining recommended changes.

## Shared language

- One **language document**: `LANGUAGE.md` at the repo root. No domain language files.
- **Project guidance** pointers: `AGENTS.md` Language section; README Agent directives.
- When naming, describing, or changing project concepts, read `LANGUAGE.md`. Prefer a pointer over duplicating terminology.

## Current state

This checkout is a personal Markdown skills library. There is no application runtime, UI, schema, or test harness.

Conceptual locality at the skill-folder grain already matches the language document: **library skills** under `skills/<skill-id>/SKILL.md`, **project skills** under `.cursor/skills/<skill-id>/SKILL.md`, install procedure in `local-skills-folder`, **changelog of skill ids** in `CHANGELOG.md`. Definitions live in `LANGUAGE.md`. `AGENTS.md` Language is a pointer, not a second glossary.

Already done in this alignment run (do not redo):

- T-010: `LANGUAGE.md` written; `AGENTS.md` Language pointer.
- T-014 / C-001: `AGENTS.md` Authoring uses **project skill**, not workflow skill.
- T-014 / most of C-003: README uses **user copy** instead of “install local copies” / “local install”; Agent directives point at `LANGUAGE.md`.
- T-015: `LANGUAGE.md` F1–F10 (subagent as role noun; ticket YAML vs frontmatter; alignment-analysis dimensions; qualified UI module; human-facing copy as parent; obsolete user copies; skill folder extra files; skill id as one identifier; design system and theme; publish path set).

Remaining alignment value is wording: `AGENTS.md` still says **local skills folder** for the destination; README heading and install examples are incomplete; project-skill and some library-skill prose still use avoided names; `LANGUAGE.md` Contents is section-only, and two T-013 residuals remain (Alignment analysis leftover “documentation”; Hook rejection “in-scope failure”); five user-invoked skills still set unused `metadata.invocation`. The T-005 testability sentence in Alignment analysis stays (T-018 accepted current `LANGUAGE.md`).

Implementation order for a later run: C-003 residual, C-002, C-009, C-004, C-005, C-006, C-007, C-008 (same wording pass as C-004–C-007), C-010 (optional last).

Do not add `docs/plans/` or a test harness. Do not rename skill ids `local-skills-folder` or `update-local-skills`. Do not migrate every `SKILL.md`.

## C-001 - AGENTS.md Authoring: project skill

Already done in this alignment run (T-014). Do not redo.

### Problem

The language document’s canonical kind is **project skill**. `AGENTS.md` Authoring used “workflow skills”. An agent that followed `AGENTS.md` without reopening `LANGUAGE.md` would use the superseded name.

### Target

Authoring uses **project skill**. Skill id remains the folder name.

### Affected areas

`AGENTS.md` Authoring (Do and Don't).

### Benefit

High

This was the primary kind-name split. `AGENTS.md` is the checkout entry point.

### Change size

Low

Two lines.

### Dependencies

Accepted `LANGUAGE.md` names (T-011). Done.

### Verification

Artifact inspection: `AGENTS.md` has no “workflow skill”; Authoring says “this checkout's project skills”. T-014 completed this check.

## C-003 - README user copies and LANGUAGE.md pointer

Mostly already done in this alignment run (T-014). Residual work is the next change. Do not redo the done portion.

### Problem

README used “install local copies”, “local install”, and a heading that did not name **project skills**. Agent directives pointed at `AGENTS.md` but not `LANGUAGE.md`.

### Target

Human catalog uses **user copy** and **user-level skills folder**. Agent directives mention `LANGUAGE.md` as the terminology document (pointer, not a glossary).

### Affected areas

`README.md` (Repo management, Install, Agent directives).

### Benefit

High

README is the human and clone-path entry. “Local copies” is on the language document’s Avoid list. The missing `LANGUAGE.md` link was the remaining discoverability gap after the `AGENTS.md` pointer.

### Change size

Low

A few sentences and a heading.

### Dependencies

Accepted `LANGUAGE.md` names (T-011). Done for the user-copy and pointer work.

### Verification

Artifact inspection: README does not use “local copies” or “local install” as the canonical install phrase; Agent directives link `LANGUAGE.md`. T-014 completed this check for the done portion.

## C-003 residual - README heading, changelog verb, destination candidates

Not done. Later implementation run.

### Problem

README heading is still “Repo management”, which does not name this checkout’s **project skills**. Agent directives still say “retired user copies” as a changelog verb. Install copy/symlink examples name only the Cursor default destination; `local-skills-folder` also considers Codex/agents and Claude Code.

### Target

Heading names **project skills** (this checkout). Changelog sentence uses added, removed, and renamed, or “obsolete user copies”, not **retired** as a changelog verb. Keep Cursor paths as the create fallback; add one sentence that other **destination candidates** exist and that automated install follows `local-skills-folder`. Do not paste that skill’s candidate table into README.

### Affected areas

`README.md` (Repo management heading, Install, Agent directives changelog sentence).

### Benefit

Medium

The High-benefit user-copy and pointer work is done. What remains is kind-name visibility, changelog verb, and destination completeness.

### Change size

Low

Heading, one verb, one Install sentence.

### Dependencies

C-003 done portion (T-014). `LANGUAGE.md` changelog of skill ids already uses “obsolete user copies” (T-015).

### Verification

Artifact inspection: heading names project skills; README changelog sentence does not use **retired** as a changelog verb; Install mentions other destination candidates and `local-skills-folder` without pasting its table. Agent review that the catalog still lists only library skills in the install copy/symlink commands.

## C-002 - AGENTS.md destination wording and definition vs pointer

Not done. Later implementation run.

### Problem

The language document destination is **user-level skills folder**. `AGENTS.md` Don't still says “Replace or empty the local skills folder” and “changelog-listed local skill”. Sync, Authoring, and Frontmatter still restated packaging definitions the language document now owns. Operational Do/Don't (suggest updating user copies, do not empty the destination, do not install project skills) are still needed; the definitions are the duplicate.

### Target

Use **user-level skills folder** for the destination. Keep operational checkout rules. Where a paragraph only restates a `LANGUAGE.md` definition (skill id, invocation kinds, client-only fields), replace with a pointer. Keep Frontmatter Do/Don't that agents need while authoring, using language-document names (`name` is the skill id written for the loader).

### Affected areas

`AGENTS.md` Sync, Authoring, Frontmatter.

### Benefit

Medium

Stops `AGENTS.md` and `LANGUAGE.md` drifting; keeps procedures next to the checkout agent.

### Change size

Medium

Must not delete operational rules while swapping names.

### Dependencies

C-001 (done). Residual “local skills folder” / “local skill” lines are independent of C-003 residual and may run in parallel with it.

### Verification

Artifact inspection: destination wording is **user-level skills folder**; “local skills folder” is not used as a destination synonym; operational Don't rules still forbid emptying the destination, touching foreign skills, copying `.cursor/skills/` into user-level directories, and installing project skills; Language section remains a pointer, not a glossary. Agent review that Frontmatter still tells an authoring agent what to write.

## C-009 - LANGUAGE.md Contents and residual polish

Not done. Later implementation run.

### Problem

Six section anchors are not enough to find **skill id**, **invocation kinds**, **user copy**, **alignment plan**, or **commit set** in a long single file. Splitting the file is not recommended (N-001).

T-015 applied T-013 F1–F10. Two residuals remain: Alignment analysis lists leftover “documentation” next to “discoverability of documentation and project decisions” (the project-alignment skill list has only the latter). Hook rejection still says “in-scope failure” next to Commit set Avoid of unqualified **in-scope**.

Do not treat the T-005 testability sentence as leftover. T-018 accepted current `LANGUAGE.md`; that sentence stays.

### Target

Expand Contents with in-section links to the main term clusters (library / repo / user / project skill; invocation kinds; writing artifact classes; orchestrator / subagent / ticket / run; alignment plan; UX finding vs ticket finding; git stage vs product decision; destination vs deletion candidate). Do not add `docs/language/`.

Drop leftover “documentation,” before discoverability of documentation and project decisions. Reword Hook rejection so it does not use unqualified **in-scope** (commit-set wording, with C-007). Keep the T-005 testability sentence.

### Affected areas

`LANGUAGE.md` Contents; Alignment analysis; Hook rejection.

### Benefit

Medium

Navigability of the agreed single language document. Residual self-contradictions T-013 still reported after T-015.

### Change size

Low

Contents list plus two sentence edits.

### Dependencies

`LANGUAGE.md` as accepted and patched (T-011, T-015). Independent of remaining `AGENTS.md` / README wording. Hook rejection wording lands with C-007 so `LANGUAGE.md` and git-stage-commit do not drift.

### Verification

Artifact inspection: Contents links reach those term clusters; still one `LANGUAGE.md`; no `docs/language/`; Alignment analysis does not list leftover “documentation” next to discoverability; Hook rejection does not use unqualified **in-scope**; T-005 testability sentence remains. Agent review that the list stays a contents list, not a second glossary.

## C-004 - Project-skill prose: destination is user-level skills folder

Not done. Later implementation run.

### Problem

`publish-skill` and `update-local-skills` frontmatter descriptions say “install into the local skills folder”. `local-skills-folder` body uses the same phrase for the destination, and its Resolve heading is unqualified “Candidates” next to later “deletion candidates”. **Local skills folder** is the skill id; the destination concept is **user-level skills folder**. LANGUAGE.md Avoid: unqualified **candidate**.

### Target

Descriptions and body use **user-level skills folder** for the destination. Qualify the Resolve table as **destination candidates**. Keep **deletion candidates** distinct. Keep skill ids `local-skills-folder` and `update-local-skills`. Keep the one-line “This is a project skill for this checkout” guard on each project skill.

### Affected areas

`.cursor/skills/publish-skill/SKILL.md`, `.cursor/skills/update-local-skills/SKILL.md`, `.cursor/skills/local-skills-folder/SKILL.md` (prose and descriptions, not folder names; Resolve table is destination candidates).

### Benefit

High

Same overloaded “local” cluster as C-003, in the procedures that actually install.

### Change size

Medium

Loader `description` lines change (user-invoked menu text, not auto-invoke routing). Body sentences change. Skill ids do not.

### Dependencies

None beyond accepted destination terms. Same files as parts of C-007 (`publish-skill`); do those as one wording pass on that file.

### Verification

Artifact inspection: destination prose is **user-level skills folder**; `local-skills-folder` Resolve table is **destination candidates**; **deletion candidates** remain a separate term; skill ids unchanged; checkout guard lines remain. Agent review that install procedure behaviour is unchanged (additive copy, skip symlinks, changelog deletion ask).

## C-005 - project-alignment: alignment plan, and qualify target-project skills

Not done. Later implementation run.

### Problem

The skill body and Start goal 4 say **implementation plan**. README and `LANGUAGE.md` use **alignment plan** for the same artifact. The skill also says “project skills” for a **target project**’s agent-facing skills, which collides with this checkout’s **project skill**.

### Target

Body uses **alignment plan**, with a note that it is the input to a later implementation run (one document, not two). Where “project skills” means the target project’s skills, say that (target project’s agent-facing skills), not this library’s checkout-only project skills.

### Affected areas

`skills/project-alignment/SKILL.md` (opening, Start goal 4, Value and change size, Plan, Completion). Two “project skills” lines in Research and Agent and project guidance.

### Benefit

Medium

This skill owns the alignment-plan term and is the collision site for **project skill**.

### Change size

Low to Medium

Several sentences in one file. Description already says “project alignment plan”. Default path in the skill may keep `docs/plans/project-alignment.md` as the generic default; this library’s established equivalent is repo-root `project-alignment-plan.md`.

### Dependencies

None beyond accepted terms. Independent of C-004 file set.

### Verification

Artifact inspection: body uses **alignment plan** for this document; target-project skills are qualified. Agent review that Start still requires orchestrated-run and still forbids implementing planned refactors in the alignment run. Do not treat a path-string change as a product behaviour change.

## C-006 - orchestrated-run: subagent for the role, worker as adjective

Not done. Later implementation run.

### Problem

The language-document role is **subagent**; **worker** is the ticket-section adjective. The skill still uses “the worker” as the executing agent. Orchestrated-run is the git hotspot, so this wording will keep being copied into tickets.

### Target

Role noun is **subagent**. Keep **worker-owned**, **worker-maintained**, and “worker sections”. Assignment-prompt text that says “the worker” can say “the subagent” or “this assignment”.

### Affected areas

`skills/orchestrated-run/SKILL.md` (Tickets, Assignment, Reconciliation, Steering, Adversarial Review, remaining “the worker” role-noun uses, and prompt templates).

### Benefit

Medium

Highest-churn library skill.

### Change size

Medium

A few dozen noun uses. Must not rename worker-maintained fields.

### Dependencies

None beyond accepted role terms. Independent of C-004–C-005 files.

### Verification

Artifact inspection: executing-role noun is **subagent**; worker-owned / worker-maintained / worker sections remain. Agent review that assignment prompts still match the shared agent rules and that ticket YAML field names are unchanged.

## C-007 - git-stage-commit: commit set; git commit vs product decision

Not done. Later implementation run.

### Problem

The language document Avoids unqualified **scope** / **in-scope** next to **commit set**, and mixing **git commit** with English “committing to” a **product decision**. The skill uses “If the user named a scope”, “in-scope work”, and “committing to a product decision”. The skill heading is `## Scope`. `publish-skill` “in-scope skill changes” / “in-scope paths” should be **publish path set** or **commit set**.

### Target

Paths this request may stage are the **commit set**. Rename `## Scope` so it is not unqualified **scope** (name **commit set**). Exclusion of orchestrated-run product choices uses a phrase that is not “committing to” (for example: it does not govern agreeing to a product decision). Hook text and LANGUAGE.md Hook rejection (C-009) switch together to commit-set wording; do not keep unqualified **in-scope** in either. `publish-skill` uses **publish path set** or **commit set** as `LANGUAGE.md` defines them.

### Affected areas

`skills/git-stage-commit/SKILL.md` (including `## Scope`). Related: `.cursor/skills/publish-skill/SKILL.md` Scope / In-scope paths.

### Benefit

Medium

Exact collision the language document documents, in the two skills that own git commit and publish.

### Change size

Low to Medium

One library skill plus publish-skill scope sentences.

### Dependencies

Do `publish-skill` sentences in the same wording pass as C-004. LANGUAGE.md Hook rejection polish is C-009; land that with or before this item.

### Verification

Artifact inspection: commit set / publish path set used for path sets; `## Scope` is not an unqualified heading; product-decision wording is not “committing to”; hook text is not unqualified **in-scope**. Agent review that git-stage-commit and publish-skill procedures are unchanged (preview vs execute, no force-push, changelog of skill ids still library-only).

## C-008 - Small collision and spelling fixes

Not done. Later implementation run. Ship with C-004–C-007 as one wording pass.

### Problem

`user-response` says “engine tickets”; canonical for that class is **engine text**, and **ticket** is the orchestrated-run name. `ux-ui-reviewer` uses UK **artefacts**; language-document spelling is **artifact**.

Do not rename publish-skill “working tree”. LANGUAGE.md Worktree: **working tree** is a synonym (N-010).

### Target

user-response matches public-docs (“engine text”). ux-ui-reviewer “artefacts” → “artifacts”.

### Affected areas

`skills/user-response/SKILL.md` (one line); `skills/ux-ui-reviewer/SKILL.md` (one word).

### Benefit

Low

Real collisions, limited effect. Include because Low/Low and they are recurring Avoid items.

### Change size

Low

### Dependencies

The two library-skill one-liners can ship with C-004–C-007 as one wording pass. No `publish-skill` phrase on this item.

### Verification

Artifact inspection: those two strings match the language document; publish-skill still says “working tree”. Agent review that no other procedure text was rewritten.

## C-010 - metadata.invocation unused field

Not done. Optional last item for a later implementation run.

### Problem

Five user-invoked skills set `metadata.invocation: user-only`. `metadata` does not affect loading; `metadata.invocation` is unused by this repo’s loading rules. `AGENTS.md` already forbids using metadata to invoke.

### Target

Strip the field from those five files. Leaving it as unused annotation is compatible with `LANGUAGE.md` as written; stripping is the recommendation because it is a client-only field this repo does not rely on.

### Affected areas

`skills/orchestrated-run/SKILL.md`, `skills/project-alignment/SKILL.md`, `skills/ux-ui-reviewer/SKILL.md`, `.cursor/skills/publish-skill/SKILL.md`, `.cursor/skills/update-local-skills/SKILL.md`.

### Benefit

Low

Confusion only if a reader treats metadata as the invoke switch.

### Change size

Low

Five frontmatter blocks. Loader behaviour unchanged.

### Dependencies

Do after C-004–C-008 so metadata strip is not mixed with prose edits on the same files. Optional; skip if a later run prefers to keep the annotation.

### Verification

Artifact inspection: field absent from those five files if stripped, or still documented as unused if kept. Agent review that `disable-model-invocation: true` remains the user-invoked control and that no client-only field was added.

## Changes not recommended

### N-001 - Split LANGUAGE.md into docs/language/ domain files

Benefit: Medium
Change size: High

Agreed language location is one `LANGUAGE.md`. C-009 is the navigability fix that stays inside that decision. Layout, pointers, and T-003 / NG-005 all forbid a `docs/language/` tree.

### N-002 - Broad SKILL.md terminology migration (especially ux-ui-reviewer)

Benefit: Medium in this library’s language document; Low for agents who only load ux-ui-reviewer on a target project (unqualified “module” and “library” are correct in a UI review).
Change size: High

`LANGUAGE.md` already qualifies UX finding, UI module, component library. Migrating the reviewer body would add this-library collisions into a skill whose audience is another project’s UI. NG-003. Owner-skill passes C-005–C-008 are the bounded alternative.

### N-003 - Rename skill ids local-skills-folder or update-local-skills

Benefit: Medium (ids would match destination wording).
Change size: High

Skill id is stable. C-004 changes prose only. `LANGUAGE.md` already says Local skills folder is the skill id, not the destination synonym. Changelog of skill ids, user copies, slash-command ids, and callers would all move.

### N-004 - Extract a third writing skill or merge public-docs and user-response

Benefit: Low for a two-skill split that already works; independent install requires each user copy to carry the rules it applies.
Change size: High

Keep skill-owned, non-identical AI-tell lists. Duplicated tells are required runtime copy, not a locality bug. NG-005. New library skill id or a merge would need changelog and install commands.

### N-005 - Sync overlapping AI-tell catalogs into one list

Benefit: Low. Punctuation tells already match. Catalog breadth differs on purpose (user-response allows a group of three; public-docs forbids forced groups of three).
Change size: Medium if merged; Low if only stock-word tweaks.

Merging would change chat behaviour. Not language alignment. Leave lists skill-owned.

### N-006 - Slim project-alignment’s restated orchestrated-run process

Benefit: Medium (less duplicate process text).
Change size: High

The skill is user-invoked and must still specify Start goals and which ticket types to use. Independent install of project-alignment still depends on orchestrated-run; the restatement is how this specialised run starts. Already says it requires `/orchestrated-run`. Rewriting Start is behaviour-adjacent and low value next to C-005.

### N-007 - Remove “This is a project skill for this checkout” from the three project skills

Benefit: Low
Change size: Low

Project skills are not independently installed, but an agent that opens one skill file still needs the install guard. That is conceptual locality of the constraint, not duplication to delete. C-004 keeps these lines.

### N-008 - Test harness or checkable-contract programme

Benefit: Low for this alignment (testability is out of this run’s analysis).
Change size: High

T-005 / H-008. Verification stays artifact inspection and agent review. Do not add a test runner as organisation (NG-005).

### N-009 - Reorganise skill folders or add docs/plans/

Benefit: Low
Change size: High for folder reorg; Medium for a docs tree that this repo does not use.

NG-001, NG-005. Plan path is repo-root `project-alignment-plan.md`. Folder layout already matches `LANGUAGE.md`. Do not create `docs/plans/`.

### N-010 - Rename publish-skill “working tree” to worktree

Benefit: Low
Change size: Low

LANGUAGE.md Worktree: **working tree** is a synonym. git-stage-commit and update-local-skills already say worktree. Forcing one spelling is not required. C-008 does not change publish-skill “working tree”.

### N-011 - Restyle README catalog lines to LANGUAGE.md writing terms

Benefit: Low (public-facing vs human-facing copy; temporary response artifacts vs response-only artifacts).
Change size: Low

LANGUAGE.md: README catalog lines are human summaries, not frontmatter descriptions. Not a loader or procedure collision.
