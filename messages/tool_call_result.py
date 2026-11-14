#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from dataclasses import dataclass

@dataclass
class ToolCallResult:
    '''
    data class used to store tool call results in a TARecord
    '''
    id: str
    result: str