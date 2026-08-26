---
name: publish-skill
description: >-
  Commit skill changes with git-stage-commit, push to origin, and install into
  the local skills folder.
disable-model-invocation: true
argument-hint: "[optional skill names]"
metadata:
  invocation: user-only
---

# Publish skill

This skill is user-invoked. Start it only when the user explicitly invokes `publish-skill`.

This is a project skill for this checkout (`.cursor/skills/`). Do not copy it to user-level skills.

Commit in-scope skill changes with `git-stage-commit`, push to origin, then follow `local-skills-folder` to install library skills. Update `CHANGELOG.md` before the commit when the set of library skill ids in `skills/` changes.

## Scope

In-scope paths:

- named library skill folders under `skills/` when the user passed names;
- otherwise every changed path under `skills/`;
- changed paths under `.cursor/skills/` that belong to the same work;
- `CHANGELOG.md` when library skill ids were added, removed, or renamed;
- `README.md` and `AGENTS.md` when those edits belong to the same skill work.

Do not commit unrelated files. Do not record `.cursor/skills/` ids in `CHANGELOG.md`.

## Procedure

1. Confirm this checkout is the skills library (`skills/<name>/SKILL.md`).
2. Compare library skill ids in the working tree (`skills/<name>/SKILL.md` folders) to `HEAD`. Detect added and removed folder names. Treat a git rename (`git diff --name-status -M`) as `renamed`. If git does not report a rename and the same publish has exactly one removed id and one added id, record `renamed`. Otherwise record separate `removed` and `added` entries. Do not guess across several adds and removes.
3. If any library ids were added, removed, or renamed, update `CHANGELOG.md` before staging. Prepend a `## YYYY-MM-DD` section for today, or append bullets to today's section if it already exists. Dated sections may only contain `added`, `removed`, and `renamed` bullets in the format used in that file. Do not rewrite older sections. If the library skill set did not change, leave `CHANGELOG.md` as it is.
4. Read `git-stage-commit` and follow it for the in-scope paths, including `CHANGELOG.md` when it changed. That skill owns grouping, messages, secrets handling and the commit itself.
5. Stop if the commit was only a preview, was blocked, or created no commit and the branch is not ahead of origin.
6. Push the current branch to origin. Set upstream if it has none. Do not force-push.
7. Read `.cursor/skills/local-skills-folder/SKILL.md` and follow it. Do not invoke it as a slash command.

Report the commit hash and message, whether the push succeeded, and the facts `local-skills-folder` returns.
