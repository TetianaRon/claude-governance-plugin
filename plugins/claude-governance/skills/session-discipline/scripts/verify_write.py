#!/usr/bin/env python3
"""
Consolidate the file-write integrity check in guards/file-integrity.md into
one call.

It takes the signals otherwise chained by hand -- a Python read, a
subprocess read via bash, and, if a git ref is given, the committed blob --
and reports them side by side, flagging disagreement automatically. It does
not bypass a stale mount cache: a Python read goes through the same
OS-level cache as bash's `cat`, so both can be stale together.

A DISAGREE result means the working-tree reads (python vs bash) do not
match -- one of them is stale. Check the file with the `Read` tool as the
tiebreak and proceed on what `Read` shows; escalate to the contributor only
if `Read` also shows the write missing or truncated.

AGREE is not an absolute guarantee. Where the whole sandbox's view of a
file is stale, both reads can see the same wrong content. The tell is a
working tree matching --git-ref exactly after an edit that should have
changed it; there, `Read` wins, and the recovery in guards/file-integrity.md
applies.

Usage:
    python3 verify_write.py <path> [--git-ref HEAD] [--tail-lines 5]

It also scans the whole file for stray control bytes, which a size and
tail check cannot see mid-file, and reports the count of CRLF line endings.

Exit code 0 if all available signals agree and the file holds no stray
control byte. Exit code 1 otherwise.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def read_via_python(path):
    data = path.read_bytes()
    return len(data), data


def read_via_bash(path):
    try:
        out = subprocess.run(
            ["cat", str(path)], capture_output=True, check=True
        )
        return len(out.stdout), out.stdout
    except Exception as e:
        return None, f"<bash read failed: {e}>".encode()


def read_via_git(path, git_ref):
    # git show needs a path relative to the repo root
    try:
        repo_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True, cwd=str(path.parent),
        ).stdout.strip()
        rel_path = path.resolve().relative_to(Path(repo_root).resolve()).as_posix()
        out = subprocess.run(
            ["git", "show", f"{git_ref}:{rel_path}"],
            capture_output=True, check=True, cwd=repo_root,
        )
        return len(out.stdout), out.stdout
    except Exception as e:
        return None, f"<git show failed: {e}>".encode()


# Bytes that never belong in a text file: C0 controls other than tab, LF and CR.
CONTROL_BYTES = set(range(0x00, 0x09)) | {0x0B, 0x0C} | set(range(0x0E, 0x20))


def control_byte_report(data):
    """Count stray control bytes and CRLF line endings anywhere in the file."""
    stray = [i for i, b in enumerate(data) if b in CONTROL_BYTES]
    return len(stray), stray[:5], data.count(b"\r\n")


def tail_text(data, n_lines):
    try:
        text = data.decode("utf-8", errors="replace")
    except Exception:
        return "<binary content>"
    lines = text.splitlines()
    return "\n".join(lines[-n_lines:])


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="File to check")
    parser.add_argument("--git-ref", help="Git ref to cross-check against (e.g. HEAD)")
    parser.add_argument("--tail-lines", type=int, default=5, help="Lines of tail to show (default 5)")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    py_size, py_data = read_via_python(path)
    bash_size, bash_data = read_via_bash(path)

    print(f"=== {path} ===")
    print(f"\n[python] size={py_size}")
    print(tail_text(py_data, args.tail_lines))
    print(f"\n[bash] size={bash_size}")
    print(tail_text(bash_data, args.tail_lines))

    # python vs bash is the real integrity check: both read the current
    # working-tree file right now, so any difference between them means
    # one of the two is stale -- a genuine disagreement, not an expected
    # outcome of anything.
    working_tree_agrees = (py_data == bash_data)

    stray_count, stray_at, crlf_count = control_byte_report(py_data)
    print(f"\n[control bytes] {stray_count}" + (f" at offsets {stray_at}" if stray_count else ""))
    print(f"[CRLF line endings] {crlf_count}")

    git_note = ""
    if args.git_ref:
        git_size, git_data = read_via_git(path, args.git_ref)
        print(f"\n[git:{args.git_ref}] size={git_size}")
        print(tail_text(git_data, args.tail_lines))
        if git_size is None:
            git_note = f"\n(git:{args.git_ref} unreadable -- see message above; not counted either way)"
        elif git_data == py_data:
            git_note = (
                f"\nNote: working tree matches git:{args.git_ref} exactly. "
                f"Expected if no edit was intended yet; a problem if you expected "
                f"this file to already differ from {args.git_ref}."
            )
        else:
            git_note = (
                f"\nNote: working tree differs from git:{args.git_ref} -- expected "
                f"after an edit, not itself a failure signal."
            )

    print(git_note)
    print()
    if stray_count:
        print(
            f"Result: CONTROL BYTES -- {stray_count} stray control byte(s) in the file. "
            "A write carried an escape through a string literal; rewrite the damaged "
            "lines and check again.",
            file=sys.stderr,
        )
        sys.exit(1)
    if working_tree_agrees:
        print("Result: AGREE -- python and bash reads of the working tree match.")
        sys.exit(0)
    else:
        print(
            "Result: DISAGREE -- python and bash reads of the working tree do not "
            "match. Check the file with the Read tool as the tiebreak (per "
            "guards/file-integrity.md); escalate to the contributor only if Read also "
            "shows the write missing or truncated.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
