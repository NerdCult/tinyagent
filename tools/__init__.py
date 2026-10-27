import importlib, json, os, pkgutil, sys, traceback

TOOLS_DIR = os.path.dirname(__file__)

REGISTRY = {}   # name -> (schema, fn)
MAX_RESULT = 40000   # chars per tool result

def load(agentConfig):
    REGISTRY.clear()
    importlib.invalidate_caches()
    for mod_info in pkgutil.iter_modules([TOOLS_DIR]):
        if mod_info.name.startswith("_"):
            continue
        full = f"{__name__}.{mod_info.name}"
        try:
            mod = importlib.reload(sys.modules[full]) if full in sys.modules else importlib.import_module(full)
            pairs = getattr(mod, "TOOLS", None) or [(getattr(mod, "SCHEMA"), getattr(mod, "run"))]
            for schema, fn in pairs:
                REGISTRY[schema["name"]] = (schema, fn)
        except Exception:
            print(f"[tools] failed to load {mod_info.name}:")
            traceback.print_exc()
    print(f"[tools] loaded: {', '.join(REGISTRY) or 'none'}")

def schemas():
    return [{"type": "function", "function": s} for s, _ in REGISTRY.values()]

def run_tool(name, args_json):
    entry = REGISTRY.get(name)
    if not entry:
        return json.dumps({"error": f"unknown tool {name}"})
    try:
        args = json.loads(args_json or "{}")
        out = json.dumps(entry[1](**args), ensure_ascii=False, default=str)
        if len(out) > MAX_RESULT:
            out = out[:MAX_RESULT] + f"... [TRUNCATED: result was {len(out)} chars, limit {MAX_RESULT}. Request a smaller piece.]"
        return out
    except Exception as e:
        return json.dumps({"error": f"{type(e).__name__}: {e}"})

