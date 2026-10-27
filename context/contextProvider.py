import abc
from typing import List

class ContextProvider(abc.ABC):
    @abc.abstractmethod
    def get_context(self, session_id : str) -> List:
        pass
    @abc.abstractmethod
    def add_context(self, session_id: str, role: str, content: str, tool_calls= None ) -> None:
        pass
    @abc.abstractmethod
    def add_tool_result(self, session_id: str, tool_call_id: str, content: str) -> None:
        pass
    @abc.abstractmethod
    def get_session_ids(self) -> List:
        pass
    @abc.abstractmethod
    def add_session_id(self, id: str) ->  None:
        pass