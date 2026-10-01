#!/usr/bin/env python3
"""
Determine the next issues-log entry ID and print an entry
skeleton, per this skill's SKILL.md, "Default profile".

Implements the algorithm stated there: scan every file given for every
<PREFIX>-0NN it contains, in whatever form it appears, and use one more
than the highest number found; if none appear anywhere, start at 001.

Usage:
    python3 next_issue_id.py <prefix> <file> [<file> ...] [--summary "..."] \\
        [--type GAP|BUG|...] [--severity Low|Medium|High] [--observed YYYY-MM-DD]

The first <file> is the issues log itself, or a scratch copy of its text
where the log is not a local file; this script fetches nothing.
Further files are any other record allocating IDs on the same log: the
active plan, or a scratch file of entries drafted but not yet written to the log.
<prefix> is the log's short identifier (e.g. XX).

Prints the next ID on its own line, then a blank line, then the H3 entry
skeleton with Type/Severity/Observed on one line and Description/Suggested
fix on their own separate lines, matching the required structure exactly.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path


def next_id(prefix: str, text: str) -> str:
    pattern = re.compile(r"\b" + re.escape(prefix) + r"-(\d+)\b")
    matches = pattern.findall(text)
    if not matches:
        return f"{prefix}-001"
    width = max(3, max(len(m) for m in matches))
    highest = max(int(m) for m in matches)
    return f"{prefix}-{highest + 1:0{width}d}"


def build_entry(entry_id: str, summary: str, type_: str, severity: str, observed: str) -> str:
    observed = observed or datetime.date.today().isoformat()
    return (
        f"### [{entry_id}] — {summary}\n"
        f"Type: {type_} | Severity: {severity} | Observed: {observed}\n"
        f"\n"
        f"Description: \n"
        f"Suggested fix: \n"
    )


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prefix", help="The log's short identifier, e.g. XX")
    parser.add_argument("doc_paths", nargs="+",
                        help="The log document's text first, then any plan or pending-draft file")
    parser.add_argument("--summary", default="<one-line description>")
    parser.add_argument("--type", default="GAP")
    parser.add_argument("--severity", default="Medium")
    parser.add_argument("--observed", default=None, help="YYYY-MM-DD; defaults to today")
    args = parser.parse_args()

    texts = []
    for doc in args.doc_paths:
        p = Path(doc)
        if not p.exists():
            print(f"ERROR: {p} does not exist", file=sys.stderr)
            sys.exit(1)
        texts.append(p.read_text(encoding="utf-8", errors="replace"))
    entry_id = next_id(args.prefix, "\n".join(texts))

    print(f"Next ID: {entry_id}\n")
    print(build_entry(entry_id, args.summary, args.type, args.severity, args.observed))


if __name__ == "__main__":
    main()
