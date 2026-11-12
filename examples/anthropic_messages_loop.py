"""Anthropic Messages client-tool loop. Requires ANTHROPIC_MODEL and ANTHROPIC_API_KEY."""
import json
import os
from anthropic import Anthropic

TOOL = {
    "name": "multiply", "description": "Multiply two integers.",
    "input_schema": {
        "type": "object",
        "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
        "required": ["a", "b"],
    },
}


def execute(name: str, arguments: object) -> dict:
    try:
        if name != "multiply":
            raise ValueError(f"Unknown tool: {name}")
        if not isinstance(arguments, dict) or set(arguments) != {"a", "b"}:
            raise ValueError("Expected exactly a and b")
        if type(arguments["a"]) is not int or type(arguments["b"]) is not int:
            raise ValueError("Both arguments must be integers")
        return {"ok": True, "result": arguments["a"] * arguments["b"]}
    except (ValueError, TypeError) as exc:
        return {"ok": False, "error": str(exc)}


def main() -> None:
    model = os.environ["ANTHROPIC_MODEL"]
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": "Use multiply to calculate 7 times 9."}]
    for _ in range(8):
        response = client.messages.create(
            model=model, max_tokens=1024, messages=messages, tools=[TOOL],
        )
        calls = [block for block in response.content if block.type == "tool_use"]
        if response.stop_reason != "tool_use":
            if response.stop_reason != "end_turn":
                raise RuntimeError(f"Non-final stop reason: {response.stop_reason}")
            print("\n".join(block.text for block in response.content if block.type == "text"))
            return
        if not calls:
            raise RuntimeError("tool_use stop reason without tool_use block")
        messages.append({
            "role": "assistant",
            "content": [block.model_dump(exclude_none=True) for block in response.content],
        })
        results = []
        for block in calls:
            result = execute(block.name, block.input)
            results.append({
                "type": "tool_result", "tool_use_id": block.id,
                "content": json.dumps(result), "is_error": not result["ok"],
            })
        messages.append({"role": "user", "content": results})
    raise RuntimeError("Tool-loop iteration limit exceeded")


if __name__ == "__main__":
    main()
