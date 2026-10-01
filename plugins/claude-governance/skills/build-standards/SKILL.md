---
name: build-standards
description: >
  Runs the workflow for designing, building, refining, auditing and distributing
  Claude projects, skills, subagents and plugins, and holds the standards they are
  built and audited against. Use whenever the intent is to design, build, refine, or
  audit any of them — regardless of which project the session is in. Triggers on any
  of: "design a project", "design a skill", "design a subagent", "build a plugin",
  "new project", "refine a project", "update a skill", "improve this skill", "update
  the project instructions", "refine this workflow", "let's update the standards",
  "this needs a workflow change", "audit this skill", "audit the plugin", "distribute
  the artifact", "self-improvement", "QA session", "issues triage", or any session
  where the task involves building, refining, or auditing a governed artifact. Also
  triggers when a skill update session is underway in any project, or system-level
  workflow changes are being made.
---

# build-standards

**Version:** v1.0

---

## Issues log

Identifier: GOV
Log: `ISSUES.md` at the root of the claude-governance plugin repo

---

## Guards — apply in any mode

### Rule-writing gate

**Trigger:** about to write a new rule, checklist, gate, script or automated mechanism into any skill, subagent or project file — this skill's own files included. Load `guards/rule-writing-gate.md` and follow it in full before writing.

### Instruction cleanliness

**Trigger:** about to write or revise shipped instruction content in any skill, subagent or project file — this skill's own files included. Load `guards/instruction-cleanliness.md` and follow it before writing.

---

## Mode routing

Route the task to the mode that owns its workflow.

| Signal | Mode | Sub-file | What it covers |
| --- | --- | --- | --- |
| Building a new project | Design - Project | `modes/design-project.md` | New project build — depth selection, scope, knowledge base pattern, prompt drafting, page creation, QA mode design, spec output |
| Building a new skill | Design - Skill | `modes/design-skill.md` | New skill build — intent capture, scope and edge cases, SKILL.md drafting, frontmatter, test and iterate, version management, output and install |
| Building a new subagent | Design - Subagent | `modes/design-subagent.md` | New subagent build — delegability, catalogue search, definition drafting, scored test dispatch, wiring the dispatching skill, output |
| Building a new plugin | Design - Plugin | `modes/design-plugin.md` | New plugin build — members and composition, manifest and README, build and verify, live test, output |
| Targeted adjustment, audit, improvement, or plan execution for any project, skill, subagent or plugin — this skill included | Improve | `modes/improve.md` | Improvement orchestrator — audit, produce and maintain an improvement plan, execute through the Design sub-file for the target's class; `references/` sub-files load on demand from within it |
| Not sure which kind of artifact is the right output | Ask one clarifying question, then route | — | — |

**Improve executes through Design.** Improve's Phase 3 loads the Design sub-file for the target's class — `modes/design-skill.md`, `modes/design-project.md`, `modes/design-subagent.md` or `modes/design-plugin.md` — at the improvement entry point that sub-file states.

If the opening message has not already named the mode, ask:

```
Question: "What are we working on today?"
Options:
- Build a new project or skill
- Build a new subagent or plugin
- Improve or refine something
- Not sure yet — help me decide
```

If the contributor selects a "Build" option, ask which of its two it is:

```
Question: "Which are we building?"
Options:
- [The first artifact class the option names]
- [The second artifact class the option names]
```

If they select "Not sure yet", gather one more sentence of context before routing.

Once the mode is identified, present a confirmation:

```
Question: "Based on what you've described, [Mode name] looks like the right fit
because [one-sentence reason]. Does that work?"
Options:
- Yes, let's go with that
- Actually I want something different
- Tell me more about the options
```

If they select "Tell me more", summarise the five modes (Design - Project, Design - Skill, Design - Subagent, Design - Plugin, Improve) from the routing table above without loading any additional sub-files.

If the contributor has already named a mode, validate it against the routing table. If it fits, confirm and proceed. If a different mode would serve them better, say so — then respect their decision.

---

## Distribution

**Trigger:** a skill zip or plugin archive is rebuilt, or project files are finalized and confirmed ready. Load `workflows/distribution.md` and follow it at once — not at session end. It may fire several times in one session.

---

## Referrals

- `session-discipline` — the Human Checkpoint Convention
- `issue-logging` — logging and resolving issues-log entries
- `plan-discipline` — creating and maintaining an improvement plan
- `standards-auditor` — auditing one target against supplied standards

## Behavioural rules

- Never load a sub-file speculatively — only what the identified mode, a guard's trigger, or the Distribution trigger requires
- Never load `references/` sub-files at startup — load them only when a guard or the active mode workflow directs it
- Always confirm the mode before loading its sub-file
- Do not prompt for commit, tag, or push until the contributor explicitly confirms the content is finalized and reviewed
