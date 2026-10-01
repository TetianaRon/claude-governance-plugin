---
name: session-discipline
description: >
  Universal session startup behaviors for governed Claude projects and skills: opening
  message check, source loading discipline, out-of-scope boundaries, model
  recommendation, reading plan confirmation, session wrap-up, token efficiency, and the
  guards on mounted-surface writes, git operations and identifying data. This is a
  session-startup gate — load it as the first action when a governed session begins,
  before engaging with task content.

  Triggers at the start of any session whose project instructions name this skill, when
  a handoff message opens the session, or when the opening message signals continuing
  prior governed work ("picking up", "continue", "session start", "handoff"). Where
  project instructions name this skill, those instructions govern invocation.
user-invocable: false
---

# session-discipline

**Version:** v1.0

---

## Issues log

Identifier: GOV
Log: `ISSUES.md` at the root of the claude-governance plugin repo

---

## Session behaviors — apply on every invocation

**Startup gate.** When a project's instructions define a startup sequence, the full sequence completes before any task content is processed. Loading this skill is not the whole gate — confirm every startup skill the project requires is loaded first. A task-rich opening message or handoff does not change this order.

This skill's body holds the fundamentals every session needs, plus a trigger condition for each detailed behavior. When a trigger fires, load the named sub-file and follow it in full before continuing — never paraphrase it from memory of a prior session.

### 0. Opening message check

Before asking for any context, link, or specification, read the opening message in full. Extract everything it already provides — task intent, project or skill name, mode or workflow named (e.g., "targeted adjustment", "improve", "new skill"), artifacts or files mentioned, decisions already described, goals or constraints stated, deferred session files, rework plans, issue lists, handoff messages, or any other content that answers a question Claude would otherwise ask as part of session startup or task identification. Treat extracted context as confirmed. Do not ask for something the opening message already supplies.

### 1. Source loading discipline

Load only sources the current phase requires. Do not fetch pages speculatively. A source the current step does not need is not loaded, even where it seems likely to be useful later.

### 2. Out-of-scope boundaries

Do not ask whether anything is out of scope. An exclusion the contributor names — in the opening message or at any point in the session — is a hard boundary for the session: produce no output on the excluded area, and do not flag its exclusion as a gap.

### 3. Issue logging

**Trigger:** Claude or the contributor notices a workflow issue — incorrect output, workflow gap, redundant step, routing failure, documentation drift, or missing guardrail. The task type is owned by the skill named for it under Referrals.

### 4. Model recommendation standard

**Session-health check.** Before significant work, and again at each phase boundary or natural milestone, assess whether the session's context is already long. Read the surface's own measure of context use where it reports one, rather than judging by feel. Where the check flags a long session, recommend wrapping and starting fresh before the next phase of work.

Once Claude has enough context to scope the work ahead, recommend the most efficient model for the remaining task — even where that means switching from the current one.

**Rest the recommendation on the confirmed current model.** Read it where the surface reports it — in the session environment or in an opening handoff. Where it is not reported, ask the contributor. Never infer it from behaviour, and never assume it carried over from a prior session.

Be specific: name the model, give a one-line reason, and, for a mixed task, note which parts each model suits.

**Model mismatch check.** Where the session opens with a handoff recommending a model, compare it to the current model before significant work. Where they differ, ask:

```
Question: "The handoff recommends [model] but you're on [current model]. How would you like to proceed?"
Options:
- Switch to [model] — follow the handoff recommendation
- Continue with [current model] — stay on the current model
```

Repeat the recommendation whenever the task's scope materially changes — planning → implementation, drafting → QA, research → writing — and another model fits the new scope better.

**Trigger:** the contributor agrees to switch models mid-session. Load `workflows/model-handoff.md` and follow the handoff process before the model changes.

### 5. Reading plan confirmation

Before loading any source beyond what the current step requires, state what you intend to read and why, and wait for the contributor's go-ahead. A short prose statement and an implicit go-ahead are sufficient.

### 6. Session wrap-up

**Trigger:** the natural close of a session, or before handing off to another model or surface.

Producing a close or a handoff is its own trigger, checked fresh at the moment of producing it — loading this skill earlier in the session does not satisfy it. Load `workflows/session-wrapup.md` and follow it in order every time a close or handoff is written. For a handoff, also load `workflows/model-handoff.md` in full for its format, rather than drafting a summary from memory of it.

### 7. Token efficiency

Avoid these by default:

1. **Post-edit re-reads** — do not re-read a file you just wrote or edited, except where §9's trigger applies.
2. **Full-file reads for partial content** — use offset and limit when only a section is needed. State which section before reading.
3. **Verbose response preamble** — do not open responses with "Here's what I'll do…" summaries. Begin with the work. *(This covers narration only — it does not suppress review completion checks or phase confirmations.)*
4. **Sequential calls that could be batched** — combine them into a single call where possible, except where a guard says to run a command alone.
5. **Over-long drafts before scope confirmation** — for substantial outputs, confirm scope and structure before producing a full draft.
6. **Subagent-drafted content not persisted as produced** — content a subagent drafts to persist (a document, a migration, a long draft) is written to a file as it is produced, not carried back only on its return payload.

Project skills may override specific rules where the project context warrants it.

---

### 8. Plan work and review awareness

**Trigger — plan work:** the session works with a plan document in any way — advancing its phases, executing from it, updating its status, or reviewing it. The task type is owned by the skill named for it under Referrals.

**Review in progress.** When the contributor is reviewing content and gives feedback, a batch of notes does not signal the end of the review. After applying a batch, confirm before moving on:

```
Question: "Applied. Is your review complete, or do you have more?"
Options:
- Review complete — move to the next item
- More feedback coming — wait
```

Do not proceed to the next task until the contributor signals the review is done.

---

