#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from typing import Protocol, Iterator, runtime_checkable
from .agent_runtime import AgentRuntime
from ...messages.tool_call_result import ToolCallResult
from ...messages.tool_call import ToolCall

@runtime_checkable
class Toolbox(Protocol):
    ''' Gives a session the ability to 'load()' tools, provide tool 'schemas()' and 'handle_tool_calls()' '''
    def load(self): ...
    def schemas(self) -> list[dict]: ...
    def handle_tool_calls(self, calls: list[ToolCall]) -> Iterator[ToolCallResult]: ...

@runtime_checkable
class ToolboxAdvanced(Toolbox, Protocol):
    ''' 
    provides the same abilities as Toolbox, and the additional ability to 'create_tool()'
    create_tool() is designed to work with a session aware create_tool() tool that is a pass thru to ToolBoxAdvanced.create_tool()
    '''
    def set_session(self, session: AgentRuntime): ...
    def create_tool(self, tool_name: str, code:str): ...
