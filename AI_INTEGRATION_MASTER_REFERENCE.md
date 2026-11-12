# AI Integration Reference — Single-File Edition

> As of **2026-11-11**. This is an all-in-one reading copy. For agent workloads, prefer `SKILL.md` and load selected modular pages. Relative links inside embedded pages refer to their original paths.

## Contents
- [README.md](#readmemd)
- [SKILL.md](#skillmd)
- [AGENTS.md](#agentsmd)
- [DECISION_GUIDE.md](#decision_guidemd)
- [COMPATIBILITY.md](#compatibilitymd)
- [GOTCHAS.md](#gotchasmd)
- [VALIDATION.md](#validationmd)
- [architecture/adapter-contract.md](#architecture-adapter-contractmd)
- [architecture/session-and-events.md](#architecture-session-and-eventsmd)
- [protocols/tool-calls.md](#protocols-tool-callsmd)
- [protocols/mcp.md](#protocols-mcpmd)
- [protocols/files-and-multimodal.md](#protocols-files-and-multimodalmd)
- [protocols/streaming-and-output.md](#protocols-streaming-and-outputmd)
- [providers/openai.md](#providers-openaimd)
- [providers/anthropic.md](#providers-anthropicmd)
- [providers/gemini.md](#providers-geminimd)
- [providers/meta.md](#providers-metamd)
- [providers/openrouter.md](#providers-openroutermd)
- [providers/local.md](#providers-localmd)
- [providers/secondary.md](#providers-secondarymd)
- [harnesses/codex.md](#harnesses-codexmd)
- [harnesses/claude-code.md](#harnesses-claude-codemd)
- [harnesses/hermes.md](#harnesses-hermesmd)
- [harnesses/openclaw.md](#harnesses-openclawmd)
- [harnesses/code-puppy.md](#harnesses-code-puppymd)
- [harnesses/other-harnesses.md](#harnesses-other-harnessesmd)
- [examples/README.md](#examples-readmemd)
- [SOURCES.md](#sourcesmd)

---

<a id="readmemd"></a>
<!-- SOURCE FILE: README.md -->
## README.md

# AI Provider & Agent Harness Integration Reference

**Edition:** 2026-11-11 · **Audience:** coding agents, orchestration/backend engineers · **Primary implementation language:** Python; TypeScript where the native harness integration is stronger.

> **Purpose:** Pick the correct integration surface, create valid requests, preserve tool/reasoning/session state, execute tools safely, parse responses reliably, and verify real capabilities before switching between providers or harnesses.

## Start here (minimal-context navigation)

| Your question | Read first | Then |
|---|---|---|
| What backend should this project use? | [DECISION_GUIDE.md](DECISION_GUIDE.md) | [COMPATIBILITY.md](COMPATIBILITY.md) |
| Why does tool calling break when I switch providers? | [GOTCHAS.md](GOTCHAS.md) | [protocols/tool-calls.md](protocols/tool-calls.md) |
| What is the exact tool request/result wire shape? | [protocols/tool-calls.md](protocols/tool-calls.md) | Exact provider file |
| How do I preserve a conversation? | [architecture/session-and-events.md](architecture/session-and-events.md) | Exact provider/harness file |
| How do I use a coding harness as a backend? | [harnesses/](harnesses/) | [architecture/adapter-contract.md](architecture/adapter-contract.md) |
| What about images, PDFs, files, audio, video? | [protocols/files-and-multimodal.md](protocols/files-and-multimodal.md) | Exact provider file |
| How do I expose custom tools to many backends? | [protocols/mcp.md](protocols/mcp.md) | [architecture/adapter-contract.md](architecture/adapter-contract.md) |
| How do I prove it works? | [VALIDATION.md](VALIDATION.md) | [examples/README.md](examples/README.md) |
| I am an autonomous coding agent | [SKILL.md](SKILL.md) | Relevant files only |

## Use this public reference from another project

After publication at `https://github.com/ant3869/ai-integration-reference`, give a coding agent this link and ask it to **start at [`SKILL.md`](SKILL.md)**. Agent instructions for the repository itself are in [`AGENTS.md`](AGENTS.md).

- **Read online:** `https://github.com/ant3869/ai-integration-reference/blob/main/SKILL.md`
- **Fetch an individual file:** `https://raw.githubusercontent.com/ant3869/ai-integration-reference/main/providers/anthropic.md`
- **Clone for reliable relative navigation:** `git clone https://github.com/ant3869/ai-integration-reference.git`
- **Pin a commit SHA** in production agent workflows when reproducibility matters; `main` can change.

Agents with only one-page web retrieval should read `SKILL.md`, then fetch the *specific* documents it links to; a remote Markdown link does not automatically load the linked content.

## Install / hand to a coding agent

- **Skill-enabled harness:** copy the **entire folder** into that harness's supported skills directory; do not copy `SKILL.md` alone because its links depend on the other files. Invoke the skill when implementing or debugging provider/harness integrations. Check the harness's current skill discovery rules.
- **No skill support:** keep the folder in your repo (for example, `docs/ai-integration-reference/`) and tell your coding agent: *Read `SKILL.md`, then load only the relevant provider/harness contract and the decision guide.*
- **Single-document workflow:** use [`AI_INTEGRATION_MASTER_REFERENCE.md`](AI_INTEGRATION_MASTER_REFERENCE.md) as an offline reading/export companion, not as a default full-context system prompt. The modular bundle is the authoritative source of relative links.

## Critical taxonomy

A **model** predicts content/calls. A **provider API** handles inference, provider tools, tokens, and model-level state. A **gateway/router** translates and routes requests. An **agent harness** runs an agent loop with filesystem, subprocesses, permissions, sessions, and events. **MCP** exposes tools/resources/prompts to a host; it is *not* an inference API or an agent session protocol. A **model ID** is not necessarily an **agent ID**.

**Do not flatten these layers.** A model can support tools while a gateway drops them; a harness can have tools that the raw model API does not. Even an HTTP endpoint called `/v1/responses` may implement a subset of another provider's contract.

## Prioritized coverage

**Tier 1 — main integration targets**

| Raw provider / gateway | Harness |
|---|---|
| [OpenAI](providers/openai.md) | [Codex CLI/SDK/app-server](harnesses/codex.md) |
| [Anthropic Claude API](providers/anthropic.md) | [Claude Code / Agent SDK](harnesses/claude-code.md) |
| [Google Gemini](providers/gemini.md) | Gemini CLI (orientation in [other-harnesses.md](harnesses/other-harnesses.md)) |
| [Meta Model API / Muse](providers/meta.md) | Muse Code (orientation in [other-harnesses.md](harnesses/other-harnesses.md)) |
| [OpenRouter](providers/openrouter.md) | [Hermes Agent](harnesses/hermes.md), [OpenClaw](harnesses/openclaw.md) |
| [Ollama / LM Studio](providers/local.md) | [Code Puppy](harnesses/code-puppy.md) |

**Tier 2 — sensible broader coverage:** [LiteLLM, Groq, Mistral, xAI, Together, Azure OpenAI, Bedrock, Vertex AI](providers/secondary.md). These have integration guidance and source entry points, not an unsupported promise of identical parity or exhaustive schemas.

## How agents should use this library

1. Identify **target**, **transport** and **requested features** (tool calls? writable code workspace? images? persistence? streaming?).
2. Read [DECISION_GUIDE.md](DECISION_GUIDE.md), select one *native* protocol, then load **only** that provider/harness page.
3. Prefer native SDK or protocol for capability-critical paths; use OpenAI-compat only when the requested feature is tested through it.
4. Explicitly identify client-executed vs server-executed tools and who owns the loop.
5. Implement state identifiers, tool call IDs, approval boundaries, event mapping, retries and cancellation.
6. Run the relevant [VALIDATION.md](VALIDATION.md) probes. Record exact endpoint, model, SDK/harness version and findings.

## Evidence rules

- **Documented** means linked vendor/project documentation was checked on **2026-11-11**. This is *not* live verification against the user's account or installed version.
- **Example** means syntax is based on documented surface and has been syntax-checked where possible; no paid API or agent executions were performed for this package.
- **Probe required** means functionality is dependent on model, deployment, gateway, version, permissions or configuration and must be tested before enabling.
- **Design recommendation** is a proposed implementation contract, **not** a vendor standard.
- Avoid copying static feature booleans from a model list into permanent code. Capabilities are contextual, changing and sometimes route-specific.

## Package inventory

- `SKILL.md` — lightweight agent dispatch rules
- `AGENTS.md` — repo-level instructions for coding agents
- `AI_INTEGRATION_MASTER_REFERENCE.md` — generated, all-in-one reading copy
- `DECISION_GUIDE.md` — backend selection, responsibilities, fallback policy
- `COMPATIBILITY.md` — cross-protocol matrix and differences
- `GOTCHAS.md` — symptoms, root causes and fixes
- `VALIDATION.md` — contract tests and production readiness
- `architecture/` — proposed normalized adapter, state/event and router contracts
- `protocols/` — tool calls, MCP, files/multimodal, streaming/structured output
- `providers/` — vendor endpoints, wire details, state and caveats
- `harnesses/` — sessions, invocation modes, events and tools
- `examples/` — executable Python and TypeScript integration starters
- `SOURCES.md` — authoritative documentation links and refresh instructions

**Scope:** adapter correctness and cross-agent orchestration. **Out of scope:** every derivative harness, pricing tables, every model ID, undocumented endpoints, full reverse-engineering of every SDK, and claims that all APIs have feature parity.

---

<a id="skillmd"></a>
<!-- SOURCE FILE: SKILL.md -->
## SKILL.md

---
name: ai-backend-integration-reference
description: Use when coding, debugging or designing backends that invoke AI model providers, routers or agent harnesses, especially when handling tools, sessions, streaming, files, structured outputs, permissions or switching backends.
---

# AI Backend Integration — Agent Workflow

**Read this file first, not the entire library.** Do not load all provider files. Use relative links from the repo root.

## Trigger examples

- Implement OpenAI / Anthropic / Gemini / Meta / OpenRouter tool loops.
- Connect Codex, Claude Code, Hermes, OpenClaw or Code Puppy to an orchestration app.
- Replace or add an LLM provider without breaking tools or persistent sessions.
- Handle streaming tool arguments, reasoning signatures, file formats, background jobs, MCP or approvals.

## Routing algorithm

1. **Classify:** raw inference API, hosted agent, local agent harness, proxy/router, or tool protocol. Identify exact target and its installed/runtime version where available.
2. **Choose:** read [`DECISION_GUIDE.md`](DECISION_GUIDE.md). If the job changes code on disk, decide whether a *harness* owns that workflow rather than a bare model.
3. **Fetch a single contract:** read the matching `providers/<name>.md` or `harnesses/<name>.md`; optionally `COMPATIBILITY.md` for migration.
4. **Determine execution ownership:** for each tool, who defines it, who executes it, who confirms risky effects, and where the result goes.
5. **Preserve state:** original call IDs, model-specific opaque reasoning, full assistant messages, session IDs, response IDs, working directory, permission context and stream boundaries.
6. **Implement using explicit adapters:** inspect `architecture/adapter-contract.md` and `architecture/session-and-events.md`; do not invent one universal vendor request.
7. **Probe first:** test no-tool, one-tool, multi-tool, tool errors, multi-turn persistence and timeout; use `VALIDATION.md`. Use conservative capability flags until live verified.
8. **Report findings:** state exact route/model/version/protocol, documentary evidence, observed results, and unresolved gaps. Never claim live compatibility based solely on a docs page.

## Non-negotiable integration rules

- **No raw provider tool execution by assumption.** A returned function call is a *request*, not proof the provider executed it.
- **No parsing streamed arguments before a call is complete.** Buffer per call/choice/index and parse once finalized.
- **Never fabricate tool results, call IDs, successful approvals, or capabilities.**
- **Never drop opaque reasoning/thought-state when the active protocol requires preservation.**
- **Never silently map 'unsupported' to 'supported' using a weaker fallback.**
- **Separate permissions from model selection.** Provider credentials, gateway tokens, OS sandbox access and user approval are different boundaries.
- **Do not treat the name 'OpenAI compatible' as a compatibility certification.**

## Lookup map

- Tool shapes: [protocols/tool-calls.md](protocols/tool-calls.md)
- Multimodal: [protocols/files-and-multimodal.md](protocols/files-and-multimodal.md)
- Streaming: [protocols/streaming-and-output.md](protocols/streaming-and-output.md)
- MCP: [protocols/mcp.md](protocols/mcp.md)
- Adapter shape: [architecture/adapter-contract.md](architecture/adapter-contract.md)
- Session/event state: [architecture/session-and-events.md](architecture/session-and-events.md)
- Failure examples: [GOTCHAS.md](GOTCHAS.md)
- Live probing: [VALIDATION.md](VALIDATION.md)
- Official doc index: [SOURCES.md](SOURCES.md)

**Refresh rule:** If vendor docs conflict or the installed version differs, the installed version + actual tested behavior controls implementation. Update the reference with source URL and verification date rather than silently rewriting history.

---

<a id="agentsmd"></a>
<!-- SOURCE FILE: AGENTS.md -->
## AGENTS.md

# Instructions for coding agents

This repository is a **read-only reference** unless the current user explicitly asks you to improve it. It is not itself a model gateway or runtime.

## Efficient lookup

1. Read [SKILL.md](SKILL.md) first.
2. Choose the integration layer using [DECISION_GUIDE.md](DECISION_GUIDE.md).
3. Read only the matching provider or harness page, plus the relevant protocol page.
4. Refer to [COMPATIBILITY.md](COMPATIBILITY.md) for migrations and [GOTCHAS.md](GOTCHAS.md) for failures.
5. Consult [VALIDATION.md](VALIDATION.md) before claiming a runtime supports a feature.

Do **not** ingest the entire library into the prompt by default. Treat examples as examples, not live-tested deployment proofs. Check current upstream docs and the actual installed versions whenever behavior is version-specific.

## Editing this reference

- Prefer small, source-backed edits to the individual Markdown contract.
- Clearly distinguish documented API claims, local test results, and recommendations.
- Never publish credentials, access tokens, private project configuration, live conversation transcripts, or personal data.
- Preserve relative Markdown links. Run `python -m unittest discover -s tests -v` before committing.
- Do not assert that OpenAI-compatible endpoints, underlying models, and coding harnesses have identical capabilities.

---

<a id="decision_guidemd"></a>
<!-- SOURCE FILE: DECISION_GUIDE.md -->
## DECISION_GUIDE.md

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

---

<a id="compatibilitymd"></a>
<!-- SOURCE FILE: COMPATIBILITY.md -->
## COMPATIBILITY.md

# Compatibility Matrix — Wire Contracts, Not Marketing Labels

**Interpreting this table:** a documented surface exists; individual model/route feature support is **probe required**. A dash is not proof that an implementation cannot support a feature—it means this reference does not affirm it.

| Target | Primary surface | Client tool declaration | Model requests tool | Return tool result | Context continuation |
|---|---|---|---|---|---|
| OpenAI Responses | `POST /v1/responses` | `tools: [{type:function,name,parameters,...}]` | `output[]` item `type:function_call`, `call_id`, JSON-string `arguments` | `input[]:{type:function_call_output,call_id,output}` | `previous_response_id` or full item replay |
| OpenAI Chat | `POST /v1/chat/completions` | `tools:[{type:function,function:{name,parameters}}]` | `choices[].message.tool_calls[]` with `id`,`function.arguments` JSON string | `role:tool,tool_call_id,content` | Client resends `messages` |
| Anthropic Claude Messages | `POST /v1/messages` | `tools:[{name,description,input_schema}]` | assistant `content[]` `type:tool_use,id,input` object | next **user** message with `type:tool_result,tool_use_id` | Re-send history; optional **beta message threads** with TTL/replay |
| Gemini Interactions | `/v1beta/interactions` | `tools:[{type:function,name,parameters,...}]` | `steps[]` `type:function_call,id,arguments` | `input:[{type:function_result,call_id,name,result:[...]}]` | `previous_interaction_id` or exact history replay |
| Gemini generateContent (legacy, supported) | `models/*:generateContent` | `tools:functionDeclarations` | `candidates[].content.parts[].functionCall` | `functionResponse` parts | Full `contents`; preserve `thoughtSignature` on manual replay |
| Meta Model API Responses | `/v1/responses` | OpenAI-Responses-shaped | `function_call` + `call_id` | `function_call_output` | `previous_response_id` or encrypted replay |
| Meta Model API Chat | `/v1/chat/completions` | Chat-shaped | Chat `tool_calls` | Chat `role:tool` | Client history |
| OpenRouter Chat / Responses | OpenRouter APIs | OpenAI-style, depending on endpoint | Contract depends on selected endpoint and upstream | Endpoint-specific | History / route-specific; probe failover |
| Ollama native | `/api/chat` | Chat-style tools | `message.tool_calls[].function.arguments` **object** | `role:tool,tool_name,content` | Client history |
| LM Studio OpenAI-compatible | `/v1/chat/completions`; `/v1/responses` | Supported compatibility subset | Parsed model output/tool call events | Match selected endpoint | Endpoint- and model-dependent |
| Codex harness | SDK / app-server / `codex exec` | Harness-provided + configured tools | Harness events | Harness owns execution | Codex thread ID |
| Claude Code harness | Agent SDK / `claude -p` | Harness tools + MCP | SDK messages / structured events | Harness owns execution / SDK custom MCP | Agent SDK session ID |
| Hermes harness | REST session API / ACP / TUI RPC / Chat-compatible | Harness tools + MCP | `tool.started` etc in stream | Harness owns execution | Hermes session ID / gateway session key |
| OpenClaw harness | Gateway RPC / opt-in HTTP Chat/Responses / tools invoke | Configured agent tools | Gateway agent events | Gateway / `tools/invoke` | Gateway session key / `user` routing |

## Different meanings of 'state'

| Token | Object | Scope | Gotcha |
|---|---|---|---|
| `call_id`, `tool_call_id`, `tool_use_id` | Tool **invocation** | One model tool request | NEVER substitute another call ID; parallel calls differ |
| `previous_response_id` | Prior Responses turn | Provider API conversation | Not a Codex thread/session |
| `previous_interaction_id` | Prior Gemini Interaction | Gemini Interactions | Repeat interaction-level `tools`/instructions/config on new turns |
| Claude Message `thread.previous_message_id` | Short-lived beta Message thread | Claude API | Expires; keep full replay history |
| Codex `thread.id` | Harness conversation | Local Codex | SDK/app-server or CLI should own thread persistence |
| Claude Agent SDK `session_id` | Harness conversation | Locally stored Claude Code session | Not Anthropic Messages API state |
| Hermes `session_id` | Harness conversation | Hermes SessionDB | Keep distinct from gateway conversation key |
| OpenClaw `sessionKey` | Agent conversation | Gateway | `model` can select agent, not underlying LLM |
| `Mcp-Session-Id` | MCP transport/session | MCP connection | Does NOT resume model history |

## Tool execution truth table

| Tool class | Who runs it? | Who owes a tool result? |
|---|---|---|
| OpenAI/Claude/Gemini/Meta **custom function** | Your application (or explicit configured executor) | Your application via native protocol |
| Provider-managed web search, code execution etc | Provider | Usually provider; exceptions and pause states are provider-specific |
| Harness built-in shell, edit, browser, delegated subagent | Harness | Harness internally; integrate events and approval boundary |
| MCP server tool | MCP server, invoked by a capable client/host | MCP client/host; bridge if using it as an LLM-defined function |
| OpenClaw direct `/tools/invoke` | OpenClaw Gateway | HTTP JSON result to invoking client |

## Capability matrix: never use binary shortcuts

Track these per **target+model+protocol+version+config**:

`tools.client`, `tools.server`, `tools.parallel`, `tools.stream_arguments`, `structured_output.strict`, `reasoning.preserves_state`, `input.image`, `input.pdf`, `input.audio`, `input.video`, `streaming`, `session.resume`, `session.fork`, `approval.interactive`, `tool.mcp`, `cancellation`.

Use `unknown` until docs and a runtime probe establish support. Reference documentation is not a live feature certification. See [VALIDATION.md](VALIDATION.md).

---

<a id="gotchasmd"></a>
<!-- SOURCE FILE: GOTCHAS.md -->
## GOTCHAS.md

# Integration Gotchas — Fast Failure Lookup

Each entry names a **documented protocol behavior** or **implementation risk**; use the linked source to confirm version/model specifics.

| Symptom | Likely issue | Correction / test |
|---|---|---|
| Tool request printed as text; nothing runs | A **model-generated call isn't an execution** | Register tool dispatcher; validate/authorize/execute; send result using original ID; repeat loop. [OpenAI](https://developers.openai.com/api/docs/guides/function-calling), [Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) |
| `function_call_output` rejected | Sent Chat-shaped tool message to Responses | Use `type:function_call_output` + original `call_id`, not `role:tool`. [OpenAI](https://developers.openai.com/api/docs/guides/function-calling) |
| Chat tool result rejected | Sent Responses-shaped output to Chat | Append original assistant tool-call message and each `role:tool` with original `tool_call_id`. [OpenAI](https://developers.openai.com/api/docs/guides/function-calling) |
| Claude tool result ignored | App put result in assistant message | Use a **user** message containing `tool_result`, matching `tool_use_id`, preserving preceding `tool_use`. [Claude](https://platform.claude.com/docs/en/claude_api_primer) |
| Tool arguments fail JSON parsing while streaming | Parsed partial delta | Buffer each call by stream index/ID; parse on completion. [Streaming](protocols/streaming-and-output.md) |
| Only first of multiple tools completes | Code assumed one call | Iterate over every invocation; return one result per ID; do not reuse IDs. [OpenAI](https://developers.openai.com/api/docs/guides/function-calling) |
| Gemini thinking tool loop fails / 400 | Dropped/rewrote thought signatures or function IDs | Use native Interactions `previous_interaction_id` or preserve all exact step/part state; SDK where possible. [Gemini](https://ai.google.dev/gemini-api/docs/thought-signatures) |
| Gemini continuation silently loses system/tools | Interactions params are *per interaction* | Re-send `tools`, `system_instruction`, generation settings on continuation. [Gemini](https://ai.google.dev/gemini-api/docs/interactions-overview) |
| Gemini native feature missing via OpenAI client | Compatibility shim is a subset | Use native Gemini API for advanced files/tools/thinking. [Google](https://ai.google.dev/gemini-api/docs/partner-integration) |
| Claude API 'session' disappears | Mistook short-lived beta message threads for durable harness sessions | Keep your own full history and replay on 404/expiration; do not confuse with Claude Agent SDK `session_id`. [Threads](https://platform.claude.com/docs/en/build-with-claude/message-threads) |
| Codex project resume starts fresh | Lost/recreated Codex thread ID | Store thread ID and call SDK resume / CLI resume. [Codex](https://developers.openai.com/codex/sdk/) |
| Codex or Claude Code gives plain text rather than actionable tool calls | Called underlying model API instead of harness | Use Codex SDK/app-server or Claude Agent SDK to get built-in workspace and tool execution. [Codex](https://developers.openai.com/blog/codex-as-a-platform), [Claude](https://code.claude.com/docs/en/agent-sdk/overview) |
| OpenClaw routes to wrong model | `model` field names OpenClaw agent target | Use `openclaw/default` or `openclaw/<agentId>`; use permitted `x-openclaw-model` override to select underlying LLM. [OpenClaw](https://docs.openclaw.ai/gateway/openai-http-api) |
| OpenClaw HTTP API returns 404 | Chat/Responses endpoint disabled by default | Enable intended endpoint and verify `GET /v1/models`; don't expose operator bearer token publicly. [OpenClaw](https://docs.openclaw.ai/gateway/openai-http-api) |
| Hermes UI loses previous context | Different session ID or gateway key per call | Use `/api/sessions/{id}/chat` or the documented gateway session key consistently; inspect session APIs. [Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server) |
| Meta 400 for `reasoning_effort=none` | Muse reasoning models don't support disabling | Use supported level (`minimal` etc), not `none`. [Meta](https://dev.meta.ai/docs/reasoning) |
| Meta 400 for `reasoning_effort=max` on Contributor | `muse-spark-1.3-contributor` excludes `max` | Use up to `xhigh` for that model; test exact version. [Meta](https://dev.meta.ai/docs/reasoning) |
| Meta tool name fails schema check | Name has >1 dot or invalid chars | Follow Meta's documented name regex/dot constraint. [Meta](https://dev.meta.ai/docs/tool-calling) |
| OpenAI strict schema rejects input | `additionalProperties:false`, all fields required, JSON Schema subset | Adjust schema; use nullable union for logical optional; validate locally. [OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs) |
| OpenRouter accepted parameter but it appears unused | Upstream route does not support every parameter | Use `provider.require_parameters:true` where supported; pin route and probe exact model+provider. [OpenRouter](https://openrouter.ai/docs/guides/routing/provider-selection) |
| Tool calling works in LM Studio only some of the time | Model chat template/parser mismatches tool format | Inspect native tool support vs default prompt/parser fallback; probe that model. [LM Studio](https://lmstudio.ai/docs/developer/openai-compat/tools) |
| Ollama native tool result doesn't match OpenAI Chat | Native args are objects; tool-result role uses `tool_name` | Use Ollama native shape or the separately documented compatibility API; don't merge them. [Ollama](https://docs.ollama.com/capabilities/tool-calling) |
| Gateway switching breaks ongoing reasoning | Opaque state bound to provider/model family/route | Preserve/replay compatible state or start new context; never fabricate encrypted reasoning. [OpenAI](https://developers.openai.com/api/docs/guides/reasoning), [Meta](https://dev.meta.ai/docs/reasoning) |
| MCP subprocess hangs / JSON parse fails | Logs printed to stdio stdout | stdout only MCP JSON-RPC messages; send logs to stderr. [MCP transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) |
| MCP tool connects but LLM does not call it | MCP connection doesn't automatically create provider tool schema | Bridge `tools/list` to model tools and `tools/call` back, or configure harness's MCP client. [MCP](https://modelcontextprotocol.io/specification/2025-11-25) |
| API works once then times out on file/image | URL blocked/expired, unsupported MIME, payload large | Use provider-supported upload/reference mode; check limits, private-IP safeguards, file retention. [Files](protocols/files-and-multimodal.md) |
| Duplicate side-effect after retry | Timed-out model result was retried without reconciling tool writes | Ledger by run/call ID, effect IDs, retry only known-safe requests; reconcile writes first. [Validation](VALIDATION.md) |
| 'tool success' surfaced after denial | Approval/permission is external to model output | Map `denied` separately from tool failure and model refusal; never coerce denial to success. [Architecture](architecture/session-and-events.md) |

## Troubleshooting order

`target type → endpoint → auth → model/agent ID → tool declaration → returned call shape → completion event → matching result ID → preserved state → permission → actual side effect`.

**Rule:** do not rewrite the entire provider adapter after one bad response. Capture the raw request/response with secrets redacted, reproduce the smallest failing round trip, and update one contract test.

---

<a id="validationmd"></a>
<!-- SOURCE FILE: VALIDATION.md -->
## VALIDATION.md

# Verification Plan — Required Before Declaring a Backend Compatible

**No production API keys or running agent harnesses were available to execute live probes while authoring this reference.** The examples and schemas are documentary. Implementers must run this checklist against **exact installed versions and configured accounts**.

## Capability record (store as structured data)

For every tested route record:

```json
{
  "target": "provider-or-harness-name",
  "protocol": "responses|chat|messages|interactions|sdk|gateway-rpc|mcp",
  "model_or_agent": "resolved-runtime-id",
  "endpoint": "tested-address-or-transport",
  "sdk_version": "installed-version",
  "server_version": "reported-version-if-known",
  "tested_at_utc": "ISO-8601 timestamp",
  "feature": "tools.parallel",
  "status": "supported|unsupported|unknown",
  "evidence": "sanitized request/response fixture or test id",
  "source": "official-doc-url-or-local-version-help"
}
```

The values above are **field descriptions**, not observed test results. Never treat a record template as a verified capability.

## Minimum behavioral test matrix

| Test | Expected observable behavior | Failure signal |
|---|---|---|
| 01 text-only | Valid response and final completion status | Ambiguous streaming end or protocol error |
| 02 forced single tool (when supported) | One well-formed invocation, app runs once, result correlated, final reply | Text-only pseudo-call, lost ID, no final turn |
| 03 two parallel independent tools | Two distinct IDs; each result mapped correctly | Only one handled, wrong id or overwritten arguments |
| 04 malformed tool args / wrong tool name | No execution; structured error returned if protocol allows | Unvalidated call executed |
| 05 tool handler raises | Honest error result; run can recover or fail clearly | Fake success / silent swallow |
| 06 side-effect & timeout | No duplicate effect when retry/resume occurs | Duplicate write/command |
| 07 multi-turn reasoning | Correct continuity, preserved provider opaque state | Missing signature / rejected state / context lost |
| 08 model fallback | Feature re-gated; new model and provider recorded | Hidden route change with stale capabilities |
| 09 strict schema | Valid schema output or explicit refusal/incomplete handling | Arbitrary JSON parsed as trusted schema |
| 10 streaming text+tool args | Partial chunks safely buffered; distinct completion events | `json.loads` on partial chunk |
| 11 image/PDF input | MIME, size and upload path accepted by exact route | Silent text-only fallback |
| 12 cancel | Outstanding tasks terminate or become canceled with clear status | UI claims done while worker runs |
| 13 permissions | Denied tool never runs; approved scoped tool runs | Permission bypass |
| 14 session restart | Prior history and workspace association restored as documented | New empty thread mislabeled resume |
| 15 gateway & harness restart | Correlated run status recovered or marked unknown | Duplicate queue admission |
| 16 token budget / context limit | Truncation, compaction or clear failure policy | Infinite retries / unbounded context |
| 17 secrets & logs | API keys redacted and excluded from persisted events | Credentials in logs or client |
| 18 MCP transport | initialize, tools/list, tools/call, cancellation/error paths | stdout pollution, broken session |

## Recommended test fixture layout

```text
fixtures/
  providers/<target>/<protocol>/<model>/
    capabilities.json
    request-redacted.json
    response-redacted.json
    stream-events.jsonl
    tool-effects.jsonl
  harnesses/<target>/<version>/
    session-events.jsonl
    approvals.jsonl
```

## Pass conditions

1. Every advertised feature has at least one passing test fixture for **that target/model/endpoint combination**, or is marked `unknown`.
2. For tools, trace one original invocation ID end-to-end through validation, execution and return.
3. The adapter handles **zero**, **one** and **multiple** tool calls and appropriate terminal statuses.
4. Every retried write/tool action has a documented side-effect idempotency or reconciliation strategy.
5. Streaming updates cannot mistakenly be rendered as final answers.
6. Switching the model/gateway does not silently reuse incompatible provider state.
7. Current installed version and official source URLs are saved with the evidence.

## Quick local checks included

- `python -m compileall -q examples tests` — syntax-check Python examples (no dependency/API call).
- `python -m unittest discover -s tests -v` — run standard-library event-normalization tests.
- See [examples/README.md](examples/README.md) for optional **live** smoke tests requiring explicit environment variables.

## Version drift policy

Re-check critical contracts when the provider/harness version changes, when the deployed model changes, after a gateway routing/fallback change, or when an integration begins emitting unknown event types. Re-validate `streaming`, `tool return`, `session resume`, `files`, and `permissions` first.

---

<a id="architecture-adapter-contractmd"></a>
<!-- SOURCE FILE: architecture/adapter-contract.md -->
## architecture/adapter-contract.md

# Proposed Normalized Adapter Contract (Application Design, Not Vendor Schema)

**Use when integrating 2+ providers or 2+ agent harnesses.** Normalize application intent and events, but retain raw provider request/response for exact continuation. Do **not** attempt one universal JSON request that every provider accepts.

## Minimal interfaces

```python
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol

CapabilityStatus = Literal["supported", "unsupported", "unknown"]
RunStatus = Literal["queued", "running", "requires_tool", "requires_approval", "completed", "incomplete", "failed", "canceled", "unknown"]

@dataclass(frozen=True)
class Target:
    target_id: str
    category: Literal["provider", "gateway", "harness"]
    protocol: str
    endpoint: str
    model_or_agent_id: str
    version: str | None = None

@dataclass(frozen=True)
class ToolRequest:
    origin_id: str
    name: str
    arguments: dict[str, Any]
    raw_arguments: str | None = None

@dataclass(frozen=True)
class RunEvent:
    run_id: str
    kind: str
    data: dict[str, Any] = field(default_factory=dict)

class BackendAdapter(Protocol):
    def capabilities(self) -> dict[str, CapabilityStatus]: ...
    def start(self, prompt: str, session_id: str | None = None) -> str: ...
    def events(self, run_id: str) -> list[RunEvent]: ...
    def cancel(self, run_id: str) -> RunStatus: ...
```

This is a **conceptual sync contract**: a real system may use async iterators, event queues and durable storage. It is not a promise that any vendor exposes these method names. [See working local normalizer](../examples/normalizer.py).

## Normalize these logical concepts

**Target:** protocol + endpoint + underlying model/agent + adapter version and transport. Preserve the raw target ID sent to provider.

**Session:** app's `conversation_id`; native `session_ref` (thread ID, response ID, interaction ID, session key) and persistence mode (`client_transcript`, `provider_state`, `harness_disk`). Never use one untyped string for all kinds of IDs.

**Run:** `run_id`, parent/child relationship, task owner, workspace, timestamps, status, cancel state, approval state. A single session may have many runs.

**Tool call:** `call_id`, logical name, protocol-specific name, raw/payload arguments, validated args, authorization decision, execution location (`app`, `server`, `harness`, `mcp`), idempotency key, result, error, timestamps. A provider `call_id` differs from an inner MCP JSON-RPC `id`.

**Event:** `text.delta`, `reasoning.summary` (only if allowed), `tool.requested`, `tool.started`, `tool.completed`, `tool.failed`, `approval.requested`, `approval.resolved`, `run.completed`, `run.failed`, `run.canceled`, `stream.error`, `usage.reported`.

**Capability:** tri-state per `(target, model, protocol, version, route/config)` with `documented`, `probed`, `source`, `timestamp`. Do not invent global static flags; failures should disable only the affected route until verified.

## Where to put translation logic

```text
UI / app orchestration
    ├── Target Resolver + Capability Gate
    ├── Session/Run Store + Event Bus
    ├── Tool Registry + Permission + Idempotency Ledger
    └── Adapter Interface
         ├── OpenAIResponsesAdapter
         ├── AnthropicMessagesAdapter
         ├── GeminiInteractionsAdapter
         ├── OpenAICompatibleChatAdapter (per-gateway config)
         ├── HermesSessionAdapter
         ├── OpenClawGatewayAdapter
         ├── CodexSDKAdapter
         └── ClaudeAgentSDKAdapter
```

**Do not abstract away:** an opaque reasoning item, an Anthropic `tool_use` block, a Gemini thought signature, Codex approval decision, OpenClaw agent target, or raw error body. Store these as protocol-owned opaque payloads; only *observational* event projection is normalized.

## Tool registry / execution authority

- Registry holds authoritative implementation and JSON Schema; adapter transforms declared schema into target wire format.
- Authorization is checked on every tool, regardless of LLM requests or provider claims. For writes require scoped permission or explicit approval.
- Execution ledger `(session/run/call ID)` records whether a tool with side effect started/completed; reconcile on timeout before retry.
- Parallelize independent reads; serialize conflicting writes or use transaction/lock. A model may ask twice for the same tool with **different IDs**—these are not automatically duplicates. Design idempotency at business-operation level where needed.
- Tool outputs carry structured success/error; do not claim a script ran if permission denied.

## Example application routing decision

If caller requests `tools.parallel + session.resume + filesystem.write`, the system must decide whether a **harness** provides workspace/approvals and session, or whether to own a sandbox/tool executor itself. Do not route to raw Claude Messages merely because it supports function calls and claim it has Claude Code's file editing.

**Next:** [Session and events](session-and-events.md), [Decision guide](../DECISION_GUIDE.md), [Validation](../VALIDATION.md).

---

<a id="architecture-session-and-eventsmd"></a>
<!-- SOURCE FILE: architecture/session-and-events.md -->
## architecture/session-and-events.md

# Session Lifecycles, Event Ordering, Cancellation, Recovery

## Store these as distinct IDs

```text
application_conversation_id
└── target_session_ref: {kind, value, target_id}
    ├── run_id / turn_id
    │   ├── tool_call_id(s) → tool_execution_id(s)
    │   ├── approval_request_id(s)
    │   └── child_run_id(s)
    └── next run / turn
```

**Kinds:** `openai_response`, `gemini_interaction`, `anthropic_message_thread`, `codex_thread`, `claude_agent_session`, `hermes_session`, `openclaw_session`, `mcp_transport_session`. Not interchangeable. The app must also hold its **canonical transcript** and source-of-truth state snapshots so it can recover when external state expires or routes change.

## State machine (proposed)

`queued → running → (requires_tool ↔ running) → (requires_approval ↔ running) → completed`; failures and cancellation may happen at several points. Use terminal `completed | incomplete | failed | canceled | unknown`; avoid boolean `done`.

- **`requires_tool`**: returned client tool invocation, not necessarily execution started.
- **`requires_approval`**: human/policy decision required before running privileged tool.
- **`unknown`**: network/harness crash means outcome cannot be confirmed; reconcile before retry.
- **`incomplete`**: token limit, max iterations or truncation; surface partial text separately.
- **`canceled`**: cancellation acknowledged; beware a side effect may have occurred just before cancellation.

## Practical storage fields

```json
{
  "conversation_id":"app-generated-uuid",
  "target_id":"meta-prod-responses",
  "session_ref":{"kind":"openai_response","value":"provider-returned-id"},
  "workspace":"application-verified-worktree-path-or-null",
  "run_id":"app-generated-run-uuid",
  "status":"requires_tool",
  "pending_tool_call_ids":["provider-call-id"],
  "pending_approval_ids":[],
  "transcript_storage":"application-canonical-history",
  "last_event_sequence":14
}
```

These strings are **illustrative**, not live provider IDs. Encrypt sensitive logs/secrets at rest, redacting tool inputs where appropriate. Use a persistence store with atomic status/event updates rather than trusting UI state.

## Crash recovery algorithm

1. Load app session metadata and outstanding runs.
2. Ask native provider/harness for run/session state if supported.
3. For pending tool calls, check ledger for effects already performed; do **not** automatically execute again.
4. Reattach event stream or resume the session only with valid native reference. If external state is expired/lost, replay canonical transcript using a **fresh context** and flag any lost opaque state.
5. Restore stable workspace binding; if files changed or worktree missing, stop and require reconciliation.
6. Do not resurrect a previously denied approval.
7. Mark unconfirmable side effects `unknown` and surface to user/operator.

## Routing between agents

Each agent/harness has its own session. A mediator/orchestrator should store a **delegation record** containing parent run, child target, child session, objective, status, artifact paths, result summary, and error. Passing another agent's message as raw user/system instructions can cause authority confusion; preserve provenance and trust level.

**High-level delegation sequence**

1. Parent emits delegation request with stable app ID.
2. Mediator selects target via capability/perms/routing; creates child run.
3. Child accepts task; mediator acknowledges admission only.
4. Child reports progress and final terminal status.
5. Mediator supplies final result to parent or user; never treat admission as completion.

## Switching providers mid-conversation

Use the **app transcript** as transferable state; provider-only reasoning and short-lived message-thread/session metadata usually cannot be transplanted. Start a new target-native session and include a compact, attributed summary plus any necessary observable history. Report loss of opaque continuity as an expected constraint rather than a hidden bug.

## Event/UI projection rules

- Preserve raw event as well as normalized projection.
- Use monotonic sequence numbers per run; tolerate duplicate or out-of-order network delivery.
- Mark exact source of status: model output, harness event, verified filesystem side effect, or mediator inference.
- Track tool started and tool completed separately.
- Never show tool output as final assistant message by default; maintain provenance.

**Related:** [Adapter contract](adapter-contract.md), [Validation](../VALIDATION.md), [Gotchas](../GOTCHAS.md).

---

<a id="protocols-tool-callsmd"></a>
<!-- SOURCE FILE: protocols/tool-calls.md -->
## protocols/tool-calls.md

# Tool-Calling Protocols — Exact Boundaries

## The universal rule

A **custom tool definition** tells a model what it *may request*. A **tool-call event** is a request to the application. Your application validates, authorizes, executes, and returns the result using the **original invocation identifier**. A harness may instead own that whole loop. Server-side tools are an explicit exception: vendor executes those.

## Minimum schema translation (illustrative multiply tool)

**OpenAI Responses / Meta Responses**

```json
{"type":"function","name":"multiply","description":"Multiply integers","parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"],"additionalProperties":false}}
```

**OpenAI Chat / typical OpenRouter Chat / LM Studio Chat**

```json
{"type":"function","function":{"name":"multiply","description":"Multiply integers","parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}}
```

**Anthropic Messages**

```json
{"name":"multiply","description":"Multiply integers","input_schema":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}
```

**Gemini Interactions**

```json
{"type":"function","name":"multiply","description":"Multiply integers","parameters":{"type":"object","properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"]}}
```

**Ollama native** uses Chat-like tool declaration but returns native object `arguments`; tool result uses `tool_name`, not `tool_call_id`. **Gemini generateContent** uses `functionDeclarations` and `functionResponse` parts, not Interactions steps.

## Cross-protocol result correlation

| Protocol | Invocation identity | Result holder |
|---|---|---|
| Responses | `call_id` in `function_call` | `function_call_output.call_id` |
| Chat | `tool_calls[].id` | `role:tool, tool_call_id` |
| Claude Messages | `tool_use.id` | `tool_result.tool_use_id` in **user** content |
| Gemini Interactions | `function_call.id` | `function_result.call_id` |
| Gemini generateContent | `functionCall` name/(id where present) | `functionResponse` part, preserve thoughtSignature |
| Ollama native | `function.name` + native call context (API-specific ID may differ) | `role:tool,tool_name` |
| MCP | JSON-RPC request ID for `tools/call` | JSON-RPC response with matching ID (tool result may include `isError`) |

## Safe app-managed tool-loop state machine

`MODEL_REQUEST → RECEIVE_RESPONSE → extract N calls → validate/authorize each → execute each at most once → assemble N results → CONTINUE_MODEL_REQUEST → ... → FINAL | ERROR | CANCELED`.

- **Zero calls**: final text only if terminal status indicates completed; an empty/incomplete response is not success.
- **One or many calls**: process all, preserve each ID; parallel execution only if independent and permitted.
- **Malformed args/unknown tool**: return a truthful structured tool error where supported; do not execute.
- **Write tool**: approval and idempotency or reconciliation before retry; cancellation may arrive after side effect.
- **Max iterations**: terminate with explicit incomplete status; avoid infinite tool loops.
- **Streaming**: text deltas are not tool invocations; tool-argument deltas must be buffered to final call completion before execution.
- **Harness**: don't externally run built-in tool event a second time.

## Implementation recommendations

Normalize the *logical tools*, not the wire envelopes. Store the raw protocol-specific message for accurate continuation and diagnostics. Map tool names through a registry; JSON Schema validation and authorization happen in your app independent of model claims. Keep `is_error` / error-state distinct from a normal successful result text.

**Source trail:** [OpenAI](https://developers.openai.com/api/docs/guides/function-calling), [Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works), [Gemini](https://ai.google.dev/gemini-api/docs/function-calling), [Meta](https://dev.meta.ai/docs/tool-calling), [Ollama](https://docs.ollama.com/capabilities/tool-calling), [MCP](https://modelcontextprotocol.io/specification/2025-11-25).

---

<a id="protocols-mcpmd"></a>
<!-- SOURCE FILE: protocols/mcp.md -->
## protocols/mcp.md

# MCP — Model Context Protocol (Tools, Resources, Prompts)

**Specification baseline consulted:** 2025-11-25 version on [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-11-25) (checked 2026-11-11). Check for newer protocol revisions before implementation.

## Architecture

- **Host:** AI application/harness (Codex, Claude Code, OpenClaw, Hermes etc.) managing clients.
- **Client:** protocol connection maintained by host to a server.
- **Server:** offers tools, resources and prompts, and may support other optional features.
- **Transport:** JSON-RPC 2.0 over **stdio** or **Streamable HTTP**; HTTP+SSE transport is legacy (migration rules apply).
- **MCP is not an LLM inference API**, not a provider's `tool_calls` JSON shape, and not a persistent model conversation.

## Lifecycle

1. Initialize protocol version and capabilities; wait for initialized notification per spec.
2. Discover capabilities (`tools/list`, `resources/list`, `prompts/list` as applicable).
3. To invoke, call `tools/call` with tool name and arguments via JSON-RPC; parse `content`, structured content and `isError` when present.
4. Support protocol errors, cancellation, notifications and session transport rules as implemented. MCP transport session ID is not agent session ID.

Illustrative JSON-RPC call:

```json
{"jsonrpc":"2.0","id":17,"method":"tools/call","params":{"name":"multiply","arguments":{"a":7,"b":9}}}
```

## Bridging MCP into native model tools

A host may list MCP tool schemas and translate them to the active model tool declaration. On invocation, the host calls the MCP server and translates returned content into **that provider's** native tool-result shape. **Your app owns this bridge unless the harness's MCP client already does.**

Example: Gemini Interactions `function_call` → app's MCP client `tools/call` → `function_result` with matching Gemini `call_id`. The MCP JSON-RPC ID is a distinct inner request ID, **not** the Gemini `call_id`.

## Transport security gotchas

- **stdio:** newline-delimited JSON-RPC only on stdout. Logging belongs on stderr. No free-form print statements.
- **Streamable HTTP:** same MCP endpoint supports POST/GET as specified, with optional SSE; implement authorization, origin validation, network access controls and server capabilities as required.
- A model/tool description is untrusted text. Tools touching files, shell or credentials need explicit authority and human approval policies.
- Don't blindly forward OAuth bearer tokens or MCP tool prompts across tenants.
- If an MCP server dynamically changes tool catalog, refresh and re-validate mapping, permission and namespace conflicts.

**Sources:** [Specification](https://modelcontextprotocol.io/specification/2025-11-25), [Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports), [Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools).

---

<a id="protocols-files-and-multimodalmd"></a>
<!-- SOURCE FILE: protocols/files-and-multimodal.md -->
## protocols/files-and-multimodal.md

# Files & Multimodal — Payload Format Is Provider/Endpoint Specific

**Rule:** A file path on the agent machine is not automatically visible to a cloud model, and a tool named `read_file` is not the same as a model-native PDF/image input. Plan each upload/reference/transport route independently.

## File transfer checklist

1. **Content kind:** text, image, PDF, audio, video or binary artifact.
2. **Where bytes live:** local harness filesystem, browser, object storage URI, provider Files API, base64 inline, MCP resource.
3. **Accepted request shape:** endpoint-specific typed parts, file ID, upload URI, public URL, etc.
4. **Limits:** size, page/frame duration/count, MIME, resolution, retention, download network rules, cost and feature tiers.
5. **Security:** private URLs/SSRF, signed URI expiration, secrets embedded in documents, upload retention and Contributor/data-use settings.
6. **Response handling:** textual model answer versus returned file/artifact ID; metadata vs bytes; missing/failed frames.

## Quick protocol orientation

| Target | Supported strategy classes to inspect | Do **not** assume |
|---|---|---|
| OpenAI Responses | typed `input_image`/`input_file` content, provider file uploads and references | Chat-style content parts identical to Responses |
| Anthropic Messages | typed image/document blocks, file inputs per API | Raw URL pasted in text means provider fetched it |
| Gemini Interactions | native multimodal input/file service; typed content steps | OpenAI-compat shim exposes all Gemini Files features |
| Gemini generateContent | `inlineData`, `fileData`, File API/URI by supported mode | Can reuse Interactions step schema |
| Meta Model API | endpoint-specific image/video/audio/PDF input; variant support | All Muse versions treat audio with same quality |
| OpenRouter | model/provider file handling or routing plugins; may transform uploads | Every upstream model gets same bytes and citations |
| LM Studio/Ollama | local server/model capabilities; model-specific vision support | Server accepting HTTP JSON implies PDF/video native support |
| Codex/Claude Code/Hermes/OpenClaw harness | file path may be read by authorized built-in filesystem tools | Agent has permission to arbitrary file on caller's computer |
| MCP | `resources/read`, tool results, structured resource content | MCP resources magically become provider file IDs |

## Design recommendation: represent media in app metadata

Use separate logical descriptors:

```json
{
  "kind":"image",
  "source_kind":"local_path|blob|provider_file_id|remote_url|mcp_resource",
  "media_type":"image/png",
  "size_bytes":2048,
  "sha256":"<actual-hash-when-available>",
  "retention_policy":"application-defined",
  "authorization_scope":"application-defined"
}
```

This is an **internal proposed descriptor**; never pass it unchanged as a vendor API payload. Only add a verified remote upload step when the chosen endpoint requires it. The example values are illustrative, not a real uploaded file.

## On failed inputs

Return `unsupported_media_type`, `file_unavailable`, `expired_reference`, `file_too_large`, `permission_denied` or `upload_failed` as distinct errors. Do not silently replace video analysis with a text-only prompt and claim the model viewed frames. If applying frame extraction/transcription as a fallback, label it as a different capability with expected loss and test it.

**Sources:** [OpenAI file inputs](https://developers.openai.com/api/docs/guides/file-inputs), [Anthropic PDF](https://platform.claude.com/docs/en/build-with-claude/pdf-support), [Gemini files](https://ai.google.dev/gemini-api/docs/file-inputs), [Meta models](https://dev.meta.ai/docs/models), [OpenRouter files](https://openrouter.ai/docs/guides/features/files), [MCP resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources).

---

<a id="protocols-streaming-and-outputmd"></a>
<!-- SOURCE FILE: protocols/streaming-and-output.md -->
## protocols/streaming-and-output.md

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

---

<a id="providers-openaimd"></a>
<!-- SOURCE FILE: providers/openai.md -->
## providers/openai.md

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

---

<a id="providers-anthropicmd"></a>
<!-- SOURCE FILE: providers/anthropic.md -->
## providers/anthropic.md

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

---

<a id="providers-geminimd"></a>
<!-- SOURCE FILE: providers/gemini.md -->
## providers/gemini.md

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

---

<a id="providers-metamd"></a>
<!-- SOURCE FILE: providers/meta.md -->
## providers/meta.md

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

---

<a id="providers-openroutermd"></a>
<!-- SOURCE FILE: providers/openrouter.md -->
## providers/openrouter.md

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

---

<a id="providers-localmd"></a>
<!-- SOURCE FILE: providers/local.md -->
## providers/local.md

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

---

<a id="providers-secondarymd"></a>
<!-- SOURCE FILE: providers/secondary.md -->
## providers/secondary.md

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

---

<a id="harnesses-codexmd"></a>
<!-- SOURCE FILE: harnesses/codex.md -->
## harnesses/codex.md

# Codex — Coding Harness, Not the OpenAI Responses API

**Priority:** Tier 1 · **Official docs checked:** 2026-11-11 · **Version caveat:** app-server development interfaces can change.

## Choose your integration surface

| Mode | When | Core integration |
|---|---|---|
| `codex exec` | Scripts, CI, one-off bounded coding tasks | Noninteractive CLI; stdout/JSONL; capture process exit/errors and session info |
| **Codex SDK** | App starts/continues/resumes Codex coding tasks | **Python** `openai-codex` or **TypeScript** `@openai/codex-sdk` |
| **Codex app-server** | Native frontend with threaded sessions, approvals and rich streaming event UI | JSON-RPC-style app-server client, stdio/WebSocket transport and versioned methods |
| `codex` interactive CLI | Human terminal workflows | Not the recommended integration for structured app control |

SDK packages documented in Nov 2026: Python `pip install openai-codex` with `from openai_codex import Codex`; TypeScript `npm install @openai/codex-sdk`. Python controls a local Codex app-server; TS manages local threads. **Do not treat OpenAI model-inference `response.id` as Codex harness `thread.id`.**

## Python SDK (official current shape)

```python
from openai_codex import Codex, Sandbox

with Codex() as codex:
    thread = codex.thread_start(sandbox=Sandbox.workspace_write)
    result = thread.run("Inspect tests and propose the smallest safe fix.")
    print(result.final_response)
```

Use configured default model unless a verified available model ID is intentionally selected. Inspect installed version's SDK for resume/interrupt/streaming options; Python and TypeScript may have different method spelling. The TypeScript SDK provides `startThread()`, `thread.run(...)`, and `codex.resumeThread(threadId)`. A complete TypeScript example is [examples/codex_thread.ts](../examples/codex_thread.ts).

## App-server integration

Official app-server is for products that need **authentication, conversation history, approvals and streamed agent events**. It uses a client protocol, separate from API tool-calling. Model control and actual shell/file operations are performed by the harness subject to configured sandbox/permissions.

**Do not** parse terminal ANSI/text as a durable event protocol or directly replay each model function call from app-server events. Treat approval requests as decisions that must be answered by the authorized user/policy, not model instructions.

## Sessions, workspaces, permissions

- Persist `thread.id` and project working directory; explicitly choose run/resume/fork behavior. On resume, ensure the working tree still corresponds to the task or stop/reconcile.
- Keep run ID/turn ID distinct from thread ID; record cost, status, final response, tool event, approvals and cancellation as separate concepts.
- Sandbox modes and approvals protect local filesystem/process execution; permission bypasses are not generic compatibility fixes.
- The SDK is appropriate for coding job orchestration; app-server is better for interactive native session UX.
- Model provider selection inside Codex is a separate configuration topic; changing base URL to a compatible gateway can change features and still leave the harness semantics intact. Validate target protocol.

## Gotchas

1. Calling OpenAI Responses API and expecting Codex to edit files autonomously.
2. Restarting a new thread every time instead of resuming `thread.id`.
3. Assuming app-server HTTP/WS events are OpenAI Responses stream deltas.
4. Using experimental app-server method names from stale docs without a version check.
5. Treating a textual 'I changed files' answer as proof; inspect actual worktree and tests.

**Sources:** [Codex SDK](https://developers.openai.com/codex/sdk/), [Codex app-server](https://developers.openai.com/codex/app-server/), [CLI reference](https://learn.chatgpt.com/docs/cli/reference), [Codex as platform](https://developers.openai.com/blog/codex-as-a-platform).

---

<a id="harnesses-claude-codemd"></a>
<!-- SOURCE FILE: harnesses/claude-code.md -->
## harnesses/claude-code.md

# Claude Code & Claude Agent SDK — Harness Contract

**Priority:** Tier 1 · **Official docs checked:** 2026-11-11.

## Don't collapse these three products

1. **Claude API / Messages:** direct model inference; app owns client-tool loop. [Provider page](../providers/anthropic.md).
2. **Claude Code CLI:** terminal coding harness; runs tools/permissions/sessions.
3. **Claude Agent SDK:** invoke Claude Code's agent loop from Python/TypeScript in an application, with tool use, sessions, hooks, MCP and permissions. SDK runs the Claude Code binary; it is not just a Messages SDK wrapper.

Claude docs also describe **Managed Agents**, a distinct hosted agent surface; evaluate separately if needed rather than conflating with local Agent SDK.

## CLI for subprocess integration

Use `claude -p "<task>" --output-format json` for a bounded machine-readable result, or `--output-format stream-json` when detailed events are needed. `--resume <session-id>` or `--continue` access CLI conversations; capture stdout/stderr and process status. Avoid treating raw terminal output as machine protocol.

**Permissions:** Configure allowed tools/permission mode, handle prompts/denials. Never use a blanket 'skip permissions' flag as the integration strategy.

## Python Agent SDK

```python
import asyncio
from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

async def main() -> None:
    options = ClaudeAgentOptions(max_turns=4, permission_mode="default")
    async for message in query(
        prompt="Review the current project and report the most serious test risk.",
        options=options,
    ):
        if isinstance(message, ResultMessage):
            print(message.result)
            print("session_id:", message.session_id)

asyncio.run(main())
```

The SDK emits messages with assistant/text/tool activity and a final result; consume types explicitly. Session IDs are **harness session IDs**. Docs describe `resume=session_id` in `ClaudeAgentOptions` and options for continue/fork. The SDK writes conversation transcripts locally; it does **not** snapshot code changes; file checkpointing is a distinct feature. For durable cross-host persistence, follow SDK session-storage docs and deploy accordingly.

## Events, tools and approvals

- Harness owns built-in Read/Edit/Bash etc tools. Connect custom tools via SDK MCP support or registered tool extensions; define ownership and permission path.
- A streaming event indicating a tool **started** is not proof it completed; the final run result is separate.
- Handle approval requests and user input through supported SDK interfaces; do not preapprove every shell command because a UI lacks a popup.
- Preserve session associations across process restart and working-directory changes; revalidate workspace.
- `-p` CLI + output JSON is a fallback for apps that cannot embed SDK; for fine-grained control prefer SDK.

## Gotchas

1. Calling `anthropic.messages.create` and assuming Claude Code's tools/session are present.
2. Reusing `tool_use_id` from raw Messages API as SDK session ID.
3. Treating the session transcript as file-system restoration.
4. Failing to handle approval requests in headless mode.
5. Treating every SDK message as final text.

**Sources:** [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), [Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart), [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions), [CLI reference](https://code.claude.com/docs/en/cli-reference), [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions).

---

<a id="harnesses-hermesmd"></a>
<!-- SOURCE FILE: harnesses/hermes.md -->
## harnesses/hermes.md

# Hermes Agent (NousResearch) — Gateway, Sessions, ACP and TUI RPC

**Priority:** Tier 1 for cross-agent work · **Official project docs checked:** 2026-11-11 · **Live installation may differ**.

## Integration options documented by project

| Surface | Transport | Best use |
|---|---|---|
| **API server** | HTTP REST + SSE | Web apps / orchestration + external session control |
| **ACP** | JSON-RPC over stdio | IDEs/hosts implementing Agent Client Protocol |
| **TUI gateway RPC** | JSON-RPC over stdio or WebSocket | More detailed session, slash command, approval and streaming controls |
| CLI | Local process | One-off use and configuration |

The Hermes agent owns its internal tools, memory, provider selection, MCP integrations, execution and session logic. An external application should **not** assume every event is a raw model function call.

## API server and auth

Project docs specify `API_SERVER_ENABLED=true` and `API_SERVER_KEY=<secret>` in `~/.hermes/.env`; API server uses configured gateway (example port `8642`) and bearer auth. Don't check secrets into repo. Documented OpenAI-style `/v1/chat/completions` makes simple frontend integration possible; **native session endpoints are better for persistent control**.

Native REST resources include:

- `GET /api/sessions` — list, page/filter sessions.
- `POST /api/sessions` — create session.
- `GET /api/sessions/{id}` and `/messages` — metadata/history.
- `POST /api/sessions/{id}/chat` — one synchronous agent turn.
- `POST /api/sessions/{id}/chat/stream` — SSE turn with events such as `assistant.delta`, `tool.started`, `tool.completed`, `run.completed`.
- `POST /api/sessions/{id}/fork` — branch; `PATCH`/`DELETE` manage metadata/session with version-specific rules.
- `GET /v1/capabilities` advertises available feature flags/endpoints in current docs.

Request body example for stream:

```json
{"input":"Inspect active tasks and give a concise status report."}
```

Use existing REST session ID in the **path**. Read the actual SSE event protocol and capability flags on the running server, including any current revision/identity preconditions. Hermes also documents gateway conversation keys (`X-Hermes-Session-Key`) in its API server implementation; keep that key distinct from immutable transcript/session IDs.

## Tool calls, provider routing and profiles

- Hermes tools include shell/file, browser, memory/recall, agent delegation, MCP and other toolsets depending on configuration. Tool gateway and external model provider are separate concerns.
- An HTTP compatible call can start/continue an agent turn, **not just generate raw model text**. Don't double-execute tools indicated in Hermes event stream.
- Gateway profiles/default model selection are installation-specific; query local status/config, don't hardcode profile names or ports from a different machine.
- Hermes may route tools via Nous Portal's Tool Gateway; verify current tool provider configuration rather than assuming API key means every tool is enabled.

## Resilience checklist

Capture `session_id`, declared conversation key, profile, model, task/job ID if present, event order and terminal state. SSE reconnect is not necessarily turn replay; re-query server state before reissuing a potentially side-effectful task. On 409/503, inspect current session/workflow status and preserve the error, rather than creating a fresh session silently.

## Pitfalls

1. Treating gateway model-call compatibility as proof every Hermes session API endpoint exists in installed version.
2. Losing session key when transitioning WebSocket/REST/CLI clients.
3. Treating `tool.started` as completed.
4. Passing an API server shared key to an untrusted browser.
5. Assuming local gateway profiles or port `8642` are universal defaults.

**Sources:** [Hermes programmatic integration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/programmatic-integration.md), [API server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server), [Tools](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools/), [Official repo](https://github.com/NousResearch/hermes-agent).

---

<a id="harnesses-openclawmd"></a>
<!-- SOURCE FILE: harnesses/openclaw.md -->
## harnesses/openclaw.md

# OpenClaw — Agent-First Gateway (not a Plain LLM Proxy)

**Priority:** Tier 1 · **Docs checked:** 2026-11-11. **Security:** shared-secret gateway access can act as an operator.

## Available surfaces

- **Gateway protocol** for rich native agent control and streaming over WebSocket.
- Opt-in OpenAI-compatible `POST /v1/chat/completions` and opt-in OpenResponses-style `POST /v1/responses` — both disabled unless enabled in gateway config. Additional `/v1/models`, embeddings surfaces vary by enabled endpoint/version.
- `POST /tools/invoke` on the gateway port directly invokes an allowed tool with agent policy context. This is **operator-level** functionality; never publish publicly without a proper trust boundary.
- Internal session orchestration tools (e.g. `sessions_list`, `sessions_send`, `sessions_spawn`, `sessions_history`) are agent tools and distinct from the external Gateway RPC client.

## OpenAI-compatible HTTP is agent-first

`model` is an OpenClaw **agent target**, not raw upstream LLM model:

| Request model | Meaning |
|---|---|
| `openclaw/default` | Stable alias to configured default OpenClaw agent |
| `openclaw/<agentId>` | Named configured agent |
| `openclaw` | Default agent (alias) |

To override the underlying provider/model, docs list `x-openclaw-model` (subject to caller auth/scope). Explicit `x-openclaw-session-key` can target a gateway session, and docs describe `user` as a stable application conversation key on Chat Completions. Keep provider model, agent ID and session key as different fields.

## Example request (enabled Chat endpoint)

```json
{
  "model":"openclaw/default",
  "user":"conversation-42",
  "messages":[{"role":"user","content":"Inspect the current workspace status."}]
}
```

Auth is gateway bearer credential or supported trusted proxy boundary; use loopback/tailnet/private ingress, not an unauthenticated public URL. The gateway's common default port is `18789` but must be discovered from actual installation.

## Direct tool invocation

```json
{"tool":"sessions_list","args":{},"sessionKey":"main"}
```

`POST /tools/invoke` accepts `tool`/`name`, optional `args`, `sessionKey`, `agentId`, `idempotencyKey` and other documented fields. Which tools are callable depends on policy. **Do not pass model API function-call envelopes** directly into `tools/invoke`. Use one direct tool action only when the caller is authorized; distinguish it from a full agent turn.

## Session and subagent control

- Gateway agent sessions persist under configured session store and routing rules. Use stable keys per UI conversation, never one shared main session for every end user.
- Built-in session tools can send work to, list and spawn subagents, often asynchronously. Track run/child session IDs and terminal outcome rather than guessing completion from task admission.
- Different gateway protocols may expose differing event detail; choose native Gateway protocol for rich state and approval UX, not only Chat delta text.
- `GET /v1/models` lists **agent targets**, not every upstream LLM model.

## Gotchas

1. HTTP Chat/Responses endpoints are opt-in. Verify enablement.
2. `model=openclaw/...` is **not** `anthropic/claude-*` or another upstream model identifier.
3. Shared token is not scoped customer identity; apply authenticated gateway boundary, do not reveal to browsers.
4. Don't equate direct `/tools/invoke` with long-running agent delegation.
5. A single tool invoke may have side effects; use `idempotencyKey` and reconcile before retrying where supported.

**Sources:** [Gateway](https://docs.openclaw.ai/gateway), [Chat API](https://docs.openclaw.ai/gateway/openai-http-api), [OpenResponses](https://docs.openclaw.ai/gateway/openresponses-http-api), [Direct tool invoke](https://docs.openclaw.ai/gateway/tools-invoke-http-api), [Session tools](https://docs.openclaw.ai/session-tool).

---

<a id="harnesses-code-puppymd"></a>
<!-- SOURCE FILE: harnesses/code-puppy.md -->
## harnesses/code-puppy.md

# Code Puppy — Python CLI Coding Agent

**Priority:** Tier 1 user stack, but a lighter integration contract than Codex/Claude SDKs · **Project docs checked:** 2026-11-11.

## Documented features

Code Puppy is a CLI-first, Python-based open-source coding agent with file/shell tools, agent profiles, provider switching, MCP integration and autosaved/resumable sessions.

- Launch interactive CLI with `code-puppy`; official installation via `pip install code-puppy` or `uvx code-puppy`.
- In CLI: `/agent <name>`, `/model <name>`, `/tools`, `/mcp list`, `/session`, `/resume`, `/compact`.
- Project-specific `AGENT.md` may define local instructions; custom agents are JSON-based under `~/.code_puppy/agents/`.
- Custom model definitions/config use `~/.code_puppy/extra_models.json` and app config; actual per-provider API behavior is determined by its adapter and model.

## Backend integration recommendation

**Do not assume a stable programmatic RPC/session protocol solely from the existence of an interactive CLI.** When embedding into a product, inspect exact installed source/docs for noninteractive mode, machine-readable output, session restoration and cancellation flags. If absent, treat it as **interactive-only / experimental subprocess integration** and expose capabilities conservatively.

For a temporary subprocess bridge:

1. Check `code-puppy --help` from installed version for noninteractive input/output modes.
2. Run in an explicit working directory and constrained environment; persist config/model/agent identity.
3. Capture stdout/stderr/exit code separately. Do not parse human-facing colorized output as authoritative structured protocol.
4. Manage approvals; no unattended broad shell access.
5. Resume an autosaved session only via the version's documented session mechanism, after validating the workspace.

## Best extension surface

MCP for external tools and custom agents for structured roles are documented. Different model providers may have different tool function and tool-result behavior; inspect which provider adapter Code Puppy uses before applying raw provider-specific patches.

## Do not assume

- Stable HTTP API, JSON-RPC server, or SDK with Codex-equivalent event types.
- Ability to resume an exact in-flight tool operation from a CLI transcript.
- Global tool support merely because its model catalog lists a model.

**Sources:** [Code Puppy](https://code-puppy.dev/), [Commands](https://code-puppy.dev/pages/commands.html), [Configuration](https://code-puppy.dev/pages/configuration.html), [Custom agents](https://code-puppy.dev/pages/custom-agents.html).

---

<a id="harnesses-other-harnessesmd"></a>
<!-- SOURCE FILE: harnesses/other-harnesses.md -->
## harnesses/other-harnesses.md

# Other Major Harnesses — Orientation (Not Exhaustive)

This keeps the reference broad without sprawling into forks and niche derivatives. **Full integration specifications should be added only when the harness becomes an actual target.**

## Gemini CLI

Google's open-source terminal coding assistant is distinct from Gemini native inference APIs. It provides an agent/harness experience with tools and sessions. For integration, inspect the official CLI's installed `--help`, headless/JSON output interface and any supported SDK/ACP interface; do not assume raw Gemini Interactions endpoints expose the CLI's filesystem tools. [Project](https://github.com/google-gemini/gemini-cli).

## Muse Code

Meta describes a coding-agent CLI (`muse`) as a separate execution system backed by Meta Model API (Muse Spark, and some other model variants), with sandbox and approval functions. Raw Model API calls do **not** automatically gain Muse Code's shell/file tools. Inspect current Muse Code CLI docs for headless/session mode before wiring into a product. [Meta overview](https://dev.meta.ai/docs/overview).

## OpenAI Agents SDK / hosted agents

These are **additional layers** beyond OpenAI Responses and beyond Codex; avoid treating an Agents SDK run or hosted Agents API session as a Codex SDK thread. Agent orchestration/observability, built-in tools and hosted sandbox support are feature- and product-specific. [OpenAI Agents API](https://developers.openai.com/api/docs/guides/agents), [OpenAI Agents SDK Python](https://openai.github.io/openai-agents-python/).

## GitHub Copilot CLI / IDE agent

Treat as its own agent harness, potentially mediated by IDE/auth and repo/organization policies. Do not borrow CLI args, tool schemas or event formats from Claude Code or Codex without verification. [GitHub Copilot](https://docs.github.com/en/copilot).

## When to promote a harness to Tier 1

Document a stable programmatic interface, actual tool ownership and permission rules, session IDs and resume semantics, lifecycle event mapping, cancellation, error semantics and live contract tests. Avoid adding a provider merely because it has a popular CLI.

---

<a id="examples-readmemd"></a>
<!-- SOURCE FILE: examples/README.md -->
## examples/README.md

# Runnable Integration Examples

These are **small, functional model-tool loops**, not fake tool-call simulations. They use a safe local `multiply(a,b)` function and return one result per model-requested call. Running the live scripts requires an installed SDK, credentials, network access and a model with function calling enabled. **No paid network tests were run during document authoring.**

| File | SDK | Environment needed | Purpose |
|---|---|---|---|
| `openai_responses_loop.py` | `pip install openai` | `OPENAI_API_KEY`, `OPENAI_MODEL` | Native Responses function loop |
| `anthropic_messages_loop.py` | `pip install anthropic` | `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL` | Native Claude content-block tool loop |
| `gemini_interactions_loop.py` | `pip install google-genai` | `GEMINI_API_KEY`, `GEMINI_MODEL` | Native Gemini interaction step loop |
| `chat_compatible_loop.py` | `pip install openai` | `MODEL_BASE_URL`, `MODEL_ID`, plus `MODEL_API_KEY` for authenticated endpoints | OpenAI-compatible Chat loop: OpenRouter/LM Studio/Meta Chat etc |
| `codex_thread.ts` | `npm install @openai/codex-sdk` | Working Codex auth/config | Codex harness thread run+resume; run with TS runner |
| `claude_agent_sdk.py` | `pip install claude-agent-sdk` | Working Claude Code / Anthropic auth environment | Agent SDK local harness run+final result |
| `normalizer.py` | Python 3.10+ standard library | none | Deterministic **nonstreaming** response normalization |
| `../tests/test_normalizer.py` | Python 3.10+ `unittest` | none | Offline tests for parser/correlator |

**Run Python examples:** `python examples/<name>.py` from the package root after setting variables and installing the correct SDK. Examples intentionally refuse to run when model ID and required API keys aren't provided. For local LM Studio `MODEL_API_KEY` defaults to a harmless local value; if authenticated, set a real key. For Meta Chat, set `MODEL_BASE_URL` to `https://api.meta.ai/v1`, `MODEL_API_KEY` to your Meta Model API credential, and `MODEL_ID` to an enabled Meta model such as `muse-spark-1.3`. Never commit API keys. For OpenRouter: `MODEL_BASE_URL=https://openrouter.ai/api/v1` and its API key.

For the TypeScript Codex example, install a TypeScript runner such as `tsx` (`npm install --save-dev tsx`), then run `npx tsx examples/codex_thread.ts` in a properly authenticated workspace.

**Safety:** the local multiply tool does not write files or invoke shell commands. Adapt the tool registry only after adding schema validation, authorization and idempotent execution as specified in [adapter contract](../architecture/adapter-contract.md).

**Examples are version-sensitive:** run `python -m compileall -q examples tests` and the offline unit suite, then live-probe the installed SDK/models before production use.

---

<a id="sourcesmd"></a>
<!-- SOURCE FILE: SOURCES.md -->
## SOURCES.md

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
