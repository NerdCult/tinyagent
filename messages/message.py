from dataclasses import dataclass
from typing import Literal
from .tool_call import ToolCall

@dataclass
class Part:
    type: str
    data: dict

RoleType = Literal['system', 'user', 'assistant', 'tool']
@dataclass
class Message:
    role: RoleType
    content: list[Part]
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None

def user_message( text: str) -> Message:
    return Message(role='user', content=[Part('text', {'text': text})])

def assistant_message( text: str) -> Message:
    return Message(role='assistant', content=[Part(type='text', data={'text': text})])

def system_message(text: str) -> Message:
    return Message(role='system', content=[Part(type='text', data={'text': text})])