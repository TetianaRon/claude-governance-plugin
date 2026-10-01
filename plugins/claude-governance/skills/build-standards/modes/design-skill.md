# SKILL-BUILD
# Design - Skill Build | build-standards

**Purpose:** Design a new skill from scratch. The output is a skill directory with SKILL.md and any supporting files, ready for installation.

---

## Phase 1 — Intent capture

If the current conversation already contains a workflow the contributor wants to capture, extract what you can from the history before asking anything.

Otherwise, open with a single question:

> "Tell me about the task you want to turn into a skill — what does it do, and when do you find yourself reaching for it?"

From the answer, confirm before moving on:
- What the skill enables Claude to do
- When it should trigger (specific phrases, contexts, session types)
- What the expected output looks like
- Whether there are edge cases or things the skill should explicitly not handle

For output type, present a structured choice if not clear from context:

```
Question: "Is the skill's output something that can be objectively checked,
or is it more of a judgment call?"
Options:
- Objectively checkable (e.g. a file is produced, steps are followed, data is extracted)
- Judgment-based (e.g. writing tone, recommendations, analysis)
- Mix of both
```

---

## Phase 2 — Scope and edge cases

Before writing, establish:
- What the skill handles
- What it explicitly does not handle
- Any inputs that look similar but should be treated differently
- Whether an existing skill already covers this — settled by the catalogue search below, before Phase 3

If the scope is genuinely ambiguous, ask one clarifying question before proceeding.

---

## Before drafting — search the catalogues

An existing skill serving the workflow is a skill this estate does not author. Run this before Phase 3, not after a draft exists.

1. **Search.** The estate's own skills — every skill source tree the session can reach and every installed plugin — are the one sanctioned catalogue and the only one this step requires. Search them on the task the contributor described in Phase 1, not on the name being considered for the new skill. Where the surface in use offers its own skill catalogue or the repo already draws from a marketplace, search those too and name each one searched; neither is a sanctioned root, so a candidate found there is a candidate to assess rather than a source to trust.
2. **Record the candidates.** For each near match, write down what it covers and the property it lacks against the scope settled in Phase 2.
3. **Route on the criteria.** Test the closest candidate against the adoption properties in references/skill-standards.md. Where all of them hold, adopt it — declare it per `common-standards.md`'s Adopted artifacts and draft nothing. Where some hold, take it as a foundation; what results is authored and governed in full. Where none holds, or no candidate exists, author fresh and carry the named property into Phase 3.

A search returning nothing is a result to record rather than a step to skip. Name what was searched.

---

## Before writing a new rule or gate

If this session is editing an existing skill to add a new behavioral rule, checklist, or gate (not first-pass drafting of a brand-new skill), apply guards/rule-writing-gate.md before writing it in. This applies whether the edit is reached via Improve mode's Phase 3 execute or via a targeted adjustment that loaded this file directly.

---

## Improving an existing skill

Reached from Improve's Phase 3 or a targeted adjustment. Phases 1 and 2, the catalogue search, Naming and Decide on structure belong to a new build and are not run. For the parts being changed: apply the rule-writing check above to any new rule or script, draft against references/skill-standards.md, and run Validate the draft. Run Phase 4 where the change touches the description or a triggered behaviour. Package through Phase 5 at release.

---

## Phase 3 — Load standards and draft

Load references/skill-standards.md. Apply the naming convention, file structure rules, frontmatter requirements, and description quality rules throughout this phase.

### Naming

Derive the skill name following the `[purpose]` or `[project]-[purpose]` convention from COMMON-STANDARDS. Present the suggestion and confirm before writing anything:

```
Question: "I'll name this skill [name]. Does that work?"
Options:
- Yes, that works
- I'd prefer a different name — I'll type it in chat
```

### Decide on structure

If the skill is simple (single task, one mode): a single SKILL.md is sufficient.

If the skill is complex (multiple modes, significant reference material, or the body would exceed 500 lines): SKILL.md stays lean and carries the routing logic, with detailed content in subfolders named per SKILL-STANDARDS → Subfolder naming (`references/`, `tasks/`, `modes/`, `workflows/`, `scripts/`). Every sub-file is referenced from SKILL.md with an explicit load condition and read only when that condition fires — never at startup, and never as an always-loaded core file. Confirm the structure before writing.

