import abc
from typing import List
from tinyagent.messages.message import Message

class ContextProvider(abc.ABC):
    @abc.abstractmethod
    def set_system_prompt(self, system_prompt: str) -> None:
        pass
    @abc.abstractmethod
    def get_context(self, session_id : str) -> List:
        pass
    @abc.abstractmethod
    def add_context(self, session_id: str, message: Message ) -> None:
        pass
    @abc.abstractmethod
    def get_session_ids(self) -> List:
        pass
    @abc.abstractmethod
    def add_session_id(self, id: str) ->  None:
        pass