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
