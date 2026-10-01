# SKILL-STANDARDS
# build-standards

Authoritative reference for how governed Claude skills are structured and maintained. Load it when building, auditing, or refining a skill — never at session startup. Load `common-standards.md` alongside it: this file states only what is specific to skills.

---

# Part 1 — Placement

What is a skill, what is a sub-file, and what is neither.

---

## Granularity rules

Every unit of content is a skill, a sub-file of a skill, or a guard. Decide which before writing it.

### Whether it needs authoring at all

This estate's catalogue is not the only one. Official and third-party libraries carry skills, and a workflow one of them already serves is a workflow this estate does not author. The question is settled before N1 and N2 are asked: where an existing skill serves the workflow, the shape of a new unit never arises.

Three outcomes, each carrying its own consequence:

- **Adopted as it stands.** The estate depends on a skill it does not author, and no class standard certifies it.
- **Taken as a foundation.** The estate authors a unit derived from an existing one. What it inherits is content, so the result is authored, governed and audited in full.
- **Authored fresh.** Nothing available serves the workflow, and the property the existing candidates lack is nameable.

**When an existing skill can be adopted as it stands.** Four properties, all of which hold:

- it covers the whole workflow rather than part of it — a partial match is a foundation candidate and not an adoption one
- it produces a correct result without any governance convention it cannot carry
- its behaviour is inspectable, so a project declaring it can state what it relies on
- its update path is known

An adopted skill's standing — declared, uncertified — is stated in `common-standards.md` under Adopted artifacts.

Work that certifies against a governed standard is authored, even where a capable existing skill serves the workflow.

**Audit checkpoint:** For every skill the estate authored, name the closest skill in the catalogues available to it and state the property that skill lacks. Where no such property can be named, the existing skill serves the workflow and the authored one is redundant. For every adopted skill, test all four adoption properties and name each that fails; a skill failing any of them is not an adoption and qualifies only as a foundation.

**Judgment call:** what the catalogues available to the estate hold, and whether an outside skill's behaviour is inspectable and its update path known, rest on artifacts outside the estate. They are read from the catalogues themselves and confirmed with the contributor.

### The test for a skill

Two necessary conditions. Both must hold, or the content is a sub-file — or a guard, which fails N1 by construction and is placed by its own rule below.

**N1 — Entry point.** Can a contributor plausibly open a session and ask for this workflow as the whole task, with no larger workflow already running?

- If yes, it is a candidate skill.
- If it is only ever reached partway through some other workflow, it is a sub-file of that workflow.

The test is whether the workflow is *asked for*, not whether it is useful in many places. A step that many workflows pass through is still a step.

**N2 — Describable trigger.** Can its trigger be written as a description that fires on the task itself, without naming another skill and without depending on session state?

A description that has to say "during a governance session" or "once another workflow is already running" describes a sub-file, not an entry point.

**Startup gates.** A skill that consuming projects' instructions invoke as a startup gate passes N1 and N2 on that gate: the project's invocation is its entry point and its trigger.

A skill is not guaranteed to load. It loads when a project's instructions invoke it, when the contributor asks for it, or — best-effort only — when its description matches. No skill is ambiently present: a workflow a contributor can ask for directly is reachable only if it is independently invocable.

### Necessary references

The verdict turns on whether any reference crossing a boundary is **necessary**. A reference is necessary when both sides need each other at runtime and neither can state its rule without the other. One necessary reference means the boundary is in the wrong place.

No other kind of reference constrains placement. A reference existing because content sits in the wrong file, because the same rule is stated on both sides, because one side is written as specific to the other, or because a lower layer points forward into a higher one, is a property of the current text rather than of the domain. Count necessary references; a total count answers a different question.

### Counterweights

A unit that passes N1 and N2 with no necessary crossing reference is eligible to be a skill, not confirmed as one. Four costs weigh against every skill that exists:

1. **Invocation risk.** One more description that has to fire, with no guarantee. A workflow rarely asked for by name may be reached more reliably as a sub-file of something that is reliably invoked.
2. **Single ownership.** Where a rule two skills both need cannot be assigned to one of them, the boundary between them is in the wrong place.
3. **Orchestration burden.** Each new skill is another line every consuming project declares, and a workflow needing two skills together is composed by that project under `project-standards.md`'s Projects explicitly invoke their skills section.
4. **Distribution burden.** Another version to track, another install and sync target.

