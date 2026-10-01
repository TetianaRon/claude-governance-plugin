#!/usr/bin/env python3
"""
Package a governed skill directory into a distributable .skill file.

Ported from Anthropic's skill-creator package_skill.py, adapted to this plugin's
own zip-naming rule and validation script (validate_skill.py, same
directory). Refuses to package a skill that fails validate_skill's
blocking checks — warnings are printed but do not block packaging.

Usage:
    python3 package_skill.py <path/to/skill-folder> [output-directory] [--estate DIR ...]

The zip is always named <name-from-SKILL.md-frontmatter>.skill — no
version suffix. The version lives in SKILL.md's **Version:** body line
— never as a version: key in frontmatter — and in git tags (see
skill-standards.md's "Zip filename rule" and "Version management"
sections).
"""

import fnmatch
import re
import sys
import zipfile
from pathlib import Path

# Importing a sibling module normally writes its bytecode cache into
# scripts/__pycache__ — exactly the build-artifact class validate_skill.py
# now flags (AU-2). Suppress that before the import so packaging never
# recreates the artifact it's supposed to guard against.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skill import validate_skill  # noqa: E402

# Patterns excluded when packaging — build artifacts and OS junk, never
# content a skill needs at runtime.
EXCLUDE_DIRS = {"__pycache__", "node_modules"}
EXCLUDE_GLOBS = {"*.pyc"}
EXCLUDE_FILES = {".DS_Store"}


def should_exclude(rel_path: Path) -> bool:
    """rel_path is relative to skill_path.parent, so parts[0] is the skill
    folder name itself."""
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)


def _skill_name_from_frontmatter(skill_md_text: str, fallback: str) -> str:
    match = re.search(r"^name:\s*(.+)$", skill_md_text, re.MULTILINE)
    if match:
        return match.group(1).strip().strip('"').strip("'")
    return fallback


def package_skill(skill_path, output_dir=None, estate=()):
    """Package a skill folder into a .skill file. Returns the output Path, or
    None on validation failure or error."""
    skill_path = Path(skill_path).resolve()

    if not skill_path.is_dir():
        print(f"Error: not a directory: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: SKILL.md not found in {skill_path}")
        return None

    print("Validating skill...")
    ok, errors, warnings = validate_skill(skill_path, estate)
    for w in warnings:
        print(f"WARNING: {w}")
    if not ok:
        for e in errors:
            print(f"ERROR: {e}")
        print("Validation failed — fix the errors above before packaging.")
        return None
    print("Validation passed.\n")

    skill_name = _skill_name_from_frontmatter(skill_md.read_text(encoding="utf-8"), skill_path.name)
    if skill_name != skill_path.name:
        print(
            f"NOTE: SKILL.md name ('{skill_name}') differs from the folder name "
            f"('{skill_path.name}') — packaging as '{skill_name}.skill' per the "
            "frontmatter name."
        )

    output_path = Path(output_dir).resolve() if output_dir else Path.cwd()
    output_path.mkdir(parents=True, exist_ok=True)
    skill_filename = output_path / f"{skill_name}.skill"

    try:
        with zipfile.ZipFile(skill_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob("*"):
                if not file_path.is_file():
                    continue
                arcname = file_path.relative_to(skill_path.parent)
                if should_exclude(arcname):
                    print(f"  Skipped: {arcname}")
                    continue
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

        print(f"\nPackaged skill to: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"Error creating .skill file: {e}")
        return None


def main():
    sys.stdout.reconfigure(errors="replace")  # a cp1252 console cannot print every message
    args = sys.argv[1:]
    estate = []
    while "--estate" in args:
        i = args.index("--estate")
        estate.append(args[i + 1] if i + 1 < len(args) else "")
        del args[i:i + 2]
    if not 1 <= len(args) <= 2 or "" in estate:
        print("Usage: python3 package_skill.py <path/to/skill-folder> [output-directory] [--estate DIR ...]")
        sys.exit(1)

    skill_path = args[0]
    output_dir = args[1] if len(args) > 1 else None

    result = package_skill(skill_path, output_dir, estate)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
