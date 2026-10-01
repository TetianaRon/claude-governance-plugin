# PLUGIN-STANDARDS
# build-standards

Authoritative reference for how governed plugins are structured and maintained. Load it when building, auditing, or refining a plugin — never at session startup. Load `common-standards.md` alongside it: this file states only what is specific to plugins.

---

## What a plugin is

A plugin is a bundle and nothing else. It carries no workflow content of its own. Its content is the governed artifacts it bundles, each of which remains subject to its own class standard.

Whether an existing artifact already serves a workflow is asked of each member and never of the bundle. An existing plugin is not adopted; its members are, each under its own class standard.

### Bundle payload

The platform accepts a wide payload: skills, subagents, commands, workflows, output styles, hooks, MCP servers, LSP servers, themes, monitors, channels, plugin dependencies, and user configuration. A governed plugin bundles only artifacts of governed classes, certified under their class standards. A payload of any other kind in a bundle is an audit gap.

Plugin dependencies are a bundle mechanic rather than payload, and are governed by this file.

**Audit checkpoint:** Enumerate every component the bundle carries, including those present by default discovery rather than by manifest declaration. Every entry resolves to an artifact of a governed class with a standards file covering it. Flag every entry that does not. Flag any plugin recorded as adopted, and any member whose adoption status is taken from the bundle's rather than assessed on its own.

---

## Bundle layout

A plugin is a directory, and a governed plugin directory holds one layout:

```
<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── skills/
│   └── <skill-name>/
│       └── SKILL.md
└── agents/
    └── <subagent-name>.md
```

- `.claude-plugin/` holds the manifest, and a catalog file only where the directory is also a catalog's root.
- Each skill is a directory under `skills/`, laid out as its class standard requires.
- Each subagent is one definition file under `agents/`, named for the subagent.
- The root holds nothing else. A directory for a class the bundle has no member of is absent.

Every component sits where the platform finds it without declaration, so the manifest carries no component key.

The plugin directory is the editable source of every member, and the one source the archive and each member's standalone release are built from. No built artifact is an input to another.

An archive of the directory is the plugin's installable form rather than a separate kind of plugin. `.zip` and `.plugin` are both accepted, and the archive's content is the directory unchanged.

**Audit checkpoint:** Confirm the plugin directory holds the layout above and nothing else at its root, that every skill's `SKILL.md` sits where its class standard places it, and that every subagent is one definition file under `agents/`. Confirm `.claude-plugin/` holds manifest and catalog metadata only. Compare any published archive against the directory and flag every difference. Flag every member whose editable source sits outside the plugin directory, every member copied in at build time, and any standalone release built from anywhere but the member's place in the directory.

---

## Manifest

A plugin's manifest is `.claude-plugin/plugin.json`. The platform requires no manifest at all: with none present, components are discovered at their default locations and the bundle takes its name from its directory.

A governed plugin carries a manifest, and that manifest carries more than the one key the platform requires:

- `name` — required by the platform. Names the bundle under the naming convention in `common-standards.md`.
- `version` — the distribution revision: the bundle's own version, bumped on any change to any member. It belongs to the bundle, and replaces no member's content revision, which is under version management in `common-standards.md`.
- `description` — what the bundle carries, in one line.
- `author` — the plugin's owner.

A governed manifest carries no component key.

A manifest carrying only `name` is an audit gap.

Where no explicit version is stated, the consuming surface derives one. A bundle relying on a derived version has no distribution revision, and is an audit gap.

**Audit checkpoint:** Confirm the manifest exists at `.claude-plugin/plugin.json` and states `name`, `version`, `description` and `author`. Confirm the manifest carries no component key. Confirm the version is explicit rather than derived, and that every member still carries its own content revision.

---

## Naming and identity

A plugin's name is its manifest `name`, which matches the plugin directory's name, under the naming convention in `common-standards.md`.

**A bundle is not a namespace the estate can rely on.** How a consuming surface presents a bundled artifact's name varies by component type — on one surface a bundled skill is presented flat and a bundled subagent under a form composed with the bundle's name. The bundle adds nothing to a member's name for the uniqueness rule in `common-standards.md`.

**Audit checkpoint:** Confirm the manifest name matches the plugin directory's name.

**Judgment call:** whether a consuming surface composes a bundled artifact's name with the bundle's is read from that surface's own behaviour rather than from any file in the estate, and is confirmed with the contributor.

---

## Bundle composition

Co-bundling is one of two ways a set of artifacts travels together. A plugin may instead declare `dependencies` on other plugins, so that installing one reaches the others without merging them into a single bundle.

The two differ in what they fix:

- **Co-bundling** gives one distribution revision, one install act, and one enable-and-disable control for the whole set.
- **Dependency** leaves each bundle its own distribution revision and control, and states a required relationship between them.

Artifacts sharing a consumer set and a change cadence co-bundle. Artifacts one of which requires another, on different cadences or with different consumer sets, stand as separate plugins with a dependency declared.

Three properties fix the boundary:

- **Adoption set.** Installing a bundle installs every member. A member outside the shared consumer set is carried by consumers who want none of it.
- **Change cadence.** The bundle's distribution revision tracks every member. Members on very different cadences leave that revision saying little about any of them.
- **Context cost.** Every installed plugin adds tokens to every turn of every session it is enabled in, and the install surface states the amount. A member a consumer never uses is a cost that consumer pays on each turn.

**Audit checkpoint:** For every plugin, name the one consumer set and the one change cadence its members share. Flag every member outside either. For every declared dependency, name what the depending plugin needs from the other, and confirm the two differ in consumer set or change cadence.

**Judgment call:** a bundle's consumer set rests on the contributor population, and its members' change cadence on their release history; neither is in the bundle's files, and both are confirmed with the contributor.

---

## Members do not share content

Co-bundling grants no sharing permission. Two artifacts in one bundle stand in exactly the relationship they would stand in as separate artifacts: the content-coupling rule in each one's class standard holds unchanged, and a path-substitution mechanism the bundle makes available is not a sanctioned route around it.

A member names another member only under the referral constraints its own class standard states. A dependency between plugins is a distribution relationship and grants no content-sharing permission either.

**Audit checkpoint:** Scan every member for a path resolving into a sibling member's directory. Any such path is content coupling, whatever mechanism resolves it. Separately, for every reference a member makes to a sibling, test it against the referral constraints in the referring member's own class standard and flag every breach, whether or not a path is involved.

---

## Issues log declaration

`common-standards.md` states where a plugin's declaration sits and in what form.

A plugin's issues log holds bundle-level entries only: manifest, layout, composition and dependency. An entry about a member's own content belongs to that member's log.

**Audit checkpoint:** Flag any entry in the plugin's log that is about a member's content.

---

## Shared rules

Naming, version management, editing workflow, repository setup, distribution, instruction cleanliness, external references and checkpoint markers are the same for every governed artifact and are stated in `common-standards.md`, which also records the plugin-specific deltas. None of them is restated here. The naming rule covering a bundle's identity is stated above.
