# Decision Guide — Pick the Right Integration Surface

> **Status:** architecture recommendations grounded in the linked provider/harness docs; not a universal standard.

## Decision tree

```text
Need changes to files, shell commands, IDE/workspace activity?
├─ YES → Does a harness already own tools, approvals and session lifecycle?
│   ├─ YES → Use harness's native SDK/RPC/session API. Do NOT rebuild its tool loop.
│   └─ NO  → Choose a harness or implement an explicitly sandboxed agent runtime.
└─ NO  → Need general model inference, classification, data extraction or app-defined tools?
    ├─ YES → Use native provider API for maximum feature fidelity.
    └─ Routing between providers? → Use a router ONLY if it preserves required semantics.

Need provider-specific reasoning, file attachments, native server tools, exact schema?
├─ YES → Native API or feature-proven adapter. Test every capability/model/route.
└─ NO  → OpenAI-compatible Chat Completions is a pragmatic common denominator.

Need long-lived session with a coding agent?
├─ YES → Harness session/thread ID; maintain owner/workspace/permission mapping.
└─ NO  → Stateless request or provider-managed conversation, depending on cost/control.
```

## Use these surfaces (priority order)

| Desired integration | Recommended first | Avoid confusing with |
|---|---|---|
| Programmatically run a coding task using Codex | Codex SDK (`openai-codex` Python, `@openai/codex-sdk` TS) | OpenAI Responses inference alone |
| Build a detailed Codex UI (approval & streamed event control) | Codex app-server protocol | Parsing terminal text |
| Programmatically run Claude Code with filesystem tools | Claude Agent SDK (Python/TS) | Anthropic `messages.create` (raw model API) |
| Call Claude directly and own tool loop | Anthropic Messages API | Claude Code CLI or Agent SDK |
| External HTTP client for Hermes persistent sessions | Hermes API server REST `/api/sessions/*` | Assuming `/v1/chat/completions` is the only interface |
| External client of OpenClaw with persistent agent state | OpenClaw Gateway protocol or enabled agent-first HTTP API | Treating `model=openclaw/...` as provider model name |
| Native multi-turn Gemini with tools and managed state | Gemini Interactions API | Google OpenAI-compat shim as parity layer |
| AI provider tool calling with OpenAI | OpenAI Responses API | Confusing Chat `tool_calls` with Responses `function_call` |
| Muse long tool loops with reasoning continuity | Meta Responses API | Assuming Contributor model supports `max` effort |
| Gateway across models | OpenRouter, LiteLLM, or own adapter router | Treating routing as guaranteed tool/schema parity |
| Local LLM with app-owned tools | Ollama native or LM Studio Chat/Responses as documented | Equating a local model's tool accuracy with wire-format acceptance |
| Share external tools across clients | MCP server and client | Assuming MCP supplies model inference or agent session state |

## Architecture rule: capability-aware routing

Use a **three-stage gate**, not a preferred-provider string:

1. **Endpoint/protocol gate:** does the endpoint expose the required wire protocol (native Responses, Chat, Messages, Interactions, SDK, RPC)?
2. **Model/route gate:** does that exact model and route support the feature (tool calls, multiple calls, file MIME, JSON schema subset, thought continuation, streaming)?
3. **Runtime/permission gate:** are the tool executor, filesystem/network permissions, approval handling and storage actually available?

A feature is usable only when the needed gates are **documented and verified** for the deployment. Classify `supported`, `unsupported`, `unknown` separately. When unknown, probe or surface the limitation; don't quietly downgrade.

## Default adapter policy

- **Provider adapters** transform *logical* tool specifications into a protocol-specific request, and protocol-specific outputs into normalized `ToolRequest`/`TextDelta`/`RunStatus` events. The app still owns executing its own tools.
- **Harness adapters** receive higher-level tasks and map harness events, permissions and session lifecycle. The harness owns most inner tools; don't intercept and re-execute them unless the harness explicitly supports that.
- **Gateway adapters** are distinct from their underlying providers. Record the gateway route, upstream target and request protocol. Re-probe on failover.
- **MCP bridge** maps MCP tool discovery/execution to app tools; it is an extension layer, not a new inference provider.

## Fallback / failover policy

- Retry requests only if failure is known-safe and side effects haven't occurred, or with idempotent/transactional tool execution.
- Never replay a write-producing tool just because a model/gateway timed out. Reconcile its result first.
- On model or provider switch, start a new provider context unless the destination explicitly supports and receives a complete compatible history; always retain the app's canonical transcript.
- Fail closed if target lacks an essential feature such as tool IDs, media type, approval flow, strict schema, or durable session semantics.
- Separate **model failure**, **transport failure**, **tool failure**, **permission denied**, **canceled**, and **context lost** in UI and logs.

## Questions an agent must answer in code review

1. What is the source of truth for conversation state? App, provider response ID, gateway, or harness session?
2. Is a requested tool executed in the app, at provider, through MCP, or inside the harness?
3. What do we store to resume after crash/reboot: response IDs, full history, session ID, workspace path, pending calls?
4. Which *exact* streamed events mean tool args are complete and the run is finished?
5. What happens if two tools are returned, one fails, and the other already had a side effect?
6. What happens when switching providers mid-thread, or a fallback changes the upstream?
7. Which request shapes are verified and which were merely inferred from compatibility marketing?

**Related:** [COMPATIBILITY.md](COMPATIBILITY.md), [architecture/adapter-contract.md](architecture/adapter-contract.md), [VALIDATION.md](VALIDATION.md).
