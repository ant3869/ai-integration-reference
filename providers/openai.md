# OpenAI API — Responses vs Chat Completions

**Priority:** Tier 1 · **Verified against:** official OpenAI developer docs, 2026-11-11 · **Test status:** documentation checked; runtime/model-specific probe required.

## Endpoint selection

- **Responses:** `POST https://api.openai.com/v1/responses`; recommended native path for stateful/reasoning/tool-rich workflows. SDK `OpenAI().responses.create(...)`.
- **Chat Completions:** `POST https://api.openai.com/v1/chat/completions`; familiar compatibility baseline. SDK `OpenAI().chat.completions.create(...)`.
- Auth: bearer `OPENAI_API_KEY`; don't expose secrets to browser/remote untrusted clients. See [official guide](https://developers.openai.com/api/docs/guides/function-calling).

## Tool call contract: Responses (native)

```json
{
  "model": "<runtime-selected-model-id>",
  "input": [{"role":"user","content":"Multiply 7 and 9 using the tool."}],
  "tools": [{
    "type":"function","name":"multiply","description":"Multiply two integers.",
    "parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"],"additionalProperties":false},
    "strict":true
  }]
}
```

Model-generated `response.output` may include an item like:

```json
{"type":"function_call","name":"multiply","call_id":"call_abc","arguments":"{\"a\":7,\"b\":9}"}
```

Execute client-side, then continue with:

```json
{"model":"<same-model>","previous_response_id":"<response.id>","input":[{"type":"function_call_output","call_id":"call_abc","output":"63"}]}
```

**Important:** the JSON snippets use **descriptive IDs/model placeholders** and illustrate contract shape; never send placeholder values to a live API. `arguments` is serialized JSON text; `call_id` must match exactly. The second request can carry `tools` again when the model may need further tools. A response may contain multiple function calls; complete all calls or account for each failure. `response.output_text` is a useful SDK convenience **for text**; it is not a substitute for iterating `response.output` for tool calls.

**Working Python:** [examples/openai_responses_loop.py](../examples/openai_responses_loop.py).

## Tool call contract: Chat

```json
{"tools":[{"type":"function","function":{"name":"multiply","description":"Multiply integers","parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}}]}
```

The assistant reply has `choices[0].message.tool_calls[]` and each `function.arguments` is a JSON string. Append the **full original assistant message**, then a tool result for each call:

```json
{"role":"tool","tool_call_id":"<tool-call-id>","content":"63"}
```

Then resend messages. **No Chat Completions `tool_call_id` should be used as a Responses `call_id` unless translated and correlated in your adapter.** [Official function calling](https://developers.openai.com/api/docs/guides/function-calling).

## Conversation/reasoning

- Responses: use `previous_response_id`, a supported conversation resource, or replay response items. When replaying manually, retain the appropriate reasoning items, ordering, tool calls and tool outputs. Some reasoning content is opaque and may be carried as encrypted state; never synthesize it.
- Chat: application owns full `messages` history, not a persisted `previous_response_id` link. Chat history does not carry the same native reasoning items.
- On switching model *families*, reasoning continuity is not guaranteed; verify compatibility and preserve visible transcript in your application.
- Detect `status`, `incomplete_details`, refusals and request failures; don't assume all non-error HTTP responses are complete.

## Structured output and streaming

- Responses structured outputs use `text: {"format": {"type":"json_schema","name":"...","schema":{...},"strict":true}}` (the exact `name` is required in the schema config). Chat uses `response_format: {"type":"json_schema","json_schema":{...}}`.
- Strict schema: object `additionalProperties:false`, all fields required (nullable values for logical optional), supported JSON Schema subset; handle refusals and max-token incompleteness explicitly.
- Streaming Responses has typed `response.*` events (e.g. output item added/complete, function arguments deltas/done, completion); Chat streams `choices[].delta` with tool-call fragments and a finish reason. Buffer before parsing.
- Tool-choice and parallel-call availability vary by model; probe the exact model.

## Files / media

Responses input is an array of messages/typed content parts (`input_text`, `input_image`, `input_file`, etc.). Use the documented Files and image input routes; file ID vs URL vs base64 may have different limits. **A URI is not automatically treated as a downloadable media attachment.** See [files guide](https://developers.openai.com/api/docs/guides/file-inputs) and [multimodal](../protocols/files-and-multimodal.md).

## Gotchas to remember

1. `output_text` can be empty when the model wants tools; inspect all output items.
2. Returning tool results in a **new user text prompt** is not the native contract.
3. Don't reuse `previous_response_id` across a different provider endpoint.
4. Keep opaque reasoning items intact in stateless mode; don't reformat them.
5. Use the right JSON-schema config for the API you actually called.

**Sources:** [Function calling](https://developers.openai.com/api/docs/guides/function-calling), [Reasoning](https://developers.openai.com/api/docs/guides/reasoning), [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Responses API](https://developers.openai.com/api/docs/guides/text), [SDK](https://developers.openai.com/api/docs/libraries).
