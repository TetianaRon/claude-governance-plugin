# claude-governance

Governance skills for Claude work, bundled as one plugin with the subagent they dispatch. The plugin carries no workflow content of its own. Each skill keeps its own version and can be built as a standalone `.skill` zip. Every member shares one issues log, except `git-commit-message`, which falls under the vendor-neutral exemption.

## Issues log

Identifier: GOV
Log: `ISSUES.md` at the root of the claude-governance plugin repo

## Bundle contents

| Artifact | Class | Location |
|---|---|---|
| `session-discipline` | skill | `skills/session-discipline/SKILL.md` |
| `issue-logging` | skill | `skills/issue-logging/SKILL.md` |
| `plan-discipline` | skill | `skills/plan-discipline/SKILL.md` |
| `doc-formatting` | skill | `skills/doc-formatting/SKILL.md` |
| `build-standards` | skill | `skills/build-standards/SKILL.md` |
| `git-commit-message` | skill | `skills/git-commit-message/SKILL.md` |
| `standards-auditor` | subagent | `agents/standards-auditor.md` |

Every member sits at its default location, so the manifest declares no component paths.

**Composition.** Every member serves one consumer set — governed Claude work in personal projects — and the members release together.
