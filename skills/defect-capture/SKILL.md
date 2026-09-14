---
name: defect-capture
description: Capture defect reports into a durable defect list through one background ticket writer per report. Use only when explicitly invoked by the user.
disable-model-invocation: true
argument-hint: "[optional list name or existing defect-list path]"
---

# Defect capture

This skill is user-invoked. Start it only when the user explicitly invokes
`defect-capture`.

Read [DEFECT-TICKETS.md](DEFECT-TICKETS.md) before creating, assigning,
updating, or recovering a defect ticket. It owns the schema, field ownership,
status lifecycle, and ticket-writer prompt.

## Start or resume a list

Use the current project as the target project.

When the invocation identifies an existing defect-list folder, resume it.
Otherwise create:

`<project>/.agent-runs/defect-lists/<timestamp>-<short-name>/`

Create its `assets/` directory when the first attachment needs to be copied.
When creating `<project>/.agent-runs/`, add `.agent-runs/` to the project
`.gitignore` if that line is missing. Create `.gitignore` if needed.

Use stable defect IDs such as `D-001`. Scan existing `D-*.md` files, then
allocate the next number. Creating the placeholder reserves that ID. Never
reuse an ID.

One user context bundle is one defect unless the user clearly supplies several
independent defects. For several, allocate and dispatch one ticket per defect.
Do not merge reports merely because they concern the same area; triage owns
duplicate and relationship decisions.

## Capture a defect

For each submitted defect:

1. Allocate its ID and create `D-<number>.md` from the contract template with
   `status: backlog`, `capture_state: drafting`, and a unique non-null
   `capture_owner` assignment identifier. Include the user's original text
   under Captured context before dispatch so a failed writer cannot lose it.
2. Copy supplied images and screenshots into `assets/`. Name them with the
   defect ID, a sequence number, and a safe form of the original filename. Do
   not overwrite an existing asset. Link the copied paths from the placeholder.
   If a source cannot be copied, retain its source path and record that it is
   not yet durable.
3. Dispatch one background subagent with the initial ticket-writer prompt from
   `DEFECT-TICKETS.md`, the defect path, the user's context, and the copied
   attachments. Pass the same assignment identifier. Give attachments to the
   subagent as images when the client supports it.
4. Return to the user after dispatch with the allocated ID and list path. Do
   not wait for other ticket writers before accepting the next defect.

If dispatch fails before the writer starts, retain the placeholder and captured
context, set `capture_state: failed`, record the failure, and clear
`capture_owner`.

Each subagent owns only its assigned defect file. Independent writers may run
in parallel because their ticket and asset paths are disjoint.

If background subagents are unavailable, state that capture will be sequential
and execute the same prompt one ticket at a time.

## Reconcile writers

When a writer returns, read its ticket:

- `capture_state: ready` means the report is usable;
- `capture_state: failed` retains the captured context and error for retry;
- an invalid or incomplete record is failed, not silently treated as ready.

Record the assignment result in History, then clear `capture_owner`. Before
dispatching a retry, confirm that field is `null`, assign a new identifier, and
preserve the original context and earlier evidence.

After compaction, treat every non-null `capture_owner` as an active ownership
claim. Resume or wait for that assignment when the client can identify it. Do
not dispatch another writer until the coordinator has evidence that the prior
assignment returned or no longer exists.

Recover the active list from the invocation when it names one. Otherwise scan
defect-list folders for non-null capture owners. Resume the only matching list;
when several lists have active owners, ask which capture session the user
means. Do not select a list merely because its timestamp is newest.

If the user adds information to an existing defect, append it under Additional
context with its capture time. Use the amendment-writer prompt with a new
`capture_owner` when synthesis is needed; never replace the earlier report or
evidence and never change capture state for an amendment.

If an orchestrated defect run is active for the list, classify the amendment as
steering before dispatch. Check active run-ticket Reads and any inspection
freeze for a conflict with the source defect or evidence paths. Queue the
amendment without editing the source while a conflict exists. After the
amendment returns and `capture_owner` is cleared, continue through the run's
amendment-steering process.

## Start defect resolution

When the user asks to start resolving the current list, start
`/orchestrated-defect-run <defect-list-path>` in this conversation. Do not copy
the defect tickets into the orchestrated-run folder.

Capture may continue while that run is active. Each newly ready defect enters
the run through its steering process. Tickets still drafting or failed are not
eligible for triage.

During an active run, allocating and dispatching a user-submitted capture and
acknowledging its ID are defect-capture process work. The defect-run working
hint authorises that acknowledgement in addition to orchestrated-run's normal
returns for closed tickets and human asks.
