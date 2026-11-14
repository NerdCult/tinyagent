#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from typing import Protocol, runtime_checkable
from .client import Client

@runtime_checkable
class Provider(Protocol):
    '''
    creates a connection to the api and supports listing available models and creating a client to handle the interactions
    '''
    def list_models(self) -> list[str]: ...

    def make_client(self, model_name) -> Client: ...