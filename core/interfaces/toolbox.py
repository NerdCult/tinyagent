from typing import Protocol
from .context_manager import ContextManager

class Toolbox(Protocol):
    ''' Gives a session the ability to 'load()' tools, provide tool 'schemas()' and 'run_tool()' '''
    def load(self, context: ContextManager):
        pass
    def schemas(self):
        pass
    def run_tool(self, name: str, args) -> str:
        pass

class ToolboxAdvanced(Toolbox, Protocol):
    ''' provides the same abilities as Toolbox, and the additional ability to 'create_tool()' '''
    def create_tool(self, tool_name: str, code:str, context: ContextManager):
        pass
