#!/usr/bin/env python3
"""
Compare a skill's declared version across up to three locations: the repo
source, an installed copy, and a packaged .skill zip.

Replaces a per-session prose Intake step (comparing versions by eye) with a
deterministic three-way check — the prose version competed for the same
attention budget that let a real drift go unnoticed (see the Version
management section of skill-standards.md).

Each location is read for a `**Version:**` line in SKILL.md's body (never
a `version:` frontmatter key — skill-standards.md forbids that). At least
one of --source/--installed/--packaged is required; only the ones given
are compared.

Usage:
    python3 check_version_drift.py --source <path> [--installed <path>] [--packaged <path-to-.skill>]

<path> for --source/--installed may be either a skill directory (containing
SKILL.md) or a direct path to a SKILL.md file. <path> for --packaged is a
.skill zip file.

Exit code 0: every given location's version agrees.
Exit code 1: at least two given locations disagree.
Exit code 2: a given location could not be read at all.
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

VERSION_RE = re.compile(r"^\*\*Version:\*\*\s*(\S+)", re.MULTILINE)


def _extract_version(text: str):
    m = VERSION_RE.search(text)
    return m.group(1) if m else None


def _read_skill_md_path(path_str: str) -> Path:
    p = Path(path_str)
    if p.is_dir():
        p = p / "SKILL.md"
    return p


def read_version_from_path(path_str: str):
    """Returns (version_or_None, error_or_None) for a directory or SKILL.md path."""
    p = _read_skill_md_path(path_str)
    if not p.exists():
        return None, f"{p} does not exist"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return None, f"could not read {p}: {e}"
    version = _extract_version(text)
    if version is None:
        return None, f"{p} has no '**Version:**' line in its body"
    return version, None


def read_version_from_zip(zip_path_str: str):
    """Returns (version_or_None, error_or_None) for a .skill zip file."""
    p = Path(zip_path_str)
    if not p.exists():
        return None, f"{p} does not exist"
    try:
        with zipfile.ZipFile(p) as zf:
            skill_md_names = [n for n in zf.namelist() if n.endswith("/SKILL.md") or n == "SKILL.md"]
            if not skill_md_names:
                return None, f"{p} contains no SKILL.md"
            # Prefer the shallowest match (top-level <skill-name>/SKILL.md).
            skill_md_names.sort(key=lambda n: n.count("/"))
            text = zf.read(skill_md_names[0]).decode("utf-8", errors="replace")
    except Exception as e:
        return None, f"could not read {p}: {e}"
    version = _extract_version(text)
    if version is None:
        return None, f"{p}'s SKILL.md has no '**Version:**' line in its body"
    return version, None


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", help="Path to the repo source skill directory or its SKILL.md")
    parser.add_argument("--installed", help="Path to the installed copy's skill directory or its SKILL.md")
    parser.add_argument("--packaged", help="Path to a packaged .skill zip file")
    args = parser.parse_args()

    if not (args.source or args.installed or args.packaged):
        print("ERROR: at least one of --source, --installed, --packaged is required", file=sys.stderr)
        sys.exit(2)

    results = {}
    had_read_error = False

    if args.source:
        version, err = read_version_from_path(args.source)
        results["source"] = version
        if err:
            print(f"ERROR reading source: {err}", file=sys.stderr)
            had_read_error = True

    if args.installed:
        version, err = read_version_from_path(args.installed)
        results["installed"] = version
        if err:
            print(f"ERROR reading installed: {err}", file=sys.stderr)
            had_read_error = True

    if args.packaged:
        version, err = read_version_from_zip(args.packaged)
        results["packaged"] = version
        if err:
            print(f"ERROR reading packaged: {err}", file=sys.stderr)
            had_read_error = True

    print("Version comparison:")
    for label, version in results.items():
        print(f"  {label}: {version if version is not None else '<unreadable>'}")

    if had_read_error:
        sys.exit(2)

    distinct_versions = {v for v in results.values() if v is not None}
    if len(distinct_versions) <= 1:
        print("Result: AGREE — all given locations report the same version.")
        sys.exit(0)
    else:
        print(
            "Result: DRIFT — given locations report different versions. "
            "Confirm which is current before shipping or distributing.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
