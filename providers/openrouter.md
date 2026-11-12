# OpenRouter — Multi-Provider Gateway, Not One Uniform Model API

**Priority:** Tier 1 · **Checked:** 2026-11-11 · **Runtime probe:** essential for exact provider/model route.

## When to use

Use for model selection, multi-vendor routing, fallback, provider preference, and compatible Chat/Responses integrations. Do **not** treat it as proof that every upstream provider preserves every tool, reasoning, JSON schema, multimodal or streaming nuance.

## Chat API tool loop

For conventional OpenAI-compatible Chat clients use OpenRouter's configured base URL/API key and model ID. Tool specs are Chat-style nested `tools[].function` and assistant messages may return `tool_calls[]` with JSON-string arguments. **Your app executes user-defined tools**, appends every tool result with original `tool_call_id`, resends tool definitions (as OpenRouter's tool-loop guide stresses), and repeats until no tool calls or a bounded stop condition. Use [examples/chat_compatible_loop.py](../examples/chat_compatible_loop.py) with `MODEL_BASE_URL=https://openrouter.ai/api/v1`.

## Route awareness

- Request can select or influence provider routing; a model alias may reach different upstream endpoints. Record resolved model/provider route where the API exposes it.
- Official docs describe `provider` routing preferences, provider ordering, endpoint targeting, and `require_parameters` to filter providers that don't support requested parameters. **Parameter acceptance is not equivalent to identical semantics or quality.**
- Provider fallbacks can change the upstream without the app changing model ID. For capability-critical operations, constrain route or verify fallback equivalence.
- Distinguish user-defined client tools (`type:function`) from OpenRouter-managed `openrouter:*` server tools and plugins. Server tools execute at OpenRouter, while app-defined functions require app execution.

## Tool result and stream caveats

- Keep all tool definitions on subsequent turns; validate JSON strings and return one result per tool call ID.
- Stop conditions: no tool calls, max agent iterations, repeated failed identical call, user cancellation, budget exhausted. A network error is not itself a tool-result error.
- If using OpenRouter Responses rather than Chat, follow **its Responses documentation and test target**; do not mechanically swap Chat and Responses fields.
- Provider-specific reasoning, tool search, file parsing, prompt caching and structured-output support may be transformed or require extra flags. Verify per route.

## Recommended production policy

1. Configure provider allowlist/order and fallback policy explicitly for critical workflows.
2. `require_parameters` can help filter unsupported parameters, but keep integration tests.
3. Store upstream route/model along with API-level model ID for postmortems.
4. Never replay side-effectful tools after gateway failure without reconciliation.
5. If you need precise Gemini thought signatures or Anthropic native content blocks, prefer their native endpoints unless OpenRouter's exact route/endpoint is demonstrably compatible.

**Sources:** [Provider selection](https://openrouter.ai/docs/guides/routing/provider-selection), [Tool-calling guide](https://openrouter.ai/blog/tutorials/build-tool-calling-agent-loop/), [Server tools](https://openrouter.ai/docs/guides/features/server-tools/overview), [API reference](https://openrouter.ai/docs/api/reference/overview).
