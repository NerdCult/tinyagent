import importlib, pkgutil, traceback, os

KEYS_DIR = './keys'
CONNECTIONS ={}

def read_key(filename):
    with open(os.path.join(KEYS_DIR, filename), encoding="utf-8") as f:
        return f.read().strip()

def load():
    CONNECTIONS.clear()
    for info in pkgutil.iter_modules(__path__):
        if info.name.startswith("_"):
            continue
        try:
            mod = importlib.import_module(f"{__name__}.{info.name}")
            client = mod.make_client()
            models = []
            if hasattr(mod, "list_models"):
                try:
                    models = list(mod.list_models(client))
                except Exception as e:
                    print(f"[connections] {info.name}: could not list models ({e})")
            
            CONNECTIONS[info.name] = {"name": mod.NAME, "client": client, "models": models, "make_provider": mod.make_provider}
        except Exception:
            print(f"[connections] failed to load {info.name}:")
            traceback.print_exc()
    print(f"[connections] loaded: {', '.join(CONNECTIONS) or 'none'}")

def summary():
    return [{"id": k, "name": v["name"], "models": v["models"]}
            for k, v in CONNECTIONS.items()]

    
def get(pid):
    return CONNECTIONS.get(pid) or CONNECTIONS.get("openAiApi") or next(iter(CONNECTIONS.values()))