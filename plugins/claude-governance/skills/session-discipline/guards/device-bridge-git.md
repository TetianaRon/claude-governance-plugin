# Device-bridge git | session-discipline

**Load when:** about to run a git write (`add`, `commit`, `tag`) against a device-bridge mounted repo, or about to rely on sandbox `git status`, `git log` or `git diff` output from one.

---

## Locks and stuck commits

A git write run through `device_bash` on a device-bridge repo can leave `.git/index.lock` or `.git/HEAD.lock` behind after it succeeds, and the next write then fails with "File exists". A `git commit` can also hang past the tool's timeout behind a lock it created itself, leaving HEAD unchanged and a fresh 0-byte `.git/index.lock`. Accumulated `.git/objects/tmp_obj_*` files refusing unlink block a commit the same way. A refused `rm -f` on a lock means a host-side process holds it.

Before a git write through `device_bash`, check for `.git/index.lock` and `.git/HEAD.lock`. Where one is found, a write fails with "File exists", a commit times out, or tmp objects block it:

⏸ HUMAN CHECKPOINT [Token] — hand the contributor copy-paste commands to run locally: delete the lock (`del .git\index.lock` / `rm .git/index.lock`), then the `git add`, `git commit`, `git push` and `git tag` commands themselves. For a multi-line commit message, give the exact message text to save as a local message file and commit with `git commit -F <message-file>`, which works in cmd, PowerShell and Git Bash alike. Do not retry the sandbox's own `rm` or git commands against the same lock.

Once the contributor confirms the commit, verify it with `git log -1` before recording its hash in any plan or tracking document.

## Reading git state

Sandbox `git status`, `git log` and `git diff` on a device-bridge repo are not reliably current: an already-committed file can show as modified, and an edited file as unchanged. Use them only to draft candidate commands for the contributor. Where the contributor reports a different state, theirs is authoritative.

- **A surprising diff** is cross-checked with `python3 <skill-dir>/scripts/verify_write.py <path> --git-ref HEAD`, whose git read comes from the object database, before it is treated as staleness. A real diff is a normal result.
- **"Not a git repository … Stopping at filesystem boundary"** can mean the mount is scoped below the real repo root. Say the sandbox sees only the mounted folder, and ask the contributor whether a parent directory is the repo root.
- **Before drafting a commit or tag handoff**, ask the contributor to run `git log --oneline -- <changed-paths>` and share the result, so no commit is proposed for a change already committed.
- **`git status` runs alone**, with an explicit timeout, never batched with other commands. `git diff --stat` answers "which files changed" and is fast.

---

## Behavioural rules

- Check for a lock before every git write through `device_bash`; on a lock, a "File exists" failure, a timed-out commit or tmp-object buildup, hand the commands to the contributor
- Treat sandbox git output as a draft signal, never as fact to report; cross-check a surprising diff with `verify_write.py --git-ref`
- Have the contributor share `git log --oneline -- <changed-paths>` before drafting a commit or tag handoff
- Run `git status` alone with an explicit timeout
