#!/usr/bin/env python3
"""
Validate a skill directory against SKILL.md upload requirements and
this plugin's own governance conventions (see references/skill-standards.md).

Ported from Anthropic's skill-creator quick_validate.py and extended with
Governance-specific checks: the [project]-[purpose] naming convention,
the required "## Issues log" section, the 500-line SKILL.md guideline,
and the mechanically-detectable Instruction Cleanliness / structural
checks below.

Usage:
    python3 validate_skill.py <skill_directory> [--estate DIR ...]

Findings are split into two tiers:
- errors   — failures that break upload, install or routing. Blocking.
- warnings — Governance convention gaps and maintenance smells. Surfaced to
             the contributor but do not block packaging on their own
             (package_skill.py still prints them so nothing is missed
             silently).

Checks beyond SKILL.md frontmatter/body walk every text file in the skill
directory (excluding build-artifact directories):
- `**Version:**` present in the body; no `version:` key in frontmatter
- Issues log section declares a location (a URL or a repo path), not just
  the heading
- every sibling file referenced by name (in backtick spans) exists on disk
- internal numbered-step references ("step(s) N[-M]") resolve to a step
  that exists in that file's own numbered lists
- narrative-marker scan (Instruction Cleanliness pass 1): "no longer",
  "used to", "as of <date>", bare ISO dates — backward-looking
  constructions that are rare in correct present-tense instructions, so a
  hit is worth a human's look even with occasional false positives.
- no build artifacts (`__pycache__`, `*.pyc`) in the source tree
- the same normalised paragraph block appearing in more than one file
- every bullet in a `## Referrals` section names a skill in the estate
  (blocking), and an estate skill name mentioned anywhere else is flagged;
  the estate is every skill directory and .skill zip under the repo root,
  plus each --estate DIR
- every URL has the shape of a durable shared root or is this skill's own
  issues log; a per-artifact instance or an unrecognised host is flagged
  (common-standards.md, External references)
- a shared skill names no project, and a project-specific skill names only
  its own; the projects are the projects/ directories of the repo and of
  each --estate DIR, plus each --estate DIR holding a CLAUDE.md at its root,
  named by its directory name
- a cited "file.md's X section" has a heading X in that file, and a filename
  written without backticks exists in the skill
- in the standards family (references/*-standards.md, standards-format.md),
  the mechanical part of standards-format.md's Audit checkpoints contract:
  a checkpoint closes its section, a '##' group carrying rule-shaped
  language carries a checkpoint, a checkpoint points at no claim about the
  text, and a judgment call names who confirms it

Exit code 0 means no blocking errors (warnings may still be present).
Exit code 1 means at least one blocking error was found.
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# Directories whose contents are never packaged, so a SKILL.md inside them
# shouldn't count toward the single-SKILL.md check below. Mirrors the
# exclusion rules in package_skill.py.
EXCLUDED_DIR_PARTS = {"__pycache__", "node_modules"}

ALLOWED_FRONTMATTER_KEYS = {
    "name", "description", "license", "allowed-tools", "metadata",
    "compatibility", "when_to_use", "disable-model-invocation", "user-invocable",
}

MAX_SKILL_MD_LINES = 500  # skill-standards.md guideline, not a hard spec limit

TEXT_SUFFIXES = {".md"}

NARRATIVE_MARKERS = ["no longer", "used to", "as of "]
ISO_DATE_RE = re.compile(r"\b(19|20)\d{2}-\d{2}-\d{2}\b")
STEP_REF_RE = re.compile(r"\bsteps?\s+(\d+)(?:\s*[-–—]\s*(\d+))?\b", re.IGNORECASE)
ORDERED_ITEM_RE = re.compile(r"^\s*(\d+)\.\s+", re.MULTILINE)
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
FILE_REF_RE = re.compile(r"\.(md|py|json|ya?ml|txt)$", re.IGNORECASE)
PLACEHOLDER_PREFIX_RE = re.compile(r"^<[^>]+>/")

MIN_DUP_BLOCK_CHARS = 80

URL_RE = re.compile(r"https?://[^\s)>\]\"'`|]+")
# common-standards.md "External references": durable shared roots pass on shape.
ROOT_URL_RES = [
    re.compile(r"^https?://drive\.google\.com/drive/folders/[^/]+/?$"),
    re.compile(r"^https?://github\.com/[\w.-]+/[\w.-]+/?$"),
]
INSTANCE_URL_RES = [
    (re.compile(r"drive\.google\.com/file/"), "an individual file's link"),
    (re.compile(r"github\.com/[\w.-]+/[\w.-]+/(blob|releases/download)/"), "an individual file's link"),
    (re.compile(r"github\.com/[\w.-]+/[\w.-]+/(issues|pull)/\d+"), "an individual issue or pull request"),
]
SECTION_REF_RE = re.compile(
    r"`?([\w./-]+\.md)`?'s\s+(?:\"([^\"]+)\"|([A-Z][\w/&'-]*(?:[ ][A-Z][\w/&'-]*)*))"
)
# File types and platform files a skill names without holding one.
CONVENTION_FILES = {"CLAUDE.md", "README.md", "SKILL.md", "qa-standards.md", "ISSUES.md",
                    "plugin.json", "marketplace.json", "hooks.json", ".mcp.json", ".lsp.json"}
PLACEHOLDER_CHARS = ("[", "<")
BARE_FILE_RE = re.compile(r"(?<![`\w/.-])([\w-]+(?:/[\w-]+)*\.md)(?![`\w])")

REFERRALS_SECTION_RE = re.compile(r"^## Referrals[ \t]*\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
REFERRAL_LINE_RE = re.compile(r"^\s*[-*]\s+`([a-z0-9-]+)`\s+[—–-]+\s+\S")
# A thematic break closing the section is layout, not a referral.
HRULE_RE = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")


def _counts_as_skill_md(rel_path: Path) -> bool:
    """True if a SKILL.md at rel_path (relative to the skill root) would be packaged."""
    dir_parts = rel_path.parts[:-1]
    return not any(part in EXCLUDED_DIR_PARTS for part in dir_parts)


def _is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIR_PARTS for part in path.parts)


def _iter_text_files(skill_path: Path):
    """Yield every non-excluded text file (currently: .md) in the skill tree."""
    for p in sorted(skill_path.rglob("*")):
        if p.is_file() and not _is_excluded(p.relative_to(skill_path)) and p.suffix in TEXT_SUFFIXES:
            yield p


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _check_build_artifacts(skill_path: Path, warnings: list) -> None:
    for p in sorted(skill_path.rglob("*")):
        rel = p.relative_to(skill_path)
        if p.is_dir() and p.name == "__pycache__":
            warnings.append(
                f"Build artifact directory present: {rel} — must not be committed to "
                "source (package_skill.py excludes it from the zip, but it should not "
                "be sitting in the source tree either)."
            )
        elif p.is_file() and p.suffix == ".pyc":
            warnings.append(f"Build artifact file present: {rel}")


def _check_sibling_references(skill_path: Path, files: list, warnings: list) -> None:
    all_basenames = {}
    for p in skill_path.rglob("*"):
        if p.is_file() and not _is_excluded(p.relative_to(skill_path)):
            all_basenames.setdefault(p.name, []).append(p)

    for f in files:
        text = _read_text(f)
        for m in BACKTICK_RE.finditer(text):
            token = m.group(1).strip()
            if not token or " " in token or "\n" in token:
                continue
            if token.startswith("http://") or token.startswith("https://"):
                continue
            if not FILE_REF_RE.search(token):
                continue
            token_clean = PLACEHOLDER_PREFIX_RE.sub("", token)
            if (skill_path / token_clean).exists():
                continue
            basename = Path(token_clean).name
            if basename in all_basenames or basename in CONVENTION_FILES:
                continue
            if any(c in token_clean for c in PLACEHOLDER_CHARS):
                continue
            warnings.append(
                f"{f.relative_to(skill_path)}: references '{token}' — no file by "
                "that name found in the skill directory."
            )


def _check_step_references(files: list, skill_path: Path, warnings: list) -> None:
    for f in files:
        text = _read_text(f)
        item_numbers = [int(n) for n in ORDERED_ITEM_RE.findall(text)]
        if not item_numbers:
            continue
        max_item = max(item_numbers)
        for m in STEP_REF_RE.finditer(text):
            nums = [int(g) for g in m.groups() if g]
            if any(n > max_item for n in nums):
                warnings.append(
                    f"{f.relative_to(skill_path)}: references '{m.group(0)}' but the "
                    f"file's highest numbered list item is {max_item}."
                )


def _check_narrative_markers(files: list, skill_path: Path, warnings: list) -> None:
    for f in files:
        text = _read_text(f)
        lower = text.lower()
        found_markers = sorted({marker.strip() for marker in NARRATIVE_MARKERS if marker in lower})
        if found_markers:
            warnings.append(
                f"{f.relative_to(skill_path)}: contains narrative-marker language "
                f"({', '.join(found_markers)}) — Instruction Cleanliness pass 1 flags "
                "change-history/explanatory framing in shipped instructions; review "
                "for a legitimate exception (e.g. defining the marker itself) before "
                "rewriting."
            )
        if ISO_DATE_RE.search(text):
            warnings.append(
                f"{f.relative_to(skill_path)}: contains a bare ISO date — Instruction "
                "Cleanliness flags dated language in shipped instructions."
            )


def _normalize_block(block: str) -> str:
    return re.sub(r"\s+", " ", block).strip()


def _iter_blocks(text: str):
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if block:
            yield block


def _check_duplicate_blocks(files: list, skill_path: Path, warnings: list) -> None:
    seen = {}
    for f in files:
        text = _read_text(f)
        for block in _iter_blocks(text):
            if len(block) < MIN_DUP_BLOCK_CHARS:
                continue
            norm = _normalize_block(block)
            seen.setdefault(norm, set()).add(str(f.relative_to(skill_path)))
    for norm, file_set in seen.items():
        if len(file_set) > 1:
            snippet = norm[:100] + ("…" if len(norm) > 100 else "")
            warnings.append(
                f"Duplicate block across {', '.join(sorted(file_set))}: \"{snippet}\""
            )


def _check_external_references(files: list, skill_path: Path, content: str,
                               warnings: list) -> None:
    """A URL passes on the shape of a durable shared root or as this skill's
    own issues log; any other shape needs the three-part test applied."""
    own_log = re.search(r"^## Issues log\s*\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
    own_urls = set(URL_RE.findall(own_log.group(1))) if own_log else set()
    for f in files:
        rel = f.relative_to(skill_path)
        for url in sorted(set(URL_RE.findall(_read_text(f)))):
            url = url.rstrip(".,;:")
            host = url.split("/")[2] if url.count("/") >= 2 else ""
            if "." not in host or url in own_urls or any(r.search(url) for r in ROOT_URL_RES):
                continue
            kind = next((k for r, k in INSTANCE_URL_RES if r.search(url)), None)
            reason = (f"names {kind}, a per-artifact instance" if kind else
                      "names a destination not recognised as a shared root; confirm it "
                      "meets the three-part test")
            warnings.append(f"{rel}: {url} {reason} (common-standards.md, External references).")


def _vendor_neutral_names() -> set:
    """Names under common-standards.md's vendor-neutral exemption, read from the
    exemption paragraph itself so this script names no artifact."""
    standards = Path(__file__).resolve().parent.parent / "references" / "common-standards.md"
    try:
        text = standards.read_text(encoding="utf-8")
    except OSError:
        return set()
    m = re.search(r"\*\*Exemption — vendor-neutral artifacts\.\*\*(.*?)(?:\n\n|\Z)", text, re.DOTALL)
    return {n for n in re.findall(r"`([a-z0-9-]+)`", m.group(1)) if not n.endswith("-")} if m else set()


def _project_names(skill_path: Path, estate) -> set:
    roots = [Path(r) for r in estate]
    root = _repo_root(skill_path.resolve())
    if root:
        roots.append(root)
    names = {p.name for r in roots if (r / "projects").is_dir()
             for p in (r / "projects").iterdir() if p.is_dir()}
    # A project held in a repo of its own is an estate dir with a root CLAUDE.md.
    for r in estate:
        r = Path(r).resolve()
        if (r / "CLAUDE.md").is_file() and r != root:
            names.add(r.name)
    return names


def _check_project_names(files: list, skill_path: Path, skill_name: str,
                         projects: set, warnings: list) -> None:
    """A shared skill names no project; a project-specific skill names only its own
    (skill-standards.md, Skill/project file-reference boundary)."""
    own = {p for p in projects if skill_name.startswith(f"{p}-")}
    for f in files:
        text = _read_text(f)
        rel = f.relative_to(skill_path)
        for p in sorted(projects - own):
            words = p.split("-")
            # The kebab form in any case; the spaced form only as a Title Case
            # name, since "social media" in lower case is ordinary prose.
            kebab = r"(?i:" + "-".join(map(re.escape, words)) + ")"
            title = " ".join(re.escape(w.capitalize()) for w in words)
            pattern = r"(?<![\w-])(?:" + kebab + "|" + title + r")(?![\w])"
            # A skill name carrying the project segment is a skill, not the project.
            hits = [m for m in re.finditer(pattern, text)
                    if not re.match(r"-[a-z0-9]", text[m.end():m.end() + 2])]
            if hits:
                warnings.append(
                    f"{rel}: names the project '{p}' {len(hits)} time(s) — "
                    + ("a shared skill names no project" if not own else
                       "a project-specific skill names only its own project")
                    + " (skill-standards.md, Skill/project file-reference boundary)."
                )


def _headings(path: Path) -> list:
    return [re.sub(r"[`*_]", "", h).strip().lower()
            for h in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", _read_text(path), re.MULTILINE)]


def _check_section_and_bare_references(files: list, skill_path: Path, warnings: list) -> None:
    """Extends the sibling check: a named section must exist in the file named,
    and a filename written without backticks must exist too."""
    by_name = {}
    for p in skill_path.rglob("*.md"):
        if not _is_excluded(p.relative_to(skill_path)):
            by_name.setdefault(p.name, p)
    for f in files:
        text = _read_text(f)
        rel = f.relative_to(skill_path)
        for m in SECTION_REF_RE.finditer(text):
            target = by_name.get(Path(m.group(1)).name)
            section = (m.group(2) or m.group(3) or "").strip().lower()
            if target is None or not section:
                continue
            if not any(h == section or h.startswith(section) or section.startswith(h)
                       for h in _headings(target)):
                warnings.append(
                    f"{rel}: cites {m.group(1)}'s '{section}' section — no heading by "
                    "that name in that file."
                )
        prose = BACKTICK_RE.sub("", text)
        for name in sorted(set(BARE_FILE_RE.findall(prose))):
            if Path(name).name in CONVENTION_FILES or any(c in name for c in PLACEHOLDER_CHARS):
                continue
            if Path(name).name not in by_name and not (skill_path / name).exists():
                warnings.append(
                    f"{rel}: names '{name}' without backticks — no file by that name "
                    "in the skill directory."
                )


RULE_WORD_RE = re.compile(r"\b(must|never|always|may not|is required|are required|cannot)\b", re.IGNORECASE)
CLAIM_WORD_RE = re.compile(r"✅|\bbyte counts?\b|\bworklog|\bcertification claim|\bapproval note|\bstatus marker", re.IGNORECASE)
LIST_ITEM_RE = re.compile(r"^(\d+\.|[-*])\s")


def _is_standards_file(rel: Path) -> bool:
    return (len(rel.parts) >= 2 and rel.parts[-2] == "references"
            and (rel.name.endswith("-standards.md") or rel.name == "standards-format.md"))


def _sections(text: str):
    """Yield (heading, [paragraphs]) for each heading's own body, fenced code
    removed and '---' rules treated as paragraph breaks."""
    text = re.sub(r"^```.*?^```[ \t]*$", "", text, flags=re.MULTILINE | re.DOTALL)
    heading, level, body = None, 0, []
    for line in text.split("\n") + ["# end"]:
        if re.match(r"^#{1,6}\s", line):
            if heading is not None:
                paras = [p.strip() for p in re.split(r"\n\s*\n|^---\s*$", "\n".join(body), flags=re.MULTILINE)]
                yield heading, level, [p for p in paras if p]
            # A level-1 heading is the file's title, not a section.
            level = len(line) - len(line.lstrip("#"))
            heading, body = (line.lstrip("#").strip() if level > 1 else None), []
        else:
            body.append(line)


def _check_notation(files: list, skill_path: Path, warnings: list) -> None:
    """standards-format.md's Audit checkpoints contract, where it is mechanical.
    Whether a section holds a rule at all is the auditor's call."""
    for f in files:
        rel = f.relative_to(skill_path)
        if not _is_standards_file(rel):
            continue
        sections = list(_sections(_read_text(f)))
        for n, (heading, level, paras) in enumerate(sections):
            where = f"{rel} § {heading}"
            cps = [i for i, p in enumerate(paras) if p.startswith("**Audit checkpoint:**")]
            # A checkpoint closing a later block under the same '##' reaches this
            # block's rules too: the requirement is per rule, not per section.
            group = []
            for later_heading, later_level, later_paras in sections[n + 1:]:
                if later_level <= 2:
                    break
                group.append(later_paras)
            covered_later = any(p.startswith("**Audit checkpoint:**") for ps in group for p in ps)
            for i in cps:
                rest = paras[i + 1:]
                while rest and LIST_ITEM_RE.match(rest[0]):  # the checkpoint's own list
                    rest = rest[1:]
                if any(not p.startswith("**Judgment call:**") for p in rest):
                    warnings.append(f"{where}: an 'Audit checkpoint:' line does not close the section.")
                # The section defining the rule names the claim forms it forbids.
                if heading != "Claims about the text" and CLAIM_WORD_RE.search(paras[i]):
                    warnings.append(
                        f"{where}: the checkpoint points at a claim about the text — a status "
                        "marker, byte count, worklog, certification or approval "
                        "(standards-format.md, Claims about the text)."
                    )
            if not cps and not covered_later and any(RULE_WORD_RE.search(p) for p in paras):
                warnings.append(
                    f"{where}: rule-shaped language and no 'Audit checkpoint:' — confirm the "
                    "section is definitional, a pointer or shared rules, or add the checkpoint."
                )
            for p in paras:
                if p.startswith("**Judgment call:**") and "confirm" not in p.lower():
                    warnings.append(f"{where}: a 'Judgment call:' marking names no one who confirms it.")


