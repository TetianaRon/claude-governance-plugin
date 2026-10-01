# PROJECT-STANDARDS
# build-standards

Authoritative reference for how governed Claude projects are structured and maintained. Load it when building, auditing, or refining a project — never at session startup. Load `common-standards.md` alongside it: this file states only what is specific to projects.

---

## What a project is

A project is a self-contained workflow system. It has an instruction layer, task files, and optionally templates and per-project content.

---

## Project anatomy

Every project consists of:

- **`CLAUDE.md`** — the instruction layer. Thin routing and session orientation only. Uploaded to the chat Project or accessed via mounted repo. Use an `instructions/` subfolder when multiple surfaces need distinct instruction files.
- **Task files** (`[project-id]-task-[artifact].md`) — one per workflow task. All task detail lives here, not in the instruction layer.
- **Templates** (`[project-id]-template-[category]-[artifact].md`) — optional. Used when tasks produce structured outputs following a repeatable format.
- **Per-project content files** — optional. Output artifacts or project-specific data the workflow produces and references.
- **A human-facing documentation surface** — optional. Valid for issues logs, project overviews, stakeholder briefs, and finalized artifacts. Never a Claude runtime dependency.

**Audit checkpoint:** Confirm the project carries an instruction layer and at least one task file; each absence is a defect. For every other file present, name which of the three optional components it is, and flag one belonging to none of them. Read the instruction layer and the task files for a step that cannot complete while the human-facing surface is unavailable; each is a runtime dependency and a defect.

---

## File naming convention

File names must be self-describing without folder context. A chat Project is flat — it has no folders — and the same file name is used in the repo, where folders provide context, and in the chat Project, where they do not.

Files fall into two groups with different patterns.

**Project files** — the project's own infrastructure: tasks, templates, the instruction layer. Prefixed with the project identifier so they are self-describing in a flat context.

| Pattern | Applies to |
| --- | --- |
| `[project-id]-task-[artifact].md` | Task workflow files |
| `[project-id]-template-[category]-[artifact].md` | Template files |

**Content files** — output artifacts the workflow produces for specific instances. Prefixed with category so files in the same category sort together.

| Pattern | Applies to |
| --- | --- |
| `[category]-[name]-[artifact].ext` | Per-project output files |

Where **`[project-id]`** is the short project identifier, **`[category]`** is the workflow or content category, **`[name]`** is the specific instance or topic, and **`[artifact]`** is the file's role or content type. A task file for a copy workflow in a project identified as `abc` is `abc-task-copy.md`; a copy output for one instance in that project's segment category is `segment-[name]-copy.md`.

`CLAUDE.md` is always named exactly that, with no prefix, in every project.

**Repo versus chat Project:** the repo may use subfolders. The chat Project is always flat. File names work in both without translation.

**Audit checkpoint:** Test every file name against the pattern for its group — task file, template, or content file — and flag each one that does not match. Confirm the instruction file is named `CLAUDE.md` exactly, with no prefix. Read each name with its folder removed and flag one whose role cannot be stated from the name alone.

**Judgment call:** whether a file's role can be stated from its name alone is read from the name's meaning, and is confirmed with the contributor where the reading is not obvious.

---

## File organization

File organization and reference format depend on which surfaces the project runs on.

**Chat Project.** Files are uploaded flat; the surface does not support folders for contributor-managed content. All uploadable files live in the project root. Subfolders exist in the repo only for files that are never uploaded — instruction variants, archived files. References in task files and the instruction layer use the **filename only**, with no path prefix.

**Repo-only surfaces.** No flat requirement. Files live in subfolders as the repo structure suits. References use the **full path** relative to the repo root.

**Hybrid.** Files stay flat-uploadable for the chat Project. Where a file lives in a repo subfolder and is also uploaded to the chat Project, reference it with the plain filename first and the repo path in parentheses, so the reference is unambiguous on both surfaces without duplicating content.

**What may sit in subfolders, repo only, never uploaded:** surface-specific instruction files, and retired versions.

**Audit checkpoint:** Name the surfaces the project runs on. Test every reference in the task files and the instruction layer against the format those surfaces take — filename only, full path from the repo root, or filename with the repo path in parentheses — and flag each one in the wrong form. List the files sitting in repo subfolders and flag every one that is neither a surface-specific instruction file nor a retired version.

---

## Claude-writable project knowledge

Some surfaces expose a tool that reads, writes, searches, and deletes project-knowledge docs directly.

**A doc that already exists** is written directly, at its exact existing path; the write replaces it in place and keeps it flat, whether the doc was Claude-authored or contributor-uploaded.

