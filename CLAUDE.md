# Claude Governance Plugin — Project Instructions

**Version:** v1.0

This repo is the source and distribution home of the `claude-governance` plugin: its bundled skills, its subagent, the built archives, and the working artifacts for improving them. Claude builds, refines, audits and releases these artifacts with the contributor. Projects that use the plugin live in their own repos and are not governed here.

---

## Session startup

**This is a hard startup gate.** Before reading, planning, researching, or acting on any task, handoff, or request in this session, your first two actions must be — in order:

1. Invoke `session-discipline`
2. Invoke `build-standards`

Do not engage with task content until both are loaded. A detailed or task-rich opening message — including a handoff that names a specific task — does not change this order: startup runs first, then the task. If a skill is already loaded this turn, do not re-invoke it.

Both skills ship in the `claude-governance` plugin. Its skill list may show them with the plugin prefix, as `claude-governance:<name>`. If either is not installed, name it, say it ships in the `claude-governance` plugin, ask the contributor to install the plugin and restart the session, and stop.

---

## Production flow

1. **Build or improve** — a skill, subagent or plugin change, run through `build-standards`. Work spanning sessions is tracked in a plan in `meta/`.
2. **Release** — version bump, rebuilt zips and plugin archive, contributor confirmation, commit and tag.
3. **Install** — `build-standards`' distribution steps.

---

## Skills

| Skill | When it applies | Gate |
|---|---|---|
| `session-discipline`, then `build-standards` | Session startup, whatever the opening message contains | Hard |
| `plan-discipline` | Any work with a plan document in `meta/` | Hard |
| `issue-logging` | Logging or resolving an issues-log entry | Hard |
| `doc-formatting` | Drafting or restructuring user-facing documentation | Soft |
| `git-commit-message` | Composing a commit message | Soft |

---

## Default paths

- **Plugin source:** `plugins/claude-governance/` — the editable plugin directory: manifest, README, and every bundled member at its default location. It is the one source for the plugin archive and for each member's standalone zip
- **Skill source:** `plugins/claude-governance/skills/[skill-name]/`
- **Subagent source:** `plugins/claude-governance/agents/[subagent-name].md`
- **Local catalog:** `.claude-plugin/marketplace.json` — the catalog Claude Code installs the plugin from
- **Built zips:** `dist/` — built `.skill` zips and the plugin `.zip` archive only. Every zip is built here, never to a scratch folder. A zip is finalized once it is committed, after contributor approval
- **Working artifacts:** `meta/` — plans, audit findings and drafts; cleaned up as addressed
- **Issues log:** `ISSUES.md` at the repo root

---

## Version control

Commit after every meaningful update — skill, subagent or plugin changes, CLAUDE.md changes, or `meta/` additions and removals.

**Version tags.** `[artifact-name]/v[X.Y]` for a skill or subagent (e.g. `session-discipline/v1.1`), and `claude-governance/v[X.Y.Z]` for the plugin. Create a tag only once the version is fully shipped: its finalized zip or archive is committed, not merely its source. A tag created on the source commit alone is moved to the commit that carries the finalized artifact.

Tags are lightweight: push them with `git push origin --tags`.

---

## Behavioural rules

1. Never load a source speculatively — only what the current task requires.
2. Always confirm before creating pages, tickets, or other external artifacts.
3. Always confirm before modifying documentation, prompts, or project instructions.
4. Any time a workflow issue is noticed — incorrect output, workflow gap, redundant step, routing failure, documentation drift, or missing guardrail — ask whether to log it now or hold it for later, under `issue-logging`.
5. When referencing a documentation page by name, include a hyperlink on first mention within a given context.

---

## Issues log

Identifier: GOV
Log: `ISSUES.md`
