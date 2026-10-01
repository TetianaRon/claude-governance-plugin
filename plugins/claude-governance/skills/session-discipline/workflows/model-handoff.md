# MODEL-HANDOFF
# session-discipline

*Load this file only when the user has agreed to switch models mid-session.*

*Re-load and re-follow this file fresh every time a handoff is actually being produced — even if it was already loaded earlier in the session. Drafting a handoff from memory of this format, rather than reading it again at the moment of writing, is the failure mode this guards against.*

---

## When to switch

* Current model is more capable than the task requires (high-capacity model on mechanical work)
* Current model is less capable than the task requires (reasoning limits on hard work)
* Task scope has materially changed — planning → implementation, drafting → QA, research → writing

---

## How to prepare the handoff

When a switch is agreed, prepare a handoff message in the following format before the user changes models. Keep it short — the next model should be able to act on it without re-reading the full prior conversation.

Deliver the entire handoff — startup directive through Files to re-upload — inside a single fenced code block, with no prose sections split outside it. One clearly bounded block gives the contributor an unambiguous start and end and lets them copy it in one action, rather than a flat message they have to delineate by hand.

The handoff must begin with a startup directive so startup runs before the next model engages the task:

> **Start of session** — before acting on anything below, run this project's session startup first, then load the skills listed under "Required skills". Only then pick up the task.

Then include:

**Current model** — what was running this leg

**Recommended next model** — and a one-line reason

**Required skills** — the skills the next session needs loaded for this task: the project's startup skills plus any task-specific skills. List each by name — do not assume the next model will infer them.

**Work to date** — concise summary of what has been done

**Current state** — files and pages touched, their contents or state, anything in progress

**Decisions made** — explicit decisions that should not be re-litigated

**What the next model should pick up** — the immediate next task

**Open questions** — anything pending the user's input

**Files to re-upload** — any files uploaded in this session that the next session will need. List each file by its original filename. Do not reference session-specific upload paths — they will not resolve in the new session. Instruct the user to re-upload each file when starting the new session.

Before writing "None required," confirm every artifact the "What the next model should pick up" section depends on is saved to a durable location the next session can read, not only delivered in this session's chat. If one isn't yet durable, persist it first, or list it here instead of writing "None required."

---

## After the switch

The user pastes the handoff message into the new session as the first message and re-uploads any listed files.

The new model:

1. Runs the project's session startup first — this is the gate. Load the startup skills and any skills listed under "Required skills" before engaging the handoff task.
2. Acknowledges the handoff briefly
3. Confirms any open questions before proceeding — or proceeds immediately if there are none
4. Picks up at the next task
