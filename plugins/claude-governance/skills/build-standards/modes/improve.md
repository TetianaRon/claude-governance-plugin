# Improve | build-standards

**Purpose:** Orchestrate improvement work on any skill or project — including this skill itself — from targeted adjustments through full audit-and-plan cycles. Improve owns the plan when one exists and maintains coherence across the entire improvement effort.

---

## When to use this mode

Use when:
- A targeted adjustment needs to be made to a skill or project
- A skill or project needs auditing, refining, or updating
- An improvement plan exists and needs executing
- This skill itself needs QA, optimisation, or maintenance

---

## Intake

Ask what is being improved:

```
Question: "What are we improving?"
Options:
- A skill (this one included)
- A project
- A subagent
- A plugin
```

Ask for the skill or project name — one target, or a set of targets for a multi-target audit. Claude will read the files directly if accessible; otherwise ask for the skill zip or a link to its files for each. Do not continue until that context is loaded for every named target.

**Drift check (Hybrid shared projects).** If the target is a Hybrid project — a claude.ai Project with a separate repo-backed local surface — confirm the repo-backed instruction file matches the live claude.ai Project copy before treating it as current. Ask the contributor to confirm the repo file is current, or read the live project-knowledge doc directly and reconcile any difference, before proceeding.

**Version drift.** Where the session can reach an installed copy of the target, compare the version in its entry-point file with the source's, and flag a difference before work starts.

Then ask:

```
Question: "How would you describe the scope of this work?"
Options:
- Targeted adjustment — a specific, clearly defined change
- Broader improvement — needs audit and a plan before we start
```

If **targeted adjustment**: skip Phase 1 and Phase 2. Load the Design sub-file for the target's class at its improvement entry point and apply the change. If the change writes a new rule, script or automated mechanism, apply guards/rule-writing-gate.md inline first. Still run session close at the end.

If **broader improvement**: proceed through Phase 1 → Phase 2 → Phase 3 in order.

If an improvement plan already exists for this target, check its status before deciding how to proceed — a prior plan is not automatic license to skip the audit:

- **Resuming the same, still-open piece of work** (a phase was approved and left mid-execution, or the contributor is picking up exactly where a prior session on this same audit stopped) — load the plan and skip to Phase 3.
- **Starting a new, distinct improvement cycle** on a target whose existing plan is complete, held, or blocked — this is not a continuation. Do not skip to Phase 3 and do not append the new work into the old plan file. Run a fresh Phase 1 (Audit) against current standards and draft a genuinely new North Star in Phase 2, even though a prior plan exists for this target. Start a new plan file for this cycle — reserve reusing/extending a plan file for continuations within the *same* audit, never as a shortcut across separate cycles.

When in doubt which case applies, ask the contributor rather than assuming the old plan still governs.

---

## Phase 1 — Audit

**Architectural fit.** Before the class audit, ask of the target's content — task files above all — whether any of it belongs in a different governed class, given the classes the estate has: a recurring project workflow as a skill, a delegable step as a subagent or as ad-hoc dispatch, a set of co-released skills as a plugin. Record each answer as a finding. The class audit below is one input to Phase 1, run against the shape this step leaves.

**Rule fitness.** For each rule the target states, name the failure it prevents for this target, and weigh it against the checks in guards/rule-writing-gate.md. A rule whose purpose cannot be named, or whose purpose belongs to another kind of artifact, is a finding. Where the purpose is not recoverable from the target's issues log or git history, ask the contributor.

Load the target. Assess against the relevant standard:

- Skill → references/skill-standards.md
- Project → references/project-standards.md
- Plugin → references/plugin-standards.md
- Subagent → references/subagent-standards.md
- A standards file itself → references/standards-format.md

Each class file states the rules it adds to `references/common-standards.md`; load that alongside it.

If the target has a `qa-standards.md`, load it and include its criteria in the audit alongside the generic standards.

If the target has an issues log, retrieve all active issues and include them in the audit. Read the "Issues log" section in the target's SKILL.md or CLAUDE.md to get the log's location, then read that document. Drafting and resolving its entries is owned by the skill named for issue logging under SKILL.md's Referrals.

**Issues-log coverage check (global or multi-target audits).** Before assessing targets, confirm every skill and project is accounted for. Take the master list from the skill and project source trees the session can reach. Each issues log is findable only through its own declaration. Confirm, for each skill or project on the master list, that its "Issues log" section declares a location. Flag any skill or project with none declared — a real gap. Ask where the log lives, and record the resulting location in that target's "Issues log" section:

```
Question: "[target] declares no issues log. Where should it live?"
Options:
- The shared `ISSUES.md` of the repo holding its source
- An `ISSUES.md` of its own
- Other — I'll name it
```

