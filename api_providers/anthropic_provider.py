from collections.abc import Iterator

from anthropic import Anthropic

from ..messages.message import Message, Part
from ..messages.stream_events import StreamEvent
from ..messages.tool_call import ToolCall
from .client import Client
from .provider import Provider

DEFAULT_MAX_TOKENS = 8192


class AnthropicClient(Client):
    def __init__(self, connection: Anthropic, model_name: str, max_tokens: int = DEFAULT_MAX_TOKENS):
        self.connection = connection
        self.model_name = model_name
        self.max_tokens = max_tokens

    def _part_to_anthropic(self, part: Part) -> dict:
        if part.type == "text":
            return {"type": "text", "text": part.data.get("text", "")}
        if part.type == "image":
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": part.data.get("media_type"),
                    "data": part.data.get("data", ""),
                },
            }
        return {"type": part.type, **part.data}

    def _message_to_anthropic(self, message: Message) -> dict | None:
        if message.role == "system":
            return None

        if message.role == "assistant":
            content = []
            for part in message.content or []:
                if part.type == "text" and not part.data.get("text"):
                    continue
                content.append(self._part_to_anthropic(part))
            for call in message.tool_calls or []:
                content.append({
                    "type": "tool_use",
                    "id": call.id,
                    "name": call.name,
                    "input": call.args or {},
                })
            if not content:
                content = [{"type": "text", "text": ""}]
            return {"role": "assistant", "content": content}

        if message.role == "tool":
            text = ""
            if message.content:
                text = message.content[0].data.get("text", "")
            return {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": message.tool_call_id,
                    "content": text,
                }],
            }

        return {
            "role": message.role,
            "content": [self._part_to_anthropic(p) for p in (message.content or [])],
        }

    def _to_wire(self, messages: list[Message]) -> tuple[str | None, list[dict]]:
        system_parts = []
        wire = []
        for message in messages:
            if message.role == "system":
                for part in message.content or []:
                    text = part.data.get("text", "") if part.type == "text" else ""
                    if text:
                        system_parts.append(text)
                continue
            converted = self._message_to_anthropic(message)
            if converted is None:
                continue
            # Consecutive tool results are separate user turns. Anthropic wants them in one user message.
            if (
                wire
                and converted["role"] == "user"
                and wire[-1]["role"] == "user"
                and converted["content"]
                and converted["content"][0].get("type") == "tool_result"
                and wire[-1]["content"]
                and isinstance(wire[-1]["content"], list)
                and wire[-1]["content"][0].get("type") == "tool_result"
            ):
                wire[-1]["content"].extend(converted["content"])
                continue
            wire.append(converted)
        system = "\n\n".join(system_parts) if system_parts else None
        return system, wire

    def _to_anthropic_tools(self, tools: list[dict] | None) -> list[dict] | None:
        if not tools:
            return None
        converted = []
        for tool in tools:
            fn = tool.get("function", tool)
            converted.append({
                "name": fn["name"],
                "description": fn.get("description", ""),
                "input_schema": fn.get("parameters") or {"type": "object", "properties": {}},
            })
        return converted

    def chat(self, messages: list[Message], tools: list[dict] | None = None) -> Iterator[StreamEvent]:
        system, wire = self._to_wire(messages)
        anthropic_tools = self._to_anthropic_tools(tools)
        kwargs = {
            "model": self.model_name,
            "max_tokens": self.max_tokens,
            "messages": wire,
        }
        if system:
            kwargs["system"] = system
        if anthropic_tools:
            kwargs["tools"] = anthropic_tools

        calls: dict[int, ToolCall] = {}

        # messages.stream() yields SDK helper events (text, thinking, input_json,
        # content_block_start/stop), not the raw SSE event types.
        with self.connection.messages.stream(**kwargs) as stream:
            for event in stream:
                event_type = getattr(event, "type", None)

                if event_type == "text":
                    yield StreamEvent(event_type="replying", content=event.text)
                    continue

                if event_type == "thinking":
                    yield StreamEvent(event_type="thinking", content=event.thinking)
                    continue

                if event_type == "content_block_start":
                    block = event.content_block
                    if getattr(block, "type", None) == "tool_use":
                        calls[event.index] = ToolCall(id=block.id, name=block.name, args={})
                    continue

                if event_type == "input_json":
                    continue

                if event_type == "content_block_stop":
                    block = getattr(event, "content_block", None)
                    if block is not None and getattr(block, "type", None) == "tool_use":
                        args = getattr(block, "input", None) or {}
                        if not isinstance(args, dict):
                            args = {"_value": args}
                        call = calls.get(event.index) or ToolCall(id=getattr(block, "id", ""), name=getattr(block, "name", ""))
                        call.id = getattr(block, "id", call.id)
                        call.name = getattr(block, "name", call.name)
                        call.args = args
                        calls[event.index] = call
                        yield StreamEvent(event_type="tool_call", tool_calls=dict(calls))
                    continue

                if event_type == "error":
                    err = getattr(event, "error", None)
                    message = getattr(err, "message", None) or str(err or event)
                    yield StreamEvent(event_type="done", content=message, raw=event)
                    return

        yield StreamEvent(event_type="done", content="", tool_calls=calls or None)


class AnthropicProvider(Provider):
    def __init__(self,  base_url: str, api_key: str, max_tokens: int = DEFAULT_MAX_TOKENS):
        kwargs = {"api_key": api_key or None}
        kwargs["base_url"] = base_url
        self.connection = Anthropic(**kwargs)
        self.max_tokens = max_tokens

    def list_models(self) -> list[str]:
        models = []
        page = self.connection.models.list(limit=100)
        models.extend(m.id for m in page.data)
        while getattr(page, "has_more", False) and getattr(page, "last_id", None):
            page = self.connection.models.list(limit=100, after_id=page.last_id)
            models.extend(m.id for m in page.data)
        return models

    def make_client(self, model_name: str) -> AnthropicClient:
        return AnthropicClient(self.connection, model_name, max_tokens=self.max_tokens)
