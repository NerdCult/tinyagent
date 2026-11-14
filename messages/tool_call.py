#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from dataclasses import dataclass 

@dataclass
class ToolCall:
    '''
    data class for storing LLM tool calls for internal handling
    '''
    id: str | None = None
    name: str | None = None
    args: dict | None = None
