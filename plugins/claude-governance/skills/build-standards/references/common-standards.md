# COMMON-STANDARDS
# build-standards

Rules that hold for every governed artifact regardless of class — naming, versioning, editing, repository setup, distribution, registration, instruction quality, external references, and checkpoint markers. Load it alongside the relevant class standard when building, auditing, or refining any artifact — never at session startup.

The placement rules governing this file and the class standards, together with the family's checkpoint notation, are in `standards-format.md`.

---

## Governed artifact classes

Four classes are governed: **projects**, **skills**, **plugins**, **subagents**. Every rule below applies to all four unless a class delta is stated.

An artifact of any class that no standard covers is an audit gap. A class with no standards file cannot be certified, and nothing uncertified ships. An artifact the estate uses and did not author is adopted rather than governed, and stands under Adopted artifacts below.

**Audit checkpoint:** Name the class of every artifact under audit and confirm it is one of the four. Confirm a standards file exists for each class named. Flag an artifact whose class is none of the four, and a class named by an artifact for which no standards file exists. Separate the adopted artifacts before certifying and assess each under Adopted artifacts instead.

---

## Adopted artifacts

The estate ships only what it can certify. It may depend on what it cannot.

An adopted artifact is one the estate uses and did not author. Its content sits outside the estate's control, so no class standard is applied to it and none certifies it. What is governed is the dependency rather than the artifact: an adopted artifact carries a declaration by name and gate strength in every project reaching it, and a recorded version in use.

It sits outside the naming convention, which governs the names the estate gives.

Two things an adopted artifact is never. It is never a member of a governed bundle; what a bundle may carry is in the plugin standard. And it is never named as the owner of a rule, and no estate file restates what it says; the form a referral to it takes is in the skill standard.

**Audit checkpoint:** List every artifact the estate depends on and did not author. For each, confirm a recorded version in use and a declaration with gate strength in every project reaching it, naming each absence. Flag an adopted artifact certified against a class standard, one held as a member of a governed bundle, and every estate file restating its content.

---

## Naming convention

**Shared artifacts:** `[purpose]`
**Project-specific artifacts:** `[project]-[purpose]`

- **project** — the project's own name in kebab-case. Present only for project-specific artifacts; a shared artifact carries no scope marker at all.
- **purpose** — the workflow the artifact performs, in plain English, kebab-case. It names what the artifact does, not the context it runs in or the surface it runs on.
- All names: lowercase, hyphens only, maximum 64 characters.
- The version never appears in the name.

Every artifact's name is unique across the estate.

**Exemption — vendor-neutral artifacts.** An artifact implementing an external public standard, with no governance-specific content, is named for the standard it implements. `git-commit-message` is the estate's instance.

**Class deltas.**

- **Project** — a project also carries a short identifier used to prefix its own files. The identifier is not the name; the file naming convention is in the project standard.
- **Plugin** — the bundle's own name, and the names its bundled artifacts carry, are governed in the plugin standard.
- **Skill, subagent** — no delta.

**Audit checkpoint:** Parse every artifact name against the two forms. Three failures to look for: a leading segment that is a scope marker naming no real project; a project segment naming a project that does not exist; and a purpose segment naming a session type, a surface, or a context rather than a workflow. Confirm every name is lowercase, uses hyphens as its only separator, runs to 64 characters or fewer, and carries no version substring. Parse every name against the full roster of governed artifacts and flag every collision.

**Judgment call:** whether a purpose segment names a workflow rather than a session type, a surface or a context is read from the name's meaning; where the reading is not obvious it is confirmed with the contributor.

---

## Version management

Two versions exist, with different objects. Neither is "the version" in the abstract, and neither substitutes for the other.

**The content revision.** The artifact's own version, tracked as `vMAJOR.MINOR` in a `**Version:**` line near the top of the artifact's entry-point file body — never as a frontmatter or manifest key. This is what a contributor reads to know which revision of the rules they are running, and it is the version any release note cites.

| Change type | Increment |
|---|---|
| A sub-file added or removed | Minor |
| Content change to an existing sub-file | Minor |
| Structural change to entry-point routing | Major |
| More than half of the artifact's lines added, removed or rewritten, counted on the release's cumulative diff | Major |

Where more than one row applies, the highest increment applies.

**Class deltas.**

