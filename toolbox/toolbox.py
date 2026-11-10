import abc
from ..context.context_provider import ContextProvider

class ToolBox(abc.ABC):
    @abc.abstractmethod
    def load(self, context: ContextProvider):
        pass
    @abc.abstractmethod
    def schemas(self):
        pass
    @abc.abstractmethod
    def run_tool(self, name: str, args) -> str:
        pass
