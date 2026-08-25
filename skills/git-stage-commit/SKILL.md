---
name: git-stage-commit
description: >-
  Analyses git changes and prepares, stages or creates reviewable git commits.
  Load whenever a request is about preparing or creating git commits, staging
  files in git or invoking git-stage-commit.
---

# Git stage and commit

Apply this skill to work that prepares or changes the git index or creates git
commits. Where it applies, its safety and workflow rules are required.

This skill governs git staging and commit work. It does not govern staging
environments, committing to a product decision or orchestrated-run work unless
the user also asked for git commit work.

## Authority

Follow git and commit rules supplied by the user or project. They win for scope,
grouping and message structure. Use this skill where those rules are silent.

Look for explicit guidance in project rules, `AGENTS.md`, contributor docs and
commit tooling. Inspect recent commits for the repository's established message
format and commit granularity.

An explicit stage or commit request authorises ordinary non-destructive git
operations only. Project rules do not waive these safeguards:

- do not push unless the user explicitly asked;
- do not run destructive git operations, rewrite history or discard work unless
  the user separately authorised it;
- do not stage environment files, credentials, private keys or other secrets
  unless the user explicitly included them;
- do not bypass hooks unless the user explicitly asked; and
- do not amend a commit after a hook rejected it.

## Scope

Apply this skill when the user asks to:

- prepare, group or preview git commits;
- stage files in git;
- create one or more git commits; or
- invoke `git-stage-commit`.

Do not apply it to:

- staging or deployment environments;
- committing to a decision or course of action;
- general git work with no staging or commit task; or
- internal instructions that say an agent must not commit.

## Use agent-compatible git

Use git output and invocation forms that an agent can consume:

- start with machine-readable status such as
  `git status --porcelain=v1 -b`;
- use `--no-pager` with `log`, `diff` and `show`;
- use non-interactive commands and pass commit messages without opening an
  editor; and
- do not use interactive add or rebase.

## Analyse

Inspect the whole worktree before changing it. Establish the branch, staged,
unstaged and untracked paths, diff summaries and recent commit messages. Use
targeted staged or unstaged diffs when a change or commit boundary is unclear.

If the user named a scope, stay within it. If the user asked to commit without
a narrower scope, include the current changes except secrets. Preserve
unrelated work. If existing staged changes conflict with the intended groups,
stop and ask rather than silently changing their staging state.

## Group

Follow the repository's grouping rules and recent commit granularity. Where the
repository is silent, group files by observable relationships such as package
or folder cohesion, a manifest and its lockfile, a change and its tests, types,
docs or wiring, and files that must move together for correctness.

Do not invent motivation or mix unrelated changes. Split when diffs show
separate change types or unrelated work.

## Write messages

Follow the repository's message structure. Where none exists, use Conventional
Commits as the fallback:

```text
<type>[optional scope]: <imperative factual subject>
```

Keep the subject under 72 characters. Common fallback types are `feat`, `fix`,
`docs`, `refactor`, `test`, `chore` and `build`.

## Execute

Do not stage or commit unless the user asked for that work. For a plan or
preview, report the proposed groups and messages, then stop.

Otherwise, stage only the first group, commit it with the repository's required
non-interactive message form and check status. Repeat one group at a time until
the in-scope work is committed or blocked.

If a hook rejects a commit, fix only a clear in-scope failure and create a new
commit attempt. Do not amend the rejected commit.

Report created hash and message pairs, whether the in-scope work is complete and
any remaining paths. If blocked, report the issue, why user input is required
and the expected groups.
