# Hermes Agent (NousResearch) — Gateway, Sessions, ACP and TUI RPC

**Priority:** Tier 1 for cross-agent work · **Official project docs checked:** 2026-11-11 · **Live installation may differ**.

## Integration options documented by project

| Surface | Transport | Best use |
|---|---|---|
| **API server** | HTTP REST + SSE | Web apps / orchestration + external session control |
| **ACP** | JSON-RPC over stdio | IDEs/hosts implementing Agent Client Protocol |
| **TUI gateway RPC** | JSON-RPC over stdio or WebSocket | More detailed session, slash command, approval and streaming controls |
| CLI | Local process | One-off use and configuration |

The Hermes agent owns its internal tools, memory, provider selection, MCP integrations, execution and session logic. An external application should **not** assume every event is a raw model function call.

## API server and auth

Project docs specify `API_SERVER_ENABLED=true` and `API_SERVER_KEY=<secret>` in `~/.hermes/.env`; API server uses configured gateway (example port `8642`) and bearer auth. Don't check secrets into repo. Documented OpenAI-style `/v1/chat/completions` makes simple frontend integration possible; **native session endpoints are better for persistent control**.

Native REST resources include:

- `GET /api/sessions` — list, page/filter sessions.
- `POST /api/sessions` — create session.
- `GET /api/sessions/{id}` and `/messages` — metadata/history.
- `POST /api/sessions/{id}/chat` — one synchronous agent turn.
- `POST /api/sessions/{id}/chat/stream` — SSE turn with events such as `assistant.delta`, `tool.started`, `tool.completed`, `run.completed`.
- `POST /api/sessions/{id}/fork` — branch; `PATCH`/`DELETE` manage metadata/session with version-specific rules.
- `GET /v1/capabilities` advertises available feature flags/endpoints in current docs.

Request body example for stream:

```json
{"input":"Inspect active tasks and give a concise status report."}
```

Use existing REST session ID in the **path**. Read the actual SSE event protocol and capability flags on the running server, including any current revision/identity preconditions. Hermes also documents gateway conversation keys (`X-Hermes-Session-Key`) in its API server implementation; keep that key distinct from immutable transcript/session IDs.

## Tool calls, provider routing and profiles

- Hermes tools include shell/file, browser, memory/recall, agent delegation, MCP and other toolsets depending on configuration. Tool gateway and external model provider are separate concerns.
- An HTTP compatible call can start/continue an agent turn, **not just generate raw model text**. Don't double-execute tools indicated in Hermes event stream.
- Gateway profiles/default model selection are installation-specific; query local status/config, don't hardcode profile names or ports from a different machine.
- Hermes may route tools via Nous Portal's Tool Gateway; verify current tool provider configuration rather than assuming API key means every tool is enabled.

## Resilience checklist

Capture `session_id`, declared conversation key, profile, model, task/job ID if present, event order and terminal state. SSE reconnect is not necessarily turn replay; re-query server state before reissuing a potentially side-effectful task. On 409/503, inspect current session/workflow status and preserve the error, rather than creating a fresh session silently.

## Pitfalls

1. Treating gateway model-call compatibility as proof every Hermes session API endpoint exists in installed version.
2. Losing session key when transitioning WebSocket/REST/CLI clients.
3. Treating `tool.started` as completed.
4. Passing an API server shared key to an untrusted browser.
5. Assuming local gateway profiles or port `8642` are universal defaults.

**Sources:** [Hermes programmatic integration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/programmatic-integration.md), [API server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server), [Tools](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools/), [Official repo](https://github.com/NousResearch/hermes-agent).
