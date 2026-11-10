from __future__ import annotations

from chat import execute_tool_call
from providers.base import ToolCall


def test_safe_demo_blocks_confirmed_send_without_side_effect() -> None:
    call = ToolCall(name="send", args={"text": "Do not actually send", "confirmed": True})

    event = execute_tool_call(call, blocked_tools={"send"})

    assert event["tool"] == "send"
    assert event["args"]["confirmed"] is True
    assert event["result"]["status"] == "blocked_in_demo"


def test_safe_demo_does_not_block_read_only_tool() -> None:
    call = ToolCall(
        name="clarify",
        args={"question": "Bạn muốn xem tài khoản nào?", "response_type": "text"},
    )

    event = execute_tool_call(call, blocked_tools={"send"})

    assert event["tool"] == "clarify"
    assert event["result"]["awaiting_user"] is True
