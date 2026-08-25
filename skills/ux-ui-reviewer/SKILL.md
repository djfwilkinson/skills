---
name: ux-ui-reviewer
description: >-
  Strict pragmatic review of an implemented interface for task completion,
  hierarchy, consistency, forms, feedback, accessibility, responsive behaviour,
  content and maintainability.
disable-model-invocation: true
argument-hint: "[optional screen, flow or area]"
metadata:
  invocation: user-only
---

# UX/UI review

Review an implemented interface as a user completing a task. Report concrete usability, consistency, accessibility and maintainability problems. Do not redesign the product, invent features, or propose large refactors.

Scope: the named screen, flow or area first. Nearby flow only when it affects the same task.

If this file is on an orchestrated-run ticket's Reads, follow it as the ticket contract.

Look for the project's design system, component library and theme. Use them as references for what the interface should be doing.

This skill reports correctness. Inconsistency is incorrect too. Preferring existing components, modules and library options is a consistency rule: implement with what the project already has, do not invent a parallel. Established does not mean right. If a design system, library, theme or established pattern has a UI/UX problem, raise a finding. If that source lives in the project, it is in scope.

## Authority

1. When choosing how to implement a fix, project guidelines, components, modules, tokens, layout and theming win when they exist.
2. Then prefer the native component library's props, variants, slots, layout utilities, configuration and theming over custom CSS. Do not recommend custom CSS when the library already supports the behaviour.
3. Do not recommend a native library component, prop, slot or utility when the project already provides an equivalent. Item 1 outranks item 2.

Other preferences:

- Established project patterns over novel ones. Simple maintainable implementations over elaborate ones.
- Reuse existing project components, editors, forms and interaction patterns. DRY shared behaviour; do not abstract a few repeated lines.
- Project semantic tokens over literal colours, spacing or one-off styling. Colour through the project theme, including light and dark.
- Targeted fixes. Do not replace a working flow unless there is a clear user-facing problem.
- Challenge unnecessary screens, dialogs, steps, prompts and confirmations.
- Visual polish is not UX.
- User-facing terms over implementation terms.
- Every recommendation states the user problem it solves.

## Inspection

Default: if a simple, fast, efficient visual path is already obvious (documented URL, running app, existing preview command, or a path given in the ticket or Reads), use it. Do not invent a visual path. Do not add preview infra to make one.

Default: throwaway scripts are allowed when the direction is clear and obvious and the required tools are already installed. You may write a short script on that path. Do not install new tools or frameworks. Delete any artefacts this task created before return.

If the caller, ticket or assignment revokes browser or throwaway scripts, do not use them.

Record in Evidence whether the finding came from code, visual inspection, a throwaway script, or more than one.

## Section importance

Each section has `importance: high | medium | low`. That is how much weight to give the section when findings compete. It is not finding severity and not review order.

Walk the user's task flow. Apply every relevant section. Do not skip a `high` section because it appears later.

## Sections

### Task completion

`importance: high`

User goal. Main action identifiable. Task completable without guessing. No unnecessary steps. No asking for known information. No internal-only distinctions. Important actions not hidden without reason. Default path is the common path. Predictable end state. Recovery after mistakes. Destructive actions distinct from ordinary ones.

Report stop, hesitate, misunderstand, abandon.

### Information hierarchy

`importance: high`

Most important information dominant. Primary action more prominent than secondary. Descriptive headings. Related grouped, unrelated separated. Not equal-weight noise. Progressive disclosure where appropriate. Scannable. Context at the point of need. Labels clearer than icons alone.

No decorative hierarchy changes unless they improve comprehension or task completion.

### Interaction consistency

`importance: high`

Similar actions look and behave similarly. Buttons, links, menus, selectable rows used consistently. Row click predictable. Primary actions placed consistently. Save, cancel, close, back, delete consistent. Dialogs consistent. Equivalent forms structured the same. Same terms for the same concepts.

### Module consistency

`importance: high`

Same problem uses the same project module, component or pattern. No near-duplicate modules. No bypassing a project wrapper for a library primitive. Shared editors, tables, dialogs, lists and form kits reused. Drift between copies of the same module flagged.

### Layout consistency

`importance: high`

Shared page chrome, grids, spacing rhythm, breakpoints and content width used the same way across screens in the flow. Alignment and density match sibling views. Stacking and responsive composition follow the project's layout system. One-off layout that breaks the established structure flagged.

### Navigation and context

`importance: high`

User knows where they are. Specific page or dialog title. Return path clear. Back goes where expected. List position, filtering or selection preserved after view or edit. Nested screens or dialogs not confusing. Destinations discoverable. Opening an item goes to the right view. No unnecessary intermediate choice screens.

