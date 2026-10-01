#!/usr/bin/env python3
"""
Package a governed plugin into a single installable archive.

The plugin directory is the plugin, laid out at its default locations:
the manifest at .claude-plugin/plugin.json, a README.md, each skill at
skills/<name>/SKILL.md and each subagent at agents/<name>.md. It is the
one source every member publishes from, for the archive and for each
standalone .skill alike (plugin-standards.md: no built artifact is an
input to another). The archive is that directory unchanged.

The README's "Bundle contents" table names each member in backticks, its
class, and its location in the bundle:

    | `example` | skill | `skills/example/SKILL.md` |
    | `example-auditor` | subagent | `agents/example-auditor.md` |

Refuses to package when:
- the manifest lacks name, version, description or author, or carries a
  component key (plugin-standards.md: every component sits at its default
  location);
- the README lacks an "## Issues log" section with an identifier and an https link;
- the plugin root holds anything other than .claude-plugin/, README.md,
  skills/ and agents/ (plugin-standards.md: a governed bundle carries only
  governed classes);
- the Bundle contents table and the members present under skills/ and
  agents/ differ in either direction;
- a skill member fails validate_skill's blocking checks;
- a subagent member's frontmatter lacks name, description, tools or model,
  or names it differently from its file;
- a member's text uses the plugin-root path variable, the substitution
  route into a sibling member (plugin-standards.md: members do not share
  content).

Usage:
    python3 package_plugin.py <plugin-dir> [output-directory] [--estate DIR ...]

The archive is named <manifest name>.zip, with no version suffix, and is
rooted at the plugin root. Build artifacts are left out, as package_skill.py
leaves them out of a .skill. Once written, the archive is read back and
every entry compared byte for byte against the file it came from; a
missing, extra or differing entry removes the archive and refuses.
"""

import json
import re
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from package_skill import should_exclude  # noqa: E402
from validate_skill import validate_skill  # noqa: E402

REQUIRED_KEYS = ("name", "version", "description", "author")
ROOT_ENTRIES = {".claude-plugin", "README.md", "skills", "agents"}
COMPONENT_KEYS = ("skills", "agents", "commands", "hooks", "mcpServers", "lspServers", "outputStyles")
MEMBER_ROW_RE = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|\s*skill\s*\|", re.MULTILINE)
AGENT_ROW_RE = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|\s*subagent\s*\|", re.MULTILINE)
AGENT_KEYS = ("name", "description", "tools", "model")
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n", re.DOTALL)
ISSUES_LOG_RE = re.compile(
    r"^## Issues log[ \t]*\n+Identifier:\s*\S+[ \t]*\nLog:\s*\S+", re.MULTILINE
)
PLUGIN_ROOT_RE = re.compile(r"\$\{?CLAUDE_PLUGIN_ROOT\b")
TEXT_SUFFIXES = {".md", ".py", ".txt", ".json", ".yaml", ".yml"}


def _entries(directory: Path):
    """The directory's entries, build artifacts left out."""
    if not directory.is_dir():
        return []
    return [p for p in directory.iterdir() if not should_exclude(Path(p.name))]


def _check_source(plugin_dir: Path, errors: list):
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    readme_path = plugin_dir / "README.md"
    manifest = {}
    if not manifest_path.is_file():
        errors.append(f"No manifest at {manifest_path}")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"Manifest is not valid JSON: {e}")
        for key in REQUIRED_KEYS:
            if not manifest.get(key):
                errors.append(f"Manifest states no '{key}'")
        declared = [k for k in COMPONENT_KEYS if k in manifest]
        if declared:
            errors.append(f"Manifest carries component keys: {declared}")
    extra = [p.name for p in _entries(plugin_dir / ".claude-plugin")
             if p.name not in ("plugin.json", "marketplace.json")]
    if extra:
        errors.append(f".claude-plugin/ holds more than manifest and catalog metadata: {extra}")
    stray = sorted(p.name for p in _entries(plugin_dir) if p.name not in ROOT_ENTRIES)
    if stray:
        errors.append(f"Plugin root holds entries outside the governed layout: {stray}")

    members, agents = [], []
    if not readme_path.is_file():
        errors.append(f"No README.md at {readme_path}")
    else:
        readme = readme_path.read_text(encoding="utf-8")
        if not ISSUES_LOG_RE.search(readme):
            errors.append("README.md has no '## Issues log' section stating an identifier and a location")
        members = MEMBER_ROW_RE.findall(readme)
        agents = AGENT_ROW_RE.findall(readme)
        if not members and not agents:
            errors.append("README.md's Bundle contents table names no member")
    return manifest, members, agents


def _check_roster(plugin_dir: Path, members: list, agents: list, errors: list) -> None:
    """The Bundle contents table and the directory name the same members."""
    skill_entries = _entries(plugin_dir / "skills")
    agent_entries = _entries(plugin_dir / "agents")
    for p in skill_entries:
        if not p.is_dir():
            errors.append(f"skills/{p.name} is not a skill directory")
    for p in agent_entries:
        if not (p.is_file() and p.suffix == ".md"):
            errors.append(f"agents/{p.name} is not a subagent definition file")
    present_skills = {p.name for p in skill_entries if p.is_dir()}
    present_agents = {p.stem for p in agent_entries if p.is_file() and p.suffix == ".md"}
    for name in sorted(set(members) - present_skills):
        errors.append(f"Bundle contents names skill '{name}', but skills/{name}/ does not exist")
    for name in sorted(present_skills - set(members)):
        errors.append(f"skills/{name}/ is present but Bundle contents does not name it")
    for name in sorted(set(agents) - present_agents):
        errors.append(f"Bundle contents names subagent '{name}', but agents/{name}.md does not exist")
    for name in sorted(present_agents - set(agents)):
        errors.append(f"agents/{name}.md is present but Bundle contents does not name it")


