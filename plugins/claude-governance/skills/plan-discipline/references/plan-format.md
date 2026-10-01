# Plan Format | plan-discipline

**Purpose:** Standard structure for a plan document — a phased effort toward a stated end state, maintained across sessions.

---

## File naming

`[target-name]-[kind]-plan.md` — for an improvement effort, `[target-name]-improvement-plan.md`.

---

## Required sections

### Header

```
# [Target Name] Improvement Plan
**Created:** YYYY-MM-DD
**Status:** [Planning | In progress — Phase N complete YYYY-MM-DD | Complete]
**Session context:** [One sentence on what triggered this plan]
```

---

### North Star

What the target should look like when the improvement is done. Written as principles or a brief description — not a task list. This section anchors all decisions made during execution.

---

### Current State

What the target looks like now. Factual, not evaluative. Written after the audit.

---

### Gap Analysis

Table mapping current state to north star. Identifies what needs to change and why.

| Area | Current | North Star | Gap |
|---|---|---|---|

---

### Issue coverage map

Required where the plan works issues-log entries. One row for every open entry on every log the plan touches — every open entry, not only those the plan fixes — naming the entry, the log it sits on now, its decision (fix, redirect, defer or close), its target log, and the phase working it. The retirement redraft is built from this map.

| Entry | Log now | Decision | Target log | Phase |
|---|---|---|---|---|

---

### Improvement Roadmap

Ordered phases. Each phase ends with a contributor checkpoint before the next begins.

For each phase:
- Phase name and status (⏳ pending / 🔄 in progress / ✅ complete)
- What will be done
- What decisions need to be made
- A `⏸ HUMAN CHECKPOINT [Governance]` or `⏸ HUMAN CHECKPOINT [Token]` marker

---

### Drafts Inventory

Track files produced during the improvement. Update status as work progresses.

| File | Status | Notes |
|---|---|---|
| `filename.md` | 🔄 Drafted / ✅ Reviewed / ✅ Applied | |

---

### Deferred Items

Anything surfaced during the improvement that is out of scope for this plan, each with the trigger that would bring it back.

---

### Session Worklog

The last section of the file. One entry per session, oldest first and appended at the end, in the entry format this skill's SKILL.md states under Worklog.

---

## Behavioural rules

- The plan is approved before execution begins
- Section order and content match the Required sections above; a plan may add sections of its own between them. `scripts/plan_check.py` checks the order
- Maintenance mechanics — worklog format, phase-status markers, cross-plan impact — are this skill's SKILL.md, not this template