def _repo_root(path: Path):
    for p in (path, *path.parents):
        if (p / ".git").exists():
            return p
    return None


def _estate_names(skill_path: Path, estate) -> set:
    """Skill and subagent names the estate knows (skill-standards.md's Referral
    constraint 5): every skill directory, .skill zip and agents/ definition
    under the repo root and each estate dir."""
    roots = [Path(r) for r in estate]
    root = _repo_root(skill_path.resolve())
    if root:
        roots.append(root)
    skip = EXCLUDED_DIR_PARTS | {".git"}
    names = set()
    for r in roots:
        for md in r.rglob("SKILL.md"):
            if skip.intersection(md.relative_to(r).parts):
                continue
            names.add(md.parent.name)
            m = re.search(r"^name:\s*(\S+)", _read_text(md), re.MULTILINE)
            if m:
                names.add(m.group(1).strip("'\""))
        names.update(z.stem for z in r.rglob("*.skill") if not skip.intersection(z.relative_to(r).parts))
        for md in r.rglob("*.md"):
            parts = md.relative_to(r).parts
            if "agents" not in parts[:-1] or skip.intersection(parts):
                continue
            m = re.search(r"\A---\s*\n.*?^name:\s*(\S+)", _read_text(md), re.MULTILINE | re.DOTALL)
            if m:
                names.add(m.group(1).strip("'\""))
    return names


