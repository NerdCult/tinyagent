import abc
from .client import Client

class Provider(abc.ABC):
    @abc.abstractmethod
    def list_models(self) -> list[str]:
        pass

    @abc.abstractmethod
    def make_client(self, model_name) -> Client:
        pass