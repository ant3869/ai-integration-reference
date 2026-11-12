"""Offline nonstreaming response normalizer. Does not execute model-requested tools."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
import json


@dataclass(frozen=True)
class ToolCall:
    call_id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class Normalized:
    text: str
    calls: tuple[ToolCall, ...]
    status: str
    protocol: str


def _args(value: object) -> dict[str, Any]:
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict):
        raise ValueError("Tool arguments must decode to a JSON object")
    return value


def _call(call_id: object, name: object, arguments: object) -> ToolCall:
    if not isinstance(call_id, str) or not call_id:
        raise ValueError("Tool call missing nonempty ID")
    if not isinstance(name, str) or not name:
        raise ValueError("Tool call missing nonempty name")
    return ToolCall(call_id=call_id, name=name, arguments=_args(arguments))


def normalize(protocol: str, response: Mapping[str, Any]) -> Normalized:
    """Convert completed response dictionaries into observed text, tool calls and status."""
    calls: list[ToolCall] = []
    text: list[str] = []
    if protocol == "openai_responses":
        for item in response.get("output", []):
            if item.get("type") == "function_call":
                calls.append(_call(item.get("call_id"), item.get("name"), item.get("arguments")))
            if item.get("type") == "message":
                for part in item.get("content", []):
                    if part.get("type") == "output_text":
                        text.append(part.get("text", ""))
        raw_status = response.get("status", "unknown")
        status = "requires_tool" if calls else ("completed" if raw_status == "completed" else str(raw_status))
    elif protocol == "openai_chat":
        choices = response.get("choices", [])
        if not choices:
            raise ValueError("Chat response has no choices")
        choice = choices[0]
        msg = choice.get("message", {})
        if isinstance(msg.get("content"), str):
            text.append(msg["content"])
        for item in msg.get("tool_calls", []) or []:
            fn = item.get("function", {})
            calls.append(_call(item.get("id"), fn.get("name"), fn.get("arguments")))
        finish = choice.get("finish_reason")
        status = "requires_tool" if calls else ("completed" if finish == "stop" else str(finish or "unknown"))
    elif protocol == "anthropic_messages":
        for block in response.get("content", []):
            if block.get("type") == "text":
                text.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                calls.append(_call(block.get("id"), block.get("name"), block.get("input")))
        stop = response.get("stop_reason")
        status = "requires_tool" if calls else ("completed" if stop == "end_turn" else str(stop or "unknown"))
    elif protocol == "gemini_interactions":
        for step in response.get("steps", []):
            if step.get("type") == "function_call":
                calls.append(_call(step.get("id"), step.get("name"), step.get("arguments")))
            elif step.get("type") == "model_output":
                for part in step.get("content", []):
                    if part.get("type") == "text":
                        text.append(part.get("text", ""))
        raw_status = response.get("status", "unknown")
        status = "requires_tool" if calls else str(raw_status)
    else:
        raise ValueError(f"Unsupported protocol: {protocol}")

    ids = [call.call_id for call in calls]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate tool call IDs in one model response")
    return Normalized("".join(text), tuple(calls), status, protocol)
