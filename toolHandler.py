from providers.provider import ToolCall
from dataclasses import dataclass

@dataclass
class ToolCallResult:
    id: str
    result: str


def handle_tool_calls(calls: dict[int, ToolCall]) -> list[ToolCallResult]:

    ordered = [calls[i] for i in sorted(calls)]
           
    for i, c in enumerate(ordered):
        box = {}
        def _run(name=c.name, args=c.args, box=box):
            box["out"] = tools.run_tool(name, args)
            worker = threading.Thread(target=_run, daemon=True)
            worker.start()
            while worker.is_alive():
                worker.join(0.25)
                yield ToolCallResult(
                    id=c.id,
                    result=box.get("out", "")
                )