A unit is a skill when N1 and N2 hold, no necessary reference crosses its boundary, and a concrete benefit outweighs the four costs — an existing adoption boundary, a materially different change cadence, or a workflow genuinely asked for on its own. Otherwise it is a sub-file.

### Sub-files

A sub-file holds a sub-task, mode, or step within its parent skill's domain, and is never triggered independently of it.

### Project-specific skills

A project-specific skill's workflow belongs to one project and has no use outside it. A workflow two projects could reasonably use is not project-specific.

Never put project-specific content in a shared skill. A shared skill's scope is its domain, not any project.

**Audit checkpoint:** For every skill, state which of N1 and N2 it passes and on what task; for a skill passing on a startup gate, name the project instructions invoking it. A skill that cannot be named as a task a contributor asks for is misplaced, however coherent its contents. List every reference crossing the skill's boundary and mark each necessary or not, with the reason; one necessary reference puts the boundary in the wrong place, and a count of references of any other kind answers a different question. For a skill passing both conditions with no necessary crossing reference, name the concrete benefit outweighing the four costs — an existing adoption boundary, a materially different change cadence, or a workflow genuinely asked for on its own — and flag one for which none can be named. Read every shared skill for content belonging to a single project; each instance is a defect. For every sub-file, confirm neither the skill's description nor any other trigger reaches it independently of its parent. For every project-specific skill, confirm its workflow has no use in a second project.

**Judgment call:** whether a contributor would plausibly ask for a workflow as the whole task — the test N1 states and the checkpoint rests on — is a property of the contributor population rather than of any file. Whether a second project could reasonably use a workflow, and which projects invoke a startup-gate skill, rest on projects outside the skill's files. Each is confirmed with the contributor where the reading is not obvious.

---

## Action-triggered guards

A guard fires on an **action type** rather than on a task: a git write, a write to a mounted path, a bulk external write, writing a new rule, revising shipped instruction text. It has no entry point — nobody asks for it — and it is not a step in one parent domain, since any workflow can trip it.

A guard fails N1 by construction, and is placed by the rule below rather than as an ordinary sub-file.

**Placement rule.** A guard lives with the most reliably-invoked skill whose actions it governs, undivided — it is never stated partly in one skill and partly in another. Where a guard governs an action that occurs in sessions that do not invoke that skill, the fix is the calling project invoking the guard's carrier explicitly.

**Reliability follows the carrier's invocation.** A guard's reliability is a property of its carrier's invocation and of nothing else — not its file location, its packaging or its install path.

**File placement.** Guards live in `guards/`, one file per action type. A skill with a single guard still uses the folder.

**Audit checkpoint:** Three passes. First, scan for content that fires on an action type rather than a task and sits as an ordinary sub-file — reclassify it. Second, scan the estate for the same action governed in two skills; a guard stated twice is a defect regardless of whether the two statements agree. Third, confirm every guard sits in its carrier's `guards/` folder, one file per action type, including in a skill carrying a single guard. For every guard, name its carrier and the skills whose actions it governs, and flag a guard whose carrier is not the most reliably invoked of them.

**Judgment call:** which skill is most reliably invoked rests on how the projects calling them invoke them, not on any file in the skill, and is confirmed with the contributor.

---

## Skill self-sufficiency

A skill is self-contained within its own domain. Self-sufficiency means self-triggering: the description is broad enough that the skill loads when the right task is present.

Two things a skill might do to another skill look similar and are not. One is forbidden; one is permitted under constraints.

### Content coupling — forbidden

One skill containing another's rules, or reading a file inside another skill, is content coupling. It is forbidden in every direction, including where the content is framed as an example, a summary, a reminder, or a convenience copy.

### Referral — permitted, narrowly

Referral is one skill naming another as the owner of a task type. No content is shared and no file is read. It is permitted under five constraints, all of which must hold:

