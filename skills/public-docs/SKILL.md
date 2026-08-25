---
name: public-docs
description: >-
  Writes and edits public human-facing copy, including README files, published
  documentation, changelogs, release notes, GitHub descriptions, human-facing
  work items, landing pages, emails, UI strings, error messages and other
  user-facing copy in source files. Load whenever a request creates or changes
  that copy.
---

# Public docs

Apply this skill to copy written for people outside the agent workflow. Where it
applies, its writing process is required.

This skill governs copy intended for a repository, publication, product or human
work tracker. `user-response` governs chat and response-only artifacts such as
Canvas or temporary Markdown, even when the harness stores them in a file.

## Authority

Follow copy, tone and terminology rules supplied by the user or project. They
win where they conflict with this skill. Use this skill where those rules are
silent.

Look for explicit guidance in project rules, contributor docs and brand or
content guides. Do not treat nearby copy as a rule unless the project identifies
it as a convention.

Facts, exact required wording and legal obligations take priority over style.

## Scope

Apply this to:

- README files, published docs, changelogs, release notes and GitHub
  descriptions;
- landing pages, marketing copy, help text, emails and other public prose;
- Jira, Linear and GitHub work items written for people;
- user-facing product strings, including strings stored in source files. Apply
  it to the copy, not the surrounding code.

Do not apply it to:

- `SKILL.md`, `AGENTS.md`, `.cursor/rules` or other agent instructions;
- orchestrated-run tickets, run files, internal plans, prompts or other engine
  text written for agents;
- reasoning, tool inputs, code, diffs, schemas, fixtures or structured data;
- implementation comments, API contracts or internal identifiers;
- licenses, legal text, quotations or wording that must remain exact;
- response-only artifacts such as Canvas or temporary Markdown;
- the chat reply that reports the work. Use `user-response` for that.

## Write and review

For a new page or section, or a substantial multi-paragraph rewrite:

1. Identify the audience and what the copy must help them know or do.
2. Preserve facts, links, commands, names, requirements and intentional terms.
3. Scan the draft for the tells below.
4. Rewrite it in plain, specific language.
5. Add human voice where it clarifies what matters.
6. Ask, "What makes this obviously AI generated?" Fix the answer.

For a short description, product string, small edit or conventional instruction
block, make the same checks in one pass. Do not turn a small edit into a writing
workshop.

## Write for people

- Say what the reader needs to know or do.
- Say what something does, not how it feels. Name the mechanism, result or
  number.
- Be specific. If a generic sentence adds no information, cut it or ground it in
  this project. Keep conventional instructions when they state an exact step the
  reader needs.
- Prefer active voice when the actor is known.
- Use the plain word and split sentences that make the reader backtrack.
- Use "I" or "we" only when a real person or project owner is speaking.
- Have a point of view when the facts support one. Do not invent balance or
  attribution.
- Let some human irregularity remain. Do not force equal sections, repeated list
  shapes or a rule of three.
- Use sentence-case headings and lists only when they help the reader.

## Remove AI tells

### Content and claims

- Puffery and promotional language such as pivotal, testament, vibrant,
  groundbreaking, renowned and must-visit.
- Vague attribution such as "experts believe", "industry reports suggest" and
  "some critics argue".
- Name-dropping that lists people, publications or tools without explaining
  their relevance.
- Superficial `-ing` phrases that imply a consequence without explaining it,
  such as highlighting, ensuring, reflecting, showcasing and fostering.
- Formulaic contrast, generic challenges and conclusions that say nothing
  specific.
- Cutoff disclaimers such as "While specific details are limited" when the copy
  can state the known facts or omit the claim.
- Chatbot phrases or sycophancy such as "Great question", "Certainly" and "I
  hope this helps".

### Language

- Stock words such as additionally, crucial, delve, enduring, enhance, garner,
  interplay, intricate, landscape as an abstraction, showcase, tapestry and
  underscore.
- Fancy ways to say "is", including serves as, stands as, boasts and features.
- "Not just X, but Y" framing and false "from X to Y" ranges.
- Synonym cycling. Pick the right term and reuse it.
- Filler, stacked hedging, weak adverb-plus-verb pairs and fancy synonyms.
- Abstract metaphors such as substrate, wedge, vector, nexus, scaffolding,
  modality, paradigm, north star and flywheel when a concrete word exists.

### Structure and punctuation

- Perfectly balanced sections, forced groups of three and repeated list shapes.
- Dense sentences that stack unrelated clauses.
- Bold labels that restate the sentence, decorative emojis, curly quotes and
  title-case headings.
- Colons used as sentence connectors. Colons are fine before a real list or
  example.
- Em dashes or en dashes used as prose punctuation. Preserve hyphens, minus
  signs, ranges, names, commands, code and quoted text that require them.

## Final check

Confirm that:

- explicit project copy rules were followed;
- facts, links, commands and exact wording still match the source;
- each section of substantial copy gives the reader useful information;
- the result has no obvious tell listed above.
