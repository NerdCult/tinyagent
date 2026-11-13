from dataclasses import dataclass 
from typing import Literal, Any
from ..messages import ToolCall

EventType = Literal["thinking", "replying", "tool_call", "done", 'error']

@dataclass
class StreamEvent:
    event_type: EventType
    content: str | None = None
    tool_calls: dict[int, ToolCall] | None = None
    raw:  Any = None
