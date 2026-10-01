# Distribution | build-standards

**Purpose:** Carry a confirmed skill version, subagent, plugin or set of project files from the repo to every place it is used. Load it when a skill zip or plugin archive is rebuilt, or project files are finalized and confirmed ready — immediately, not at session end. It may run several times in one session.

---

## Repo access and file delivery available

1. **Build and check.** Run `python3 <skill-dir>/scripts/smoke_package.py` from the repo root. It packages every skill in the repo on both frontmatter parser paths and needs PyYAML installed. Present no zip until it reports zero failures. Then confirm the rebuilt zip carries the source's version with `python3 <skill-dir>/scripts/check_version_drift.py --source <skill-source-dir> --packaged <zip>`, and present no zip it reports as drifted. Build every zip straight into the distribution location the repo's own instructions declare, never into a scratch folder. For a plugin, `package_plugin.py` also verifies the archive against the plugin directory and refuses on any difference.
2. **Deliver.** Deliver the rebuilt zip or archive into the conversation from that location, alone in its own turn, with no question in the same turn.

   ⏸ HUMAN CHECKPOINT [Governance] — the contributor confirms the delivered zip is good. Silence or task continuation is not confirmation. Ask for it in the following turn.

3. **Commit.** A zip in the working tree is a candidate, not a finalized artifact. Once confirmed, commit it in the same commit as its source changes, never as a separate, later commit. It is finalized from that commit. The version's git tag sits on that commit; a tag on a source-only commit is moved to it.
4. **Sync repos.** Ask which repos hold a copy of the artifact under `.claude/skills/`:

   ```
   Question: "Sync [skill-name] into any repos?"
   Options:
   - Yes — I'll name which
   - None this time
   ```

   Sync every confirmed repo in one pass with `python3 <skill-dir>/scripts/sync_copies.py <skill-source-dir> <repo>/.claude/skills/<skill-name> [...]`, which copies the tree into each target and compares every copied file's bytes against its source. Flag a repo the session cannot reach for manual sync.
5. **Reinstall.** Remind the contributor to reinstall the new version wherever they use it — a Claude Code install of the plugin, or a claude.ai account installing the zip through Customize → Skills. Where the artifact declares a further distribution route, follow its declaration.

Steps 3–5 run as one continuous pass once step 2's checkpoint is passed.

---

## No repo access (the contributor uploaded a zip or worked from installed skill files)

- **Skill updated:** present the updated files or zip for the contributor to save and install via Customize → Skills.
- **Project files updated:** present the updated files for the contributor to upload to the project knowledge.
- Prompt the contributor to commit the change to the source repo, and sync `.claude/skills/<skill-name>/` in each repo holding a copy.

---

## Hybrid projects

When a Hybrid project's instruction or task file changes, confirm the change reached the live claude.ai Project before marking the update complete. For a file that already exists as project knowledge, confirm the direct write landed; for a brand-new file, confirm the contributor uploaded it through the project-knowledge interface.