- **Skill** — content revision in `SKILL.md`'s body.
- **Project** — content revision in `CLAUDE.md`'s body.
- **Plugin** — no content revision of its own; its content is the artifacts it bundles, each keeping its own. The bundle's distribution revision is in the plugin standard.
- **Subagent** — content revision in its definition file's body.

**A release is the unit the version tracks.** An artifact's source changes many times between releases and owes nothing for each change. A release is one act carrying three properties, and an artifact that has been released holds all three: the version in its entry-point file is the version released; the installable artifact's filename carries no version suffix, the version living inside the artifact; and the installable file built from that version is committed with its source and tagged. An artifact holding some but not all of these is mid-release rather than released.

Installing on a surface the session cannot reach is the contributor's own action. Claude hands over the artifact and names each surface.

**Audit checkpoint:** Locate the `**Version:**` line in the artifact's entry-point file body, and confirm no frontmatter or manifest key carries the content revision. Confirm the installable artifact's filename carries no version suffix. Name the change behind the current revision against the increment table and confirm the increment matches.

**Judgment call:** which increment a change warrants rests on the artifact's prior state, which the file under audit does not hold. It is read from the change itself, and confirmed with the contributor where the reading is not obvious.

---

## Editing workflow

Edit the source, never the install.

An artifact's content lives on one surface or several. Which surfaces it uses, and which is authoritative for each piece of its content, is a property of the artifact rather than a default this file sets.

**Every artifact's surfaces are declared.** The declaration names each surface its content lives on and, for every piece of that content, the one surface authoritative for it. It sits in the artifact's own entry-point file, or in the instructions of the repo holding the artifact's source, which then covers every artifact the repo holds.

**Edit the authoritative surface.** A copy anywhere else is derived. An edit to a derived copy diverges it from its source with no version change and no signal at the source, and a derived copy is evidence of itself and never of what its source holds.

**Content on more than one surface states how it syncs** — the direction it travels, what triggers it, and who performs it.

**A surface whose write path can fail states a fallback route.**

**Audit checkpoint:** Find the artifact's declaration of surfaces, in its entry-point file or in the instructions of the repo holding its source. Confirm every piece of its content is authoritative on exactly one named surface, and flag content authoritative on none and content authoritative on two. For content present on more than one surface, confirm a sync mechanic naming direction, trigger and who performs it. Compare every derived copy against its authoritative surface and flag each difference. Confirm a fallback route is stated for every surface whose write path can fail.

**Judgment call:** which surfaces an artifact can use, and whether a surface's write path is reliable for the content it carries, are read from the surfaces themselves rather than from any file in the estate, and are confirmed with the contributor.

---

## Repository setup

A repo holding any governed artifact ships a `.gitattributes` at its root, created as its first commit. A repo whose `.gitattributes` postdates its committed content carries a one-time `git add --renormalize .` against that content.

Minimum content:

```
* text=auto eol=lf
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.svg text eol=lf
*.pdf binary
*.zip binary
*.skill binary
*.plugin binary
```

The requirement attaches to the repo, not to any artifact in it.

**Audit checkpoint:** Confirm a `.gitattributes` at the repo root carrying at least the lines above. Flag a missing file, and every listed pattern absent from one that exists. From the repo's history, confirm the file arrived in the first commit, or that a renormalize commit follows the commit that added it.

---

## Distribution

Every artifact is released as one installable file built from its source: a `.skill` zip for a skill, and an archive of the plugin directory for a plugin and every member it carries. Installing that file on a surface is the contributor's own step.

An artifact reaching any surface or person by another route declares that route itself — in its entry-point file or, for a bundled artifact, in the bundle's README — and its distribution follows the declaration.

**Audit checkpoint:** Confirm the artifact's installable file builds from its source. Where the artifact declares a further route, confirm the declaration names the route and the steps it takes.

---

## Issues log declaration

Every governed artifact declares its issues log explicitly in its entry-point file, in a dedicated **"Issues log"** section near the top. The section states only the short identifier and the log's location — a repo path or a single direct link to the document serving as that artifact's issues log.

    ## Issues log

    Identifier: ARTIFACT-ID
    Log: [repo path or direct link to the issues log]

A missing declaration is an audit gap in its own right.

**Class deltas.**

