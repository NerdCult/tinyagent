import importlib, pkgutil, traceback

PROVIDERS ={}

def load():
    PROVIDERS.clear()
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
                    print(f"[providers] {info.name}: could not list models ({e})")
            if mod.DEFAULT_MODEL not in models:
                models.insert(0, mod.DEFAULT_MODEL)
            PROVIDERS[info.name] = {"name": mod.NAME, "client": client,
                                    "default_model": mod.DEFAULT_MODEL, "models": models}
        except Exception:
            print(f"[providers] failed to load {info.name}:")
            traceback.print_exc()
    print(f"[providers] loaded: {', '.join(PROVIDERS) or 'none'}")

def summary():
    return [{"id": k, "name": v["name"], "default_model": v["default_model"], "models": v["models"]}
            for k, v in PROVIDERS.items()]

    
def get(pid):
    return PROVIDERS.get(pid) or PROVIDERS.get("local") or next(iter(PROVIDERS.values()))