import importlib, pkgutil, traceback
from typing import List

CONTEXTS ={}


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