# Local Models — Ollama, LM Studio, vLLM/SGLang Orientation

**Priority:** Tier 1 for local dev · **Docs checked:** 2026-11-11. Feature fidelity depends heavily on model, template, local server and hardware.

## Ollama: native API

- Base native URL default `http://localhost:11434`; `POST /api/chat` for native chat, `GET /api/tags` for native model discovery. The Python/JS Ollama SDK wraps this.
- Native `tools` are OpenAI-Chat-like definitions, but function call `arguments` may be an **object**, not JSON text, and tool result uses **`role:tool`, `tool_name`, `content`**. Example:

```json
{"role":"assistant","tool_calls":[{"type":"function","function":{"name":"multiply","arguments":{"a":7,"b":9}}}]}
{"role":"tool","tool_name":"multiply","content":"63"}
```

The two JSON objects above are sequential **message entries** (not one JSON document). Append tool result, resend conversation and tools as needed. Ollama has a separate OpenAI-compatibility surface; do not pass native object arguments through a Chat parser that assumes a JSON string.

## LM Studio: OpenAI compatibility

- Default documented local OpenAI-compatible base URL `http://localhost:1234/v1` (only after server is started).
- Docs list `/v1/chat/completions`, `/v1/responses`, `/v1/models`, `/v1/embeddings` among endpoints; select by actual local server version and model support.
- Tool use goes through both the **model chat template** and **LM Studio parser**. Native tool support vs default/fallback prompting changes fidelity; model may print pseudo-tool syntax in `content` rather than structured tool calls when parsing fails. **Endpoint 200 is not proof tool call works.**
- Query local model list; never assume the model loaded in UI is the same ID the API expects. Media/tool capability varies per model.

## vLLM / SGLang / other OpenAI-style local servers

- Their API surfaces and tool parser flags/config vary by version/model. Do not guess universal tool support from an OpenAI-compatible URL. Verify actual `GET /v1/models`, tool response shape, streaming, `parallel_tool_calls`, structured output and reasoning options on exact server image.
- For smaller local models prefer **simple schemas** and **few tools**, and measure success rate through actual tool-loop tests rather than relying on marketing support.

## Environment/security

- Keep local inference servers on loopback/private network or add authenticated reverse proxy. A local endpoint is not inherently private once bound publicly.
- Local model memory/context usage, prompt caching, GPU offload, load/unload, idle deadlines, prompt templates and thinking controls are engine-specific; don't assume the provider cloud default.
- Use [examples/chat_compatible_loop.py](../examples/chat_compatible_loop.py) for compatible Chat paths; native Ollama requires the native argument/result adapter above.

**Sources:** [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling), [Ollama API](https://docs.ollama.com/api/introduction), [LM Studio OpenAI compatibility](https://lmstudio.ai/docs/developer/openai-compat), [LM Studio tool use](https://lmstudio.ai/docs/developer/openai-compat/tools), [OpenClaw local backend guidance](https://docs.openclaw.ai/gateway/local-models).
