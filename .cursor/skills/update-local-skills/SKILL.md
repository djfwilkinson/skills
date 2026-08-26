---
name: update-local-skills
description: Pull the latest from origin and install into the local skills folder.
disable-model-invocation: true
metadata:
  invocation: user-only
---

# Update local skills

This skill is user-invoked. Start it only when the user explicitly invokes `update-local-skills`.

This is a project skill for this checkout (`.cursor/skills/`). Do not copy it to user-level skills.

Pull the latest from origin in this skills library, then follow `local-skills-folder` to install library skills from `skills/`.

## Procedure

1. Confirm this checkout is the skills library (`skills/<name>/SKILL.md`).
2. If the worktree has uncommitted changes, stop and ask. Do not pull over them.
3. Fast-forward pull from the tracked origin branch. If the pull cannot fast-forward, stop and report. Do not rebase or force.
4. Read `.cursor/skills/local-skills-folder/SKILL.md` and follow it. Do not invoke it as a slash command.

Report the pull result and the facts `local-skills-folder` returns.
