from .messages import Message, Part, AgentMessage, ToolCall, assistant_message
from .core.interfaces import Client

class Agent:
    def __init__(self, client: Client):
        self.client: Client = client

    def process_context(self, context: list[Message], tools: list[dict]):
            content, calls = "", {}
            
            for event in self.client.get_stream(context, tools):
                if event.event_type == "thinking":
                    yield AgentMessage(behavior= 'thinking', content= event.content)

                if event.event_type == "replying":
                    yield AgentMessage(behavior='replying', content= event.content)
                    content = content + event.content

                if event.event_type == "tool_call":
                    calls = event.tool_calls
                    yield AgentMessage(behavior='tool_calls', content=calls)

                if event.event_type  == "done":
                    yield AgentMessage( behavior= 'done', content= event.content)

            if not calls:
                if content:
                    yield AgentMessage(behavior='message', message=assistant_message(content))

            tool_calls = [ToolCall(id=c.id, name=c.name, args=c.args or {}) for c in calls.values()] 

            yield AgentMessage(behavior='message', message=Message(role='assistant', content=[Part(type='text', data={'text': content})] if content else None, tool_calls=tool_calls))

                