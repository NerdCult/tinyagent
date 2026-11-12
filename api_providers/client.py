from typing import Protocol, Iterator
from ..messages.stream_events import StreamEvent
from ..messages.message import Message

class Client(Protocol):
    def chat(self, messages: list[Message], tools: list[dict] | None = None) -> Iterator[StreamEvent]:
        pass