import abc
from collections.abc import Iterator
from dataclasses import dataclass 
from typing import Literal, Any

EventType = Literal["thinking", "content", "tool_call", "done"]

@dataclass
class ToolCall:
    id: str | None = None
    name: str | None = None
    args: str | dict | None = None

@dataclass
class StreamEvent:
    event_type: EventType
    content: str | None = None
    tool_calls: dict[int, ToolCall] | None = None
    raw:  Any = None


class Provider(abc.ABC):
    @abc.abstractmethod
    def chat(self, messages: list[str], tools: list[object]) -> Iterator[StreamEvent]:
        pass