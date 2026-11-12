"""OpenAI Responses client-tool loop. Requires OPENAI_MODEL and OPENAI_API_KEY."""
import json
import os
from openai import OpenAI

TOOL = {
    "type": "function", "name": "multiply", "description": "Multiply two integers.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
        "required": ["a", "b"], "additionalProperties": False,
    },
}


def execute(name: str, arguments: str) -> str:
    try:
        if name != "multiply":
            raise ValueError(f"Unknown tool: {name}")
        args = json.loads(arguments)
        if not isinstance(args, dict) or set(args) != {"a", "b"}:
            raise ValueError("Expected exactly a and b")
        if type(args["a"]) is not int or type(args["b"]) is not int:
            raise ValueError("Both arguments must be integers")
        return json.dumps({"ok": True, "result": args["a"] * args["b"]})
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return json.dumps({"ok": False, "error": str(exc)})


def main() -> None:
    model = os.environ["OPENAI_MODEL"]
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=model, input="Use multiply to calculate 7 times 9.", tools=[TOOL],
    )
    for _ in range(8):
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            if response.status != "completed":
                raise RuntimeError(f"Non-completed response: {response.status}")
            print(response.output_text)
            return
        outputs = [
            {"type": "function_call_output", "call_id": call.call_id,
             "output": execute(call.name, call.arguments)}
            for call in calls
        ]
        response = client.responses.create(
            model=model, previous_response_id=response.id, input=outputs, tools=[TOOL],
        )
    raise RuntimeError("Tool-loop iteration limit exceeded")


if __name__ == "__main__":
    main()
