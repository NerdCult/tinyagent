from dataclasses import dataclass 

@dataclass
class ToolCall:
    id: str | None = None
    name: str | None = None
    args: str | dict | None = None
