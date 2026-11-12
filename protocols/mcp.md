# MCP — Model Context Protocol (Tools, Resources, Prompts)

**Specification baseline consulted:** 2025-11-25 version on [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-11-25) (checked 2026-11-11). Check for newer protocol revisions before implementation.

## Architecture

- **Host:** AI application/harness (Codex, Claude Code, OpenClaw, Hermes etc.) managing clients.
- **Client:** protocol connection maintained by host to a server.
- **Server:** offers tools, resources and prompts, and may support other optional features.
- **Transport:** JSON-RPC 2.0 over **stdio** or **Streamable HTTP**; HTTP+SSE transport is legacy (migration rules apply).
- **MCP is not an LLM inference API**, not a provider's `tool_calls` JSON shape, and not a persistent model conversation.

## Lifecycle

1. Initialize protocol version and capabilities; wait for initialized notification per spec.
2. Discover capabilities (`tools/list`, `resources/list`, `prompts/list` as applicable).
3. To invoke, call `tools/call` with tool name and arguments via JSON-RPC; parse `content`, structured content and `isError` when present.
4. Support protocol errors, cancellation, notifications and session transport rules as implemented. MCP transport session ID is not agent session ID.

Illustrative JSON-RPC call:

```json
{"jsonrpc":"2.0","id":17,"method":"tools/call","params":{"name":"multiply","arguments":{"a":7,"b":9}}}
```

## Bridging MCP into native model tools

A host may list MCP tool schemas and translate them to the active model tool declaration. On invocation, the host calls the MCP server and translates returned content into **that provider's** native tool-result shape. **Your app owns this bridge unless the harness's MCP client already does.**

Example: Gemini Interactions `function_call` → app's MCP client `tools/call` → `function_result` with matching Gemini `call_id`. The MCP JSON-RPC ID is a distinct inner request ID, **not** the Gemini `call_id`.

## Transport security gotchas

- **stdio:** newline-delimited JSON-RPC only on stdout. Logging belongs on stderr. No free-form print statements.
- **Streamable HTTP:** same MCP endpoint supports POST/GET as specified, with optional SSE; implement authorization, origin validation, network access controls and server capabilities as required.
- A model/tool description is untrusted text. Tools touching files, shell or credentials need explicit authority and human approval policies.
- Don't blindly forward OAuth bearer tokens or MCP tool prompts across tenants.
- If an MCP server dynamically changes tool catalog, refresh and re-validate mapping, permission and namespace conflicts.

**Sources:** [Specification](https://modelcontextprotocol.io/specification/2025-11-25), [Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports), [Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools).
