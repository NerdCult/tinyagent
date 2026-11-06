import abc
from collections.abc import Iterator
from tinyagent.messages.stream_events import StreamEvent
from tinyagent.messages.message import Message

class Provider(abc.ABC):
    @abc.abstractmethod
    def chat(self, messages: list[Message]) -> Iterator[StreamEvent]:
        pass