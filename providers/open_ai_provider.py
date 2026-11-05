from providers.provider import Provider
from messages.stream_events import StreamEvent
from messages.tool_call import ToolCall
from messages.message import Message

class OpenAIProvider(Provider):
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name

    def message_to_openai_format(self, messages: list[Message]):
        openai_messages = []
        for m in messages:
            openai_messages.append(m.to_openai())
        return openai_messages
    
    def chat(self, messages: list[Message], tools: list[object]):
        stream = self.client.chat.completions.create(
            model=self.model_name, 
            messages=self.message_to_openai_format(messages),
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