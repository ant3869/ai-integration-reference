# Session Lifecycles, Event Ordering, Cancellation, Recovery

## Store these as distinct IDs

```text
application_conversation_id
└── target_session_ref: {kind, value, target_id}
    ├── run_id / turn_id
    │   ├── tool_call_id(s) → tool_execution_id(s)
    │   ├── approval_request_id(s)
    │   └── child_run_id(s)
    └── next run / turn
```

**Kinds:** `openai_response`, `gemini_interaction`, `anthropic_message_thread`, `codex_thread`, `claude_agent_session`, `hermes_session`, `openclaw_session`, `mcp_transport_session`. Not interchangeable. The app must also hold its **canonical transcript** and source-of-truth state snapshots so it can recover when external state expires or routes change.

## State machine (proposed)

`queued → running → (requires_tool ↔ running) → (requires_approval ↔ running) → completed`; failures and cancellation may happen at several points. Use terminal `completed | incomplete | failed | canceled | unknown`; avoid boolean `done`.

- **`requires_tool`**: returned client tool invocation, not necessarily execution started.
- **`requires_approval`**: human/policy decision required before running privileged tool.
- **`unknown`**: network/harness crash means outcome cannot be confirmed; reconcile before retry.
- **`incomplete`**: token limit, max iterations or truncation; surface partial text separately.
- **`canceled`**: cancellation acknowledged; beware a side effect may have occurred just before cancellation.

## Practical storage fields

```json
{
  "conversation_id":"app-generated-uuid",
  "target_id":"meta-prod-responses",
  "session_ref":{"kind":"openai_response","value":"provider-returned-id"},
  "workspace":"application-verified-worktree-path-or-null",
  "run_id":"app-generated-run-uuid",
  "status":"requires_tool",
  "pending_tool_call_ids":["provider-call-id"],
  "pending_approval_ids":[],
  "transcript_storage":"application-canonical-history",
  "last_event_sequence":14
}
```

These strings are **illustrative**, not live provider IDs. Encrypt sensitive logs/secrets at rest, redacting tool inputs where appropriate. Use a persistence store with atomic status/event updates rather than trusting UI state.

## Crash recovery algorithm

1. Load app session metadata and outstanding runs.
2. Ask native provider/harness for run/session state if supported.
3. For pending tool calls, check ledger for effects already performed; do **not** automatically execute again.
4. Reattach event stream or resume the session only with valid native reference. If external state is expired/lost, replay canonical transcript using a **fresh context** and flag any lost opaque state.
5. Restore stable workspace binding; if files changed or worktree missing, stop and require reconciliation.
6. Do not resurrect a previously denied approval.
7. Mark unconfirmable side effects `unknown` and surface to user/operator.

## Routing between agents

Each agent/harness has its own session. A mediator/orchestrator should store a **delegation record** containing parent run, child target, child session, objective, status, artifact paths, result summary, and error. Passing another agent's message as raw user/system instructions can cause authority confusion; preserve provenance and trust level.

**High-level delegation sequence**

1. Parent emits delegation request with stable app ID.
2. Mediator selects target via capability/perms/routing; creates child run.
3. Child accepts task; mediator acknowledges admission only.
4. Child reports progress and final terminal status.
5. Mediator supplies final result to parent or user; never treat admission as completion.

## Switching providers mid-conversation

Use the **app transcript** as transferable state; provider-only reasoning and short-lived message-thread/session metadata usually cannot be transplanted. Start a new target-native session and include a compact, attributed summary plus any necessary observable history. Report loss of opaque continuity as an expected constraint rather than a hidden bug.

## Event/UI projection rules

- Preserve raw event as well as normalized projection.
- Use monotonic sequence numbers per run; tolerate duplicate or out-of-order network delivery.
- Mark exact source of status: model output, harness event, verified filesystem side effect, or mediator inference.
- Track tool started and tool completed separately.
- Never show tool output as final assistant message by default; maintain provenance.

**Related:** [Adapter contract](adapter-contract.md), [Validation](../VALIDATION.md), [Gotchas](../GOTCHAS.md).
