"""Offline contract smoke tests: nonstreaming response normalization only."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from normalizer import normalize


class NormalizerTests(unittest.TestCase):
    def test_openai_responses_parallel(self):
        item = {
            "status": "completed", "output": [
                {"type": "function_call", "call_id": "c1", "name": "multiply", "arguments": '{"a":2,"b":3}'},
                {"type": "function_call", "call_id": "c2", "name": "multiply", "arguments": '{"a":4,"b":5}'},
            ]
        }
        result = normalize("openai_responses", item)
        self.assertEqual("requires_tool", result.status)
        self.assertEqual(["c1", "c2"], [c.call_id for c in result.calls])
        self.assertEqual(20, result.calls[1].arguments["a"] * result.calls[1].arguments["b"])

    def test_openai_chat(self):
        msg = {"choices": [{"finish_reason": "tool_calls", "message": {
            "content": None, "tool_calls": [{"id": "id1", "function": {
                "name": "multiply", "arguments": '{"a":7,"b":9}'}}]}}]}
        result = normalize("openai_chat", msg)
        self.assertEqual("requires_tool", result.status)
        self.assertEqual({"a": 7, "b": 9}, result.calls[0].arguments)

    def test_anthropic_blocks(self):
        result = normalize("anthropic_messages", {"stop_reason": "tool_use", "content": [
            {"type": "text", "text": "Calculating."},
            {"type": "tool_use", "id": "toolu_1", "name": "multiply", "input": {"a": 7, "b": 9}},
        ]})
        self.assertEqual("Calculating.", result.text)
        self.assertEqual("toolu_1", result.calls[0].call_id)

    def test_gemini_steps(self):
        result = normalize("gemini_interactions", {"status": "requires_action", "steps": [
            {"type": "function_call", "id": "fc1", "name": "multiply", "arguments": {"a": 7, "b": 9}},
        ]})
        self.assertEqual("requires_tool", result.status)
        self.assertEqual("fc1", result.calls[0].call_id)

    def test_no_tool_final(self):
        result = normalize("openai_responses", {"status": "completed", "output": [
            {"type": "message", "content": [{"type": "output_text", "text": "63"}]}
        ]})
        self.assertEqual(("63", "completed", 0), (result.text, result.status, len(result.calls)))

    def test_invalid_and_duplicate_ids(self):
        payload = {"status": "completed", "output": [
            {"type": "function_call", "call_id": "c1", "name": "multiply", "arguments": "{}"},
            {"type": "function_call", "call_id": "c1", "name": "multiply", "arguments": "{}"},
        ]}
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            normalize("openai_responses", payload)
        payload["output"][1]["call_id"] = "c2"
        payload["output"][1]["arguments"] = "[1,2]"
        with self.assertRaisesRegex(ValueError, "JSON object"):
            normalize("openai_responses", payload)

    def test_unknown_protocol(self):
        with self.assertRaisesRegex(ValueError, "Unsupported protocol"):
            normalize("mcp", {})


if __name__ == "__main__":
    unittest.main()