1. **Name only.** A referral names the skill and the task type it owns. It never describes what that skill does, restates any of its rules, or points at a path inside it.
2. **No conditional phrasing.** Never "if available" or "if connected". State the routing plainly; if the target is absent the invocation simply fails.
3. **Nothing gated on it.** A referral is a routing preference, not a precondition. No workflow step may depend on it having succeeded.
4. **One direction only.** The owner of a task type never refers back to its referrers.
5. **Validator-checkable.** A referral is a bullet in a `## Referrals` section of `SKILL.md`, in the form `` - `skill-name` — task type ``, and every referral names a skill or subagent that exists in the estate.

**Where referral applies.** Referral is the route from a skill in context to a guard's carrier. For an entry-point workflow the description is the route, and a referral does not stand in for a description that fails to fire.

**Audit checkpoint:** For every mention of another skill, decide which of the two it is. A mention carrying any of the other skill's rules, or any path inside it, is content coupling and a defect however it is framed. A referral breaching any of the five constraints is a defect on that constraint. Flag a referral to an entry-point skill made in place of that skill's own description firing on the task.

**Judgment call:** whether a referral stands in for a description that would not fire rests on how the description performs on contributors' requests, and is confirmed with the contributor.

---

## Internal routing

A skill may route internally between its own sub-workflows or modes. This is expected. Internal routing does not make a skill a project manager — the skill still covers one domain.

---

## Skills-as-project-managers antipattern

A skill is not responsible for routing between projects, managing a project's task sequence, or owning a project's knowledge sources. A skill doing any of these means the project is underspecified. A skill must be usable across multiple invocations without re-explaining project context.

**Audit checkpoint:** Scan the skill for routing between named projects, for a project's task sequence, and for a project's knowledge sources held as the skill's own; each is a defect and evidence the project calling it is underspecified. Read the skill's entry point for project context it expects an earlier invocation to have supplied.

---

## Skill/project file-reference boundary

The boundary between a skill and the project that calls it runs in both directions. Each side describes what it needs from the other by **type**, never by naming the other's actual files, paths, or internal structure.

**A skill must never name a project-specific file, path, page identifier, or URL** — not as an illustrative example, and not wrapped in a caveat. A skill describes the **type** of information it needs — a local issue record, a running allowlist, a findings-history log — and the action to take with it, then resolves the actual location from the calling project's own instructions or task file, or by asking the contributor when the project has not declared one.

**A project must never name a skill's internal file structure** — its `scripts/`, `references/`, `guards/`, `modes/` paths, or any other file inside the skill's directory. A project's task or instruction file references a skill by name only.

**Audit checkpoint:** Scanning a skill, flag filenames, file extensions, path fragments, page identifiers, or project names appearing anywhere outside the external-reference allowlist in `common-standards.md`, including ones presented as non-binding examples. Scanning a project's task and instruction files, flag any reference to a path inside one of its skills. In both directions, replace the reference with a description of the information by type.

---

# Part 2 — Authoring

How a skill's files are organised and written.

---

## File structure

Every skill is a directory. SKILL.md is the only required file.

```
skill-name/
├── SKILL.md              required — entry point, routing logic, frontmatter
└── [subfolder]/          optional — sub-files loaded on demand, never speculatively
    ├── subtask-a.md
    └── subtask-b.md
```

SKILL.md runs under 500 lines. Detailed content sits in subfolders, referenced from SKILL.md with explicit load conditions.

**Audit checkpoint:** Confirm the skill is a directory carrying `SKILL.md` at its root, and that every other file sits in a subfolder. Count SKILL.md's lines and flag a count above 500. Flag every sub-file SKILL.md names no load condition for.

---

## Subfolder naming

Subfolders are named for their content type:

- `references/` — templates, standards, knowledge bases, reference material
- `tasks/` — discrete behavioural sub-tasks
- `modes/` — distinct operational modes with their own intake and routing
- `workflows/` — multi-step procedural sub-files
- `guards/` — action-triggered guards, one file per action type
- `scripts/` — executable code for deterministic, repetitive mechanics. A step that is objectively checkable, needs no judgment, and pays for a script — it runs often, is error-prone by hand, or costs many tool calls — is carried by a script rather than prose: validation, packaging, formatting. Scripts execute without loading their source into context; reference them from the relevant SKILL.md phase with the exact invocation command.

A skill may have several subfolders. The rule covering all of them: contents load on demand, never speculatively.