**Stale-assumption check (direct project-knowledge writes).** For every audit target, check whether its guidance assumes Claude cannot write project-knowledge docs directly on a Cowork-attached claude.ai Project — project-standards.md's "Claude-writable project knowledge" section states the actual behaviour. Watch for phrasing like "Claude cannot upload/write this directly" or "prompt the contributor to re-upload," applied to a doc that already exists as project knowledge, and correct it to that section's rule. This is distinct from the custom-instructions field, which stays genuinely unwritable (project-standards.md's "Updating project instructions" section) — do not flag a correct statement about that field as an instance of this same stale assumption.

**Multi-target audits — dispatching the auditor.** Where an audit covers more than one target, dispatch the auditor subagent named under SKILL.md's Referrals once per target. Give each dispatch, as absolute paths:

- `TARGET` — the target's directory, or its file where the target is a single file
- `STANDARDS` — the class file named above for the target's class, plus `references/common-standards.md`
- `SCOPE` — the target's own directory, plus the directory of every file the target names
- `OUTFILE` — a findings file of its own, in the session's scratch space

Read each findings file, not the return summary, and record the scope each dispatch used alongside its findings. Settle every item under Judgment calls with the contributor. Carry out every Not assessable check in the session, from the source it names. A dispatch that returned with no findings file did not complete: dispatch that target again. A target's `qa-standards.md` criteria and its issues-log entries are assessed in the session, alongside the findings.

Identify gaps — specific, actionable, traceable to a standard or observed failure.

**An issues log is one input to the audit, not a substitute for it.** If "broader improvement" was triggered by a backlog of open issues-log entries, still assess the target against its relevant standard (skill-standards.md or project-standards.md) — do not let triaging the ticket list stand in for a genuine standards-based audit.

**Before including a fix that adds a new automated mechanism or rule**, apply guards/rule-writing-gate.md. A gap that doesn't clear that check belongs in Deferred Items as a watch-item, not as a roadmap phase — not every finding needs a new gate.

---

## Reorganising across a proposed boundary

When an audit proposes moving content between files, sub-files or skills, classify every reference crossing the proposed boundary before accepting or rejecting it. Only a necessary reference — as `references/skill-standards.md`'s Necessary references section defines it — blocks the boundary. Every other class is resolved rather than counted:

| Class | Meaning | Resolution |
|---|---|---|
| **Incidental** | A convenience pointer or a "see also"; deleting it loses nothing | Delete it |
| **Inverted** | A lower layer pointing forward into a higher one — a reference or guard file pointing at a mode | Cut it; the edge is itself a defect, whether or not anything moves |
| **Relocatable** | The edge exists because content sits in the wrong file | Move the content |
| **Duplicative** | The same rule is stated on both sides | Consolidate to one owner |
| **Scoping** | One side is written as specific to the other, and the edge would disappear if it were written generically | Rewrite the scope |

**Measure necessary references, not total references.** Report the necessary count as the finding, and the others as the work that resolves them.

---

## Phase 2 — Plan

Draft an improvement plan in the format owned by the skill named for plan work under SKILL.md's Referrals.

Present the full plan to the contributor before proceeding — deliver the plan file directly into the conversation alongside the in-chat summary so the contributor has the actual document, not just a description. Do not begin execution until the plan is approved.

⏸ **HUMAN CHECKPOINT [Governance]** — plan approved before execution begins.

---

## Phase 3 — Execute

When the contributor is ready to execute a phase, load the Design sub-file SKILL.md names for the target's class, at the improvement entry point that sub-file states. Design mode applies the changes. Improve remains active throughout to maintain the plan.

**A handed-off inventory is re-checked before it is executed.** Where a phase works a list of textual instances — stale pointers, actor names, duplicated phrasing — built in an earlier session or by a subagent, re-run the search that defined the list against the current file set first, and add every instance the list missed.

---

## Plan maintenance

Plan mechanics — cross-plan impact, worklog format, phase-status markers, live revision during review, retirement — are owned by the skill named for plan work under SKILL.md's Referrals. Within this workflow they fire: after each decision made during Phase 3 execution, at each phase end before confirming the next phase's scope, and whenever the contributor is reviewing the plan document itself.

---

## Optional closing sweep — instruction-cleanliness verification

Once every phase in a broader-improvement plan is complete, offer one additional pass: re-check the target's full file set against the Instruction cleanliness standard (`common-standards.md`), even where an earlier phase already ran a cleanliness rewrite. This is optional and offered, not run by default; decline and move to session close if the contributor passes.

This is a narrow find-and-fix pass, not a new cycle — no new North Star or plan file needed, and no re-run of Phase 1's full audit. Present any findings as a single batch for review before writing.

```
Question: "Want a closing instruction-cleanliness sweep before we wrap this plan up?"
Options:
- Yes — run the sweep
- No — go straight to session close
```

---

## Session close

At the end of every session:

- Update the plan with all decisions made and current phase status (or note the targeted adjustment made)
- If the target has an issues log and any issue was noticed but not yet drafted this session, draft it now, under the skill named for issue logging.
- If a skill was updated, confirm its source is saved at the skill source location the repo's instructions declare, and committed.
- Once every phase in the plan is complete, the plan-retirement prompt applies. If the plan resolved or redirected any issues-log entries, draft that redraft under the skill named for issue logging — it does not depend on whether the plan is retired.
- Close on one structured question:

```
Question: "Before we close: draft a handoff?"
Options:
- No handoff needed
- Draft a handoff
```

---

## Behavioural rules

- Targeted adjustments skip Phase 1 and Phase 2 — do not run the full workflow for clearly scoped changes
- Never begin a broader improvement without an approved plan
- Never resolve a finding in isolation — integrate it into the plan first
- Never skip session close — even a targeted adjustment confirms the handoff
- Never implement changes without explicit contributor approval
- If a gap in task coverage is identified, consult references/qa-standards-format.md before proposing a new task
- At any HUMAN CHECKPOINT that follows a file edit, deliver the changed file(s) directly into the conversation with a one-line scope note — not just a text description
