from .messages.message import Message, Part
from .messages.agent_message import AgentMessage
from .messages.tool_call import ToolCall
from .core.interfaces.client import Client
from .core.interfaces.session_manager import SessionManager
from .session_managers.default_session_manager import DefaultSessionManager

DEFAULT_MAX_ROUNDS = 10

class Agent:
    def __init__(self, client: Client, session: SessionManager= DefaultSessionManager(), max_rounds: int = DEFAULT_MAX_ROUNDS):
        self.client: Client = client
        self.session: SessionManager = session
        self.max_rounds = max_rounds

    def handle_user_message(self, message: Message):
        for _ in range(self.max_rounds):
            self.session.add_context(message)
            messages = self.session.get_context()
            tools = self.session.tools()
            content, calls = "", {}
            
            for event in self.client.get_stream(messages, tools):
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
                self.session.add_context( Message(role='assistant', content=[Part(type='text', data={'text': content})]))
                break

            tool_calls = [ToolCall(id=c.id, name=c.name, args=c.args or {}) for c in calls.values()] 
            self.session.handle_tool_calls(tool_calls)

            self.session.add_context( message= Message(role='assistant', content=[Part(type='text', data={'text': content})] if content else None, tool_calls=tool_calls))
                