**Audit checkpoint:** List the skill's subfolders and flag every name outside the set above. For each step the skill states that is objectively checkable and needs no judgment, name what a script would save; where it pays for one, confirm a script in `scripts/` carries it and that the SKILL.md phase using it names the exact invocation command. A step of that kind written as prose is a defect. Confirm every subfolder's contents are reached by SKILL.md's routing on demand rather than loaded at startup.

**Judgment call:** whether a step pays for a script rests on how often it runs and how it fails by hand, which the files do not record, and is confirmed with the contributor.

---

## Thin-trigger pattern

An inline behaviour whose description runs beyond a few lines, or that has been revised more than once, sits in a sibling file, with its SKILL.md entry a short trigger condition — whether or not the skill is under the 500-line ceiling. This applies to any multi-behaviour skill, not only multi-mode ones.

This section decides only **whether to extract**. Whether the extracted content becomes a sub-file of this skill, its own skill, or a guard is a placement question — decide it under Granularity rules and the guard placement rule.

**Audit checkpoint:** Check for inline sections that have grown large, cover more than one sub-topic, or have been revised repeatedly without extraction. Flag them as a structural gap even where the skill is within the line-count ceiling.

**Judgment call:** how often a section has been revised rests on the artifact's history rather than on the file, and is read from version control or confirmed with the contributor.

---

## Sub-file splitting

The thin-trigger pattern applies recursively: a sub-file showing the same signals is itself a splitting candidate.

**When to split:** the content divides into two or more genuinely independent sub-workflows — the kind where a session needs one of them and not the others. Split each into its own file under a nested subfolder, with the parent doing only the routing.

**When not to split:** a long sub-file describing one coherent workflow that every session reads start to finish is not a splitting candidate on length alone. A growing checklist or an increasingly detailed single step is normal maintenance.

As above, this section decides only whether to split. Where the pieces belong is a placement question for Granularity rules.

**Audit checkpoint:** Apply the thin-trigger signals to every sub-file. For each sub-file, name the sub-workflows it holds and whether a session needs one without the others; flag a sub-file holding two or more such sub-workflows unsplit, and a parent of a split doing more than routing. Do not flag a sub-file on length alone where it describes one workflow every session reads start to finish.

**Judgment call:** whether a session needs one part of a sub-file without the others rests on how sessions use it, and is confirmed with the contributor.

---

## Startup simplicity

SKILL.md is the entry point and holds the routing logic. Sub-files are loaded on demand by that routing, never at startup.

**Hard rule:** SKILL.md must not instruct Claude to fetch any external page or source on invocation. No pointer pages, no runtime version checks, no external reads of any kind at startup.

**Audit checkpoint:** Read SKILL.md for an instruction to fetch an external page or source on invocation — a pointer page, a runtime version check, or any other external read. Each is a defect. Confirm every sub-file is reached by SKILL.md's routing rather than loaded at startup.

---

## No fallback state

A skill is either installed and running, or it is not. There is no fallback page, no degraded mode, no alternative load path.

**Audit checkpoint:** Scan the skill for a fallback page, a degraded mode, and an alternative load path reached when the skill is absent or incomplete; each is a defect.

---

## SKILL.md structure

Every SKILL.md has two parts: YAML frontmatter and a markdown body.

### Frontmatter

```yaml
---
name: skill-name
description: >
  What this skill does and the specific contexts that should trigger it.
  Put the key use case first. Be explicit — Claude tends to undertrigger.
  List trigger phrases.
---
```

Required fields: `name`, `description`.

`description` is the primary triggering mechanism. It states what the skill does, when it should be used — specific contexts, trigger phrases, session types — and enough detail that Claude loads it rather than proceeding without it. It is capped at 1,024 characters. `when_to_use` carries further trigger context beyond the cap.

Optional frontmatter fields:

- `when_to_use` — additional trigger context, appended to the description in the skill listing
- `disable-model-invocation: true` — prevents auto-loading; the contributor invokes with `/skill-name`
- `user-invocable: false` — hides from the `/` menu; Claude loads it automatically when relevant
- `allowed-tools` — pre-approves specific tools while the skill is active
- `license` — license identifier
- `metadata` — free-form key-value data
- `compatibility` — version or environment constraints

