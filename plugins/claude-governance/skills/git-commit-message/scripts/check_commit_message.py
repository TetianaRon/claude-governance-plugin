#!/usr/bin/env python3
"""
Check a drafted commit message against the mechanical rules in this skill's
SKILL.md. The imperative mood and the content of the body are not checked.

Errors:
- subject over 72 characters
- subject not starting with a capital letter
- subject ending in a period
- a body not separated from the subject by exactly one blank line
- a body line over 72 characters (a URL or a trailer line may run long)

Warnings:
- subject over 50 characters

Usage:
    python3 check_commit_message.py <message-file>

Exits non-zero on any error.
"""

import re
import sys
from pathlib import Path

TRAILER_RE = re.compile(r"^[A-Za-z-]+: \S")
URL_RE = re.compile(r"https?://\S+")


def check(message: str):
    errors, warnings = [], []
    lines = message.rstrip("\n").split("\n")
    subject = lines[0] if lines else ""
    if not subject.strip():
        return ["the subject line is empty"], warnings
    if len(subject) > 72:
        errors.append(f"subject is {len(subject)} characters; the ceiling is 72")
    elif len(subject) > 50:
        warnings.append(f"subject is {len(subject)} characters; the target is 50")
    if not subject[0].isupper():
        errors.append("subject does not start with a capital letter")
    if subject.rstrip().endswith("."):
        errors.append("subject ends in a period")
    if len(lines) > 1:
        if lines[1].strip():
            errors.append("line 2 is not blank; a body is separated from the subject by one blank line")
        elif len(lines) > 2 and not lines[2].strip():
            errors.append("more than one blank line between subject and body")
        for n, line in enumerate(lines[1:], start=2):
            if len(line) > 72 and not URL_RE.search(line) and not TRAILER_RE.match(line):
                errors.append(f"line {n} is {len(line)} characters; body lines wrap at 72")
    return errors, warnings


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print("Usage: python3 check_commit_message.py <message-file>")
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: {path} does not exist")
        sys.exit(1)
    errors, warnings = check(path.read_text(encoding="utf-8"))
    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if not errors:
        print("OK: the message passes the mechanical checks")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
