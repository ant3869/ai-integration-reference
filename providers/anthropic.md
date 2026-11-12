# Anthropic Claude — Messages API (not Claude Code)

**Priority:** Tier 1 · **Documented:** 2026-11-11 · **Runtime probe:** required.

## Core request shape

- Native endpoint: `POST https://api.anthropic.com/v1/messages` (Python: `anthropic.Anthropic().messages.create`). Auth is `x-api-key` plus versioned vendor HTTP headers; use the SDK to handle defaults.
- `model`, `max_tokens`, `messages`, optional `system` and `tools` are typical request fields. **A model API call does not give you Claude Code's filesystem tools or persistent local sessions.**

```json
{
  "model":"<runtime-selected-claude-model>",
  "max_tokens":1024,
  "messages":[{"role":"user","content":"Multiply 7 by 9 using the tool."}],
  "tools":[{"name":"multiply","description":"Multiply two integers.","input_schema":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}]
}
```

When `stop_reason == "tool_use"`, collect **all** assistant blocks of `type:"tool_use"`, each with `id`, `name`, `input` (an **object**). Add the entire assistant message to history, run the relevant tools, then add a **user** turn containing result blocks:

```json
{"role":"user","content":[{"type":"tool_result","tool_use_id":"<returned-tool-id>","content":"63"}]}
```

Use `is_error:true` when a client-executed tool fails, preserve request/response order, and repeat while `stop_reason == tool_use`. Terminal states also include `end_turn`, `max_tokens`, `pause_turn`, refusal and other model/version-specific stop reasons; do not treat all non-tool states as success. [Tool-use guide](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works).

## Client vs provider tools

- **Client-executed:** your custom function tools and certain Anthropic-defined client schemas such as shell/edit/computer. You execute them and send `tool_result`.
- **Server-executed:** supported web search/fetch, code execution and tool search execute on Anthropic infrastructure; do not manufacture client tool results. Some flows can pause or combine server and client work.
- JSON-schema tool definitions use `input_schema`, not OpenAI Chat's `function.parameters` or Gemini's `tools[].parameters`.
- Fine-grained tool streaming can emit partial arguments; do not parse before completion.

## Conversation and beta thread distinction

- The normal Messages API accepts client-managed conversation history.
- Anthropic also documents a **beta message threads** feature (`thread: {type:create|continue, ...}` and an SDK helper using a beta header). Threads are short-lived (docs specify inactivity expiry around five minutes and replay fallback); the application must retain full history to recover. Do **not** treat this as a durable agent-workspace session.
- Claude **Agent SDK `session_id`** refers to a different, local harness history. See [Claude Code](../harnesses/claude-code.md).

## Streaming / structured output / files

- Streamed Messages use `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_delta`, `message_stop` event families; content blocks may contain text, tool input, thinking, and provider tools. Preserve order.
- Structured-output tooling and strict parameters are feature/version dependent; consult active API docs and do not equate with OpenAI strict JSON schema behavior.
- Image and document content uses typed blocks (sources such as base64, URL, file reference depending on API/product). Image, PDF and file API constraints differ; consult current docs. Don't embed binary bytes as plain message text.

## Implementation traps

1. Passing `tool_result` as an assistant block rather than a **user** block.
2. Failing to pass the whole preceding assistant content, including non-tool blocks required by continuation.
3. Calling `messages.create` expecting the harness to run Bash, edit repo files, or prompt for user approval.
4. Treating a short-lived beta message thread as long-term durable storage.
5. Losing a streamed `tool_use` block boundary or mistakenly parsing partial JSON.

**Working Python:** [examples/anthropic_messages_loop.py](../examples/anthropic_messages_loop.py).

**Sources:** [API primer](https://platform.claude.com/docs/en/claude_api_primer), [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works), [Messages API](https://platform.claude.com/docs/en/api/messages), [Message threads](https://platform.claude.com/docs/en/build-with-claude/message-threads), [Agent SDK comparison](https://code.claude.com/docs/en/agent-sdk/overview).