def _check_agent(agent_file: Path, errors: list) -> None:
    """A subagent member is one definition file (subagent-standards.md)."""
    name = agent_file.stem
    text = agent_file.read_text(encoding="utf-8", errors="replace")
    fm = FRONTMATTER_RE.match(text)
    if not fm:
        errors.append(f"[{name}] {agent_file.name} has no YAML frontmatter")
        return
    keys = dict(re.findall(r"^([a-z]+):[ \t]*(.*)$", fm.group(1), re.MULTILINE))
    for key in AGENT_KEYS:
        if not keys.get(key, "").strip():
            errors.append(f"[{name}] frontmatter states no '{key}'")
    if keys.get("name", "").strip() not in ("", name):
        errors.append(f"[{name}] frontmatter names '{keys['name'].strip()}', not its file name")
    if PLUGIN_ROOT_RE.search(text):
        errors.append(
            f"[{name}] uses the plugin-root path variable — "
            "a path into the bundle is content coupling between members"
        )


def _check_member(skill_dir: Path, estate, errors: list) -> None:
    ok, member_errors, warnings = validate_skill(skill_dir, estate)
    for w in warnings:
        print(f"  WARNING [{skill_dir.name}]: {w}")
    if not ok:
        errors.extend(f"[{skill_dir.name}] {e}" for e in member_errors)
    for f in skill_dir.rglob("*"):
        if f.is_file() and f.suffix in TEXT_SUFFIXES and not should_exclude(f.relative_to(skill_dir.parent)):
            if PLUGIN_ROOT_RE.search(f.read_text(encoding="utf-8", errors="replace")):
                errors.append(
                    f"[{skill_dir.name}] {f.relative_to(skill_dir)} uses the plugin-root path variable — "
                    "a path into the bundle is content coupling between members"
                )


def _verify_archive(archive: Path, expected: dict) -> list:
    """Read the archive back and compare every entry with its source file."""
    problems = []
    with zipfile.ZipFile(archive) as zipf:
        names = set(zipf.namelist())
        for arcname, source in expected.items():
            if arcname not in names:
                problems.append(f"{arcname} is missing from the archive")
            elif zipf.read(arcname) != source.read_bytes():
                problems.append(f"{arcname} differs from its source {source}")
        for extra in sorted(names - set(expected)):
            problems.append(f"{extra} is in the archive but has no source")
    return problems


def package_plugin(plugin_dir, output_dir=None, estate=()):
    """Validate and archive the plugin directory. Returns the archive Path, or None."""
    plugin_dir = Path(plugin_dir).resolve()
    errors = []

    print("Checking plugin directory...")
    manifest, members, agents = _check_source(plugin_dir, errors)
    if len(set(members + agents)) != len(members + agents):
        errors.append(f"Bundle contents names a member twice: {members + agents}")
    _check_roster(plugin_dir, members, agents, errors)

    for name in agents:
        agent_file = plugin_dir / "agents" / f"{name}.md"
        if agent_file.is_file():
            print(f"Validating member {name}...")
            _check_agent(agent_file, errors)

    for name in members:
        skill_dir = plugin_dir / "skills" / name
        if not skill_dir.is_dir():
            continue
        if not (skill_dir / "SKILL.md").is_file():
            errors.append(f"Member '{name}' has no SKILL.md at skills/{name}/")
            continue
        print(f"Validating member {name}...")
        _check_member(skill_dir, estate, errors)

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        print("Packaging refused — fix the errors above.")
        return None

    output_path = Path(output_dir).resolve() if output_dir else Path.cwd()
    output_path.mkdir(parents=True, exist_ok=True)
    archive = output_path / f"{manifest['name']}.zip"

    expected = {}
    for f in sorted(plugin_dir.rglob("*")):
        rel = f.relative_to(plugin_dir)
        if f.is_file() and not should_exclude(rel):
            expected[rel.as_posix()] = f

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zipf:
        for arcname, source in expected.items():
            zipf.write(source, arcname)

    mismatches = _verify_archive(archive, expected)
    if mismatches:
        for m in mismatches:
            print(f"ERROR: {m}")
        archive.unlink()
        print("Packaging refused — the archive does not match its sources.")
        return None

    print(f"\nPackaged {manifest['name']} {manifest['version']} "
          f"({len(members)} skills, {len(agents)} subagents, {len(expected)} files verified) to: {archive}")
    return archive


def main():
    sys.stdout.reconfigure(errors="replace")  # a cp1252 console cannot print every message
    args = sys.argv[1:]
    estate = []
    while "--estate" in args:
        i = args.index("--estate")
        estate.append(args[i + 1] if i + 1 < len(args) else "")
        del args[i:i + 2]
    if not 1 <= len(args) <= 2 or "" in estate:
        print("Usage: python3 package_plugin.py <plugin-dir> [output-directory] [--estate DIR ...]")
        sys.exit(1)

    result = package_plugin(args[0], args[1] if len(args) > 1 else None, estate)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
