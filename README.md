# Skills

Cursor agent skills I keep here so I can install them on another machine.

## Skills

- [orchestrated-run](skills/orchestrated-run/SKILL.md): Run a project through one orchestrator, shared run files, and ticketed subagents.
- [project-alignment](skills/project-alignment/SKILL.md): Establish a project's shared language and write an alignment plan.

project-alignment depends on orchestrated-run.

## Install

Copy each folder into `~/.cursor/skills/`:

```sh
cp -R skills/orchestrated-run ~/.cursor/skills/
cp -R skills/project-alignment ~/.cursor/skills/
```

Or:

```sh
npx skills add djfwilkinson/skills
```
