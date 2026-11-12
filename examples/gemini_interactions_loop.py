"""Gemini Interactions tool loop. Requires GEMINI_MODEL and GEMINI_API_KEY."""
import json
import os
from google import genai

TOOL = {
    "type": "function", "name": "multiply", "description": "Multiply two integers.",
    "parameters": {
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
    model = os.environ["GEMINI_MODEL"]
    os.environ["GEMINI_API_KEY"]
    client = genai.Client()
    interaction = client.interactions.create(
        model=model, input="Use multiply to calculate 7 times 9.", tools=[TOOL],
    )
    for _ in range(8):
        calls = [step for step in interaction.steps if step.type == "function_call"]
        if not calls:
            if interaction.status != "completed":
                raise RuntimeError(f"Non-completed interaction: {interaction.status}")
            print(interaction.output_text)
            return
        inputs = []
        for step in calls:
            result = execute(step.name, step.arguments)
            inputs.append({
                "type": "function_result", "call_id": step.id, "name": step.name,
                "result": [{"type": "text", "text": json.dumps(result)}],
            })
        interaction = client.interactions.create(
            model=model, previous_interaction_id=interaction.id,
            tools=[TOOL], input=inputs,
        )
    raise RuntimeError("Tool-loop iteration limit exceeded")


if __name__ == "__main__":
    main()
