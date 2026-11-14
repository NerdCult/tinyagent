from typing import Protocol, Iterator
from ...messages import TARecord, AgentMessage

class AgentRuntime(Protocol):
    def handle_user_message(self, message: TARecord) -> Iterator[AgentMessage]: ...