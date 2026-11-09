import abc
from ..messages.message import Message

class ContextProvider(abc.ABC):
    @abc.abstractmethod
    def set_system_prompt(self, system_prompt: str) -> None:
        pass
    @abc.abstractmethod
    def get_context(self, ) -> list[Message]:
        pass
    @abc.abstractmethod
    def add_context(self, message: Message ) -> None:
        pass
    