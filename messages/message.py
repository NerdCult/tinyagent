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

    def to_openai(self) -> dict:
        """Adapt this Part into an OpenAI-wire part dict."""
        if self.type == "text":
            text = self.data['text'] or ''
            return {"type": "text", "text": self.data.get("text", "")}
        elif self.type == "image_url":
            return {"type": "image_url", "image_url": self.data}
        elif self.type == "audio":
            return {"type": "audio", "audio": self.data}
        return {"type": self.type, **self.data}

    def to_anthropic(self) -> dict:
        """Adapt this Part into an Anthropic-wire part dict."""
        if self.type == "text":
            return {"type": "text", "text": self.data.get("text", "")}
        elif self.type == "image":
            return {"type": "image", "source": {
                "type": "base64", "media_type": self.data.get("media_type"),
                "data": self.data.get("data", "")
            }}
        return {"type": self.type, **self.data}

RoleType = Literal["system", "user", "assistant", "tool"]
@dataclass
class Message:
    """One turn in the context. Internal unit, all roles."""
    role: RoleType
    content: list[Part]
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None

    def to_openai(self) -> dict:
        if self.role == "tool":
            return {
                "role": "tool",
                "tool_call_id": self.tool_call_id,
                "content": self.content[0].data.get("text", ""),
            }
        result = {"role": self.role, "content": [p.to_openai() for p in self.content]}
        if self.tool_calls:
            result["tool_calls"] = [{'id': tc.id, 'type': 'function', 'function': {'name': tc.name, 'arguments': tc.args}} for tc in self.tool_calls]
        return result

    def to_anthropic(self) -> dict:
        if self.role == "assistant":
            result = {"role": "assistant"}
            result["content"] = [p.to_anthropic() for p in self.content]
            if self.tool_calls:
                result["tool_calls"] = [tc.to_anthropic() for tc in self.tool_calls]
            return result

        if self.role == "tool":
            return {
                "role": "user",
                "content": [{"type": "tool_result",
                             "tool_use_id": self.tool_call_id,
                             "content": self.content[0].data.get("text", "")}]
            }

        return {"role": self.role, "content": [p.to_anthropic() for p in self.content]}

    @classmethod
    def from_text(cls, role: str, text: str) -> "Message":
        """Quick constructor for a plain text turn."""
        return cls(role=role, content=[Part("text", {"text": text})])