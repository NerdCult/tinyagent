import abc
from .client import Client

class Provider(abc.ABC):
    @abc.abstractmethod
    def list_models() -> list[str]:
        pass

    @abc.abstractmethod
    def make_client(model_name) -> Client:
        pass