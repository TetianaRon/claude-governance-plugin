# PLUGIN-BUILD
# Design - Plugin Build | build-standards

**Purpose:** Design a new plugin. The output is a plugin directory holding its manifest, its README and every member, an archive of that directory, and a passed live test, ready for release.

A plugin is a bundle with no workflow content of its own. Every workflow question in this mode is a question about a member, answered in that member's own Design mode.

---

## Phase 1 — Intent capture

If the current conversation already names the artifacts the contributor wants to ship together, extract them from the history before asking anything.

Otherwise, open with a single question:

> "Which skills or subagents should ship together, and who installs them?"

From the answer, confirm before moving on:
- Every intended member, by name and class
- The contributors who install it, and the accounts and surfaces they use
- How often each member changes

---

## Phase 2 — Members and composition

Load references/plugin-standards.md and references/common-standards.md.

**Each member is asked on its own.** A plugin is never adopted, and whether an existing artifact already serves a workflow is asked of each member, never of the bundle. A member that does not yet exist is built first in its own Design mode, which runs that class's catalogue search. For a candidate that is a delegable step, ask first whether it needs a definition at all, under Ad-hoc dispatch in references/subagent-standards.md. A member that exists is an artifact of a governed class with a standards file. Anything else cannot be bundled.

**Composition.** Apply Bundle composition in references/plugin-standards.md to the member list: name the one consumer set and the one change cadence the members share. Present any member outside either, with the choice it forces:

```
Question: "[member] sits outside the shared [consumer set / cadence]. How should it travel?"
Options:
- Keep it in this bundle
- Separate plugin, with a dependency declared
- Leave it out and ship it standalone
```

---

## Improving an existing plugin

Reached from Improve's Phase 3 or a targeted adjustment. Phase 1 and Naming belong to a new build and are not run. Rerun Phase 2's composition check where a member is added or removed. Where a member's editable source sits outside the plugin directory, move it in, as "Write the plugin directory" states, before the build. Update the manifest and README for the change, then run Phase 4's build and verify, Phase 5's live test, and Phase 6.

---

## Phase 3 — Name, manifest and README

### Naming

Derive the bundle name under the naming convention in references/common-standards.md, naming what the bundle carries. Present it and confirm before writing anything:

```
Question: "I'll name this plugin [name]. Does that work?"
Options:
- Yes, that works
- I'd prefer a different name — I'll type it in chat
```

Parse every member's name for estate-wide uniqueness against the full roster, not against the bundle alone.

### Write the plugin directory

Create the plugin directory at the repo's plugin source location, which the repo's own project instructions declare. The directory is the plugin, and the one source of every member: each skill at `skills/<name>/`, each subagent at `agents/<name>.md`. Every member's standalone release is built from its place in the directory. A member whose source sits elsewhere in the repo is moved in with its history kept.

- **`.claude-plugin/plugin.json`**: `name`, `version` (`1.0.0` for a first release), `description` in one line, and `author`. It carries no component key.
- **`README.md`**: the bundle's purpose in one paragraph, its `## Issues log` declaration, a `## Bundle contents` table naming every member with its class and its location in the bundle, and a `## Distribution` section only where the plugin reaches a surface by a route beyond its archive.

A plugin takes an issues log of its own, holding bundle-level entries only. Ask the contributor for the log's location and identifier, and record them in the README.

Present both files and confirm:

```
Question: "How do the manifest and README look?"
Options:
- Good — let's build it
- I want to adjust the members or composition
- Several parts need changes
```

---

## Phase 4 — Build and verify

Build the archive with the bundled script, straight into the repo's plugin distribution location:

```bash
python3 <skill-dir>/scripts/package_plugin.py <plugin-dir> <output-directory>
```

The script validates the plugin directory and archives it unchanged. It refuses on a missing manifest key or issues-log declaration, on a plugin-root entry other than `.claude-plugin/`, `README.md`, `skills/` and `agents/`, on any difference between the README's Bundle contents table and the members present, on a member failing its own validation, and on any member text using the plugin-root path variable. Fix every refusal before continuing.

Then confirm, against references/plugin-standards.md:
- the archive's content is the plugin directory unchanged
- every member's standalone release is built from its place in the plugin directory
- no member reaches into a sibling's directory by path

---

## Phase 5 — Live test ⏸ HUMAN CHECKPOINT [Token]

The contributor installs the archive and opens a fresh session once the plugin shows as enabled. The test runs in that new session.

In that session, confirm every member appears, and invoke each one once. Record the names as the surface presents them: a surface may present a bundled member under a form composed with the bundle's name.

The contributor reports the result before Claude continues.

---

## Phase 6 — Output

**Commit and tag — ⏸ HUMAN CHECKPOINT [Governance].** The archive is a candidate until the contributor confirms it. Once confirmed, commit it with its source in one commit, then tag it `[plugin-name]/v[X.Y.Z]` on that commit.

**Distribution.** Run `workflows/distribution.md`.

**Every later change.** The distribution revision bumps on any change to any member, and each member keeps its own content revision.

---

## Behavioural rules

- Always load plugin-standards.md and common-standards.md at Phase 2 — never lay out a bundle from memory of the standard
- Never bundle an artifact that is not of a governed class with a standards file
- Never put workflow content in the plugin itself; it belongs in a member
- Never tag a plugin before its confirmed archive is committed
