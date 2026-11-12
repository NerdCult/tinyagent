from typing import Protocol
from .client import Client

class Provider(Protocol):
    def list_models(self) -> list[str]:
        pass

    def make_client(self, model_name) -> Client:
        pass