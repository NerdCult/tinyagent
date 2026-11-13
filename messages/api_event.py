from dataclasses import dataclass 
from typing import Literal, Any
from . import ToolCall

EventType = Literal["thinking", "replying", "tool_call", "done", 'error']

@dataclass
class ApiEvent:
    event_type: EventType
    content: str | None = None
    tool_calls: dict[int, ToolCall] | None = None
    raw:  Any = None
