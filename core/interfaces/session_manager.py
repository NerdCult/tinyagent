import abc
from typing import Any
from collections.abc import Iterator
from ...messages.message import Message
from ...messages.agent_message import AgentMessage
from ...messages.tool_call import ToolCall
from ...messages.tool_call_result import ToolCallResult

class SessionManager(abc.ABC):
    @abc.abstractmethod
    def chat(self, message: Message) -> Iterator[AgentMessage]:
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
    def tools(self):
        pass
    @abc.abstractmethod
    def create_tool(self, tool_name: str, code: str):
        pass