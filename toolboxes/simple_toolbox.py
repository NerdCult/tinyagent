import importlib, json, os, traceback, sys
from pathlib import Path
from .toolbox import Toolbox
from ..context_managers.context_manager import ContextManager

DEFAULT_TOOLS_DIR = F'{os.path.dirname(__file__)}/tools'
DEFAULT_MAX_RESULTS_LENGTH = 50_000

class SimpleToolbox(Toolbox):
    registry: dict = {}

    def __init__(self,  tools_dir: str = DEFAULT_TOOLS_DIR, max_results_length: int = DEFAULT_MAX_RESULTS_LENGTH):
        self.tools_dir: str = tools_dir
        self.max_results_length = max_results_length

    def load(self, context: ContextManager):
        for file in Path(self.tools_dir).glob('*.py'):
            if file.stem.startswith('__'):
                continue
            spec = importlib.util.spec_from_file_location(file.stem, file)
            if spec is None or spec.loader is None:
                raise ImportError(file)
            try:
                mod = importlib.util.module_from_spec(spec)
                sys.modules[file.stem] = mod
                spec.loader.exec_module(mod)
                schema = getattr(mod, "SCHEMA")
            
                if hasattr(mod, "get_context_aware_run"):
                    fn = getattr(mod, "get_context_aware_run")(context)
                else:
                    fn = getattr(mod, "run")
                self.registry[schema["name"]] = (schema, fn)
            except Exception:
                traceback.print_exc()

    def schemas(self):
        return [{"type": "function", "function": s} for s, _ in self.registry.values()]

    def run_tool(self, name, args) -> str:
        entry = self.registry.get(name)
        if not entry:
            return json.dumps({"error": f"unknown tool {name}"})
        try:
            out = json.dumps(entry[1](**args), ensure_ascii=False, default=str)
            if len(out) > self.max_results_length:
                out = out[:self.max_results_length] + f"... [TRUNCATED: result was {len(out)} chars, limit {self.max_results_length}. Request a smaller piece.]"
            return out
        except Exception as e:
            return json.dumps({"error": f"{type(e).__name__}: {e}"})