**A new doc that must sit flat at the project root** is produced as finished content for the contributor to add through the upload interface. A first write to a new bare filename lands under a `claude/` prefix, not the project root, and the contributor cannot manage that namespace through the upload interface.

The flat-file naming convention applies to docs at the root and under `claude/` alike.

**Audit checkpoint:** List every instruction in the project that writes a project-knowledge doc. For one naming a doc that already exists, confirm it writes to that doc's exact existing path. For one creating a doc that must sit flat at the project root, confirm it produces finished content for the contributor to add through the upload interface rather than writing a bare filename. Flag every statement that an existing project-knowledge doc cannot be written directly.

---

## Surface arrangement

A project commonly spans more than one surface: a chat Project several contributors share, and a local working surface that may be shared or per-contributor. Neither is authoritative by default.

**The project declares the arrangement** in its own instructions, under the rule `common-standards.md` states: which surfaces it uses, which is authoritative for each kind of content it holds, and how content present on more than one syncs. A project with no chat surface declares that too.

**Promotion.** Content larger than a single project-knowledge doc holds — spanning several files, or too large to maintain in one — sits on the local surface, the doc carries a pointer to it, and the declaration names the local surface as authoritative for it.

**Drift.** Where a contributor may edit a copy outside a Claude session, the project states a reconciliation check rather than assuming either side is current.

**Audit checkpoint:** Confirm the project declares its surfaces and names the authoritative surface for each kind of content it holds. Flag content with no named authority, and content named authoritative on two surfaces. Where content sits on the local surface, confirm it spans several files or has outgrown one doc and that a pointer to it remains. Where a contributor may edit a copy outside a Claude session, confirm a reconciliation check is stated. Confirm the declaration names the local surface as authoritative for promoted content.

**Judgment call:** whether a contributor may edit a copy outside a Claude session rests on contributor practice rather than on the project's files, and is confirmed with the contributor.

---

## `CLAUDE.md` standards

The instruction file is a thin routing and orientation layer, not a workflow document. Task detail lives in task files. It contains:

1. **Identity** — one paragraph: what the project does, who uses it, what Claude's role is
2. **Production flow** — the workflow stages in order
3. **Task routing table** — each task name mapped to its task file; Claude reads only the file for the current task
4. **Skill declaration** — see "Projects explicitly invoke their skills" below
5. **Behavioural rules** — the rules below, verbatim unless the project has a stated reason to deviate

**Five default behavioural rules for every project.** A project's `CLAUDE.md` carries the numbered block below verbatim.

1. Never load a source speculatively — only what the current task requires.
2. Always confirm before creating pages, tickets, or other external artifacts.
3. Always confirm before modifying documentation, prompts, or project instructions.
4. Any time a workflow issue is noticed — incorrect output, workflow gap, redundant step, routing failure, documentation drift, or missing guardrail — ask whether to log it now or hold it for later, under `issue-logging`.
5. When referencing a documentation page by name, include a hyperlink on first mention within a given context.

**What the instruction file must not contain:** task workflow steps, skill logic, or content duplicating a task file.

**Length principle:** workflow steps appearing in the instruction file belong in a task file.

**Audit checkpoint:** Confirm the instruction file carries all five components — identity, production flow, task routing table, skill declaration, behavioural rules — and name each absent one. Compare its behavioural rules against the five above; flag an absent rule, and a reworded one carrying no stated reason to deviate. Scan it for task workflow steps, for skill logic, and for content also held in a task file; each is a defect.

---

## Task file splitting

A task file can grow to cover more than one genuinely separable sub-workflow, the same way workflow steps outgrow `CLAUDE.md`. The criteria deciding whether the content splits are stated in `skill-standards.md`'s Sub-file splitting section and govern task files unchanged.

**The project-side delta.** Each piece a split produces is reached either as its own task file carrying its own routing-table row, or — where the pieces share one entry point — from a nested subfolder whose task file does only the routing. A nested subfolder is available only on surfaces that support folders.

This decides only whether to split. Where the resulting pieces belong — another task file, a new project, or a skill — is a placement question, decided under `skill-standards.md`'s Granularity rules.

**Audit checkpoint:** Apply `skill-standards.md`'s splitting criteria to every task file and flag each one holding more than one independently-selected sub-workflow, naming the resulting routing-table change. For every split already made, confirm each piece carries its own routing-table row, or that one task file routes into a nested subfolder and the project runs on a surface supporting folders.

---

## Instruction surfaces

The primary instruction file is `CLAUDE.md`, uploaded to the chat Project or accessed via mounted repo.

**Single surface:** `CLAUDE.md` only.