No breadcrumbs unless the hierarchy requires them.

### Forms and data entry

`importance: high`

Labels always visible. Placeholders are examples, not labels. Sensible defaults. Field order matches the user's task. Optional and required honest. Validation beside the field and how to fix it. Data preserved after errors. Input types fit the data. Disabled fields explained when the reason is not obvious. Save omitted when changes can apply immediately. Existing project form or editor reused.

Flag forms that expose database or implementation structure.

### Feedback and system state

`importance: high`

Every user action has understandable feedback: loading, empty, error, success, disabled, saving, partial-data, offline if relevant, permission-restricted. Destructive actions confirmed. Duplicate submissions prevented. Completion indicated.

No intrusive success UI for routine actions when inline state is enough.

### Error prevention and recovery

`importance: high`

Invalid actions prevented rather than rejected later. Destructive actions separated. Consequence clear. Accidental changes undoable. Cancel predictable. Warnings only when the consequence is real. Context-change behaviour or ownership warned. Errors keep enough context to recover. Failed actions retryable.

Confirmation only for meaningful, hard-to-reverse consequences.

### Accessibility

`importance: high`

Keyboard for all functionality. Focus visible. Focus order follows visual and task order. Dialog focus trapped and restored. Correct semantics. Accessible names. Icon-only controls labelled. Sufficient contrast. Colour not the only channel. Comfortable touch targets. Errors associated with fields. Usable when text is enlarged. Motion not required to understand state. Disabled controls understandable. Heading levels logical.

Fix semantics through the project's components before custom accessibility code.

### Responsive behaviour

`importance: high`

Narrow, medium, wide. No clipped important content. No accidental horizontal scroll. Actions reachable. Dialogs and forms fit small screens. Tables adapt rather than shrink. Touch layouts do not depend on hover. Stacked order still logical. Fixed elements do not obscure content. Long, translated and user-generated text wraps. Large screens not wasted. Mobile is not a broken subset of the core task.

No separate mobile and desktop implementations when the project's responsive composition is enough.

### Visual consistency

`importance: high`

Spacing scale, typography roles, semantic colours, borders, elevation, radii, icon set, variants: the project's, not one-off values. Alignment communicates relationships. Density fits the task. Custom CSS not overriding project or library behaviour the project already uses. One-off pixels flagged when visible, repeated, or harmful to hierarchy.

Do not report tiny cosmetic differences otherwise.

### Content and terminology

`importance: medium`

Labels are user concepts. Buttons name the action. Avoid vague actions ("Submit", "Continue", "OK") when a specific label is possible. Empty states say what the area is and what to do next. Errors in plain language. Descriptions do not repeat labels. Terminology consistent in the workflow. Concise without omitting needed context. Capitalisation and punctuation consistent. Instructions at the point of need.

### Implementation maintainability

`importance: medium`

Only when it affects UX consistency or future UI maintenance.

Duplicated project components. Rebuilt project or library features. CSS fighting the project's system. Literals instead of project tokens. Repeated rules likely to drift. Presentation coupled to one data example. Scattered state conditionals. Abstractions that make the interaction harder. A fix that requires disproportionate refactoring.

Smallest maintainable fix for the user-facing problem.

## Do not

- Complete redesign without a critical structural failure.
- Invent product requirements, or add features because other products have them.
- Animation as a default improvement.
- Taste as a usability issue. Perfect visual fidelity for inconsequential differences.
- Minor polish as a release blocker.
- Vague findings ("make this cleaner", "improve accessibility").
- Refactor without showing how it fixes the reported UX problem.
- Repeat the same root problem.
- Treat more options as a better experience.

## Finding severity

Exactly one per finding. Independent of section importance.

- `blocker`: primary task cannot be completed, data may be lost, or a serious accessibility barrier.
- `high`: a common task is confusing, error-prone, or substantially harder than necessary.
- `medium`: noticeable friction, inconsistency or misunderstanding that does not prevent completion.
- `low`: polish or consistency with limited effect on task completion.

Cosmetic issues are not `high` or `blocker`.

## Finding format

```text
### [severity] <what is wrong>
section: <section name> (importance: high | medium | low)
location: <screen, component or interaction>
user problem: <what the user experiences and why it matters>
evidence: <code | visual | script | mixed>; <detail>
recommended fix: <smallest specific change>
preferred implementation: <project module, component, token, pattern; library only if the project has no equivalent>
```

No finding without both a user problem and a concrete fix.

## Summary

1. Blockers
2. High
3. Medium and low
4. Module, layout or visual consistency drift
5. Library use that bypasses a project equivalent
6. Sections reviewed with no finding

Order findings by severity, then task flow.
