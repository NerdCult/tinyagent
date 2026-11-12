from typing import Protocol
from ..context_managers.context_manager import ContextManager

class Toolbox(Protocol):
    def load(self, context: ContextManager):
        pass
    def schemas(self):
        pass
    def create_tool(self, tool_name: str, code:str, context: ContextManager):
        pass
    def run_tool(self, name: str, args) -> str:
        pass
