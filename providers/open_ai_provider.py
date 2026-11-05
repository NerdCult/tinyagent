from providers.provider import Provider
from messages.stream_events import StreamEvent
from messages.tool_call import ToolCall
from messages.message import Message, Part
import tools, json

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
            result["tool_calls"] = [{'id': tc.id, 'type': 'function', 'function': {'name': tc.name, 'arguments': json.dumps(tc.args) if isinstance(tc.args, dict) else (tc.args or "{}")}} for tc in message.tool_calls]
        return result

    def messages_to_openai(self, messages: list[Message]):
        openai_messages = []
        for m in messages:
            openai_messages.append(self.message_to_openai(m))
        return openai_messages
    
    def chat(self, messages: list[Message]):
        stream = self.client.chat.completions.create(
            model=self.model_name, 
            messages=self.messages_to_openai(messages),
            tools=tools.schemas(),
            stream=True)

        calls = {}
        raw_args = {}
        for chunk in stream:
            if not chunk.choices:
                continue
            
            delta = chunk.choices[0].delta
            finish_reason = chunk.choices[0].finish_reason

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
                idx = call.index
                if call.id:
                    calls.setdefault(idx, ToolCall(id=call.id, name="", args={})).id = call.id
                if call.function:
                    if call.function.name:
                        calls.setdefault(idx, ToolCall(id=call.id, name="", args={})).name = call.function.name
                    if call.function.arguments:
                        raw_args[idx] = raw_args.get(idx, "") + call.function.arguments

            if finish_reason:
                yield StreamEvent(event_type='done', content=finish_reason)
                break
            
        if calls:
            for idx, c in calls.items():
                s = raw_args.get(idx, "").strip()
                try:
                    c.args = json.loads(s) if s else {}
                except json.JSONDecodeError:
                    c.args = {}   # or keep raw string if you want to be permissive
            yield StreamEvent(event_type="tool_call", tool_calls=calls, raw=chunk)
        
        
        
        