### Body

Write for Claude as the reader, not as human documentation. Instructions as direct commands.

Routing logic lives in SKILL.md directly. Mode and task sub-files are loaded on demand by that routing.

**Audit checkpoint:** Confirm SKILL.md opens with YAML frontmatter stating `name` and `description`, followed by a markdown body. Flag an absent required key, a `description` above 1,024 characters, a frontmatter key outside the required and optional sets above, and routing logic held in a sub-file rather than in SKILL.md. Flag body prose addressed to a human reader rather than stated as direct instruction to Claude.

**Judgment call:** whether a passage addresses a human reader or instructs Claude is read from the passage, and is confirmed with the contributor where the reading is not obvious.

---

## Description quality rules

The description is what gets Claude to load the skill. A weak description causes undertriggering — the skill exists but never runs.

**A good description:**

- states what the skill does in the first sentence
- lists specific trigger phrases or session types
- names the workflow explicitly, not just the domain
- covers edge cases that look similar and should also trigger
- stays under 1,024 characters

**Failure modes:**

- Too vague ("helps with project work") — no trigger signal
- Describes the output but not the trigger — Claude does not know when to load it
- Covers only the main case — undertriggers on related requests

**Audit checkpoint:** Read the description's first sentence and confirm it states what the skill does. Confirm the description names specific trigger phrases or session types rather than a domain alone, names the workflow rather than the domain, and runs under 1,024 characters.

**Judgment call:** whether the named triggers reach the edge cases that look similar and should also fire rests on the requests contributors actually make rather than on the skill's files, and is confirmed with the contributor.

---

## Canonical intake pattern

Present every choice point as a structured question with a fixed, clickable set of options — never a plain-text question where the answers are a fixed set. For content-production skills, route intake as channel → product → task description. Present output section by section, and follow up with a single "Anything to adjust?" only. Never present multiple variants unless asked.

**Audit checkpoint:** Enumerate every choice point and verify each presents a structured question with a fixed set of options. A plain-text question where a structured choice was possible is a gap. For a content-production skill, confirm intake routes channel → product → task description, that output is presented section by section with a single "Anything to adjust?" follow-up, and that no multiple variants are presented unasked.

---

## Feedback handling pattern

The pattern binds a content-production skill: one producing copy, design or document content for a channel or product. When feedback arrives on that output, treat it as a planning and routing problem, not a direct execution step.

1. **Parse** — extract all feedback items from every source in the session before doing anything else.
2. **Classify** — group items by type: copy, structure, factual accuracy, design.
3. **Flag conflicts** — where an item contradicts established source material, flag and pause. Do not resolve conflicts unilaterally.
4. **Clarify** — ask one clarifying question per ambiguous item before mapping it to a type.
5. **Present a plan** — a consolidated change plan grouped by type, with the action each item takes. Get confirmation.
6. **Route** — once confirmed, proceed to the appropriate sub-task or mode.

Apply no change without a confirmed plan. An item mapping to no existing sub-task or mode is flagged, with a proposed approach, before proceeding.

**Audit checkpoint:** For a content-production skill, confirm its feedback path states all six steps in the order above, and name each absent one. Flag a step applying a change before a plan is confirmed, and confirm the path states what happens to an item mapping to no existing sub-task or mode.

---

## Instruction placement: skill files only

All behavioural content — intake logic, routing, task instructions, guardrails — lives in skill files. Skills do not hardcode dependencies on external files, URLs, or services that are not intrinsic to the skill itself.

Where a workflow step requires external content, the skill instructs Claude to request it from the contributor or the project context. The project prompt or contributor supplies resource pointers; the skill defines what to do with the content once it arrives.

**Audit checkpoint:** Confirm every behavioural instruction the skill runs on is held in the skill's own files. Flag a workflow step whose instructions are resolved from an external destination at run time, and a resource pointer the skill fixes itself rather than receiving. External destinations the skill reads or writes are judged against `common-standards.md`.

---

# Part 3 — Shared rules

Naming, version management, editing workflow, repository setup, distribution, instruction cleanliness, external references, checkpoint markers and the issues-log declaration are the same for every governed artifact. They are stated once in `common-standards.md`, which also records the skill-specific deltas. None of them is restated here.
