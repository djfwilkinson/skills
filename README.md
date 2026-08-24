# Skills

Cursor agent skills I keep here so I can install them on another machine.

- [orchestrated-run](skills/orchestrated-run/SKILL.md): Run a project through one orchestrator, shared run files, and ticketed subagents.
- [project-alignment](skills/project-alignment/SKILL.md): Establish a project's shared language and write an alignment plan.

project-alignment depends on orchestrated-run.

## Install

Clone this repo, then copy or symlink each folder into `~/.cursor/skills/`.

Copy:

```sh
git clone https://github.com/djfwilkinson/skills.git
cd skills
mkdir -p ~/.cursor/skills
cp -R skills/orchestrated-run ~/.cursor/skills/
cp -R skills/project-alignment ~/.cursor/skills/
```

Symlink, so edits in this checkout apply without recopying:

```sh
git clone https://github.com/djfwilkinson/skills.git
cd skills
mkdir -p ~/.cursor/skills
ln -s "$(pwd)/skills/orchestrated-run" ~/.cursor/skills/orchestrated-run
ln -s "$(pwd)/skills/project-alignment" ~/.cursor/skills/project-alignment
```
