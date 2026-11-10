import importlib, json, os, pkgutil, sys, traceback

TOOLS_DIR = os.path.dirname(__file__)

REGISTRY = {}   # name -> (schema, fn)
MAX_RESULT = 50_000   # chars per tool result


# import importlib.util
# import sys
# from pathlib import Path

# def load_tool_file(path: Path):
#     name = f"tinyagent_tools.{path.stem}"
#     spec = importlib.util.spec_from_file_location(name, path)
#     if spec is None or spec.loader is None:
#         raise ImportError(path)
#     mod = importlib.util.module_from_spec(spec)
#     sys.modules[name] = mod
#     spec.loader.exec_module(mod)
#     return mod

def load(agentConfig):
    REGISTRY.clear()
    importlib.invalidate_caches()
    for mod_info in pkgutil.iter_modules([TOOLS_DIR]):
        if mod_info.name.startswith("_"):
            continue
        full = f"{__name__}.{mod_info.name}"
        try:
            mod = importlib.reload(sys.modules[full]) if full in sys.modules else importlib.import_module(full)
            schema = getattr(mod, "SCHEMA")
            
            if hasattr(mod, "get_context_aware_run"):
                fn = getattr(mod, "get_context_aware_run")(agentConfig.context)
            else:
                fn = getattr(mod, "run")
            REGISTRY[schema["name"]] = (schema, fn)
        except Exception:
            traceback.print_exc()

def schemas():
    return [{"type": "function", "function": s} for s, _ in REGISTRY.values()]

def run_tool(name, args):
    entry = REGISTRY.get(name)
    if not entry:
        return json.dumps({"error": f"unknown tool {name}"})
    try:
        out = json.dumps(entry[1](**args), ensure_ascii=False, default=str)
        if len(out) > MAX_RESULT:
            out = out[:MAX_RESULT] + f"... [TRUNCATED: result was {len(out)} chars, limit {MAX_RESULT}. Request a smaller piece.]"
        return out
    except Exception as e:
        return json.dumps({"error": f"{type(e).__name__}: {e}"})

