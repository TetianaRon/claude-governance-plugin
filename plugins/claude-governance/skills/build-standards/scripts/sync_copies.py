#!/usr/bin/env python3
"""
Sync a skill's source tree into one or more derived copies, and verify them.

Each target directory is made to hold exactly the source tree: files are
copied in, files the source no longer has are removed, and build artifacts
(the same exclusions package_skill.py applies) are left out. Every file in
every target is then compared byte for byte against its source.

Usage:
    python3 sync_copies.py <source-dir> <target-dir> [<target-dir> ...]

Exits non-zero if any target could not be written or any copy differs from
its source. A target whose parent directory does not exist is reported as
unreachable and skipped, not created.
"""

import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from package_skill import should_exclude  # noqa: E402


def source_files(source: Path) -> dict:
    files = {}
    for f in sorted(source.rglob("*")):
        rel = f.relative_to(source)
        if f.is_file() and not should_exclude(Path(source.name) / rel):
            files[rel.as_posix()] = f
    return files


def sync_one(files: dict, target: Path) -> list:
    problems = []
    if not target.parent.is_dir():
        return [f"{target}: parent directory does not exist; sync it by hand"]
    target.mkdir(exist_ok=True)
    for f in sorted(target.rglob("*"), reverse=True):
        rel = f.relative_to(target).as_posix()
        if f.is_file() and rel not in files:
            f.unlink()
        elif f.is_dir() and not any(f.iterdir()):
            f.rmdir()
    for rel, src in files.items():
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    for rel, src in files.items():
        dest = target / rel
        if not dest.is_file():
            problems.append(f"{dest}: missing after copy")
        elif dest.read_bytes() != src.read_bytes():
            problems.append(f"{dest}: differs from {src}")
    extra = [f for f in target.rglob("*") if f.is_file() and f.relative_to(target).as_posix() not in files]
    problems.extend(f"{f}: not in the source" for f in extra)
    return problems


def main():
    sys.stdout.reconfigure(errors="replace")
    if len(sys.argv) < 3:
        print(__doc__.strip().split("\n\n")[2])
        sys.exit(1)
    source = Path(sys.argv[1]).resolve()
    if not (source / "SKILL.md").is_file():
        print(f"ERROR: {source} holds no SKILL.md")
        sys.exit(1)
    files = source_files(source)
    failed = False
    for arg in sys.argv[2:]:
        target = Path(arg).resolve()
        problems = sync_one(files, target)
        if problems:
            failed = True
            for p in problems:
                print(f"ERROR: {p}")
        else:
            print(f"OK: {target} matches {source.name} ({len(files)} files)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
