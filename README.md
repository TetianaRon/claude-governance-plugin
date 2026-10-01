# claude-governance

Source of the `claude-governance` plugin: governance skills for Claude work, bundled with the subagent they dispatch. It keeps Claude sessions disciplined across projects — startup, plans, issue logs, documentation, commit messages — and holds the standards for building and auditing Claude projects, skills, subagents and plugins.

## Contents

| Artifact | Class | What it does |
|---|---|---|
| `session-discipline` | skill | Session startup, source loading, wrap-up and handoff discipline |
| `build-standards` | skill | The workflow and standards for building, improving and auditing projects, skills, subagents and plugins |
| `issue-logging` | skill | Logging issues to a local issues log and running its lifecycle |
| `plan-discipline` | skill | Creating and maintaining phased plan documents |
| `doc-formatting` | skill | Drafting and structuring user-facing documentation |
| `git-commit-message` | skill | Composing Git commit messages |
| `standards-auditor` | subagent | Auditing one target against supplied standards |

## Structure

```
claude-governance/
├── CLAUDE.md                  # Instructions for Claude sessions in this repo
├── .claude-plugin/
│   └── marketplace.json       # Local catalog for installing the plugin in Claude Code
├── plugins/
│   └── claude-governance/     # The plugin, edited here: manifest, README, skills/, agents/
├── dist/                      # Built .skill zips and the plugin archive
└── meta/                      # Working artifacts: plans, audits, drafts
```

## Installing

In a Claude Code session, add this repo as a local marketplace, then install the plugin:

```text
/plugin marketplace add <path-to-this-repo>
```

```text
/plugin install claude-governance@claude-governance-local
```

On claude.ai, upload `dist/claude-governance.zip`, or a single skill's `.skill` zip through Customize → Skills.

## Using it in a project

Add a startup block to the project's `CLAUDE.md`:

```markdown
## Session startup

Before acting on any task, invoke `session-discipline`, then `build-standards` where the work builds or improves Claude artifacts.

## Issues log

Identifier: XX
Log: `ISSUES.md`
```

## Working on it

Open a Claude Code session in this repo. `CLAUDE.md` runs the session startup and routes the work.
