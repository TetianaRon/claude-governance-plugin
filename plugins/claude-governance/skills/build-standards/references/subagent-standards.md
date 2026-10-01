# SUBAGENT-STANDARDS
# build-standards

Authoritative reference for how governed subagents are defined and maintained. Load it when building, auditing, or refining a subagent — never at session startup. Load `common-standards.md` alongside it: this file states only what is specific to subagents.

---

## What a subagent is

A subagent is one delegated worker. It receives a task whose inputs are complete, runs in a context of its own, writes its result to a file, and returns a summary of that result to the session that dispatched it. It holds no conversation with a contributor and carries nothing between dispatches.

Its remit is one task type. A definition covering several task types is a routing surface rather than a worker, and routing between workflows is a skill's remit.

A subagent produces an artifact; it does not decide what to do about one. The judgment a finding calls for belongs to the session that dispatched it.

**Audit checkpoint:** Name the single task type the definition covers. Flag a procedure that branches on which of several task types the subagent was handed, and any instruction directing the subagent to act on its own findings. Flag an instruction that assumes a prior dispatch's state, output or conversation is still available to this one.

---

## Whether it needs authoring at all

Whether an existing artifact already serves the work, and the three outcomes that question has, are stated in `skill-standards.md` under Whether it needs authoring at all. They hold for a subagent with built-in and third-party workers as the catalogue, and with the adoption properties below in place of a skill's. An adopted worker's standing is stated in `common-standards.md` under Adopted artifacts.

**Ad-hoc dispatch.** A delegable task whose useful content varies by invocation needs no definition: the dispatching skill composes the prompt from its own context, and the skill carries the guidance for writing that prompt. A task type is a subagent only where it recurs with the same shape — the same inputs, procedure and output contract — across dispatches by different sessions and contributors.

**When an existing worker can be adopted as it stands.** Three properties, all of which hold:

- it covers the whole task type rather than part of it
- its tool allowlist and its write scope are knowable
- it is not assessing against a governed standard; a worker assessing against one is authored whatever its capability

**Audit checkpoint:** For every subagent the estate authored, name the closest built-in or third-party worker available to it and state the property that worker lacks. A subagent assessing against a supplied authority satisfies this on the third property alone. For every adopted worker, test all three properties and name each that fails. For every subagent the estate authored, name the dispatches sharing its shape across sessions, and flag one whose inputs or procedure vary by invocation.

**Judgment call:** which workers are available, and whether an outside worker's tool allowlist and write scope are knowable, rest on a worker population and on bodies the estate holds in no file. Whether a task type recurs with the same shape rests on dispatch history. Each is read from its source and confirmed with the contributor.

---

## What is delegable

A subagent holds no route to the contributor, whatever its tool allowlist states.

A delegable task type is one whose inputs are complete at dispatch and which reaches a result without a decision the contributor owns. Audit, inventory, verification, extraction and bulk transformation are of this shape. Intake, interview, scope negotiation and any workflow carrying a checkpoint are not.

A definition carrying a checkpoint marker, a structured question, or a step conditioned on contributor confirmation states a task its own runtime cannot complete, and is an audit gap.

**Audit checkpoint:** Scan the definition for a checkpoint marker, a structured-question step, and any instruction to ask, confirm, or clarify. Each is a defect. Confirm every input the procedure consumes appears in the definition's stated input list rather than being obtained mid-run.

---

## The definition file

A subagent is one markdown file: YAML frontmatter, then a body. That file is the subagent's entry-point file, and the rules `common-standards.md` attaches to an entry-point file attach to it.

Frontmatter keys:

- `name` — names the subagent under the naming convention in `common-standards.md`.
- `description` — the task type the subagent is dispatched for.
- `tools` — the exact tool set the subagent holds.
- `model` — the model the subagent runs on.

An absent `tools` key grants the full tool set of the dispatching session. An absent `model` key leaves the model to the dispatching session. A governed subagent states both explicitly.

The body carries the procedure, the output contract, and the subagent's own rules. Nothing in the body is presented as optional: a subagent has no second pass in which a skipped step is noticed.

**Audit checkpoint:** Confirm the definition is a single markdown file whose frontmatter states `name`, `description`, `tools` and `model`. Flag every absent key. Confirm the body carries a procedure, an output contract and a rules section, and flag any step phrased as a preference rather than an instruction.

---

## Description

A subagent's description is read on its own, without the body, by the session choosing which worker to dispatch. It states the task type, the scope the subagent operates on, and whether the subagent writes anything outside its own output file.

A description naming only a domain leaves the dispatching session to open the definition to find out what the worker does, which defeats the purpose of the field. A description promising behaviour the body does not implement misroutes work to a worker that cannot do it.

**Audit checkpoint:** Read the description alone and state, from it, what the subagent does, what it operates on, and what it writes. Flag a description that leaves any of the three unanswered, and any capability it claims that the body's procedure does not carry out.

