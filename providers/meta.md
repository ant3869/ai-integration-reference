# Meta Model API — Muse Wonder / Muse Spark / Muse Ember

**Priority:** Tier 1 · **Official docs checked:** 2026-11-11 · **Runtime:** model/account capabilities must still be probed.

## Surfaces and auth

- Base URL: `https://api.meta.ai/v1` · auth bearer token in `MODEL_API_KEY`.
- Official docs expose OpenAI-style **Responses** (`/responses`) and **Chat Completions** (`/chat/completions`) plus an Anthropic-compatible **Messages** surface. For precise reasoning/tool behavior, choose **Responses** for multi-step work.
- Example model IDs in current docs include `muse-spark-1.3`, `muse-spark-1.3-contributor`, `muse-wonder-1.0`; use the account's available model catalog and do not hardcode historical snapshots globally.
- For a standard OpenAI Python SDK client, configure `base_url="https://api.meta.ai/v1"` and `api_key=os.environ["MODEL_API_KEY"]`.

## Tools

- **Responses:** flat `tools[]` entries; model emits `output[]` `type:function_call` with `call_id`, serialized arguments and status; app executes and returns `type:function_call_output` using `previous_response_id`. Meta documents built-in provider-side `web_search` and `tool_search` (distinct from your app-defined functions).
- **Chat:** nested `tools:[{type:function,function:{...}}]`; assistant `tool_calls[]`; append `role:tool` with `tool_call_id`, keep original assistant message and history.
- Meta custom `type:"custom"` tools are **Responses-only**; sending them to Chat returns HTTP 400.
- Meta documents function-name regex `^[a-zA-Z0-9_.-]+$` with **at most one dot** for function names. Multi-segment namespaced tool identifiers may require Meta namespace tools rather than sending multi-dot function names.
- Multiple tool calls may be present. Never assume the API runs app-defined functions.

## Reasoning — a known model-specific trap

| Endpoint | Field | Relevant restriction |
|---|---|---|
| Chat Completions | top-level `reasoning_effort` | Muse reasoning models reject `"none"` |
| Responses | `reasoning:{"effort":...}` | Same supported effort levels, per model |
| Muse Spark 1.3 | `minimal`, `low`, `medium`, `high`, `xhigh`, `max` | Docs show default `high` on Spark 1.3 |
| Muse Spark 1.3 Contributor | up to `xhigh` | **`max` is not supported** (HTTP 400) |
| Muse Wonder / Ember | model-specific supported efforts | Consult current model page; docs list default `max` |

For multi-turn reasoning, Responses can chain via `previous_response_id`, or use stateless encrypted reasoning replay with the provider's documented include and item formats. Human-readable reasoning summaries are **not** a substitute for encrypted reasoning state. Meta's documentation explicitly describes reasoning continuity with Responses rather than ordinary Chat history.

## Contributor vs standard — operational consideration

`-contributor` is a **different data-use mode**, not merely a pricing label. Official docs state submitted content **may be used to train future Meta models** for Contributor mode; Standard mode has different data-use rules. Route customer code/data according to the appropriate privacy policy and explicit configuration; do not auto-fallback from Standard to Contributor merely for price.

## Media

Muse Spark's docs list **text, image, video, audio, PDF input** and text output, subject to model/version behavior. Meta notes audio understanding on Spark 1.3 may be degraded. Choose media-specific model/endpoint and test real MIME, size and file handling rather than relying on broad capability labels.

## Failure checklist

- Inspect `HTTP 400` for unsupported reasoning efforts, invalid multi-dot function names, or custom-tool use on Chat.
- Confirm chosen protocol and model; Chat tool result and Responses tool result are not interchangeable.
- On retries and route changes, preserve exactly the proper reasoning items/call IDs.
- Set privacy-aware model selection explicitly (Contributor vs Standard).

**Sources:** [Meta overview](https://dev.meta.ai/docs/overview), [Muse Spark](https://dev.meta.ai/docs/muse-spark), [Tool calling](https://dev.meta.ai/docs/tool-calling), [Reasoning](https://dev.meta.ai/docs/reasoning), [Responses protocol](https://dev.meta.ai/docs/protocols/responses), [Choose a model](https://dev.meta.ai/docs/choose-a-model).
