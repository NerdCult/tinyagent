#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from dataclasses import dataclass 
from typing import Literal, Any
from . import ToolCall

EventType = Literal["thinking", "replying", "tool_call", "done", 'error']

@dataclass
class ApiEvent:
    ''' Api Clients convert the api response to this data class before passing them to the API Aggregator. 
    This data class helps support the aggregators responsibility to compose the complete response for use in a TARecord'''
    event_type: EventType
    content: str | None = None
    tool_calls: dict[int, ToolCall] | None = None
    raw:  Any = None
