from dataclasses import dataclass
from typing import Literal
from .tool_call import ToolCall

@dataclass
class Part:
    type: str
    data: dict

RoleType = Literal['system', 'user', 'assistant', 'tool']
@dataclass
class TARecord:
    role: RoleType
    content: list[Part]
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None

def user_record( text: str) -> TARecord:
    return TARecord(role='user', content=[Part('text', {'text': text})])

def assistant_record( text: str) -> TARecord:
    return TARecord(role='assistant', content=[Part(type='text', data={'text': text})])

def system_record(text: str) -> TARecord:
    return TARecord(role='system', content=[Part(type='text', data={'text': text})])