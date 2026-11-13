import abc
from collections.abc import Iterator
from ...messages import Message, AgentMessage

class SessionManager(abc.ABC):
    @abc.abstractmethod
    def handle_user_message(self, message: Message) -> Iterator[AgentMessage]:
        pass