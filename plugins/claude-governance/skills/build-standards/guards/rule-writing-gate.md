# Rule-Writing Gate | build-standards

**Purpose:** Shared decision check for whether a gap found in a skill, subagent or project should become a new rule, checklist, gate or automated mechanism — or should instead be logged as a watch-item. It applies to Improve mode's audit-to-fix flow, and to any Design mode writing a new rule into an existing artifact, whether reached via a full audit, a targeted adjustment, or direct editing.

---

## The check

**A new rule, checklist or gate** is worth writing only if it clears checks 1–3:

1. **Recurrence** — has this recurred, or is it a first occurrence? One instance is not yet evidence of a systemic problem.
2. **Manual-catch cost** — when a human is actively engaged, how cheap and fast is catching this by hand? Where a reviewer catches it in a sentence at near-zero cost, automation is not obviously worth its ongoing tax.
3. **Friction shape** — does the new rule add visible per-turn friction, or is it an invisible check that inherits the same self-application risk it is meant to close? A new enforcement mechanism competes for the same attention budget that caused the original gap.

**A script taking over a step the artifact already states** — an objectively checkable step written as prose — adds no new rule. It is judged on check 4, and checks 1–3 do not block it:

4. **Automation payoff** — how often does the step run, how error-prone is it by hand, and what does a script save in tokens or tool calls? A step that runs often, fails quietly when done by hand, or costs a long tool-call loop pays for a script.

5. **Honest output** — a gap that clears neither path is logged as a watch-item (an open issues-log entry, or Deferred Items on an active plan), not written as a new rule.

Skills, subagents and projects all accumulate rules over time; each one added is weighed against this bar, not assumed to be free.

---

## When to apply

- **Improve mode, Phase 1** — before including a fix that adds a new rule or automated mechanism in the plan's roadmap.
- **Improve mode, Intake (targeted adjustment)** — before writing a new rule directly; this path skips Phase 1, so the check is applied inline.
- **Design-Skill** — whenever editing an existing skill to add a new behavioural rule, gate or script.
- **Design-Subagent** — whenever editing an existing subagent to add a new rule.
- **Design-Project** — whenever editing an existing project's instructions or prompt to add a new hard rule or gate.

Not applicable to the initial, intentional drafting of a brand-new artifact's baseline rule set — this check is for gaps found after the fact, not first-pass design.