### 9. File integrity check

**Trigger:** a write to a device-bridge or otherwise mounted path, a write through an MCP write tool, or a multi-line edit to a file that will ship. Writes to the session's own scratch space are exempt. Load `guards/file-integrity.md` and check the write before the next edit.

---

### 10. Inference flagging

When answering a question that needs information not yet confirmed:

1. **Name the gap first** — state what is missing or unconfirmed before answering.
2. **Label inferences explicitly** — where proceeding despite the gap, mark it: "Assuming X — confirm before acting on this."
3. **Keep inferences out of external-facing outputs** — issue entries, documentation pages, handoff messages, git commit messages, memory files and similar outputs never present inferred facts as confirmed.
4. **Ask when correctness is critical** — where the information is critical to correctness, ask before answering rather than inferring.
5. **Flag before persisting to memory** — a memory file is a session-spanning, external-facing output. Where a memory would generalize a single contributor statement into a broader constraint or boundary (an access restriction, a scope limit, a standing preference), restate the inferred scope to the contributor, or ask, before persisting it. A statement about one situation is not a rule for every future one.

The default is to surface the gap, not to fill it silently.

---

### 11. Connector and tool availability

**Trigger:** a system reminder or prior message states a connector or server needs authentication or is unavailable, and Claude is about to tell the contributor a capability is blocked. Load `guards/tool-availability.md` and follow it before reporting.

---

### 12. Bulk writes and dispatch pacing

**Trigger:** about to execute many similar external writes built from one pattern, run a single oversized fetch, or dispatch several fetches or subagents together. Load `guards/bulk-write.md` and follow it before starting.

### 13. Commit messages

**Trigger:** about to compose a commit message, or run `git commit` with an inline message. The task type is owned by the skill named for it under Referrals. For a git write against a device-bridge mounted repo, §16 applies as well.

### 14. Structured questions

**Trigger:** about to call AskUserQuestion, or to deliver a file in a turn that also asks a question. Load `guards/ask-user-question.md` and follow it.

### 15. Substantial output is structured for a decision

**Trigger:** a response carries more than roughly three findings, options or items the contributor has to act on. Load `tasks/structured-output.md` and shape the response by it.

### 16. Device-bridge behavior

**Trigger — git:** about to run a git write (`add`, `commit`, `tag`) against a device-bridge mounted repo, or to rely on sandbox `git status`, `git log` or `git diff` output from one. Load `guards/device-bridge-git.md`.

**Trigger — writes:** about to make a multi-line edit or run a packaging or build script on a Windows-mounted path, to re-stage a path with `device_stage_files`, or a large-content write has stalled once on a device-bridge surface. Load `guards/device-bridge-writes.md`.

### 17. Identifying data

**Trigger:** data that identifies a person — an IP address, a visitor or fingerprint ID, a name or email address tied to a record — enters the session through a shared file, a paste or a tool result. Load `guards/identifying-data.md` and follow it before working with the data.

---

## Human Checkpoint Convention

Two categories of checkpoint apply across all projects and workflows.

**⏸ HUMAN CHECKPOINT [Governance]** — Claude does not proceed past this point until the human explicitly confirms. Use when: the action is irreversible or difficult to undo; the decision requires organisational judgment; the output will be seen by people outside the project; a prior session's decision is being re-litigated.

**⏸ HUMAN CHECKPOINT [Token]** — Claude pauses here. The human completes this step and returns the result before Claude continues. Use when a human completing the action manually is significantly cheaper and the human effort is low (under a minute). Recurring token handoff patterns are logged in the project's issues log as candidates for permanent workflow redesign.

Both checkpoint types are hard stops. Neither can be bypassed based on context or perceived intent.

**Command formatting at checkpoints:** when handing off git or shell commands, format them for easy copy-paste: (1) each command in its own fenced code block, and (2) multiple `git add` paths grouped on a single `git add` line.

---

## Referrals

- `issue-logging` — logging a workflow issue
- `plan-discipline` — working with a plan document
- `doc-formatting` — drafting or restructuring user-facing documentation
- `git-commit-message` — composing a commit message

## Behavioural rules

- Never load a sub-file speculatively — only what the current trigger requires
- Load only what the current project's instructions or a numbered trigger explicitly directs

---

## Sub-files — load only when a trigger fires

| Sub-file | When to load |
|---|---|
| `workflows/model-handoff.md` | §4 — the contributor has agreed to switch models mid-session; §6 — a handoff is being written |
| `workflows/session-wrapup.md` | §6 — session close or handoff |
| `guards/file-integrity.md` | §9 — a mounted-path write, an MCP write, or a multi-line edit to a shipping file |
| `guards/tool-availability.md` | §11 — about to report a connector or tool as unavailable |
| `guards/bulk-write.md` | §12 — a batch of similar external writes, an oversized fetch, or concurrent dispatch |
| `guards/ask-user-question.md` | §14 — an AskUserQuestion call, or a file delivery in a turn that also asks |
| `guards/device-bridge-git.md` | §16 — a git write or git-output reliance on a device-bridge repo |
| `guards/device-bridge-writes.md` | §16 — a Windows-mounted multi-line edit or packaging run, a `device_stage_files` re-stage, or a stalled large write |
| `guards/identifying-data.md` | §17 — identifying data enters the session |
| `tasks/structured-output.md` | §15 — a response carrying more than roughly three items to act on |
| `tasks/fetch-failure.md` | The project relies on documentation pages or several source pages per session |
| `tasks/complexity-estimate.md` | The session involves QA-style or long-running work where scope and cost are material |
| `tasks/multimode.md` | The project has more than one runnable mode and mode selection is non-trivial at session start |
| `tasks/skip-guardrail.md` | The project enforces a strict session startup sequence where skipping steps causes invalid output |
