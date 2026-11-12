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
