"""Run Claude Code Agent SDK from current working directory with default approvals."""
import asyncio
from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query


async def main() -> None:
    options = ClaudeAgentOptions(max_turns=3, permission_mode="default")
    completed = False
    async for message in query(
        prompt="Read the current project and summarize its structure without changing files.",
        options=options,
    ):
        if isinstance(message, ResultMessage):
            completed = True
            print(message.result)
            print("session_id:", message.session_id)
    if not completed:
        raise RuntimeError("Agent SDK returned no final result")


if __name__ == "__main__":
    asyncio.run(main())
