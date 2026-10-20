import importlib, pkgutil, traceback
import abc
from typing import List

CONTEXTS ={}

class ContextProvider(abc.ABC):
    @abc.abstractmethod
    def get_context(self) -> List:
        pass
    @abc.abstractmethod
    def add_context(self, role, content, tool_calls= None) -> None:
        pass
    @abc.abstractmethod
    def add_tool_result(self, tool_call_id, content) -> None:
        pass


def load():
    CONTEXTS.clear()
    for info in pkgutil.iter_modules(__path__):
        if info.name.startswith("_"):
            continue
        try:
            mod = importlib.import_module(f"{__name__}.{info.name}")

            context = mod.make_context()

            CONTEXTS[info.name] = {'name': mod.NAME, 'context': context}

        except Exception:
            print(f"[contexts] failed to load {info.name}:")
            traceback.print_exc()

def summary():    
    return [{"name": v["name"]}
            for k, v in CONTEXTS.items()]