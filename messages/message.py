from dataclasses import dataclass
from typing import Literal
from messages.tool_call import ToolCall

@dataclass
class Part:
    """A single typed part of a message's content.

    type: one of "text", "image_url", "audio"
    data: the payload for that type, flat, not a subclass per modality
    """
    type: str
    data: dict


RoleType = Literal["system", "user", "assistant", "tool"]
@dataclass
class Message:
    """One turn in the context. Internal unit, all roles."""
    role: RoleType
    content: list[Part]
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None

    @classmethod
    def from_text(cls, role: str, text: str) -> "Message":
        """Quick constructor for a plain text turn."""
        return cls(role=role, content=[Part("text", {"text": text})])