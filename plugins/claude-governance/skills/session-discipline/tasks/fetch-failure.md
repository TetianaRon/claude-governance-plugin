# Fetch failure | session-discipline

**Load when:** the project relies on documentation pages or several source pages per session.

---

## A required source fails to load

Claude does not proceed silently or substitute from memory.

1. Tell the contributor the fetch failed, naming the source that could not be loaded.
2. Ask how to proceed:

   ```
   Question: "[source] failed to load. How should we proceed?"
   Options:
   - Retry the fetch
   - Use a cached or provided copy
   - Proceed without it
   ```

3. Proceeding without the source, state what is unknown, and flag every output that depends on the missing content for human review before use.
4. Never infer or reconstruct the failed source's content from context or prior sessions.