def _check_referrals(content: str, own_names: set, estate_names: set, errors: list) -> None:
    """Blocking tier (decision 50): a referral that cannot route is a defect."""
    match = REFERRALS_SECTION_RE.search(content)
    if not match:
        return
    for line in match.group(1).splitlines():
        if not line.strip() or HRULE_RE.match(line):
            continue
        ref = REFERRAL_LINE_RE.match(line)
        if not ref:
            errors.append(
                f"'## Referrals' line is not in the form '- `skill-name` — task type': {line.strip()}"
            )
        elif ref.group(1) in own_names:
            errors.append(f"'## Referrals' names this skill itself: {ref.group(1)}")
        elif ref.group(1) not in estate_names:
            errors.append(
                f"Referral names '{ref.group(1)}', which is not a skill in the estate — "
                "no skill directory or .skill zip by that name under the repo "
                "(pass --estate DIR for skills held elsewhere)."
            )


def _check_skill_mentions(files: list, skill_path: Path, own_names: set,
                          estate_names: set, warnings: list) -> None:
    """A backticked estate skill name outside '## Referrals' is either an
    undeclared referral or content coupling; the audit decides which."""
    for f in files:
        text = _read_text(f)
        if f.name == "SKILL.md" and f.parent == skill_path:
            text = REFERRALS_SECTION_RE.sub("", text)
        rel = f.relative_to(skill_path)
        for name in sorted(set(BACKTICK_RE.findall(text)) & (estate_names - own_names)):
            warnings.append(
                f"{rel}: mentions `{name}` outside a '## Referrals' section — a referral "
                "belongs there; a mention carrying its rules or a path inside it is "
                "content coupling (skill-standards.md, Referral)."
            )