**Judgment call:** what a reader takes from the description alone is read from the passage's meaning, and is confirmed with the contributor where the reading is not obvious.

---

## Tool allowlist and target scope

Two separate things bound what a subagent can do, and neither substitutes for the other.

**The tool allowlist bounds capability.** `tools` names the exact set. A subagent that reads and reports holds reading and searching tools.

**The definition bounds the target.** A general-purpose tool in the allowlist — a shell, a script runner — carries write capability that the allowlist cannot subtract. A subagent holding one states in its rules what it does not touch, naming the scope rather than the tool.

A read-only subagent is one holding no write-capable tool, or holding one under a stated prohibition on writing anywhere but its own output file. A subagent described as read-only with neither property is an audit gap: the description states a guarantee nothing in the definition provides.

**Audit checkpoint:** List the allowlist and mark every entry that can write. For each, find the rule in the body naming what it may not touch. Flag a write-capable tool under no stated prohibition, and a stated prohibition naming a tool rather than a scope. Read the description for a read-only claim. Where one is made, confirm the definition holds either no write-capable tool or a prohibition scoped to the output file; a read-only claim with neither is a guarantee the definition does not provide.

---

## One file, and its authority arrives as an input

A subagent's content is the definition file and nothing else. It has no sub-files.

Content the subagent works against — a standard it assesses to, a schema it maps onto, a list it processes — arrives as a named input resolved by the dispatching session, and the subagent reads it at the start of its run. A definition embedding a copy of that content holds a second copy of a rule that has an owner elsewhere, and the copy diverges with nothing detecting it. A definition reaching for that content by a path of its own binds the worker to one caller's layout.

The definition states that the supplied authority is the only one the subagent assesses against, so that conventions carried in the model's own priors are excluded from the result.

**Audit checkpoint:** Confirm the subagent's content is one file. Scan the body for restated rules belonging to another artifact, for a path the definition resolves itself rather than receiving, and for the clause excluding unsupplied conventions. Each absence is a defect.

---

## Inputs

The definition enumerates every input the subagent is given, each named and each stated as an absolute location where it is a file or directory.

An input the procedure consumes but the list omits makes a dispatch that satisfies the list fail anyway, and the failure surfaces inside a context the dispatching session does not see.

**Audit checkpoint:** Cross-check the procedure against the input list in both directions. Flag an input the procedure uses and the list omits, an input the list states and the procedure never reads, and any input stated as a relative location.

---

## Output contract

A subagent's definition carries no schema key: the platform provides no field constraining a return payload, so the contract is stated in the definition's own section and enforced by the rules under it.

Three rules carry it.

**The file is the deliverable.** The subagent writes each unit of its result to the output location it was given as that unit is confirmed, in a structure the definition states, so the file holds every confirmed unit at every point in the run. The return payload carries a pointer to that file, the counts that let the dispatching session check the run's shape, and one line per unit of the result. The payload is a summary and is neither the artifact nor evidence of what the artifact contains.

**A unit missing its identifying fields is not a unit.** The definition states the fields every unit of the result carries — for a finding, the exact location and the clause it violates — and states that anything lacking them is dropped rather than recorded. The shape is enforced where the unit is authored, which is the only place a subagent can enforce anything.

**What was not confirmed is stated as not confirmed.** The subagent verifies each unit against its source before recording it, and reports separately anything suspected and unconfirmed. A definition without this rule returns a result in which the checked and the assumed are indistinguishable.

**Audit checkpoint:** Confirm the definition names the output location, states the file's structure, states the return payload's contents, and instructs that each unit is written to the file as it is confirmed rather than once before the return. Confirm the required fields per unit are named, that a unit lacking them is dropped, and that unconfirmed material has a stated home in the output structure. Confirm the definition instructs verifying each unit against its source before it is recorded — a stated home for unconfirmed material does not carry that instruction on its own.

---

## Naming another artifact

A subagent naming another governed artifact does so under the referral constraints in `skill-standards.md`, which owns them for every artifact that can be invoked. Nothing in them is restated here.

A subagent's own delta: its authority arrives as an input, so a subagent never names the artifact whose standard it assesses against. Naming one would fix from inside the definition what the dispatcher is required to supply.

**Audit checkpoint:** For every mention of another governed artifact in the definition, assess it against `skill-standards.md`'s referral constraints. Flag any mention of an artifact the subagent assesses against.

---

## Shared rules

Naming, version management, editing workflow, repository setup, distribution, instruction cleanliness, external references, checkpoint markers and the issues-log declaration are the same for every governed artifact and are stated in `common-standards.md`, which also records the subagent-specific delta. It is not restated here. Where a subagent ships inside a bundle, its location there is stated in `plugin-standards.md`.
