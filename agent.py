from .config import AgentConfig
from .messages.message import Message, Part
from .messages.tool_call import ToolCall
from .providers.client import Client
from .context.context_provider import ContextProvider

DEFAULT_MAX_ROUNDS = 10

class Agent:
    def __init__(self, agent_config: AgentConfig, max_rounds: int = DEFAULT_MAX_ROUNDS):
        self.client: Client = agent_config.client
        self.context: ContextProvider = agent_config.context
        self.max_rounds = max_rounds

    def chat(self, message: Message):
        self.context.add_context(message)
        for _ in range(self.max_rounds):

            messages = self.context.get_context()

            content, calls = "", {}

            tools = None

            if self.context.has_tools():
                tools = self.context.tools()
            
            for event in self.client.chat(messages, tools):
                if event.event_type == "thinking":
                    yield { 'behavior': 'thinking', 'content': event.content} 

                if event.event_type == "replying":
                    yield { 'behavior': 'replying', 'content': event.content}
                    content = content + event.content

                if event.event_type == "tool_call":
                    calls = event.tool_calls
                    for call in calls.values():
                        yield { 'behavior': 'tool_call', 'tool': call.name,'content' : f"\n`{call.args}`\n"}

                if event.event_type  == "done":
                    yield {'behavior': 'done', 'content': event.content}

            if not calls:
                self.context.add_context(Message(role='assistant', content=[Part(type='text', data={'text': content})]))
                break

            self.context.add_context(Message(role='assistant', content=[Part(type='text', data={'text': content})] if content else None, tool_calls=[ToolCall(id=c.id, name=c.name, args=c.args or {}) for c in calls.values()] or []) )
                
            for result in self.context.handle_tool_calls(calls) or []:
                self.context.add_context(Message(role='tool', content=[Part(type='text', data={'text': result.result})], tool_call_id=result.id))