### Write SKILL.md

Draft the skill file. It must include:

**Frontmatter:**
```yaml
---
name: skill-name
description: >
  [What it does + when to trigger + explicit trigger phrases]
---
```

**Body:**
- Instructions written for Claude as the reader, not as human documentation
- At least one worked example: input → process → output
- Edge cases: what the skill handles and explicitly does not handle
- If multiple steps, number them and make the sequence unambiguous
- If complex: routing table pointing to sub-files with exact load conditions

**Version declaration:**
```
**Version:** v1.0
```

### Validate the draft

Before presenting the draft, run the bundled validator:

```bash
python3 <skill-dir>/scripts/validate_skill.py <path-to-skill-directory>
```

Fix any `ERROR`-level finding before continuing — these break upload, install or routing: malformed frontmatter, a duplicate SKILL.md, bad naming, or a `## Referrals` entry naming a skill not in the estate. Pass `--estate DIR` when a referral targets a skill held outside this repo. `WARNING`-level findings are convention gaps and review prompts — references, project names, external links, cleanliness markers, and checkpoint notation in the standards family — surface them alongside the draft rather than blocking on them; the contributor decides whether they matter for this skill.

Present the draft and confirm:

```
Question: "How does the skill draft look?"
Options:
- Good — let's test it
- I want to adjust the description
- I want to adjust the instructions
- Both need changes
```

Revise before moving to testing.

---

## Phase 4 — Test and iterate

Design test cases covering:
- **Clear trigger cases** — prompts that should definitely activate the skill
- **Edge cases** — prompts at the boundary of the skill's scope
- **Non-trigger cases** — prompts that look similar but should not activate the skill

Follow the SKILL.md as written and produce the output for each case. Present results for review.

```
Question: "How did the skill perform?"
Options:
- Looks good — ready to finalise
- Some cases need work — I'll describe in chat
- Needs a significant rethink
```

Revise and retest until the skill performs correctly.

> **Note:** Quantitative benchmarking and automated description optimisation run on a surface with a command line; elsewhere, test cases run one at a time.

---

## Phase 5 — Output

**Zip filename rule:** The zip must be named `[skill-name].skill` — no version suffix. The version lives in SKILL.md's `**Version:**` body line — never as a `version:` key in frontmatter — and in git tags.

Package the skill with the bundled script rather than building the zip by hand:

```bash
python3 <skill-dir>/scripts/package_skill.py <path-to-skill-directory> <output-directory>
```

This runs `scripts/validate_skill.py` first and refuses to package on any `ERROR`-level finding, then excludes `__pycache__`, `node_modules`, `*.pyc`, and `.DS_Store` automatically. The output filename is taken from the SKILL.md `name:` field, satisfying the zip filename rule above. If the script reports `WARNING`-level findings, review them with the contributor before distributing — they don't block packaging but may still need fixing.

**Source directory:** Confirm the source files are saved at the skill source location the repo's instructions declare, and committed before the session closes.

**Present for install:** Deliver all finalized `.skill` zips directly into the conversation in a single message, alone in its own turn, so the contributor can install directly from the session.

**Distribution.** Run `workflows/distribution.md`.

**Distribution checklist** — complete before closing:

- [ ] Zip filename is `[skill-name].skill` — no version suffix
- [ ] Source committed at the repo's declared skill source location
- [ ] Contributor has reinstalled (or been prompted to reinstall) the skill in Claude.ai

Then ask:

```
Question: "Anything else before we close?"
Options:
- No, we’re done
- I want to make one more adjustment
```

Log any open questions or deferred decisions to this skill's issues log (see SKILL.md's declared "Issues log" link).

> **Note — repo-bound skills:** Repos holding a `.claude/skills/` copy of the skill are synced by the repo-sync step in `workflows/distribution.md`.

---

## Behavioural rules

- Always load SKILL-STANDARDS at Phase 3 — never invent naming or structural conventions from memory
- Never create or overwrite an existing skill file without contributor confirmation
- If a closely related skill already exists, flag it before drafting — duplication creates maintenance risk
- Never produce a zip without a confirmed name, confirmed structure, and at least one passing test
