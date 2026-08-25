# Skills

Cursor agent skills I keep here so I can install them on another machine.

- [public-docs](skills/public-docs/SKILL.md): Write public-facing docs and copy without AI tells.
- [user-response](skills/user-response/SKILL.md): Shape chat replies and temporary response artifacts without a heavy rewrite pass.
- [orchestrated-run](skills/orchestrated-run/SKILL.md): Run a project through one orchestrator, shared run files, and ticketed subagents.
- [project-alignment](skills/project-alignment/SKILL.md): Establish a project's shared language and write an alignment plan.
- [ux-ui-reviewer](skills/ux-ui-reviewer/SKILL.md): Review an implemented interface for task completion and related UX problems.
- [git-stage-commit](skills/git-stage-commit/SKILL.md): Analyze git changes, group them, and stage and commit.

project-alignment depends on orchestrated-run. A UX/UI review inside an orchestrated-run is an Agent Task that reads ux-ui-reviewer.

## Install

Clone this repo, then copy or symlink each folder into `~/.cursor/skills/`.

Copy:

```sh
git clone https://github.com/djfwilkinson/skills.git
cd skills
mkdir -p ~/.cursor/skills
cp -R skills/public-docs ~/.cursor/skills/
cp -R skills/user-response ~/.cursor/skills/
cp -R skills/orchestrated-run ~/.cursor/skills/
cp -R skills/project-alignment ~/.cursor/skills/
cp -R skills/ux-ui-reviewer ~/.cursor/skills/
cp -R skills/git-stage-commit ~/.cursor/skills/
```

Symlink, so edits in this checkout apply without recopying:

```sh
git clone https://github.com/djfwilkinson/skills.git
cd skills
mkdir -p ~/.cursor/skills
ln -s "$(pwd)/skills/public-docs" ~/.cursor/skills/public-docs
ln -s "$(pwd)/skills/user-response" ~/.cursor/skills/user-response
ln -s "$(pwd)/skills/orchestrated-run" ~/.cursor/skills/orchestrated-run
ln -s "$(pwd)/skills/project-alignment" ~/.cursor/skills/project-alignment
ln -s "$(pwd)/skills/ux-ui-reviewer" ~/.cursor/skills/ux-ui-reviewer
ln -s "$(pwd)/skills/git-stage-commit" ~/.cursor/skills/git-stage-commit
```

## Agent directives

[AGENTS.md](AGENTS.md) is for agents working in this checkout. Keep `skills/` and the machine's user-level copies in sync. Write each frontmatter field for the job the loader gives it, not for what the name sounds like.

## Credits

- [Matt Pocock's skills library](https://github.com/mattpocock/skills): influenced orchestrated-run and project-alignment
- [pstack's unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md): used as the basis for public-docs and user-response
