# Tier-2 Providers & Intermediaries — Broader Practical Coverage

This page is deliberately **orientation-level**, not invented parity. These targets matter when adding options to a backend picker, but load and verify current native docs before implementing feature-sensitive routes.

| Target | Useful role | Adapter starting point | Important divergence / validation |
|---|---|---|---|
| **LiteLLM Proxy** | Self-hosted multi-provider gateway; aliases, routing, quotas | Config-driven proxy/SDK; test selected output protocol | Router may fail over deployments; conversation stickiness/opaque state needs session affinity; don't assume all params map. [Official routing](https://docs.litellm.ai/docs/routing) |
| **Groq** | Fast hosted inference, local/remote/built-in tools on some models | Its documented API SDK/Chat surface | Parallel and built-in tool support **differ by model**; matrix in docs, not global flag. [Tool-use overview](https://console.groq.com/docs/tool-use/overview) |
| **Mistral** | General/coding/reasoning models and function calls | Mistral SDK/Chat or Conversations API | Docs describe `tool_choice` (`auto`,`any`,`none`) and `parallel_tool_calls`; verify endpoint differences. [Function calls](https://docs.mistral.ai/inference/conversations/function-calling) |
| **xAI / Grok** | Raw inference plus provider-managed web/X tools | xAI native Responses/tools | Distinguish built-in server tools vs app functions; current model-specific behavior. [Official tools](https://docs.x.ai/developers/tools/overview) |
| **Together AI** | Hosted open model inference | Its current OpenAI-compatible interface where documented | Tool use depends on the served model/template and endpoint; probe. [Docs](https://docs.together.ai/) |
| **Azure OpenAI** | Enterprise-hosted OpenAI family | Azure-specific deployment endpoint/auth/version semantics | Azure deployment name and API version may differ from OpenAI public model ID/endpoint. [Azure AI Foundry docs](https://learn.microsoft.com/azure/ai-services/openai/) |
| **Amazon Bedrock** | Managed multi-vendor model access | Native `Converse` / `ConverseStream` or specific model APIs | Different API envelopes, content blocks, tool results and permission model. [Bedrock Converse](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html) |
| **Google Vertex AI** | Enterprise Gemini on Google Cloud | Google Cloud SDK/Vertex APIs | Auth (ADC/IAM), regions/endpoints and features may differ from Gemini Developer API. [Vertex Gemini docs](https://cloud.google.com/vertex-ai/generative-ai/docs/overview) |

## Integrator guidance

- Only advertise a tier-2 target as `compatible` after testing **its protocol, chosen model, route and current SDK**. Use `unknown` for untested flags.
- Keep cloud IAM/region, API keys, and API base URLs in **target profiles**, never in universal tool schemas.
- Native APIs remain authoritative when a model's built-in tools, multimodal formats, strict schemas, reasoning state, citations or agent infrastructure are essential.
- Do not duplicate hundreds of model IDs/pricing records in this reference; query official catalogs at runtime and record the returned model identity with each run.

**See:** [COMPATIBILITY.md](../COMPATIBILITY.md), [DECISION_GUIDE.md](../DECISION_GUIDE.md), [VALIDATION.md](../VALIDATION.md).
