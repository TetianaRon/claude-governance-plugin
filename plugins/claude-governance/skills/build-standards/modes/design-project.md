# PROJECT-BUILD
# Design - Project Build | build-standards

**Purpose:** Build a new Claude project from scratch — scope, knowledge base, prompt, documentation, and QA mode. Depth is determined during intake: MVP produces a working skeleton immediately; Full produces a complete, polished project.

---

## Phase 1 — Intake and depth selection

Collect the following through conversation. Infer anything obvious from context. Ask one topic at a time.

| Field | MVP needs | Full needs |
| --- | --- | --- |
| Project name | ✓ | ✓ |
| Purpose (one sentence) | ✓ | ✓ |
| Primary tasks (names only) | ✓ | ✓ |
| Hard boundaries | ✓ if obvious | ✓ |
| Connected tools | ✓ | ✓ |
| Knowledge base sources | — | ✓ |
| Output format | — | ✓ |
| Routing logic | — | ✓ if multiple tasks |

For connected tools, present a structured multi-select choice:

```
Question: "Which tools should this project be connected to?"
Type: multi-select
Options: GitHub, Google Drive, Gmail, Google Calendar, Notion,
         Slack, Linear, Jira, Other (describe in chat)
```

After collecting the basics, select depth:

```
Question: "How far do you want to go in this session?"
Options:
- MVP — get a working skeleton live now, expand later
- Full — design the complete project properly from the start
```

If they choose MVP: proceed through all phases but apply the MVP content standard (see Phase 4). Skip knowledge base design and routing logic unless provided.

If they choose Full: collect all fields before proceeding to Phase 2.

---

## Improving an existing project

Reached from Improve's Phase 3 or a targeted adjustment. Phase 1's depth selection, Phase 2's identifier and Phase 7's file creation belong to a new build and are not run. For the parts being changed: apply the rule-writing check to any new hard rule, redraft against references/project-standards.md, and deliver through Phase 8.

---

## Phase 2 — Standards and identifier

Load references/project-standards.md before proceeding. Apply its file naming, file structure, prompt standards and documentation link rule throughout this session.

Assign a project identifier following PROJECT-STANDARDS. Present the suggestion and confirm before creating any files.

---

## Phase 3 — Scope definition (Full only)

For MVP, skip to Phase 4.

Draft a scope statement covering:
1. What Claude does in this project
2. What Claude explicitly does not do
3. Routing logic — if the project handles multiple task types, how Claude identifies the type and what it loads for each
4. Composition — for each workflow step, whether it is a task file, a skill, a subagent, or ad-hoc dispatch with no artifact (Ad-hoc dispatch under Whether it needs authoring at all in references/subagent-standards.md)

Present the scope statement and confirm before proceeding:

```
Question: "Does this scope look right before we move to the knowledge base?"
Options:
- Yes, looks good — continue
- I want to adjust something
```

---

## Phase 4 — Knowledge base design (Full only)

For MVP, skip to Phase 5.

Recommend a knowledge base pattern from PROJECT-STANDARDS's Knowledge base patterns, with a one-sentence rationale, and confirm it:

```
Question: "I recommend [pattern] because [reason]. Go with it?"
Options:
- Uploaded files
- A human-facing reference surface
- Hybrid — both
```

**Surface arrangement.** Write the project's surface declaration into its instructions under PROJECT-STANDARDS's Surface arrangement: the surfaces it uses, the authoritative surface for each kind of content, and how content on more than one syncs. A project with no chat surface declares that too.

---

## Phase 5 — Prompt

If this session is editing an existing project to add a new hard rule or gate to its instructions (not first-pass drafting of a brand-new project), apply guards/rule-writing-gate.md before writing it in.

Draft the project instruction prompt following the prompt standards in PROJECT-STANDARDS. Include all five default behavioural rules and a dedicated "Issues log" section (identifier and log location, in the form common-standards.md states). Insert the project's short identifier. If the contributor has not already said where the issues log lives, ask, and record its location:

```
Question: "Where should the issues log live?"
Options:
- `ISSUES.md` at the project repo root
- Other — I'll name it
```

**MVP standard:** Identity sentence + five default hard rules + entry-point link. Nothing else.
**Full standard:** Identity + hard rules + task routing (if applicable) + entry-point link.

Present in a code block and confirm before proceeding:

```
Question: "Does this prompt work?"
Options:
- Yes, looks good
- I want to adjust something
```

---

## Phase 6 — File list and optional QA standards

Propose the full file structure using the confirmed identifier and the file structure from PROJECT-STANDARDS.

The Improve mode is the unified QA layer for every project — projects do not need their own QA task or self-improvement workflow (see PROJECT-STANDARDS → QA standards). Ask whether this project has QA criteria specific enough to warrant its own `qa-standards.md`:

```
Question: "Does this project need a qa-standards.md — QA criteria specific to it that generic project standards wouldn't cover?"
Options:
- No — generic project standards cover this project fine
- Yes — I have project-specific criteria to capture
```

If yes, load references/qa-standards-format.md and draft the file following its structure.

Present the full file list:

```
Question: "Does this file structure look right?"
Options:
- Yes, let's create everything
- I want to adjust something first
```

---

## Phase 7 — Create files

Confirm the location:

```
Question: "Create the project files in [repo path]?"
Options:
- Yes, there
- Somewhere else — I'll give the path
```

Create all files in the approved structure, including the issues log where the contributor chose a file. Confirm the project identifier and issues log location are correctly declared in the prompt's "Issues log" section.

---

## Phase 8 — Output

**MVP:** Ask for the next step:

```
Question: "The project skeleton is live. What's the next step?"
Options:
- Ship as-is and use it — I'll expand later if needed
- Continue to Full design now
- Run the Improve mode as a QA pass after I've used it a bit
```

If they choose Full: continue from Phase 3 using the existing files as the foundation — do not repeat intake.

**Full:** Produce a source checklist (files to upload, tools to connect, skills to install). Then produce the project specification document and ask for the preferred format:

```
Question: "How would you like the project spec delivered?"
Options:
- Markdown file in the project repo
- Downloadable file (Word doc)
- Both
```

---

## Behavioural rules

- Always load PROJECT-STANDARDS before Phase 2 — never invent naming or structural conventions from memory
- Load qa-standards-format.md only if the project needs its own qa-standards.md — the Improve mode is the default QA layer for every project
- Never create files without a confirmed identifier
- Never create files without confirming the location
- Always confirm the project identifier and issues log location are declared in the prompt's "Issues log" section before finalising
- Log gaps and friction passively — do not raise in session unless blocking
- For repo-backed projects: create a `.gitattributes` at the repo root as the first commit (see COMMON-STANDARDS → Repository setup)
