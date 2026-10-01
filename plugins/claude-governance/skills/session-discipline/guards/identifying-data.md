# Identifying data | session-discipline

**Load when:** data that identifies a person enters the session — through a shared file, a paste or a tool result. Identifying data includes IP addresses, visitor or fingerprint IDs, and names or email addresses tied to a record, such as raw server logs, per-visit analytics exports and user lists.

---

## On arrival

Warn the contributor at once, naming the file or source and the identifying fields it holds.

⏸ HUMAN CHECKPOINT [Governance] — the contributor confirms they have the authority to share the raw data for this work. Until they do, work only from a de-identified extract: identifying fields removed, masked or aggregated.

## While it is in the session

- **Raw data is never committed, published, handed off or saved to memory.** Derived outputs — reports, findings, commit contents, handoffs — carry aggregates or masked values only.
- **Raw data sits in a gitignored location.** Before the next commit, confirm the ignore rule covers every raw file.

## When the work is finished

List every raw file the session used, with its location, for the contributor to delete.

---

## Behavioural rules

- Warn on arrival, naming the source and the identifying fields
- Work from a de-identified extract until the contributor confirms authority for the raw data
- Never commit, publish, hand off or memorise raw identifying data; derived outputs carry aggregates or masked values
- Keep raw data gitignored, and confirm the ignore rule before each commit
- Close the work by listing the raw files for deletion
