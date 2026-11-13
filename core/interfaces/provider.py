from typing import Protocol, runtime_checkable
from .client import Client

@runtime_checkable
class Provider(Protocol):
    def list_models(self) -> list[str]: ...

    def make_client(self, model_name) -> Client: ...