- **Plugin** — the entry-point file is a manifest and carries no prose, so the declaration sits in a `README.md` at the plugin root instead.
- **Subagent** — the entry-point file's body is the subagent's system prompt, so the section sits at the end of the file.
- **Project, skill** — no delta.

**Exemption.** An artifact under Naming's vendor-neutral exemption carries no issues log.

**Audit checkpoint:** Confirm the entry-point file — or, for a plugin, the root `README.md` — of every artifact not under the vendor-neutral exemption carries an **"Issues log"** section stating a short identifier and one location. Flag a missing section, an absent location, a location resolving to anything other than an issues log, and any content in the section beyond the identifier and the location.

---

## Rule form

Every rule states a property something has or lacks — true of an artifact that already exists and of one that does not exist yet — with no verb of transition in it. "Every rule has exactly one home" is a rule. "After the split, every rule must have exactly one home" is a condition on a change: it carries the same content in a form that expires.

Four shapes fail this:

- a rule phrased as a condition on a change
- a forward reference to a file that does not exist
- a stated class re-narrowed to a closed list in the same breath that states it
- a rebuttal of a prior position written as a rule

**Audit checkpoint:** Test every rule the artifact states against the property form. Quote each one carrying a verb of transition, each phrased as a condition on a change, each naming a file that resolves against neither the artifact nor the filesystem, each narrowing a class to a closed list in the sentence that states it, and each answering a position rather than stating a property.

---

## Instruction cleanliness

Artifact content states what to do — never why it used to say something else, what a prior version said, or the reasoning behind a design choice. No version history, no dates, no incident narratives, no "no longer" / "instead of" / "used to" framing, no tool-availability caveats phrased as explanation. State the current rule as a direct, present-tense fact.

Provenance, rationale, and decision history belong in git history, the issues log, or an improvement plan — never in a shipped artifact file.

A generic action — reading a linked document, delivering a file, posting a message, searching for a record — is described by the action itself, never by the connector, tool, or command that currently performs it. Name a concrete tool or command only where the mechanic requires it: a git invocation, a repo-owned script, a fixed API call whose parameters must match exactly.

**Audit checkpoint:** Two passes over every section.

1. **Narrative-marker scan** — flag "no longer", "instead of", "as of [date]", "because", "since [past tense]", incident descriptions, dated observations, and any concrete tool or connector name standing in for a generic action. Rewrite each as a direct, tool-agnostic rule.
2. **Content-scope scan** — check whether each section states only the rule needed to apply it, or also carries justification for that rule. Flag background reasoning not required to follow the rule, and another artifact's internal mechanics invoked to justify it. The form every rule takes is in Rule form above.

**Judgment call:** whether a passage is reasoning not required to follow the rule is read from the section's own content, and is confirmed with the contributor.

---

## External references

A governed artifact may name **stable shared infrastructure its own workflow reads or writes, identified by one durable link**. A destination qualifies when all three hold: it is durable across releases, it is shared rather than belonging to one artifact, and this artifact's own workflow reads or writes it. Destinations meeting the test include:

- the artifact's own issues log
- the distribution file store root, where installable artifacts are published

The list is not closed. A destination not shown here qualifies if it meets the three-part test, and one shown here stops qualifying if it ever fails it.

A governed artifact may **not** name a **per-artifact instance**: an individual artifact's download link, a version number, a named individual, or a page identifier belonging to another artifact's file set. Every one of these changes on a schedule the artifact does not control. Resolve them at point of use.

**Class deltas.** The skill/project file-reference boundary, which runs in both directions, is in the skill standard.

**Audit checkpoint:** Flag every external link, identifier and personal name in the artifact. A durable root the artifact's own workflow reads or writes passes. A link resolving to one artifact, a version number, a named individual, or a destination the artifact's workflow neither reads nor writes fails.

---

## Checkpoint markers

Two markers exist estate-wide: `⏸ HUMAN CHECKPOINT [Governance]` and `⏸ HUMAN CHECKPOINT [Token]`. The convention that defines them — what each means, and that both are hard stops — is owned by `session-discipline`. Use the markers as written; do not restate their meanings in any artifact, and do not define a marker of your own.

**Audit checkpoint:** Flag any stop-and-confirm point using a marker outside those two, any unlabeled checkpoint, and any artifact that restates what the markers mean rather than simply using them.
