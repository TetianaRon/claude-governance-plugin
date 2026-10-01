# SESSION-WRAPUP
# session-discipline

Load this file at the natural close of a session, or before handing off to another model or surface.

---

Run through the following in order:

1. **Skill candidates** — review the session for any repeated logic, reusable pattern, or standalone workflow worth extracting as a global skill. Surface any candidates with a one-line rationale.
2. **Skill distribution** — if any skill zip or plugin archive was rebuilt this session and its distribution has not run, surface it as pending rather than closing over it.
3. **Produced-artifact persistence** — before producing a handoff or closing the session, check whether any document produced this session (a plan, a rewritten instruction file, or any other deliverable with a canonical repo or project-knowledge home) exists only as a chat attachment. If so, write it to that canonical location first.
4. **Housekeeping** — surface any unresolved questions, deferred decisions, or flagged items. Offer to log them.
5. **Pending issues** — draft an entry for every issue noticed this session and not yet drafted, under the skill named for issue logging under SKILL.md's Referrals.
6. **Plan sync** — if a plan was active this session, verify that any memory entries made during the session don't duplicate or contradict the plan. The plan is canonical; bring memory into alignment if needed, not the other way around.
7. **Continue or hand off** — only ask if it is genuinely unclear whether the session should close here or continue on another model or surface. Skip this step if the contributor has already indicated they are wrapping up, or if only housekeeping remains. When the choice is genuinely open, present:

```
Question: "All work done. Finish here or hand off to another model or surface?"
Options:
- Finish here — close out in this session
- Hand off — produce a handoff message for another model or surface
```
8. **Handoff message** — if handing off, produce a handoff message. Read workflows/model-handoff.md for format.
