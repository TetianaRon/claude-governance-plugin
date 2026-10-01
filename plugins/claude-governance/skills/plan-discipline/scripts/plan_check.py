#!/usr/bin/env python3
"""
Check a plan document's structure and currency against this skill's SKILL.md
and references/plan-format.md.

Checks:
- the header carries **Created:**, **Status:** and **Session context:** lines
- the required sections appear, as `## ` headings, in the order plan-format.md
  states (Issue coverage map is optional; a plan may add sections between them)
- `## Session Worklog` is the last section, and its entries are chronological:
  session numbers strictly increasing, dates never decreasing
- every phase heading under `## Improvement Roadmap` carries exactly one status
  marker (⏳, 🔄, or ✅ followed by a YYYY-MM-DD date)
- no phase is 🔄 while a later phase is ✅
- a Status line naming "Phase N complete" matches a ✅ Phase N heading
- every ⏸ marker is `⏸ HUMAN CHECKPOINT [Governance]` or `⏸ HUMAN CHECKPOINT [Token]`

Usage:
    python3 plan_check.py <plan-file>

Prints one line per problem and exits non-zero if any is found.
"""

import re
import sys
from pathlib import Path

REQUIRED = [
    "North Star",
    "Current State",
    "Gap Analysis",
    "Improvement Roadmap",
    "Drafts Inventory",
    "Deferred Items",
    "Session Worklog",
]
OPTIONAL_AFTER = {"Issue coverage map": "Gap Analysis"}
HEADER_KEYS = ("**Created:**", "**Status:**", "**Session context:**")
MARKERS = ("⏳", "🔄", "✅")
CHECKPOINT_RE = re.compile(r"⏸(?! HUMAN CHECKPOINT \[(?:Governance|Token)\])")
SESSION_RE = re.compile(r"^### Session (\d+) — (\d{4}-\d{2}-\d{2})\s*$")
PHASE_RE = re.compile(r"^### (Phase (\d+)\b.*)$")


def check(text: str) -> list:
    problems = []
    lines = text.splitlines()

    for key in HEADER_KEYS:
        if not any(line.startswith(key) for line in lines[:12]):
            problems.append(f"header: no {key} line near the top")

    h2 = [(i, line[3:].strip()) for i, line in enumerate(lines) if line.startswith("## ")]
    titles = [t for _, t in h2]

    positions = []
    for name in REQUIRED:
        found = [k for k, t in enumerate(titles) if t.lower().startswith(name.lower())]
        if not found:
            problems.append(f"sections: no '## {name}' section")
        else:
            positions.append((found[0], name))
    ordered = [name for _, name in sorted(positions)]
    expected = [name for name in REQUIRED if name in ordered]
    if ordered != expected:
        problems.append(f"sections: required sections out of order: {ordered}")
    for name, after in OPTIONAL_AFTER.items():
        opt = [k for k, t in enumerate(titles) if t.lower().startswith(name.lower())]
        prev = [k for k, t in enumerate(titles) if t.lower().startswith(after.lower())]
        if opt and prev and opt[0] < prev[0]:
            problems.append(f"sections: '## {name}' sits before '## {after}'")
    if titles and not titles[-1].lower().startswith("session worklog"):
        problems.append(f"worklog: '## Session Worklog' is not the last section (last is '## {titles[-1]}')")

    def section(name):
        for k, (i, t) in enumerate(h2):
            if t.lower().startswith(name.lower()):
                end = h2[k + 1][0] if k + 1 < len(h2) else len(lines)
                return lines[i + 1:end]
        return []

    entries = []
    for line in section("Session Worklog"):
        if line.startswith("### "):
            m = SESSION_RE.match(line)
            if not m:
                problems.append(f"worklog: entry heading not in '### Session N — YYYY-MM-DD' form: {line}")
            else:
                entries.append((int(m.group(1)), m.group(2)))
    for (n1, d1), (n2, d2) in zip(entries, entries[1:]):
        if n2 <= n1:
            problems.append(f"worklog: Session {n2} sits below Session {n1}; entries are not oldest first")
        if d2 < d1:
            problems.append(f"worklog: Session {n2} ({d2}) is dated before Session {n1} ({d1}) above it")

    phases = []
    for line in section("Improvement Roadmap"):
        m = PHASE_RE.match(line)
        if not m:
            continue
        title, number = m.group(1), int(m.group(2))
        found = [mk for mk in MARKERS if mk in title]
        if len(found) != 1:
            problems.append(f"roadmap: '{title}' carries {len(found)} status markers, not one")
            continue
        status = found[0]
        if status == "✅" and not re.search(r"✅ complete \d{4}-\d{2}-\d{2}", title):
            problems.append(f"roadmap: '{title}' is ✅ without 'complete YYYY-MM-DD'")
        phases.append((number, status, title))
    for k, (number, status, title) in enumerate(phases):
        if status == "🔄" and any(s == "✅" for _, s, _ in phases[k + 1:]):
            problems.append(f"roadmap: Phase {number} is 🔄 while a later phase is ✅")

    status_line = next((line for line in lines[:12] if line.startswith("**Status:**")), "")
    m = re.search(r"Phase (\d+) complete", status_line)
    if m:
        n = int(m.group(1))
        if not any(num == n and s == "✅" for num, s, _ in phases):
            problems.append(f"header: Status names Phase {n} complete, but its heading is not ✅")

    for i, line in enumerate(lines, 1):
        if CHECKPOINT_RE.search(line):
            problems.append(f"line {i}: a ⏸ marker other than the two checkpoint markers")

    return problems


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print("Usage: python3 plan_check.py <plan-file>")
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: {path} does not exist")
        sys.exit(1)
    problems = check(path.read_text(encoding="utf-8"))
    for p in problems:
        print(f"PROBLEM: {p}")
    if not problems:
        print(f"OK: {path.name} passes every check")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