def validate_skill(skill_path, estate=()):
    """Validate a skill directory. estate adds directories whose skills count
    as existing for referral checks, beyond the repo this skill sits in.

    Returns (ok, errors, warnings) where ok is True iff errors is empty.
    """
    skill_path = Path(skill_path)
    errors = []
    warnings = []

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md not found"], warnings

    # A skill must contain exactly one SKILL.md, at <folder>/SKILL.md. The
    # Skills API and claude.ai reject multiple on upload — only Claude Code's
    # filesystem loads nested ones. Block here rather than ship an artifact
    # that's guaranteed to fail on upload.
    skill_md_files = [
        p for p in skill_path.rglob("SKILL.md")
        if _counts_as_skill_md(p.relative_to(skill_path))
    ]
    if len(skill_md_files) > 1:
        extras = sorted(
            str(p.relative_to(skill_path)) for p in skill_md_files
            if p.resolve() != skill_md.resolve()
        )
        errors.append(
            f"Found {len(skill_md_files)} SKILL.md files, but a skill must contain "
            f"exactly one at <folder>/SKILL.md. Extra: {', '.join(extras)}."
        )

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        errors.append("No YAML frontmatter found")
        return False, errors, warnings

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        errors.append("Invalid frontmatter format (missing closing ---)")
        return False, errors, warnings

    frontmatter_text = match.group(1)
    frontmatter = None
    if yaml is not None:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML in frontmatter: {e}")
    else:
        # Manual fallback if PyYAML isn't available in this environment. It
        # reads every top-level key, so key-based checks run on both paths.
        # A key's indented lines (a block scalar or a nested mapping) are
        # joined into one string; only name and description are read as values.
        frontmatter = {}
        fm_lines = frontmatter_text.split("\n")
        i = 0
        while i < len(fm_lines):
            m = re.match(r"^([A-Za-z0-9_-]+):(.*)$", fm_lines[i])
            i += 1
            if not m:
                continue
            key, value = m.group(1), m.group(2).strip()
            block = []
            while i < len(fm_lines) and (
                fm_lines[i].startswith((" ", "\t")) or not fm_lines[i].strip()
            ):
                block.append(fm_lines[i].strip())
                i += 1
            if value in ("", ">", "|", ">-", "|-", ">+", "|+"):
                value = " ".join(p for p in block if p)
            frontmatter[key] = value.strip('"').strip("'")

    if frontmatter is None:
        return False, errors, warnings

    if not isinstance(frontmatter, dict):
        errors.append("Frontmatter must be a YAML dictionary")
        return False, errors, warnings

    has_version_key = "version" in frontmatter
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS - {"version"}
    if unexpected_keys:
        warnings.append(f"Unrecognized frontmatter key(s): {', '.join(sorted(unexpected_keys))}")
    if has_version_key:
        warnings.append(
            "Frontmatter contains a 'version' key — version belongs in the body as "
            "'**Version:** vX.Y' (skill-standards.md's Version management section), "
            "never in frontmatter."
        )

    if "name" not in frontmatter:
        errors.append("Missing 'name' in frontmatter")
    if "description" not in frontmatter:
        errors.append("Missing 'description' in frontmatter")

    name = str(frontmatter.get("name", "")).strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            errors.append(f"Name '{name}' should be kebab-case (lowercase letters, digits, hyphens only)")
        if name.startswith("-") or name.endswith("-") or "--" in name:
            errors.append(f"Name '{name}' cannot start/end with a hyphen or contain consecutive hyphens")
        if len(name) > 64:
            errors.append(f"Name is too long ({len(name)} characters). Maximum is 64.")

    description = str(frontmatter.get("description", "")).strip()
    if description:
        if "<" in description or ">" in description:
            errors.append("Description cannot contain angle brackets (< or >)")
        if len(description) > 1024:
            errors.append(f"Description is too long ({len(description)} characters). Maximum is 1024.")

    if "## Issues log" not in content:
        if name not in _vendor_neutral_names():
            warnings.append(
                "No '## Issues log' section found — common-standards.md requires every "
                "skill outside the vendor-neutral exemption to declare its issues-log "
                "identifier and location near the top."
            )
    else:
        issues_match = re.search(r"## Issues log(.*?)(\n## |\Z)", content, re.DOTALL)
        issues_section = issues_match.group(1) if issues_match else ""
        if not re.search(r"^Log:\s*\S+", issues_section, re.MULTILINE):
            warnings.append(
                "'## Issues log' section has no 'Log:' location — the identifier is "
                "declared but the log's location is missing."
            )

    if not re.search(r"^\*\*Version:\*\*\s*\S+", content, re.MULTILINE):
        warnings.append(
            "No '**Version:**' line found in the body — skill-standards.md requires "
            "the version declared in the body text (see Version management)."
        )

    line_count = len(content.split("\n"))
    if line_count > MAX_SKILL_MD_LINES:
        warnings.append(
            f"SKILL.md is {line_count} lines — skill-standards.md recommends staying "
            f"under {MAX_SKILL_MD_LINES} lines and moving detail to sub-files."
        )

    # Whole-tree checks below — these read every .md file in the skill,
    # not just SKILL.md.
    all_text_files = list(_iter_text_files(skill_path))
    _check_build_artifacts(skill_path, warnings)
    _check_sibling_references(skill_path, all_text_files, warnings)
    _check_step_references(all_text_files, skill_path, warnings)
    _check_narrative_markers(all_text_files, skill_path, warnings)
    _check_duplicate_blocks(all_text_files, skill_path, warnings)

    own_names = {skill_path.resolve().name, name}
    estate_names = _estate_names(skill_path, estate)
    _check_referrals(content, own_names, estate_names, errors)
    _check_skill_mentions(all_text_files, skill_path, own_names, estate_names, warnings)
    _check_external_references(all_text_files, skill_path, content, warnings)
    _check_project_names(all_text_files, skill_path, name, _project_names(skill_path, estate), warnings)
    _check_section_and_bare_references(all_text_files, skill_path, warnings)
    _check_notation(all_text_files, skill_path, warnings)

    return len(errors) == 0, errors, warnings


def main():
    sys.stdout.reconfigure(errors="replace")  # a cp1252 console cannot print every message
    args = sys.argv[1:]
    estate = []
    while "--estate" in args:
        i = args.index("--estate")
        estate.append(args[i + 1] if i + 1 < len(args) else "")
        del args[i:i + 2]
    if len(args) != 1 or "" in estate:
        print("Usage: python3 validate_skill.py <skill_directory> [--estate DIR ...]")
        sys.exit(1)

    ok, errors, warnings = validate_skill(args[0], estate)

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if ok and not warnings:
        print("Skill is valid — no errors or warnings.")
    elif ok:
        print("Skill passes spec validation (warnings above are convention gaps, not blockers).")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
