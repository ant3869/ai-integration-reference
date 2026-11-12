# Streaming, Structured Output & Terminal States

## Streaming is not one format

| Surface | Common stream concept | Completion guard |
|---|---|---|
| OpenAI Responses | typed SSE events (`response.output_item.*`, `response.function_call_arguments.*`, `response.completed`, error/incomplete) | terminal Response event/status; tool call arguments complete |
| OpenAI Chat / compatible | streamed `choices[].delta` with content/tool call fragments and finish reason | final choice/stream end + `finish_reason`; SDK may aggregate |
| Anthropic Messages | `message_start`, `content_block_start/delta/stop`, `message_delta`, `message_stop` | `stop_reason`, all content blocks closed |
| Gemini Interactions | typed interaction steps/events and statuses | interaction `completed`, `requires_action`, error etc; provider-specific event mapping |
| Hermes API Server | SSE `assistant.delta`, `tool.started`, `tool.completed`, `run.completed` | `run.completed` or documented failure/cancel event, not text delta |
| Codex / Claude Agent SDK | harness SDK events, tool events, final result | SDK's final run/turn status; process-level errors separately |
| OpenClaw Gateway | Gateway events / opt-in Chat or Responses streams | per-interface terminal/child-session status |

## Safe buffering algorithm

1. Read event stream incrementally; preserve chronological order.
2. Separate visible text deltas from function-argument deltas, reasoning metadata and status/usage.
3. Key tool fragments by provider call ID and/or stream choice/index (depending on contract); avoid merging parallel calls.
4. Only parse JSON arguments on the protocol's **complete-tool-call event**, not on first `{` or punctuation.
5. Create a pending tool request; validate/auth before execution. For an in-flight tool triggered by a streamed model, ensure complete declaration and stable ID.
6. Terminal status can be `complete`, `requires_tool`, `incomplete`, `refused`, `canceled`, `error`, `unknown`; don't flatten into a single boolean.
7. On transport disconnection, query session/response status where supported; don't re-execute writes simply to get a clean UI event.

## Structured output is not tool output

- **JSON mode** aims at valid JSON text; **strict structured output** constrains a supported schema subset. They aren't equivalent; refusal, token limit and upstream gateway behavior remain exceptions.
- **Function arguments** are requests to invoke tools; they need validation **even if** the provider advertises strict tool schemas. The tool's execution result is not automatically a JSON-schema-constrained model final answer.
- OpenAI Responses uses `text.format` for structured output, Chat uses `response_format`; model support differs.
- Anthropic, Gemini, Meta and OpenRouter have their own structured output options; map exact schema subsets and handle unsupported keywords explicitly.
- Schema should represent only required fields and acceptable nullable values; validate again in the app before side effects.

## Telemetry to record

`request_id`, `run_id`, `session_id`, `target`, `model`, `upstream_route`, `stream_event_type`, `tool_call_id`, `tool_name`, `tool_status`, `final_status`, `stop_reason`, `usage`, `duration_ms`, `error_code`, `retry_count`, `approval_decision`. Redact sensitive arguments and never log API keys or opaque reasoning blobs by default.

**Sources:** [OpenAI streaming](https://developers.openai.com/api/docs/guides/streaming-responses), [Claude streaming](https://platform.claude.com/docs/en/build-with-claude/streaming), [Gemini Interactions](https://ai.google.dev/gemini-api/docs/interactions-overview), [Hermes API server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server), [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
