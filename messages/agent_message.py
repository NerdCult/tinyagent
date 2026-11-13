from dataclasses import dataclass
from typing import Literal
from .message import Message

agent_message_type = Literal['thinking', 'replying', 'done', 'message']

@dataclass
class AgentMessage:
    behavior: agent_message_type
    content: str = '' 
    message: Message | None = None
