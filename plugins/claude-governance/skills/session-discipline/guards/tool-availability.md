# Tool availability | session-discipline

**Load when:** a system reminder or a prior message states a connector or server needs authentication or is unavailable, and Claude is about to tell the contributor a capability is blocked.

---

## Verify before reporting

1. Search the session's available and deferred tools for the capability itself (the service's name, or the action needed), not for the server the reminder named. A plugin often ships its own connector for a service already authorised elsewhere in the session under a different tool prefix.
2. Where a candidate turns up and the result is still ambiguous, make one cheap read-only call to it.

Report the capability as blocked only once both come up empty. Where it is blocked, say so and name what the contributor can do to authorise it.

---

## Behavioural rules

- Never report a capability as unavailable before searching for it by capability and trying one read-only call to any candidate
