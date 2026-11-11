import abc
from collections.abc import Iterator
from ..messages.message import Message
from ..messages.tool_call import ToolCall
from ..messages.tool_call_result import ToolCallResult


class ContextManager(abc.ABC):
    @abc.abstractmethod
    def set_system_prompt(self, system_prompt: str):
        pass
    @abc.abstractmethod
    def get_context(self) -> list[Message]:
        pass
    @abc.abstractmethod
    def add_context(self, message: Message ):
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
        pass
    @abc.abstractmethod
    def tools(self):
        pass
    @abc.abstractmethod
    def handle_tool_calls(self, calls: dict[int, ToolCall]) -> Iterator[ToolCallResult]:
        pass