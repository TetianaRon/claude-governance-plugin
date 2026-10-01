---
name: plan-discipline
description: >
  Creates and maintains plan documents — the phased, session-spanning record of an
  improvement or build effort: its north star, phases, decisions, status and worklog.
  Use when asked to "make a plan", "write up the plan", "update the plan", "review this
  plan", "record this decision in the plan", "mark the phase complete", or "retire the
  plan", and whenever a session advances, executes from, or reviews an existing plan.
  Not for a one-off to-do list or a business proposal.
---

# plan-discipline

**Version:** v1.0

---

## Issues log

Identifier: GOV
Log: `ISSUES.md` at the root of the claude-governance plugin repo

---

## Plans are dynamic

A plan document is the source of truth for the effort it describes. It stays current at all times, not only at the end of a session.

**Creating a plan, or restructuring one:** load `references/plan-format.md` and follow its structure.

**Checking a plan's currency:** run `python3 <skill-dir>/scripts/plan_check.py <plan-file>` after each plan update that changes a phase status or adds a worklog entry, and before a plan is presented for review. Fix every problem it reports before continuing. `<skill-dir>` is the directory reported when this skill loaded.

---

## Plan document standard

### Cross-plan impact

When a decision is made, assess its impact across the full plan before moving on. Do not update only the item currently in progress. Check:

- Are any other phases affected by this decision — including completed ones?
- Does the file structure, routing table, north star, or architectural decisions section need updating?
- Are any prior decisions now superseded or partially wrong?

Update all affected locations before continuing, completed phases included.

### Approval-to-execution gate

After any contributor checkpoint is passed — a phase approved, a review accepted, a deliverable confirmed — update the plan to record the approval before executing the next step. Do not proceed from approval to execution without the plan reflecting the checkpoint was passed.

This is a hard stop. Executing changes after an approval without first updating the plan is a workflow failure.

### Worklog

Every session that touches a plan adds a worklog entry. The worklog is the last section of the plan file, `## Session Worklog`. It is chronological: oldest entry first, and each new entry appended at the end of the file.

Format:

```
### Session N — YYYY-MM-DD
[What was done. Decisions made. Phase statuses updated.]
```

`YYYY-MM-DD` is the contributor's local date. Where the environment's date can differ from it, confirm the date with the contributor rather than taking the environment's.

Record decisions as they are made, not at the end of the session.

### Phase status

Mark phases with their current status immediately when status changes:

- ⏳ pending
- 🔄 in progress
- ✅ complete YYYY-MM-DD

Never leave a completed phase marked as in progress. Never mark a phase complete until the contributor checkpoint has been passed.

**Checkpoint marker.** A roadmap phase's pause point for contributor sign-off carries one of the two checkpoint markers, `⏸ HUMAN CHECKPOINT [Governance]` or `⏸ HUMAN CHECKPOINT [Token]`, and no other.

### Completed phases

Mark completed phases — do not delete them. A completed phase is updated whenever a later decision affects it, so the plan reads as one coherent document rather than a sequential log.

### Plan retirement

A plan's working life ends when every phase in it is complete — not one phase, the whole plan. Retirement does not gate on the status of an issues log's entries.

**The resolution redraft comes first.** Before the retirement prompt, redraft every issues log the plan's issue coverage map touches, under the skill named for issue logging under Referrals: remove the entries the plan's released work resolved, and move its Deferred Items to those logs' Deferred sections. Apply the redrafts to the logs, or hand them over where a log is not writable, and retire only once they have landed.

⏸ HUMAN CHECKPOINT [Governance] — the contributor chooses the plan's retirement:

```
Question: "Every phase in this plan is complete. Retire the plan file?"
Options:
- Yes, delete it — git history is the record now
- Move it to an archive location instead
- Not yet — keep it as-is
```

Never retire a plan without asking. A plan that is merely between phases is still active. A new cycle on the same target drafts a fresh plan rather than reusing a closed one.

---

## Plan canonicity and memory

When a plan is active, the plan is the canonical record for decisions made, phase status, and what was done and why. Memory is complementary — not a substitute.

- **Record decisions in the plan first.** Do not update memory as the primary record of a plan-relevant decision.
- **Memory may supplement** — capturing cross-session context such as user preferences or project-level facts — but is never the only place a decision lives.
- **If plan and memory conflict, the plan wins.**
- **At session wrap-up:** review any memory entries made during the session. If any duplicate or contradict the plan, bring memory into alignment with the plan — not the other way around.

---

## Live plan revision

When a plan document is open for review and the contributor gives feedback on a section, apply the edit to the plan file immediately — before reading or discussing the next section. Do not batch changes for the end of the review.

After applying the edit, ask before continuing, and wait for the answer:

```
Question: "Applied to the plan. Is your review complete, or is more coming?"
Options:
- Review complete — continue
- More feedback coming — wait
```

---

## Referrals

- `issue-logging` — drafting the issues-log redrafts a plan's retirement requires

## Behavioural rules

- Record every decision in the plan as it is made — in the affected phase section and in the worklog
- Assess every decision's impact across the whole plan, completed phases included, before moving on
- Update the plan to record a passed checkpoint before executing the next step
- Update a phase's status the moment it changes; never mark a phase complete before its checkpoint passes
- Run the resolution redraft before offering retirement, and never retire a plan without asking, only once every phase is complete
