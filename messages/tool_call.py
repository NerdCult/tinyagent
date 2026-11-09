from dataclasses import dataclass 

@dataclass
class ToolCall:
    id: str | None = None
    name: str | None = None
    args: dict | None = None
