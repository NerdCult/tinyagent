from tinyagent.messages.tool_call import ToolCall
from dataclasses import dataclass
from tinyagent import tools

@dataclass
class ToolCallResult:
    id: str
    result: str


def handle_tool_calls(calls: dict[int, ToolCall]):
    for c in calls.values():
        try:
            out = tools.run_tool(c.name, c.args)
        except Exception as e:
            out = f"error: {type(e).__name__}: {e}"
        yield ToolCallResult(id=c.id, result=out)