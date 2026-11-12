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
