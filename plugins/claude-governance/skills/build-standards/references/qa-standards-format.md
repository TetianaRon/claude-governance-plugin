# QA Standards | build-standards

**Purpose:** Defines what belongs in a project or skill's optional `qa-standards.md` file. The Improve mode is the unified QA layer — it handles all audit and improvement work. A `qa-standards.md` file is not a self-improvement workflow; it is a thin reference that tells the Improve mode what to look for when auditing this specific project or skill.

---

## When to create a `qa-standards.md`

Create one when the project or skill has QA criteria that are not covered by the generic standards in `references/skill-standards.md` or `references/project-standards.md`. Examples:

- A project that produces a specific output format with known failure modes (e.g. "always check that the HTML output includes the meta viewport tag")
- A skill with edge cases that consistently cause errors in a specific context
- A project with a known integration dependency that needs to be verified each session

If there are no project-specific criteria, no `qa-standards.md` is needed.

---

## What goes in `qa-standards.md`

A `qa-standards.md` file contains only criteria that are unique to this project or skill. It must not duplicate content from the generic standards.

Structure:

```markdown
# QA Standards — [Project or Skill Name]

## What the Improve mode should check during audit

[A short list of project/skill-specific criteria. Each item should be specific enough
that the Improve mode can evaluate it directly against the output or files.]

## Known failure modes

[Optional. Patterns that have caused issues in the past, worth checking proactively.]

## Out of scope

[Optional. Things that look like issues but are intentional — to prevent false flags.]
```

---

## How the Improve mode uses it

During Phase 1 (Audit), the Improve mode checks whether the target has a `qa-standards.md`. If it does, it is loaded and its criteria are included in the audit alongside the generic standards. No special action is needed — the file is loaded on demand.

---

## Behavioural rules

- `qa-standards.md` is optional — absence does not indicate a gap
- Contents must be project/skill-specific only — no duplicating generic standards
- Keep it short — if it grows beyond a single screen, the project likely has broader design issues worth addressing through Improve
