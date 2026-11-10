from dataclasses import dataclass

@dataclass
class ToolCallResult:
    id: str
    result: str