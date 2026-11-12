# Tool-Calling Protocols — Exact Boundaries

## The universal rule

A **custom tool definition** tells a model what it *may request*. A **tool-call event** is a request to the application. Your application validates, authorizes, executes, and returns the result using the **original invocation identifier**. A harness may instead own that whole loop. Server-side tools are an explicit exception: vendor executes those.

## Minimum schema translation (illustrative multiply tool)

**OpenAI Responses / Meta Responses**

```json
{"type":"function","name":"multiply","description":"Multiply integers","parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"],"additionalProperties":false}}
```

**OpenAI Chat / typical OpenRouter Chat / LM Studio Chat**

```json
{"type":"function","function":{"name":"multiply","description":"Multiply integers","parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}}
```

**Anthropic Messages**

```json
{"name":"multiply","description":"Multiply integers","input_schema":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}
```

**Gemini Interactions**

```json
{"type":"function","name":"multiply","description":"Multiply integers","parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}
```

**Ollama native** uses Chat-like tool declaration but returns native object `arguments`; tool result uses `tool_name`, not `tool_call_id`. **Gemini generateContent** uses `functionDeclarations` and `functionResponse` parts, not Interactions steps.

## Cross-protocol result correlation

| Protocol | Invocation identity | Result holder |
|---|---|---|
| Responses | `call_id` in `function_call` | `function_call_output.call_id` |
| Chat | `tool_calls[].id` | `role:tool, tool_call_id` |
| Claude Messages | `tool_use.id` | `tool_result.tool_use_id` in **user** content |
| Gemini Interactions | `function_call.id` | `function_result.call_id` |
| Gemini generateContent | `functionCall` name/(id where present) | `functionResponse` part, preserve thoughtSignature |
| Ollama native | `function.name` + native call context (API-specific ID may differ) | `role:tool,tool_name` |
| MCP | JSON-RPC request ID for `tools/call` | JSON-RPC response with matching ID (tool result may include `isError`) |

## Safe app-managed tool-loop state machine

`MODEL_REQUEST → RECEIVE_RESPONSE → extract N calls → validate/authorize each → execute each at most once → assemble N results → CONTINUE_MODEL_REQUEST → ... → FINAL | ERROR | CANCELED`.

- **Zero calls**: final text only if terminal status indicates completed; an empty/incomplete response is not success.
- **One or many calls**: process all, preserve each ID; parallel execution only if independent and permitted.
- **Malformed args/unknown tool**: return a truthful structured tool error where supported; do not execute.
- **Write tool**: approval and idempotency or reconciliation before retry; cancellation may arrive after side effect.
- **Max iterations**: terminate with explicit incomplete status; avoid infinite tool loops.
- **Streaming**: text deltas are not tool invocations; tool-argument deltas must be buffered to final call completion before execution.
- **Harness**: don't externally run built-in tool event a second time.

## Implementation recommendations

Normalize the *logical tools*, not the wire envelopes. Store the raw protocol-specific message for accurate continuation and diagnostics. Map tool names through a registry; JSON Schema validation and authorization happen in your app independent of model claims. Keep `is_error` / error-state distinct from a normal successful result text.

**Source trail:** [OpenAI](https://developers.openai.com/api/docs/guides/function-calling), [Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works), [Gemini](https://ai.google.dev/gemini-api/docs/function-calling), [Meta](https://dev.meta.ai/docs/tool-calling), [Ollama](https://docs.ollama.com/capabilities/tool-calling), [MCP](https://modelcontextprotocol.io/specification/2025-11-25).
