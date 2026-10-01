# SUBAGENT-BUILD
# Design - Subagent Build | build-standards

**Purpose:** Design a new subagent from scratch. The output is one definition file, a skill workflow that dispatches it, and a tested run, ready for release.

---

## Phase 1 — Intent capture

If the current conversation already contains the task the contributor wants to delegate, extract what you can from the history before asking anything.

Otherwise, open with a single question:

> "What task do you want to hand to a subagent — what goes in, what comes back, and which workflow sends it?"

From the answer, confirm before moving on:
- The one task type the subagent performs
- Every input it needs, and where each comes from
- The result it produces, and what one unit of that result is
- The skill whose workflow dispatches it

---

## Phase 2 — Delegability and scope

Load references/subagent-standards.md and references/common-standards.md. Test the task against What a subagent is and What is delegable before anything else.

- **One task type.** Where the task covers several, split it into several subagents, or route the routing half to Design - Skill.
- **Inputs complete at dispatch.** Where a step needs an answer from the contributor, that step stays in the dispatching skill's workflow, and the subagent receives its result as an input.
- **No decision owned by the contributor.** Where the result needs a judgment before it is usable, the subagent records the material for that judgment, and the dispatching session makes it.

A task failing these after the split is not a subagent. Say so and route to Design - Skill.

**Whether it needs a definition at all.** Apply Ad-hoc dispatch under Whether it needs authoring at all in references/subagent-standards.md. Where the task's useful content varies by invocation, no subagent is authored: the dispatching skill composes the prompt from its own context, and the dispatching skill's workflow carries the guidance for writing it. Say so and route that guidance to Design - Skill.

---

## Improving an existing subagent

Reached from Improve's Phase 3 or a targeted adjustment. Phase 1, the catalogue search and Naming belong to a new build and are not run. For the parts being changed: apply the rule-writing check below to any new rule, redraft against references/subagent-standards.md, and rerun Phase 4's scored test dispatch. Release with the carrying plugin through Phase 6.

---

## Before drafting — search the catalogues

An existing worker serving the task type is a worker this estate does not author. Run this before Phase 3, not after a draft exists.

1. **Search.** Search the estate's own skills and subagents on the task type from Phase 1, not on a proposed name. Also list the built-in workers the surface in use offers, and any third-party worker the repo already draws from, and name each source searched.
2. **Record the candidates.** For each near match, write down what it covers and the property it lacks against the scope settled in Phase 2. Where no source yields a candidate, record that, with the sources named.
3. **Route on the criteria.** Test the closest candidate against the three properties under Whether it needs authoring at all in references/subagent-standards.md. Where all three hold, adopt it: declare it per `common-standards.md`'s Adopted artifacts and draft nothing. Where some hold, take it as a foundation, and what results is authored and governed in full. Where none holds, or no candidate exists, author fresh and carry the named property into Phase 3.

---

## Before writing a new rule or gate

If this session is editing an existing subagent to add a new rule, not drafting a new one, apply guards/rule-writing-gate.md before writing it in.

---

## Phase 3 — Draft

### Naming

Derive the name under the naming convention in references/common-standards.md, naming the task type. Present it and confirm before writing anything:

```
Question: "I'll name this subagent [name]. Does that work?"
Options:
- Yes, that works
- I'd prefer a different name — I'll type it in chat
```

### Write the definition file

Draft one markdown file at the repo's subagent source location, which the repo's own project instructions declare. Apply every section of references/subagent-standards.md as it is drafted.

**Frontmatter:** `name`, `description`, `tools` and `model`, all four stated.

**Body, in this order:**
- `**Version:** v1.0`
- One paragraph stating the task type and that the dispatching session decides what to do with the result
- `## Inputs you will be given` — every input, named, as an absolute location where it is a file or directory
- `## Procedure` — numbered steps, each an instruction, the first reading every supplied authority in full
- `## Output contract` — the output file's structure, the fields every unit carries, a home for unconfirmed material, and the return payload
- `## Rules` — the write scope by location, and the subagent's own calibration rules
- `## Issues log` — last, declaring the dispatching skill's identifier and link

Where the subagent assesses against a standard, schema or list, that content is an input. The definition neither copies it nor names the artifact that holds it.

Present the draft and confirm:

```
Question: "How does the subagent draft look?"
Options:
- Good — let's test it
- I want to adjust the inputs or procedure
- I want to adjust the output contract
- Several parts need changes
```

Revise before moving to testing.

---

## Phase 4 — Test dispatch

Dispatch the draft once against a target whose correct result is known before the run: a target with planted or already-confirmed defects, or input whose expected output is written down first. Write the expected result out before dispatching. A subagent run draws on the session's usage limit, so state the dispatch's cost when proposing it.

Score the run against the expected result:
- every expected unit found, and every miss traced to its cause: the definition, or the inputs the dispatch gave it
- no unit recorded that the target does not support
- the output file written at the location given, in the structure stated
- the return payload carrying only what the contract states

```
Question: "How did the test dispatch perform?"
Options:
- Passed — ready to wire in
- A miss traces to the definition — revise and dispatch again
- A miss traces to the dispatch inputs — fix the dispatching workflow
```

Record the test's target, expected result and score in the active plan where one exists.

---

## Phase 5 — Wire the dispatching skill

The subagent is dispatched from a skill's workflow, and that skill is edited under its own version bump.

- Add the subagent to the skill's `## Referrals` section, in the referral form references/skill-standards.md states.
- In the workflow step that dispatches it, state when it is dispatched, the value given for each input, and where the output file is written.
- State what the session does with the output: reading the file rather than the return summary, and settling every item the subagent left to the dispatching session.
- State the step for a dispatch that returns with no output file.

Run the skill's validator after the edit. A referral to a subagent the validator does not find is an `ERROR`.

---

## Phase 6 — Output

**Distribution.** A subagent ships inside the plugin that carries its dispatching skill, at the location references/plugin-standards.md states.

**Source.** Confirm the definition file is committed at the repo's subagent source location before the session closes. It ships in the plugin's next release, with the dispatching skill's bump.

Log any open questions or deferred decisions to the dispatching skill's issues log.

---

## Behavioural rules

- Always load subagent-standards.md and common-standards.md at Phase 2 — never draft a definition from memory of the standard
- Never draft a subagent for a task that fails the delegability test; route it to Design - Skill
- Never ship a definition without one scored test dispatch against a known result
- Never create or overwrite an existing definition file without contributor confirmation
