from typing import Protocol, Iterator
from ...messages.message import Message
from ...messages.tool_call import ToolCall
from ...messages.tool_call_result import ToolCallResult


class ContextManager(Protocol):
    def set_system_prompt(self, system_prompt: str):
        pass
    def get_context(self) -> list[Message]:
        pass
    def add_context(self, message: Message ):
        pass
    def load_skill(self, skill_name: str):
        pass
    def unload_skill(self, skill_name: str):
        pass
    def create_skill(self, skill_name: str, description: str, text: str):
        pass
    def has_tools(self) -> bool:
        return False
    def tools(self):
        pass
    def create_tool(self, tool_name: str, code: str):
        pass
    def handle_tool_calls(self, calls: dict[int, ToolCall]) -> Iterator[ToolCallResult]:
        pass