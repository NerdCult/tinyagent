import abc
from collections.abc import Iterator
from ..messages.stream_events import StreamEvent
from ..messages.message import Message

class Client(abc.ABC):
    @abc.abstractmethod
    def chat(self, messages: list[Message]) -> Iterator[StreamEvent]:
        pass