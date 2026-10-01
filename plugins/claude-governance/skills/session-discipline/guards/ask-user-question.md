# Structured questions | session-discipline

**Load when:** about to call AskUserQuestion, or to deliver a file in a turn that also asks a question.

---

## Keep it short

Questions are brief, and option descriptions short. Where AskUserQuestion has already failed to return once in the session, the same question is asked as plain text rather than retried.

## One rendered element per turn

- **A file delivery takes its own turn.** Never call AskUserQuestion in the same turn as a file delivery; the pairing suppresses the file's interactive card. Deliver the file alone, then ask in the following turn.
- **A question about a just-delivered file is plain text**, answered with a regular message.
- **A question sharing a message with any other rendered element** — a quote, a code block, a table — carries one extra option: label "Content not fully visible", description "I don't see the full content of your message." Where the contributor selects it, re-send the affected content as plain text in the next turn, and raise the pairing as a noticed workflow issue, naming the elements the message paired.

---

## Behavioural rules

- Keep questions and option descriptions short; after one failed return, ask in plain text
- Never pair a question with a file delivery in one turn
- A question sharing a message with another rendered element carries the "Content not fully visible" option
