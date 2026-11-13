from typing import Protocol, Iterator, runtime_checkable
from ...messages.stream_events import StreamEvent
from ...messages.message import Message

@runtime_checkable 
class Client(Protocol):
    def get_stream(self, messages: list[Message], tools: list[dict] | None = None) -> Iterator[StreamEvent]: ...