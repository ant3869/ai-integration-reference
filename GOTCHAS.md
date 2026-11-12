# Integration Gotchas — Fast Failure Lookup

Each entry names a **documented protocol behavior** or **implementation risk**; use the linked source to confirm version/model specifics.

| Symptom | Likely issue | Correction / test |
|---|---|---|
| Tool request printed as text; nothing runs | A **model-generated call isn't an execution** | Register tool dispatcher; validate/authorize/execute; send result using original ID; repeat loop. [OpenAI](https://developers.openai.com/api/docs/guides/function-calling), [Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) |
| `function_call_output` rejected | Sent Chat-shaped tool message to Responses | Use `type:function_call_output` + original `call_id`, not `role:tool`. [OpenAI](https://developers.openai.com/api/docs/guides/function-calling) |
| Chat tool result rejected | Sent Responses-shaped output to Chat | Append original assistant tool-call message and each `role:tool` with original `tool_call_id`. [OpenAI](https://developers.openai.com/api/docs/guides/function-calling) |
| Claude tool result ignored | App put result in assistant message | Use a **user** message containing `tool_result`, matching `tool_use_id`, preserving preceding `tool_use`. [Claude](https://platform.claude.com/docs/en/claude_api_primer) |
| Tool arguments fail JSON parsing while streaming | Parsed partial delta | Buffer each call by stream index/ID; parse on completion. [Streaming](protocols/streaming-and-output.md) |
| Only first of multiple tools completes | Code assumed one call | Iterate over every invocation; return one result per ID; do not reuse IDs. [OpenAI](https://developers.openai.com/api/docs/guides/function-calling) |
| Gemini thinking tool loop fails / 400 | Dropped/rewrote thought signatures or function IDs | Use native Interactions `previous_interaction_id` or preserve all exact step/part state; SDK where possible. [Gemini](https://ai.google.dev/gemini-api/docs/thought-signatures) |
| Gemini continuation silently loses system/tools | Interactions params are *per interaction* | Re-send `tools`, `system_instruction`, generation settings on continuation. [Gemini](https://ai.google.dev/gemini-api/docs/interactions-overview) |
| Gemini native feature missing via OpenAI client | Compatibility shim is a subset | Use native Gemini API for advanced files/tools/thinking. [Google](https://ai.google.dev/gemini-api/docs/partner-integration) |
| Claude API 'session' disappears | Mistook short-lived beta message threads for durable harness sessions | Keep your own full history and replay on 404/expiration; do not confuse with Claude Agent SDK `session_id`. [Threads](https://platform.claude.com/docs/en/build-with-claude/message-threads) |
| Codex project resume starts fresh | Lost/recreated Codex thread ID | Store thread ID and call SDK resume / CLI resume. [Codex](https://developers.openai.com/codex/sdk/) |
| Codex or Claude Code gives plain text rather than actionable tool calls | Called underlying model API instead of harness | Use Codex SDK/app-server or Claude Agent SDK to get built-in workspace and tool execution. [Codex](https://developers.openai.com/blog/codex-as-a-platform), [Claude](https://code.claude.com/docs/en/agent-sdk/overview) |
| OpenClaw routes to wrong model | `model` field names OpenClaw agent target | Use `openclaw/default` or `openclaw/<agentId>`; use permitted `x-openclaw-model` override to select underlying LLM. [OpenClaw](https://docs.openclaw.ai/gateway/openai-http-api) |
| OpenClaw HTTP API returns 404 | Chat/Responses endpoint disabled by default | Enable intended endpoint and verify `GET /v1/models`; don't expose operator bearer token publicly. [OpenClaw](https://docs.openclaw.ai/gateway/openai-http-api) |
| Hermes UI loses previous context | Different session ID or gateway key per call | Use `/api/sessions/{id}/chat` or the documented gateway session key consistently; inspect session APIs. [Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server) |
| Meta 400 for `reasoning_effort=none` | Muse reasoning models don't support disabling | Use supported level (`minimal` etc), not `none`. [Meta](https://dev.meta.ai/docs/reasoning) |
| Meta 400 for `reasoning_effort=max` on Contributor | `muse-spark-1.3-contributor` excludes `max` | Use up to `xhigh` for that model; test exact version. [Meta](https://dev.meta.ai/docs/reasoning) |
| Meta tool name fails schema check | Name has >1 dot or invalid chars | Follow Meta's documented name regex/dot constraint. [Meta](https://dev.meta.ai/docs/tool-calling) |
| OpenAI strict schema rejects input | `additionalProperties:false`, all fields required, JSON Schema subset | Adjust schema; use nullable union for logical optional; validate locally. [OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs) |
| OpenRouter accepted parameter but it appears unused | Upstream route does not support every parameter | Use `provider.require_parameters:true` where supported; pin route and probe exact model+provider. [OpenRouter](https://openrouter.ai/docs/guides/routing/provider-selection) |
| Tool calling works in LM Studio only some of the time | Model chat template/parser mismatches tool format | Inspect native tool support vs default prompt/parser fallback; probe that model. [LM Studio](https://lmstudio.ai/docs/developer/openai-compat/tools) |
| Ollama native tool result doesn't match OpenAI Chat | Native args are objects; tool-result role uses `tool_name` | Use Ollama native shape or the separately documented compatibility API; don't merge them. [Ollama](https://docs.ollama.com/capabilities/tool-calling) |
| Gateway switching breaks ongoing reasoning | Opaque state bound to provider/model family/route | Preserve/replay compatible state or start new context; never fabricate encrypted reasoning. [OpenAI](https://developers.openai.com/api/docs/guides/reasoning), [Meta](https://dev.meta.ai/docs/reasoning) |
| MCP subprocess hangs / JSON parse fails | Logs printed to stdio stdout | stdout only MCP JSON-RPC messages; send logs to stderr. [MCP transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) |
| MCP tool connects but LLM does not call it | MCP connection doesn't automatically create provider tool schema | Bridge `tools/list` to model tools and `tools/call` back, or configure harness's MCP client. [MCP](https://modelcontextprotocol.io/specification/2025-11-25) |
| API works once then times out on file/image | URL blocked/expired, unsupported MIME, payload large | Use provider-supported upload/reference mode; check limits, private-IP safeguards, file retention. [Files](protocols/files-and-multimodal.md) |
| Duplicate side-effect after retry | Timed-out model result was retried without reconciling tool writes | Ledger by run/call ID, effect IDs, retry only known-safe requests; reconcile writes first. [Validation](VALIDATION.md) |
| 'tool success' surfaced after denial | Approval/permission is external to model output | Map `denied` separately from tool failure and model refusal; never coerce denial to success. [Architecture](architecture/session-and-events.md) |

## Troubleshooting order

`target type → endpoint → auth → model/agent ID → tool declaration → returned call shape → completion event → matching result ID → preserved state → permission → actual side effect`.

**Rule:** do not rewrite the entire provider adapter after one bad response. Capture the raw request/response with secrets redacted, reproduce the smallest failing round trip, and update one contract test.
