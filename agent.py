from .messages.message import Message, Part
from .messages.agent_message import AgentMessage
from .messages.tool_call import ToolCall
from .core.interfaces.client import Client

DEFAULT_MAX_ROUNDS = 10

class Agent:
    def __init__(self, client: Client, max_rounds: int = DEFAULT_MAX_ROUNDS):
        self.client: Client = client
        self.max_rounds = max_rounds

    def chat(self, messages: list[Message], tools = None):
        for _ in range(self.max_rounds):

            content, calls = "", {}
            
            for event in self.client.get_stream(messages, tools):
                if event.event_type == "thinking":
                    yield AgentMessage(behavior= 'thinking', content= event.content)

                if event.event_type == "replying":
                    yield AgentMessage(behavior='replying', content= event.content)
                    content = content + event.content

                if event.event_type == "tool_call":
                    calls = event.tool_calls

                if event.event_type  == "done":
                    yield AgentMessage( behavior= 'done', content= event.content)

            if not calls:
                #self.context.add_context(Message(role='assistant', content=[Part(type='text', data={'text': content})]))
                yield AgentMessage(behavior= 'message', message= Message(role='assistant', content=[Part(type='text', data={'text': content})]))
                break

            yield AgentMessage(behavior= 'message', message= Message(role='assistant', content=[Part(type='text', data={'text': content})] if content else None, tool_calls=[ToolCall(id=c.id, name=c.name, args=c.args or {}) for c in calls.values()] or []))
            #self.context.add_context(Message(role='assistant', content=[Part(type='text', data={'text': content})] if content else None, tool_calls=[ToolCall(id=c.id, name=c.name, args=c.args or {}) for c in calls.values()] or []) )
                