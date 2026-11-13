from typing import Protocol, Iterator
from ...messages import Message, AgentMessage

class SessionManager(Protocol):
    def handle_user_message(self, message: Message) -> Iterator[AgentMessage]: ...