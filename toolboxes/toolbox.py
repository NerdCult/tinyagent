import abc
from ..context_managers.context_manager import ContextManager

class Toolbox(abc.ABC):
    @abc.abstractmethod
    def load(self, context: ContextManager):
        pass
    @abc.abstractmethod
    def schemas(self):
        pass
    @abc.abstractmethod
    def create_tool(self, tool_name: str, code:str, context: ContextManager):
        pass
    @abc.abstractmethod
    def run_tool(self, name: str, args) -> str:
        pass
