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
