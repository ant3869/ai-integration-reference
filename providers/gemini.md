# Google Gemini — Interactions, generateContent, and OpenAI Compatibility

**Priority:** Tier 1 · **Docs checked:** 2026-11-11. **Key update:** Google documents the **Interactions API** as GA (June 2026) and the recommended native path for new projects; `generateContent` remains supported as a legacy endpoint.

## Preferred for new agent workflows: Interactions API

- REST: `POST https://generativelanguage.googleapis.com/v1beta/interactions`, key via `x-goog-api-key: $GEMINI_API_KEY`.
- Python: `from google import genai; client = genai.Client(); client.interactions.create(...)`.
- `input` and typed `steps` represent the turn and timeline. A tool request is a `function_call` step with an `id`, name and parsed `arguments` object. The app executes and posts `function_result` step(s) matching `call_id`.

```json
{
  "model":"<runtime-selected-gemini-model>",
  "input":"Multiply 7 by 9 with multiply.",
  "tools":[{"type":"function","name":"multiply","description":"Multiply two integers","parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}]
}
```

Continuation after a `function_call` step:

```json
{
  "model":"<same-model>",
  "previous_interaction_id":"<prior-interaction-id>",
  "tools":[{"type":"function","name":"multiply","description":"Multiply two integers","parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}],
  "input":[{"type":"function_result","call_id":"<returned-step-id>","name":"multiply","result":[{"type":"text","text":"63"}]}]
}
```

**Important:** `previous_interaction_id` preserves history, **not** per-turn `tools`, `system_instruction`, or `generation_config`. Repeat them when needed. A response may have `status:requires_action`, `completed`, etc.; inspect `steps`, not just `output_text`. SDKs and REST versions may differ; validate.

## Reasoning/thought preservation

- Interactions separates thought steps with opaque signatures. In stateless use, replay **all model-generated steps exactly**, including thought/call steps, in the order required by docs. When using stateful `previous_interaction_id`, the server handles prior thought state.
- The older `generateContent` API represents `functionCall`, `functionResponse` and possibly `thoughtSignature` inside `Part` objects. If manually replaying generateContent history, preserve each signature in its original `Part`, do not merge or reorder. The official SDK handles this for typical flows.

## Legacy `generateContent` in existing projects

- Endpoint family `models/<model>:generateContent`; request `contents` array with role/parts and `tools:[{functionDeclarations:[...]}]`.
- Response `candidates[].content.parts[].functionCall` and follow-on user `functionResponse` part. **Not the same as Interactions `function_result`**.
- Remains supported. Migrate deliberately; do not rewrite without end-to-end tests.

## OpenAI-compatible Gemini shim

`https://generativelanguage.googleapis.com/v1beta/openai/` supports a **beta** OpenAI-library compatibility path. It is useful for conventional chat/tool apps, **not feature equivalence** with native Interactions or Files. Google's partner guidance recommends native Gemini for advanced file tools and provider-native features. Never assume thought signatures, model-level thinking parameters, built-in tools, media attachments or structured outputs map 1:1.

## Files and media

Google provides distinct native file-upload/input workflows and media limits. Do not send an OpenAI `input_file` object to native Gemini and expect it to work. Match media source and MIME to endpoint and model. See [file inputs](https://ai.google.dev/gemini-api/docs/file-inputs), [function calling](https://ai.google.dev/gemini-api/docs/function-calling), [multimodal](../protocols/files-and-multimodal.md).

## Gotchas

1. Mixing Interactions and generateContent wire types.
2. Omitting per-interaction `tools` when continuing a stateful interaction.
3. Dropping `thoughtSignature` in generateContent or thought steps in stateless Interactions.
4. Sending `function_result` with wrong `call_id`.
5. Assuming the OpenAI-compatible shim has native Interactions parity.
6. Treating incomplete/in-progress interactions as finished; background interactions must finish before chaining.

**Working Python:** [examples/gemini_interactions_loop.py](../examples/gemini_interactions_loop.py).

**Sources:** [Interactions overview](https://ai.google.dev/gemini-api/docs/interactions-overview), [Function calling](https://ai.google.dev/gemini-api/docs/function-calling), [Thought signatures](https://ai.google.dev/gemini-api/docs/thought-signatures), [OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai), [Partner integration](https://ai.google.dev/gemini-api/docs/partner-integration).
