# Skills

Cursor agent skills I keep here so I can install them on another machine.

- [public-docs](skills/public-docs/SKILL.md): Write public-facing docs and copy without AI tells.
- [user-response](skills/user-response/SKILL.md): Shape chat replies and temporary response artifacts without a heavy rewrite pass.
- [orchestrated-run](skills/orchestrated-run/SKILL.md): Run a project through one orchestrator, shared run files, and large tickets worked by personas on models you choose.
- [defect-capture](skills/defect-capture/SKILL.md): Capture defect reports in parallel as durable defect tickets.
- [orchestrated-defect-run](skills/orchestrated-defect-run/SKILL.md): Capture defects or pick up open ones, then triage, resolve, check, and review them through orchestrated-run.
- [project-alignment](skills/project-alignment/SKILL.md): Establish a project's shared language and write an alignment plan or implement the alignment changes.
- [ux-ui-reviewer](skills/ux-ui-reviewer/SKILL.md): Review an implemented interface and optionally capture selected findings as defects.
- [git-stage-commit](skills/git-stage-commit/SKILL.md): Analyze git changes, group them, and stage and commit.
- [grill-to-done](skills/grill-to-done/SKILL.md): Question the user in grouped rounds with quick-pick defaults until a plan or design is settled.
- [orchestrated-plan](skills/orchestrated-plan/SKILL.md): Survey sources in parallel, settle questions, and produce a reviewed plan file the user has accepted twice.
- [orchestrated-product-run](skills/orchestrated-product-run/SKILL.md): Frame a product problem, review wireframes or production-styled mocks, approve wholesale proposals, deliver the minimal clean build as Product Owner, then report defects for a defect run to group and fix.

orchestrated-run needs Python 3.9 or later for its action ledger, a local web page that lists open asks, keeps completed runs available as archived history, and serves run-local mocks; for the snapshot script reviewers use to read a finished unit of work while the next one is being written; and for the scripts that choose models for personas and report which models past runs used. Snapshots need git; without it, reviewers read the live files. It keeps its files in `~/.agent-runs/`, including the model database and your model choices, and reads ticket-source definitions from `skills/orchestrated-run/ticket-sources/` (`filesystem.md` by default). orchestrated-run uses user-response for the wording of its asks and progress updates. project-alignment depends on orchestrated-run. orchestrated-defect-run depends on orchestrated-run and defect-capture, including the defect-ticket contract bundled with it. ux-ui-reviewer depends on defect-capture and orchestrated-defect-run for its optional finding capture and resolution handoff. A UX/UI review inside an orchestrated-run is an Agent Task that reads ux-ui-reviewer. Adversarial Review of completed UI work may also read that skill. orchestrated-plan depends on orchestrated-run, grill-to-done and user-response, and defines its own `locator`, `plan-author` and `plan-reviewer` personas in a file beside its skill, leaving orchestrated-run unchanged. orchestrated-product-run depends on orchestrated-run, grill-to-done and user-response, offers orchestrated-defect-run when it completes, and defines its own `locator`, `product-partner`, `product-designer` and `prototyper` personas in a file beside its skill. grill-to-done stands alone and also follows user-response when it is installed.

## Repo management

[.cursor/skills](.cursor/skills/) is for this checkout only. Do not copy it to `~/.cursor/skills/`.

- [publish-skill](.cursor/skills/publish-skill/SKILL.md): commit library skill changes, push to origin, and install user copies
- [update-local-skills](.cursor/skills/update-local-skills/SKILL.md): pull the latest and install user copies
- [local-skills-folder](.cursor/skills/local-skills-folder/SKILL.md): shared install steps, not invoked on its own

## Install

Clone this repo, then copy or symlink each folder in `skills/` into `~/.cursor/skills/`.

Copy:

```sh
git clone https://github.com/djfwilkinson/skills.git
cd skills
mkdir -p ~/.cursor/skills
cp -R skills/public-docs ~/.cursor/skills/
cp -R skills/user-response ~/.cursor/skills/
cp -R skills/orchestrated-run ~/.cursor/skills/
cp -R skills/defect-capture ~/.cursor/skills/
cp -R skills/orchestrated-defect-run ~/.cursor/skills/
cp -R skills/project-alignment ~/.cursor/skills/
cp -R skills/ux-ui-reviewer ~/.cursor/skills/
cp -R skills/git-stage-commit ~/.cursor/skills/
cp -R skills/grill-to-done ~/.cursor/skills/
cp -R skills/orchestrated-plan ~/.cursor/skills/
cp -R skills/orchestrated-product-run ~/.cursor/skills/
```

Symlink, so edits in this checkout apply without recopying:

```sh
git clone https://github.com/djfwilkinson/skills.git
cd skills
mkdir -p ~/.cursor/skills
ln -s "$(pwd)/skills/public-docs" ~/.cursor/skills/public-docs
ln -s "$(pwd)/skills/user-response" ~/.cursor/skills/user-response
ln -s "$(pwd)/skills/orchestrated-run" ~/.cursor/skills/orchestrated-run
ln -s "$(pwd)/skills/defect-capture" ~/.cursor/skills/defect-capture
ln -s "$(pwd)/skills/orchestrated-defect-run" ~/.cursor/skills/orchestrated-defect-run
ln -s "$(pwd)/skills/project-alignment" ~/.cursor/skills/project-alignment
ln -s "$(pwd)/skills/ux-ui-reviewer" ~/.cursor/skills/ux-ui-reviewer
ln -s "$(pwd)/skills/git-stage-commit" ~/.cursor/skills/git-stage-commit
ln -s "$(pwd)/skills/grill-to-done" ~/.cursor/skills/grill-to-done
ln -s "$(pwd)/skills/orchestrated-plan" ~/.cursor/skills/orchestrated-plan
ln -s "$(pwd)/skills/orchestrated-product-run" ~/.cursor/skills/orchestrated-product-run
```

## Agent directives

[AGENTS.md](AGENTS.md) is for agents working in this checkout. Shared terms are in [LANGUAGE.md](LANGUAGE.md). Keep `skills/` and the machine's user copies in sync. Write each frontmatter field for the job the loader gives it, not for what the name sounds like. [CHANGELOG.md](CHANGELOG.md) records added, removed, and renamed library skill ids so install can copy this library's skills and ask before deleting retired user copies.

## Credits

- [Matt Pocock's skills library](https://github.com/mattpocock/skills): influenced orchestrated-run and project-alignment; grill-to-done took the design tree, the rounds, the recommended answer on each question, and the rule that agents find facts while users make decisions from its grilling skill
- [pstack's unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md): used as the basis for public-docs and user-response
