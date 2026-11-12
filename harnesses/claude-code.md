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
