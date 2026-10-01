---
name: issue-logging
description: >
  Logs issues to a declared issues log and runs that log's lifecycle: drafting a new
  entry, deriving its ID, and keeping each entry in its one current status until it is
  resolved and removed. Use when anyone says "log this", "log it as an issue", "add this
  to the issues log", "record this issue", "hold that for the log", or "resolve these
  entries", and whenever a workflow issue is noticed mid-session — incorrect output, a
  workflow gap, a redundant step, a routing failure, documentation drift, or a missing
  guardrail. Also covers redrafting a log after work lands, and issue logs outside
  Claude governance, such as a project's tracker of issues in its own subject matter.
---

# issue-logging

**Version:** v1.0

---

## Issues log

Identifier: GOV
Log: `ISSUES.md` at the root of the claude-governance plugin repo

---

## What a log is

An issues log is one document with one owner and one canonical location, reachable at one path or link. The rule attaches to the log, not to its owner: a skill or project may keep more than one log — one for issues with its own workflow, another for issues in the subject matter it works on — and each follows this skill separately.

This skill never names a real log. It resolves which log applies, where it lives, and what shape it takes from the declaration of the skill or project in context.

---

## Finding the log and its declaration

Read the "Issues log" section of the entry-point file of the skill or project the issue belongs to. It gives the identifier and the log's location: a file path or a direct link. Where no location is declared, ask the contributor for one and record it in that section. Read the document itself with whatever tool fits its type, and only when an entry is about to be drafted or resolved — never speculatively.

**Before drafting, look for the finding already logged.** Scan the log for an open entry on the same artifact and the same defect. Where the finding could belong to more than one log, scan each of them. A match is cited, or updated by redraft, and never drafted a second time.

The declaration may also state how the log differs from the default profile below: its medium, its write path, its section model, or its ID scheme. Follow the declaration for every parameter it states. For every parameter it leaves unstated, the default profile applies.

---

## Lifecycle — every log

These hold whatever the log's declared shape:

- **One issue, one entry, one current status.** An entry is never shown in two places at once.
- **Entries move between status groupings.** A move relocates the entry; it never copies it.
- **A resolved entry leaves the open set.** It is removed or relocated as the log's model states, never left in place marked done.
- **Structure survives every rewrite.** An entry's fields stay on their own lines, and the section structure survives any redraft, not only the content.

**The logging prompt.** On any noticed issue — including one the contributor raises first — present a structured choice, not inline text:

```
Question: "Issue noticed: [one-line description]. Log it now or hold for later?"
Options:
- Log now — draft the entry and hand it over immediately
- Hold for later — note it and revisit at the next phase end
```

**At each phase end**, not only at session end, prompt to record any issue still held. **At session close**, draft an entry for anything noticed but not yet drafted — never leave a noticed issue undrafted.

---

## Default profile

Applies to every parameter the declaration leaves unstated.

**Medium and write path.** A markdown file at the declared path, which Claude edits directly. A declared file that does not exist is created with the log's first entry. Where the declared log is a page Claude cannot write, Claude hands the contributor the content to paste, together with the log's link. Entries live in the document body, never as a comment.

**Sections.** `## To Do`, `## Deferred` and `## Blocked`, each an H2, separated by a horizontal rule. Include only the sections that currently hold entries.

- **New issue.** Always an append to the end of `## To Do` — never a full redraft.
- **Being worked.** An entry stays in `## To Do` while it is worked. Section membership does not carry "being worked"; the active plan's issue coverage map is the sole authority for that.
- **Resolved.** An entry is resolved once the fix is released — the version carrying it is packaged, distributed and tagged — not when the fix lands in source. Resolved entries are removed outright, in one redraft per cycle.
- **Deferred.** An issue surfaced but intentionally left out of the current plan moves to `## Deferred`, by redraft.
- **Blocked.** An issue stuck on something outside Claude's or the contributor's control moves to `## Blocked`, by redraft, noting what it waits on.

**Entry format.** Every entry uses a stable identifier and a structured header from the log's very first entry:

```
## To Do

### [XX-0NN] — One-line description
Type: GAP | BUG | [other type] | Severity: Low | Medium | High | Observed: YYYY-MM-DD

Description: ...
Suggested fix: ...
```

`XX` is the identifier from the declaration. `0NN` is a zero-padded, strictly incrementing sequence number, never reused or renumbered, even after an entry is removed.

**Determining the next ID.** Take one more than the highest `XX-0NN` appearing anywhere in the document, in whatever form it appears — an open entry, a reference in a resolution note, or any other mention — or allocated on the same log but not yet written to it: in the active plan, or in an entry drafted this session. If none appears anywhere, this is the log's first entry: start at `001`. Run the script on the log file — or, for a log that is not a local file, on a scratch copy of its text — together with every other record allocating IDs on the same log:

```
python3 <skill-dir>/scripts/next_issue_id.py <prefix> <doc-text-file> [<plan-or-draft-file> ...]
```

`<skill-dir>` is the directory reported when this skill loaded. The script prints the next ID and an entry skeleton in the format above. Never scan by hand.

**Resolution notes.** A log may carry narrative notes summarising what a batch of resolved entries fixed. Keep the current cycle's note in full. Collapse every older note to a one-line pointer at the durable record for its own cycle, rather than re-narrating it.

---

## Behavioural rules

- Resolve the log, its location and its shape from the declaration in context — never from memory, and never by naming a real log in this skill
- Follow the declaration for every parameter it states; apply the default profile only to what it leaves unstated
- A new entry is an append to the open section — never a full redraft
- Scan every log the finding could belong to for an existing entry before drafting a new one
- Derive the next ID with the script, from the highest number anywhere in the document or allocated in the plan or a pending draft
- Keep every entry's fields on separate lines and every section header intact through any redraft
- Prompt for held issues at each phase end, and draft every noticed issue before the session closes
