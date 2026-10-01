#!/usr/bin/env python3
"""
Packaging smoke test: package every skill directory under the given roots
and fail if any does not package.

This tests the packaging tooling, not a skill's content. Each skill is
packaged in its own subprocess, so the run uses this machine's real locale,
and twice — once with PyYAML and once with it forced absent — so both
frontmatter parser paths in validate_skill.py run. A missing PyYAML is a
failure, not a skip. Zips are written to a temporary directory and
discarded.

Usage:
    python3 smoke_package.py [root ...]      (default root: current directory)

Exit code 0 means every skill packaged on both paths.
"""

import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
PATHS = {"pyyaml": "", "fallback": "sys.modules['yaml'] = None\n"}
RUNNER = (
    "import sys\n{pre}sys.path.insert(0, {scripts!r})\n"
    "from package_skill import package_skill\n"
    "sys.exit(0 if package_skill({skill!r}, {out!r}) else 1)\n"
)


def find_skills(root: Path):
    return sorted(
        p.parent for p in root.rglob("SKILL.md")
        if not SKIP_DIRS.intersection(p.relative_to(root).parts)
    )


def check_zip(out_dir: Path):
    zips = list(out_dir.glob("*.skill"))
    if len(zips) != 1:
        return f"expected one .skill file, found {len(zips)}"
    with zipfile.ZipFile(zips[0]) as z:
        if z.testzip() is not None:
            return "zip is corrupt"
        tops = [n for n in z.namelist() if n.count("/") == 1 and n.endswith("/SKILL.md")]
        if len(tops) != 1:
            return "zip has no <folder>/SKILL.md at its root"
    return None


def smoke(skill: Path, path: str, pre: str):
    if path == "pyyaml":
        try:
            import yaml  # noqa: F401
        except ImportError:
            return "PyYAML is not installed, so this parser path cannot run"
    with tempfile.TemporaryDirectory() as out:
        code = RUNNER.format(pre=pre, scripts=str(SCRIPTS_DIR), skill=str(skill), out=out)
        run = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True,
                             text=True, encoding="utf-8", errors="replace")
        if run.returncode != 0:
            lines = (run.stdout + run.stderr).strip().splitlines()
            return next((l for l in reversed(lines) if l.startswith(("ERROR", "Error"))),
                        lines[-1] if lines else f"exit {run.returncode}")
        return check_zip(Path(out))


def main():
    sys.stdout.reconfigure(errors="replace")  # a cp1252 console cannot print every failure message
    roots = [Path(r).resolve() for r in (sys.argv[1:] or ["."])]
    skills = [s for r in roots for s in find_skills(r)]
    if not skills:
        print("No skill directories found.")
        sys.exit(1)
    failures = 0
    for skill in skills:
        for path, pre in PATHS.items():
            problem = smoke(skill, path, pre)
            failures += problem is not None
            print(f"{'FAIL' if problem else 'ok  '}  {path:<8}  {skill}"
                  + (f"\n        {problem}" if problem else ""))
    print(f"\n{len(skills)} skill(s), {failures} failure(s).")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
