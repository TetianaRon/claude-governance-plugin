---
name: doc-formatting
description: >
  Drafts, updates, restructures and retires user-facing documentation — READMEs,
  guides, how-tos, changelogs, and docs-site or wiki pages — scaled to the size of the
  change and structured for the reader. Use when asked to "write the README", "document
  this", "update the docs", "draft a guide", "add this to the page", "rewrite the page",
  "restructure this page", or "archive the page", and whenever a session is about to
  write or change documentation mid-workflow, including a docs update prompted by work
  that just landed. Not for instructions written for Claude (skills, CLAUDE.md), commit
  messages, or code comments.
---

# doc-formatting

**Version:** v1.0

---

## Issues log

Identifier: GOV
Log: `ISSUES.md` at the root of the claude-governance plugin repo

---

## Scale the edit

- A localized change — a sentence, a paragraph, one table row, one section — is drafted as just that piece, with exactly where it goes: which heading or section, and its position relative to the surrounding content.
- A new page, a full rewrite, or a restructure touching several scattered sections is drafted as the complete page.

## Know the destination

- **A file in the working repo** is edited directly.
- **A page in another tool** — a wiki, a notes app, a docs site without a repo — is a paste-ready draft handed to the contributor together with the page's link, or its intended parent's link for a new page. Where the session holds a write tool for that destination, propose writing directly, and proceed only once the contributor approves.

Draft in GitHub-flavoured markdown unless the destination calls for another format.

## Paste-safe markdown

Applies to every draft the contributor pastes into another tool.

- **Blank lines between blocks.** Every paragraph and every labeled element is separated from the next by a blank line. Adjacent lines paste as one paragraph.
- **Table separator row.** A markdown table carries its `|---|` separator row directly after the header row.
- **Inline code on text that must not link.** A domain, hostname or URL that must stay plain text is wrapped in inline code.
- **No inline code on a line carrying a link.** A name on the same line as a link is set in bold.

## Structure for the reader

- **Open with what it is and who it is for**, in one or two sentences, before any detail.
- **One `#` title, then `##` sections named for the reader's tasks** — "Install", "Configure", "Troubleshoot" — rather than for the system's internals.
- **Steps are a numbered list**, one action per step, in the order the reader performs them.
- **Commands and code sit in fenced code blocks** with a language tag, one command per block where the reader runs them one at a time.
- **A short example** follows any rule or option a reader could misapply.
- **Unrelated sections are separated** by a horizontal rule (`---`).

## Tables

- A table carries a set of comparable items. A single argument, or a sequence of steps, is prose or a list.
- Columns carry comparably sized content. A column whose content is short relative to the others — an owner, a date, a one-word status — is folded into the adjacent cell.
- A cell holds one line. Where several elements must stack in one cell and the destination renders markdown tables, the table is HTML with `<br>` between the elements.

## Status indicators

An inline code span for the status word, optionally preceded by a coloured circle emoji: 🟢 `DONE`, 🟡 `IN PROGRESS`, 🔴 `BLOCKED`.

## Voice

- Plain language, second person, present tense.
- Documentation states how things work now. Change history belongs in a changelog.
- A term the reader may not know is defined on first use.
- A documentation page named in the text carries a link on its first mention.

## Retiring a page

A page being removed is deleted or archived, and every inbound link found in the repo is updated or redirected. For a page in another tool, remind the contributor to remove or archive it there, and list the inbound links found.

---

## Behavioural rules

- Scale the draft to the edit: a localized change is just that piece plus where it goes; a new page, full rewrite or multi-section restructure is the complete page
- Edit repo files directly; hand a paste-ready draft and the link for a page in another tool, writing directly there only on the contributor's approval
- Every pasted draft is paste-safe
- Open with what the page is and who it is for; name sections for the reader's tasks; number steps; fence commands with a language tag
- Use a table only for comparable items, with comparably sized columns and one line per cell
- Document how things work now, and keep change history in a changelog
- On retirement, update or redirect every inbound link
