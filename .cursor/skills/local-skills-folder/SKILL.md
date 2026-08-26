---
name: local-skills-folder
description: Internal. Do not invoke. Local skills-folder install used by publish-skill and update-local-skills.
disable-model-invocation: true
---

# Local skills folder

Do not start this skill on its own. Read and follow it only when `publish-skill` or `update-local-skills` tells you to.

This is a project skill for this checkout (`.cursor/skills/`). Do not copy it to user-level skills.

Copy this library's skills from `skills/` additively into the machine's user-level skills folder. Then ask before deleting local folders this library removed or renamed. Do not copy `.cursor/skills/`. Do not replace or empty the local skills folder. Do not touch skills this library never shipped.

## Resolve the folder

Resolve a home directory from `$HOME`, then `$USERPROFILE`, then the current user's home.

Prefer a candidate that already contains folders matching this repo's library skill names (`skills/`). If several match, pick the one with the most matches. If none exist, create the Cursor default.

Candidates, in preference order:

| Environment | Path |
| --- | --- |
| macOS / Linux (Cursor) | `$HOME/.cursor/skills` |
| Windows (Cursor) | `%USERPROFILE%\.cursor\skills` |
| Codex / agents | `$HOME/.agents/skills` or `%USERPROFILE%\.agents\skills` |
| Claude Code | `$HOME/.claude/skills` or `%USERPROFILE%\.claude\skills` |

Do not install into `skills-cursor` (Cursor-managed built-ins).

## Copy

Copy each library skill (`skills/<name>/` that contains `SKILL.md`) into `$dest/<name>/`. Overwrite files in that skill folder. Do not copy folders from `.cursor/skills/`. Do not sync, mirror, or delete the local skills folder as a whole, and do not remove sibling folders as part of copy. If `$dest/<name>` is a symlink, skip that skill (the checkout is already live). Create `$dest` if needed.

Unix example:

```sh
rsync -a skills/<name>/ "$dest/<name>/"
```

Windows example:

```powershell
robocopy skills\<name> "$dest\<name>" /E
```

`robocopy` exit codes 0-7 are success.

## Changelog deletions

Copy does not delete. After the additive copy, read `CHANGELOG.md` and collect local folders to ask about:

- renamed: `old-id` -> `new-id`: `old-id` is present locally and is not a current library skill under `skills/` (the new id was already copied).
- removed: `skill-id`: `skill-id` is present locally and is not a current library skill under `skills/`.

Skip a line when the id is still in `skills/` (it was re-added) or is not present locally. Leave every other local folder alone, including skills that never came from this library.

Show the candidate list and wait for confirmation. Delete only the folders the user agrees to remove. If a confirmed path is a symlink, remove the link only. Do not follow it. On PowerShell, delete a symlink without `-Recurse`.

## Return

Tell the caller the install destination, copied skills, skipped symlinks, deletion candidates, and what the user confirmed.
