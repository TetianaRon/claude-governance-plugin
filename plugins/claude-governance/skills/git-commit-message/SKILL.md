---
name: git-commit-message
description: >
  Compose a Git commit message following the seven rules from cbea.ms/git-commit.
  Trigger ONLY on explicit requests to write a commit message — phrases like
  "write a commit message", "draft a commit", "compose a commit", "commit
  message for this", or when other instructions explicitly tell Claude to
  produce a commit message. Do NOT trigger when commits are mentioned
  incidentally (e.g., "I'll commit this later" or "this commit broke something"
  — those aren't requests). By default, combine three sources for the message —
  the user's description (if any), work done in the current session, and the
  actual git changes (run `git status` and `git diff --staged` or `git diff`).
  Compose only — never run `git commit` unless explicitly asked.
---

# Git Commit Message

**Version:** v1.0

You're being asked to write a Git commit message. Apply the seven rules from cbea.ms/git-commit and source the substance from the actual work.

## When to use

Trigger only on explicit request:

- "Write a commit message"
- "Draft a commit"
- "Compose a commit"
- "Commit message for this work / for what we did"
- Or when other instructions explicitly direct Claude to produce a commit message

Don't trigger on incidental mentions of commits — "let me commit this later" or "the previous commit broke X" are not requests for a message.

## Default to subject-only

The most important thing this skill can do is *not* over-write.

Most commits don't need a body. A clear, well-formed subject line is often the entire message — and that's the right answer when the change is small and self-evident:

```
Fix typo in onboarding email
```

```
Upgrade the HTTP client dependency
```

```
Update README with new install steps
```

If the diff plus the subject already tells the story, stop there. Don't pad. Don't bullet-list what changed. The reader can run `git show` if they want details.

A body is added *only* when the subject genuinely can't carry the context alone. See "When a body is warranted" below.

## Sourcing the message

Unless the user says otherwise, combine three sources:

1. **Any description the user gave.** If they said "write a commit for the rate-limit work", that's the lead — frame the message around it.

2. **Work done in the current session.** Scan the conversation for what was changed, what the user's intent was, and any "why" that surfaced. The session often contains the most useful "why" context — capture it.

3. **Actual git state.** Run `git status` and `git diff --staged` (or `git diff` if nothing is staged) to see what's actually being committed. Cross-reference with #1 and #2 — flag any meaningful gap (e.g., session implies one change but diff shows another).

If the user explicitly tells you to use a different source — e.g., "just format this description, don't read the diff" — follow that.

## The seven rules

### 1. Separate subject from body with a blank line

If the message has a body, leave exactly one blank line between subject and body. Git's tooling (`log --oneline`, `shortlog`, `format-patch`, `rebase`) depends on this separation.

### 2. Limit the subject to ~50 characters

50 is a target; 72 is the hard ceiling (GitHub truncates beyond it). If the change can't be summarized in 50 chars, the commit is probably doing too much — note this to the user, and either propose a tighter framing or suggest splitting.

### 3. Capitalize the subject

`Add user auth`, not `add user auth`.

### 4. No period at the end of the subject

`Add user auth`, not `Add user auth.`

### 5. Use imperative mood in the subject

The subject should complete the sentence: *"If applied, this commit will ___."*

Good:
- "Refactor billing module for clarity" → *If applied, this commit will refactor billing module for clarity.* ✓
- "Update getting-started docs" → ✓
- "Remove deprecated pricing endpoint" → ✓

Bad:
- "Refactored billing module" (past tense)
- "Refactoring billing module" (present participle)
- "Various billing fixes" (descriptive — doesn't say what it does)
- "More fixes" (says nothing)

Test every subject by mentally prepending *"If applied, this commit will"*. If the result isn't a coherent imperative, rewrite.

The imperative is required only in the **subject**. The body can be normal prose.

### 6. Wrap the body at 72 characters

Git doesn't wrap body text — wrap manually at 72 columns. This keeps lines readable in `git log` and email-format patches.

### 7. The body explains *why*, not *what was changed*

The diff already shows what changed. The body is for everything `git log -p` doesn't tell you: the reasoning, the constraint, the tradeoff.

The cbea.ms framing says it well: *"the way things worked before the change (and what was wrong with that), the way they work now, and why you decided to solve it the way you did."* That's what belongs in a body — code is generally self-explanatory about the rest.

**Don't narrate the diff.** This is the most common failure mode. Even careful writers drift into "renamed X to Y," "moved Z into A/," "updated asset paths" — content that's already in the diff. Cut it.

#### What that looks like in practice

✗ **Diff narration** — what `git log -p` already shows:

```
Move retry logic into the HTTP client

- Moved the retry loop out of the orders module
- Removed the retry loop from the payments module
- Added a retry loop to the HTTP client
- Updated imports in both modules
```

✓ **Intent and tradeoffs** — what the diff doesn't show:

```
Move retry logic into the HTTP client

Orders and payments each ran their own retry loop, with different
backoff and no shared limit, so an outage multiplied request volume.
One loop in the client applies the same backoff everywhere.

Retries stay capped at three, the limit orders already used.
```

The first lists what changed; the diff already does that. The second explains why anyone would do this and surfaces one tradeoff.

#### Length sniff test

If the body is mostly bullet lists of "what moved where," it's narrating. Cut and replace with reasoning.

Even a multi-phase refactor's body shouldn't need to be longer than a paragraph for the goal plus a sentence or two for any non-obvious decisions. If the body is approaching 20+ lines and most of it reads like an inventory, ask yourself: *"would a thoughtful reviewer ask why we did each of these things, or are they obvious from the diff?"* The answers that aren't obvious are the only ones that need to be in the body.

## When a body is warranted

A body is justified only when one or more of these apply:

- The "why" isn't obvious from the diff
- The commit ties together changes across files in a way the diff doesn't
- There's a side effect, breaking change, deprecation, or tradeoff worth flagging
- An issue/ticket should be referenced
- A future maintainer (including the user) is likely to ask "why did we do this?"

When in doubt, two sentences explaining the reasoning beats both no body and a sprawling one. Aim for the smallest body that covers the why.

## Check the format

Before presenting the message, save it to a scratch file and run:

```
python3 <skill-dir>/scripts/check_commit_message.py <message-file>
```

`<skill-dir>` is the directory reported when this skill loaded. Fix every error it reports. It checks the mechanical rules — subject length, capital, trailing period, the blank line, body wrapping — and not the imperative mood or the content, which stay yours to judge.

## Output format

Return the commit message inside a single fenced code block, ready to paste. Don't add commentary inside the message.

Example of a subject-only commit:

````
```
Fix typo in onboarding email
```
````

Example of a commit with a short body:

````
```
Check the feature flag in request middleware

The flag was checked in each controller, so every new controller
had to remember the call. Checking it once per request in
middleware applies it uniformly and removes the duplicated calls.

Default behavior is unchanged for tenants without the flag.

Refs: <ticket-id>
```
````

If you want to flag tradeoffs, suggest splitting into multiple commits, or note that the diff and the user's description disagree, do so **outside** the code block, after the message. Never put meta-commentary inside the message itself.

## Compose, don't commit

This skill produces the message. It does **not** run `git commit`. If the user wants the message committed after composing, they'll say so separately.

## Handle ambiguity

If the change is genuinely ambiguous — large unfocused diff, no description, session context unclear — ask one targeted clarifying question before producing the message. Don't fabricate the "why" from thin air.

Where the question is whether to split, ask it as a structured choice:

```
Question: "The diff holds two unrelated changes. One commit or two?"
Options:
- One commit
- Split into two
```

Where the motivation is missing, ask for it in one plain question: "I see the change but not the motivation — what problem were you solving?"

Ask only when the gap matters. Don't pepper the user with clarifications when the work doesn't warrant it.
