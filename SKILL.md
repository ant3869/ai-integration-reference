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
