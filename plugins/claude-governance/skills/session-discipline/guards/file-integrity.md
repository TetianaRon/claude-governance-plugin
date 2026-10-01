# File integrity | session-discipline

**Load when:** a write lands on a device-bridge or otherwise mounted path, a write goes through an MCP write tool, or a multi-line edit changes a file that will ship. Writes to the session's own scratch space are exempt.

---

## Checking a write

Check the written file before the next edit. Where the shell that ran the write can reach this skill's directory, run:

```
python3 <skill-dir>/scripts/verify_write.py <path> --git-ref HEAD
```

`<skill-dir>` is the directory reported when this skill loaded; a bare relative path to the script resolves against the working directory and fails. The script compares a Python read and a bash read of the file, scans the whole file for stray control bytes, counts CRLF line endings, and, with `--git-ref`, reads the committed copy. It exits non-zero when the reads disagree or a stray control byte is present.

Where the script cannot run, check by hand: `wc -c <file>`, `tail -c 200 <file> | cat -A`, and `grep -c $'[\x01-\x08]' <file>`, which returns 0 on a clean file. A count of 0 exits non-zero, so the scan is never chained with `&&`. Check line endings with a Python read, since `grep` on Git Bash does not match a carriage return.

Confirm the size is plausible, the tail is intact with no NUL padding, and no stray control byte is present. On a file holding non-ASCII text, a character count below the byte count is multi-byte encoding, not truncation.

## A disagreement

**`Read` is the tiebreak.** On a Windows-mounted surface the bash-side read can be stale: it can report a file unchanged after a write that landed, or show no effect from a rewrite. Where a bash-side read and `Read` disagree, proceed on what `Read` shows.

**A working tree matching the committed copy right after an edit that should have changed it** means both reads are stale together. Proceed on `Read`.

⏸ HUMAN CHECKPOINT [Governance] — where `Read` also shows the write missing or truncated, restore the file from its source, or pause and ask the contributor to confirm its state. The next edit waits until the write's integrity is resolved.

## MCP tool writes

Read back the written content immediately after the call and confirm its last lines match what was sent. A mismatch or missing content is a truncated write.

## Copying onto a possibly-synced path

A copy from the session's uploads onto a path that may be the same underlying file, or auto-synced or hard-linked to it, can zero out the source even when the copy reports success. Leave platform-synced files where they are. Where a copy to a new location is needed, confirm the source is intact afterwards with an independent check; the copy command's exit code is not that check.

## Mounted paths

The mounted-write method and packaging staleness are in `guards/device-bridge-writes.md`, loaded on its own trigger.

---

## Behavioural rules

- Check every write this guard covers before the next edit, with `verify_write.py` where it can run
- On a bash-side vs `Read` disagreement, proceed on `Read`; stop only when `Read` also shows the write missing or truncated
- Read back an MCP write's tail immediately
- Never copy onto a path that may be the same underlying file or synced to it; confirm the source afterwards on any other copy
