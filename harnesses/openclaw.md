# OpenClaw — Agent-First Gateway (not a Plain LLM Proxy)

**Priority:** Tier 1 · **Docs checked:** 2026-11-11. **Security:** shared-secret gateway access can act as an operator.

## Available surfaces

- **Gateway protocol** for rich native agent control and streaming over WebSocket.
- Opt-in OpenAI-compatible `POST /v1/chat/completions` and opt-in OpenResponses-style `POST /v1/responses` — both disabled unless enabled in gateway config. Additional `/v1/models`, embeddings surfaces vary by enabled endpoint/version.
- `POST /tools/invoke` on the gateway port directly invokes an allowed tool with agent policy context. This is **operator-level** functionality; never publish publicly without a proper trust boundary.
- Internal session orchestration tools (e.g. `sessions_list`, `sessions_send`, `sessions_spawn`, `sessions_history`) are agent tools and distinct from the external Gateway RPC client.

## OpenAI-compatible HTTP is agent-first

`model` is an OpenClaw **agent target**, not raw upstream LLM model:

| Request model | Meaning |
|---|---|
| `openclaw/default` | Stable alias to configured default OpenClaw agent |
| `openclaw/<agentId>` | Named configured agent |
| `openclaw` | Default agent (alias) |

To override the underlying provider/model, docs list `x-openclaw-model` (subject to caller auth/scope). Explicit `x-openclaw-session-key` can target a gateway session, and docs describe `user` as a stable application conversation key on Chat Completions. Keep provider model, agent ID and session key as different fields.

## Example request (enabled Chat endpoint)

```json
{
  "model":"openclaw/default",
  "user":"conversation-42",
  "messages":[{"role":"user","content":"Inspect the current workspace status."}]
}
```

Auth is gateway bearer credential or supported trusted proxy boundary; use loopback/tailnet/private ingress, not an unauthenticated public URL. The gateway's common default port is `18789` but must be discovered from actual installation.

## Direct tool invocation

```json
{"tool":"sessions_list","args":{},"sessionKey":"main"}
```

`POST /tools/invoke` accepts `tool`/`name`, optional `args`, `sessionKey`, `agentId`, `idempotencyKey` and other documented fields. Which tools are callable depends on policy. **Do not pass model API function-call envelopes** directly into `tools/invoke`. Use one direct tool action only when the caller is authorized; distinguish it from a full agent turn.

## Session and subagent control

- Gateway agent sessions persist under configured session store and routing rules. Use stable keys per UI conversation, never one shared main session for every end user.
- Built-in session tools can send work to, list and spawn subagents, often asynchronously. Track run/child session IDs and terminal outcome rather than guessing completion from task admission.
- Different gateway protocols may expose differing event detail; choose native Gateway protocol for rich state and approval UX, not only Chat delta text.
- `GET /v1/models` lists **agent targets**, not every upstream LLM model.

## Gotchas

1. HTTP Chat/Responses endpoints are opt-in. Verify enablement.
2. `model=openclaw/...` is **not** `anthropic/claude-*` or another upstream model identifier.
3. Shared token is not scoped customer identity; apply authenticated gateway boundary, do not reveal to browsers.
4. Don't equate direct `/tools/invoke` with long-running agent delegation.
5. A single tool invoke may have side effects; use `idempotencyKey` and reconcile before retrying where supported.

**Sources:** [Gateway](https://docs.openclaw.ai/gateway), [Chat API](https://docs.openclaw.ai/gateway/openai-http-api), [OpenResponses](https://docs.openclaw.ai/gateway/openresponses-http-api), [Direct tool invoke](https://docs.openclaw.ai/gateway/tools-invoke-http-api), [Session tools](https://docs.openclaw.ai/session-tool).
