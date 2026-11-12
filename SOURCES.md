# Sources and Maintenance Policy

**Research date:** 2026-11-11 (official documentation pages read during package preparation). **Important:** Sources may change after this date. Research verifies **documentation claims**, not live capability of any account, selected model, installed harness version or deployed route.

## Primary source index

| Group | Primary official docs checked |
|---|---|
| OpenAI Responses/tools | [Function calling](https://developers.openai.com/api/docs/guides/function-calling), [Reasoning](https://developers.openai.com/api/docs/guides/reasoning), [Structured output](https://developers.openai.com/api/docs/guides/structured-outputs) |
| OpenAI Codex | [Codex SDK](https://developers.openai.com/codex/sdk/), [Codex app-server](https://developers.openai.com/codex/app-server/), [Codex as platform](https://developers.openai.com/blog/codex-as-a-platform) |
| Anthropic Claude API | [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works), [API primer](https://platform.claude.com/docs/en/claude_api_primer), [Message threads](https://platform.claude.com/docs/en/build-with-claude/message-threads) |
| Claude Code | [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), [Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart), [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions) |
| Gemini | [Interactions overview](https://ai.google.dev/gemini-api/docs/interactions-overview), [Function calling](https://ai.google.dev/gemini-api/docs/function-calling), [Thought signatures](https://ai.google.dev/gemini-api/docs/thought-signatures), [OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai) |
| Meta Model API | [Overview](https://dev.meta.ai/docs/overview), [Tool calling](https://dev.meta.ai/docs/tool-calling), [Reasoning](https://dev.meta.ai/docs/reasoning), [Responses](https://dev.meta.ai/docs/protocols/responses) |
| OpenRouter | [Provider routing](https://openrouter.ai/docs/guides/routing/provider-selection), [Tool loop](https://openrouter.ai/blog/tutorials/build-tool-calling-agent-loop/), [Server tools](https://openrouter.ai/docs/guides/features/server-tools/overview) |
| Hermes | [Programmatic integration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/programmatic-integration.md), [API server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server), [Tools](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools/) |
| OpenClaw | [Gateway](https://docs.openclaw.ai/gateway), [Chat endpoint](https://docs.openclaw.ai/gateway/openai-http-api), [OpenResponses](https://docs.openclaw.ai/gateway/openresponses-http-api), [Tool invoke](https://docs.openclaw.ai/gateway/tools-invoke-http-api), [Sessions](https://docs.openclaw.ai/session-tool) |
| Code Puppy | [Homepage](https://code-puppy.dev/), [Commands](https://code-puppy.dev/pages/commands.html), [Configuration](https://code-puppy.dev/pages/configuration.html) |
| Local APIs | [Ollama tool calls](https://docs.ollama.com/capabilities/tool-calling), [LM Studio OpenAI-compatible](https://lmstudio.ai/docs/developer/openai-compat), [LM Studio tools](https://lmstudio.ai/docs/developer/openai-compat/tools) |
| MCP | [2025-11-25 spec](https://modelcontextprotocol.io/specification/2025-11-25), [Transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) |
| Tier 2 | [LiteLLM routing](https://docs.litellm.ai/docs/routing), [Groq tool support](https://console.groq.com/docs/tool-use/overview), [Mistral function calls](https://docs.mistral.ai/inference/conversations/function-calling), [xAI tools](https://docs.x.ai/developers/tools/overview) |

## Update protocol

1. For a failing adapter, check installed CLI/SDK version and current official documentation before editing.
2. Update the **smallest affected provider/harness** page with accurate source and `checked:` date; avoid bulk rewriting working contracts.
3. Add a redacted fixture demonstrating the behavior and a passing/failing test.
4. For newly available features, add `unknown` capability first and promote to `supported` after testing.
5. For deprecated features, distinguish **removed**, **unsupported by route**, and **not verified**.
6. Do not invent a stable endpoint from an example that belongs to a different version or product tier.

## Documentation vs observation

- Documentation-backed claim: official vendor/project page describes a behavior (this guide).
- Observation-backed claim: a real request/response, installed CLI/help output or locally executed test demonstrates behavior in a specific environment (add to your project's fixtures).
- Inference/recommendation: suggested adapter designs, dispatch algorithms and recovery policies (explicitly labeled as proposals here).

**Known limited areas:** exact tool schemas for every model, all model-specific MIME and file limits, latest server-specific streamed event types, per-harness RPC schema versions, current user account entitlements, and unprobed tier-2 parity. Always test before claiming support.
