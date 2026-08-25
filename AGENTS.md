# Agent directives

## Sync

Repo copy: `skills/<name>/`
User copy: the matching folder in this machine's user-level skill directories

Do:
- After commit, pull, or edit of `skills/`, suggest updating the user copies from the repo
- If a user copy has edits missing from the repo, suggest updating the repo from that user copy
- If both differ, show the difference and ask
- If a skill was removed from the repo, suggest removing the user copy

Don't:
- Overwrite without agreement
- Touch user-level skills that are not in this repo
- Suggest an update when the user copy is already the same files as the repo

## Authoring

Do:
- Put skills in `skills/<name>/SKILL.md`; folder name is the skill id
- User-invoked: `disable-model-invocation: true`
- Auto-invoked: omit that field
- After create or edit, suggest updating the user copies

Don't:
- Put skills anywhere else in this repo

## Readme

Do:
- Keep README.md listing every skill in `skills/` with a one-line description and a link to its SKILL.md
- Record skill dependencies
- Keep Install matching how this repo is actually installed
- Keep the Agent directives pointer at AGENTS.md
- Credit a source only when this library took something from it, and say what was taken

Don't:
- Credit specs, product docs, or other material that was only consulted
- Credit work that originated here
- Leave the skill list or install steps stale after adding, removing, or renaming a skill

## Frontmatter

Write each field for the loader job. Only `name` and `description` are in context before activation.

Do:
- `name`: slash-command id; must match the parent folder
- `description`: routing text the model matches against the user request. Auto-invoked: what it does and when to load it, ≤1024 chars. User-invoked: short menu line, no trigger keywords
- `argument-hint`: slash-menu placeholder when the skill takes extra text
- Keep descriptions that contain `:` valid YAML

Don't:
- Use `name` as a human title
- Use `metadata` to discover, invoke, or permission a skill
- Set `paths` on these user-level skills
- Add client-only fields unless every target loader parses them
- Expect `license`, `compatibility`, `icon`, or `color` to affect loading or triggering
