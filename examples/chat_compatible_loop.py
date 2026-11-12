"""OpenAI-compatible Chat tool loop. Set MODEL_BASE_URL, MODEL_ID and optional MODEL_API_KEY."""
import json
import os
from openai import OpenAI

TOOL = {
    "type": "function",
    "function": {
        "name": "multiply", "description": "Multiply two integers.",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
        },
    },
}


def execute(name: str, raw: str) -> str:
    try:
        if name != "multiply":
            raise ValueError(f"Unknown tool: {name}")
        args = json.loads(raw)
        if not isinstance(args, dict) or set(args) != {"a", "b"}:
            raise ValueError("Expected exactly a and b")
        if type(args["a"]) is not int or type(args["b"]) is not int:
            raise ValueError("Both arguments must be integers")
        return json.dumps({"ok": True, "result": args["a"] * args["b"]})
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return json.dumps({"ok": False, "error": str(exc)})


def main() -> None:
    base_url = os.environ["MODEL_BASE_URL"]
    model = os.environ["MODEL_ID"]
    key = os.environ.get("MODEL_API_KEY", "local-only")
    client = OpenAI(base_url=base_url, api_key=key)
    messages = [{"role": "user", "content": "Use multiply to calculate 7 times 9."}]
    for _ in range(8):
        response = client.chat.completions.create(model=model, messages=messages, tools=[TOOL])
        choice = response.choices[0]
        message = choice.message
        calls = message.tool_calls or []
        if not calls:
            if choice.finish_reason != "stop":
                raise RuntimeError(f"Non-final finish reason: {choice.finish_reason}")
            print(message.content or "")
            return
        messages.append(message.model_dump(exclude_none=True))
        for call in calls:
            messages.append({
                "role": "tool", "tool_call_id": call.id,
                "content": execute(call.function.name, call.function.arguments),
            })
    raise RuntimeError("Tool-loop iteration limit exceeded")


if __name__ == "__main__":
    main()
