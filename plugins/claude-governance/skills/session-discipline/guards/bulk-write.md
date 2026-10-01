# Bulk writes and dispatch | session-discipline

**Load when:** about to execute many similar external writes built from one pattern (N pages, N tickets, N files from one template), about to run a single oversized fetch, or about to dispatch several fetches or subagents together.

---

## Canary first

Write one instance, stop, and confirm it rendered or saved correctly before repeating the pattern across the rest of the batch.

⏸ HUMAN CHECKPOINT [Token] — where the canary is confirmed by contributor review rather than an automated read-back, wait for that confirmation before continuing.

## Chunks

A batch above a handful of items runs as chunks, with a checkpoint between chunks rather than one continuous run. Each chunk's completed items are recorded somewhere a later session can read, so a stopped session resumes from the last completed chunk.

## Oversized single fetch

Before a single large read — a big page, a big file, a wide multi-page pull — propose a scoped mini-plan: what will be read, in what order, and where the pause points are.

## Concurrent dispatch

Several fetches or subagents dispatched together follow the same scoping: propose the batch, bound how many run at once, and chunk it where it is large. A dispatched subagent writes its results as it goes, so a run stopped part-way leaves its completed units behind.

---

## Behavioural rules

- A batch of roughly three or more similar external writes starts with one canary, confirmed before the rest
- A batch above a handful of items runs in chunks, with completed chunks recorded
- A single oversized fetch starts from a proposed mini-plan
- Concurrent dispatch is bounded in width and chunked like a sequential batch