**Multiple surfaces:** an `instructions/` subfolder holds a file per surface that needs a distinct one. `CLAUDE.md` mirrors the primary instruction. Files in `instructions/` are never uploaded to the chat Project.

**Naming for surface-specific instruction files:** `instruction-for-[surface].md`.

A second instruction file is warranted only where a surface is responsible for a genuinely different set of tasks. Two surfaces handling the same tasks share `CLAUDE.md`. Where two instruction files share content, the project names which sections stay in sync and how that is checked.

**Audit checkpoint:** Count the surfaces the project runs on. Where there is one, confirm `CLAUDE.md` is the only instruction file. Where there are several, confirm every surface holding a different set of tasks has a file in `instructions/` named `instruction-for-[surface].md`, that `CLAUDE.md` mirrors the primary instruction, and that no file in `instructions/` is uploaded to the chat Project. Where two instruction files share content, confirm the project names the sections staying in sync and how that is checked.

---

## Shared projects with mixed contributor access

A project with multiple contributors on a shared chat Project does not assume every contributor has the same access. The split is designed explicitly.

**Split access without repo access.** The shared instruction layer reads correctly for a contributor with no local or repo access at all — no contributor-specific paths, named repos, or install locations. Environment-specific detail belongs only in that contributor's own local instructions layer.

**Permanent-plus-onboarding.** Where a contributor may be missing a local working surface, the project carries two standing behavioural rules rather than a one-time setup step: at the start of every session on that surface, ask whether to connect one as a soft ask, continuing normally if declined; and where none is declared for the current contributor, propose adding one once, then suppress the prompt for roughly five sessions with them if declined, recording the decline so the suppression holds across sessions, then offer again.

**Shared-versus-local split.** A shared instruction file serving multiple contributors stays generic and contributor-agnostic. Each contributor's own local instructions layer adds environment-specific paths and mechanics on top. Check whether the current contributor has a local layer before assuming any contributor-specific detail belongs in the shared file.

**Audit checkpoint:** Read the shared instruction layer for a contributor-specific path, a named repo, and an install location; each is a defect, and each belongs in that contributor's own local instructions layer. Where a contributor may be missing a local working surface, confirm the project states both standing rules — the per-session soft ask that continues normally when declined, and the propose-once-then-suppress rule recording the decline so the suppression holds across sessions — as standing behavioural rules rather than as a one-time setup step.

**Judgment call:** whether a contributor may be missing a local working surface rests on the contributor population, and whether the suppression has held for roughly five sessions rests on session history; neither is in the project's files, and both are confirmed with the contributor.

---

## Updating project instructions

A project's **custom-instructions field** is not writable through any tool, on any surface, including one with direct project-knowledge-write access. When a project instruction update is needed, produce the full updated text in a plain-text code block for the contributor to paste manually.

This is a different surface from **project-knowledge docs** — task files, templates, and reference files in the Project's knowledge base. Those are writable in place once they exist; only a brand-new one needs the manual-upload path. The two are not conflated: a statement about the custom-instructions field says nothing about a project-knowledge doc.

**Audit checkpoint:** Find every instruction that updates the project's custom-instructions field and confirm it produces the full updated text in a plain-text code block for the contributor to paste. Flag one directing a tool at that field. Confirm no statement about the field is applied to a project-knowledge doc.

---

## Project self-sufficiency

A project runs its core workflow correctly when external resources are unavailable. External resources hold content that genuinely belongs outside the project, such as governance or stakeholder transparency, and are never defaults.

Where a step uses an external resource, the project documents what happens when it is unavailable.

**Audit checkpoint:** List every step using an external resource and confirm the project documents what happens when that resource is unavailable. Then read the core workflow with every external resource treated as unavailable and name the first step that cannot complete; that dependency is a defect.

---

## External resources are optional, not default

Claude fetches an external resource because a specific step requires it, never as a startup habit. A project may use one heavily; every external fetch is justified by the step requiring it.

**Audit checkpoint:** List every external fetch the project instructs and name the step requiring each. Flag a fetch instructed at startup or on session open, and one no step names.

**Judgment call:** whether a step genuinely requires the resource it fetches is read from the step's own content, and is confirmed with the contributor.

---

## Projects explicitly invoke their skills

A project is the orchestrator: any workflow needing more than one skill is composed by the project that calls them.

### Declaring the skill set

`CLAUDE.md` carries a skill declaration naming every skill the project uses. Each entry states three things and nothing else: the skill's **name**, **when it applies**, and its **gate strength**, and never restates what the skill does beyond the task type it owns. What a project may name about a skill's internals is stated in `skill-standards.md`'s Skill/project file-reference boundary section, which owns both directions of that boundary.

### Gate strength

