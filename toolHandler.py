from providers.provider import ToolCall
from dataclasses import dataclass
import tools, threading

@dataclass
class ToolCallResult:
    id: str
    result: str


def handle_tool_calls(calls):
    for i in sorted(calls):
        c = calls[i]
        try:
            out = tools.run_tool(c.name, c.args)
        except Exception as e:
            out = f"error: {type(e).__name__}: {e}"
        yield ToolCallResult(id=c.id, result=out)