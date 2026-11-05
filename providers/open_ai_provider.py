from providers.provider import Provider
from messages.stream_events import StreamEvent
from messages.tool_call import ToolCall
from messages.message import Message, Part

class OpenAIProvider(Provider):
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name

    
    def part_to_openai(self, part: Part) -> dict:
        """Adapt this Part into an OpenAI-wire part dict."""
        if part.type == "text":
            text = part.data['text'] or ''
            return {"type": "text", "text": part.data.get("text", "")}
        elif part.type == "image_url":
            return {"type": "image_url", "image_url": part.data}
        elif part.type == "audio":
            return {"type": "audio", "audio": part.data}
        return {"type": part.type, **part.data}
    
    def message_to_openai(self, message: Message) -> dict:
        if message.role == "tool":
            return {
                "role": "tool",
                "tool_call_id": message.tool_call_id,
                "content": message.content[0].data.get("text", ""),
            }
        result = {"role": message.role, "content": [self.part_to_openai(p) for p in message.content]}
        if message.tool_calls:
            result["tool_calls"] = [{'id': tc.id, 'type': 'function', 'function': {'name': tc.name, 'arguments': tc.args}} for tc in message.tool_calls]
        return result

    def messages_to_openai(self, messages: list[Message]):
        openai_messages = []
        for m in messages:
            openai_messages.append(self.message_to_openai(m))
        return openai_messages
    
    def chat(self, messages: list[Message], tools: list[object]):
        stream = self.client.chat.completions.create(
            model=self.model_name, 
            messages=self.messages_to_openai(messages),
            tools=tools,
            stream=True)

        calls = {}
        for chunk in stream:
            if not chunk.choices:
                yield StreamEvent(
                    event_type="done"
                )
                break
            
            delta = chunk.choices[0].delta

            extra = getattr(delta, "model_extra", None) or {}
            rtext = getattr(delta, "reasoning_content", None) or extra.get  ("reasoning_content") or extra.get ("reasoning")

            if rtext:
                yield StreamEvent(
                    event_type="thinking",
                    content=rtext,
                    raw=chunk
                 )

            if delta.content:
                yield StreamEvent(
                    event_type="replying",
                    content=delta.content,
                    raw=chunk
                )

            for call in delta.tool_calls or []:
                if call.index in calls:
                    if call.function and call.function.arguments: 
                        calls[call.index].args += call.function.arguments
                else: 
                    c = calls.setdefault(call.index, ToolCall(id="", name="", args=""))
                    if call.id: c.id = call.id
                    if call.function and call.function.name: c.name = call.function.name
                    if call.function and call.function.arguments: c.args += call.function.arguments

        if calls:
            yield StreamEvent(
                event_type="tool_call",
                tool_calls=calls,
                raw=chunk
            )