Every declared skill carries one of two, stated explicitly.

**Hard gate.** The task cannot be performed correctly without the skill. Where it is absent, Claude names the missing skill and the blocked task and stops.

**Soft gate.** The skill improves the task, and the task remains coherent without it. Where it is absent, Claude states the omission once, offers to continue, and proceeds if the contributor accepts.

An entry with no stated gate strength is a defect: it leaves the absent-skill behaviour undefined.

### When a declared skill is absent

Absence is reported, never worked around. Claude does not reconstruct a missing skill's rules from a prior session, from another skill that references it, or from the project's own files. A hard gate stops; a soft gate continues with the omission stated.

### Startup declarations

A skill required before any task content is processed is declared as a startup sequence rather than a task-level entry. The full sequence completes before task content is engaged, whatever the opening message contains. A task-rich opening message does not reorder it.

### A declared skill is live

Every skill a declaration names is live for every contributor to the project: released, and installed on every surface the project runs on. A fallback name listed beside a skill that is not live does not satisfy this.

### Interaction with referral

Referral between skills is defined in `skill-standards.md`, which owns it. Project-level invocation is what makes a skill reliably present. A project does not omit a skill from its declaration because some other skill refers to it.

**Audit checkpoint:** Confirm every skill the project's task files rely on appears in the declaration with a stated gate strength, and that each entry states the skill's name, when it applies and its gate strength, and nothing further about what the skill does. A skill reached only through another skill's referral, and relied on by a task, is an undeclared dependency and a defect. For every skill the project requires before task content is processed, confirm it is declared as a startup sequence rather than as a row in the routing table, and that the declaration states the sequence completes whatever the opening message contains. For every declared skill, confirm it has a released version and an index entry, and flag one that has neither. Flag any project instruction supplying a declared skill's rules for use when the skill is absent — from a prior session, from another skill, or from the project's own files.

**Judgment call:** whether each declared skill is installed on every surface the project runs on rests on surface configuration, which no file records. It is confirmed with the contributor.

---

## Feedback is not a task

Feedback is copy editing or build editing routed through the appropriate task file. A project has no standalone feedback task.

**Audit checkpoint:** Scan the routing table and the task files for a task whose subject is feedback; each is a defect. Confirm every feedback path routes into the copy-editing or build-editing task file owning the change it makes.

---

## Knowledge base patterns

**Uploaded files.** For a core reference set living in the project and updated over time. Load only sections the current task needs, never entire files speculatively. Treat uploaded files as current; never assume content from a prior session.

**A human-facing reference surface.** For content that genuinely belongs outside the project, such as finalized copy, project briefs or the issues log. Workflow logic and behavioural rules stay in the project files. Claude fetches that content only where a task step requires it, never at startup. Hard rules live in the instruction file, in effect before any external page loads.

**Hybrid.** Most projects use both. The project maps which sources serve which purpose and states which takes precedence where they conflict.

**Audit checkpoint:** For every uploaded file, confirm the task using it names the sections to load rather than the file whole, and flag an instruction to load one speculatively. Flag an instruction treating an uploaded file as possibly stale, and one carrying content forward from a prior session. For the human-facing reference surface, confirm every fetch is tied to a task step requiring it and that no behavioural rule or hard rule lives there rather than in the instruction file. Where the project uses both patterns, confirm it maps which sources serve which purpose and states which takes precedence where they conflict.

---

## QA standards

A project carries no QA task and no self-improvement workflow of its own.

A project may hold a `qa-standards.md`. The whole contract for that file — when one exists, what belongs in it, and how an audit loads it — is in `references/qa-standards-format.md`.

**Audit checkpoint:** Scan the routing table and the task files for a QA task and for a self-improvement workflow; each is a defect. Where a `qa-standards.md` is present, assess it against `qa-standards-format.md` rather than against this file.

---

## Linking rule

When referencing a documentation page by name in any project content — Claude-facing or contributor-facing — include a hyperlink on first mention within a given context. Repeat mentions in the same context do not require one. This section is the source of the fifth default behavioural rule in the `CLAUDE.md` template above.

This applies to documentation pages. It does not apply to tool names or file names.

**Audit checkpoint:** Find every documentation page named in the project's files and confirm the first mention in each context carries a hyperlink. A tool name or a file name carrying none is not a defect.

---

## Shared rules

Naming, version management, editing workflow, repository setup, distribution, instruction cleanliness, external references, checkpoint markers and the issues-log declaration are the same for every governed artifact and are stated in `common-standards.md`, which also records the project-specific deltas. None of them is restated here. The file naming convention above governs files *inside* a project and is separate from the artifact naming convention.
