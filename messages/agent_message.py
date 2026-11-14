from dataclasses import dataclass
from typing import Literal
from .ta_record import TARecord

agent_message_type = Literal['thinking', 'replying', 'tool_calls', 'message', 'done']

@dataclass
class AgentMessage:
    behavior: agent_message_type
    content: str = '' 
    message: TARecord | None = None
