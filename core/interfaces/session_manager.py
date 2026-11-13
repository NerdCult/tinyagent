import abc
from collections.abc import Iterator
from ...messages import Message, AgentMessage
from ...messages.tool_call import ToolCall

class SessionManager(abc.ABC):
    @abc.abstractmethod
    def add_context(self, message: Message):
        pass
    @abc.abstractmethod
    def get_context(self) -> list[Message]:
        pass
    @abc.abstractmethod
    def load_skill(self, skill_name: str):
        pass
    @abc.abstractmethod
    def unload_skill(self, skill_name: str):
        pass
    @abc.abstractmethod
    def create_skill(self, skill_name: str, description: str, text: str):
        pass
    @abc.abstractmethod
    def has_tools(self) -> bool:
        return False
    @abc.abstractmethod
    def tools(self) -> str | None:
        pass
    @abc.abstractmethod
    def create_tool(self, tool_name: str, code: str):
        pass
    @abc.abstractmethod
    def handle_tool_calls(self, calls: list[ToolCall]):
        pass
    @abc.abstractmethod
    def handle_user_message(self, message: Message) -> Iterator[AgentMessage]:
        pass