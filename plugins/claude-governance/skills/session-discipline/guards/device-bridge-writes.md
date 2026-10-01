# Device-bridge writes | session-discipline

**Load when:** about to make a multi-line edit or run a packaging or build script on a Windows-mounted path, about to re-stage a path with `device_stage_files`, or a large-content write has stalled once on a device-bridge surface.

---

## Multi-line edits

The Edit tool truncates file tails on multi-line edits on a Windows-mounted path. A multi-line change there is a whole-file write — a Python `open(..., 'w')` or a heredoc rewriting the complete file — checked afterwards under `guards/file-integrity.md`.

## Packaging and build scripts

A script reading files to build an artifact can embed stale bytes even when `Read` shows the source correct, most often after several rewrites of the same path in one session. After a packaging or build run, spot-check the artifact itself — each edited file's byte count and tail inside it — for every file edited in the session, not only the last.

**A file stuck stale.** Where `touch`, `rm` or further rewrites show no effect in bash-side reads, move the file aside (`mv <file> <file>.tmp`, which works where `rm` is refused) and have the write tool recreate it at the original path. Confirm the recovery with a bash-side read, and re-spot-check any packaged artifact.

**Discarded files leave the directory.** A packaging script bundles temporary and backup files it does not recognise as build artifacts. A file moved aside is moved out of the skill or output directory entirely, and the packaged artifact's file list is checked afterwards. Where deletion in a connected folder is blocked, request delete permission rather than leaving the file in place.

## Stalled large writes

A large-content call that stalls once is retried disk-based — the content staged as a file and passed by path — not in the same call shape. An explicit contributor stop is a signal to change the approach.

## Re-staging

`device_stage_files` on a path with uncommitted container-side edits overwrites them with the device copy, silently. Never re-stage such a path. Where a fresh mtime is needed — to retry `device_commit_files` after a stale-`expectedMtimeMs` rejection — first capture a durable handle to the edited content (a `SendUserFile` file handle), and retry from that handle, never by reapplying the edit from memory.

---

## Behavioural rules

- Never use the Edit tool for a multi-line change on a Windows-mounted path; write the whole file
- After a packaging or build run, spot-check every edited file inside the artifact
- Move a stuck-stale file aside and recreate it; move every discarded file out of the skill or output directory
- Retry a stalled large write disk-based, never in the same call shape
- Never call `device_stage_files` on a path with uncommitted container-side edits
