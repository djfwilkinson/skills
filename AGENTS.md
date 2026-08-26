# Agent directives

## Language

When naming, describing, or changing project concepts, read [LANGUAGE.md](LANGUAGE.md).

## Sync

Library skill, repo copy: `skills/<name>/`
Library skill, user copy: the matching folder in this machine's user-level skill directories
Project skill: `.cursor/skills/<name>/` in this checkout only

Do:
- After commit, pull, or edit of `skills/`, suggest updating the user copies from the repo
- When the user invokes `publish-skill` or `update-local-skills`, follow that skill instead of only suggesting
- Record added, removed, and renamed library skill ids in `CHANGELOG.md` when publishing
- When installing, read and follow `.cursor/skills/local-skills-folder`. Do not invoke it.
- If a user copy has edits missing from the repo, suggest updating the repo from that user copy
- If both differ, show the difference and ask

Don't:
- Overwrite without agreement
- Replace or empty the local skills folder
- Touch user-level skills that are not in this repo
- Copy `.cursor/skills/` into user-level skill directories
- Delete a changelog-listed local skill without confirmation
- Suggest an update when the user copy is already the same files as the repo
- Suggest installing project skills into user-level directories

## Authoring

Do:
- Put library skills (installed on other machines) in `skills/<name>/SKILL.md`; folder name is the skill id
- Put this checkout's project skills in `.cursor/skills/<name>/SKILL.md`; folder name is the skill id
- User-invoked: `disable-model-invocation: true`
- Auto-invoked: omit that field
- Referenced-only: `disable-model-invocation: true`; description states it is not invoked; callers read the SKILL.md. The loader may still list it as a slash command; do not start it that way
- After create or edit of a library skill, suggest updating the user copies

Don't:
- Put library skills anywhere except `skills/`
- Put this checkout's project skills anywhere except `.cursor/skills/`
- Copy project skills to user-level skill directories

## Readme

Do:
- Keep README.md listing every skill in `skills/` with a one-line description and a link to its SKILL.md
- Record skill dependencies
- Keep Install matching how this repo is actually installed
- Keep the Agent directives pointer at AGENTS.md
- Keep CHANGELOG.md matching added, removed, and renamed library skill ids
- Credit a source only when this library took something from it, and say what was taken

Don't:
- Credit specs, product docs, or other material that was only consulted
- Credit work that originated here
- Leave the skill list, install steps, or CHANGELOG.md stale after adding, removing, or renaming a skill
- List `.cursor/skills/` entries in the install copy or symlink commands

## Frontmatter

Write each field for the loader job. Only `name` and `description` are in context before activation.

Do:
- `name`: slash-command id; must match the parent folder
- `description`: routing text the model matches against the user request. Auto-invoked: what it does and when to load it, ≤1024 chars. User-invoked: short menu line, no trigger keywords. Referenced-only: states it is not invoked, no trigger keywords
- `argument-hint`: slash-menu placeholder when the skill takes extra text
- Keep descriptions that contain `:` valid YAML

Don't:
- Use `name` as a human title
- Use `metadata` to discover, invoke, or permission a skill
- Set `paths` on these user-level skills
- Add client-only fields unless every target loader parses them
- Expect `license`, `compatibility`, `icon`, or `color` to affect loading or triggering
