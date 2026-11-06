from tinyagent.tool_handler import handle_tool_calls
from tinyagent.config import AgentConfig
from tinyagent.messages.message import Message, Part
from tinyagent.messages.tool_call import ToolCall

MAX_TOOL_CALLS = 10

class Agent:
    def __init__(self, agentConfig: AgentConfig):
        self.prov = agentConfig.provider
        self.context = agentConfig.context
        self.session_id = agentConfig.session_id

    def chat(self, message: Message):
        self.context.add_context(self.session_id , message)
        for _ in range(MAX_TOOL_CALLS ):

            messages = self.context.get_context(self.session_id)

            events = self.prov.chat(messages)

            content, calls = "", {}
            for event in events:
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
                self.context.add_context(self.session_id , Message(role='assistant', content=[Part(type='text', data={'text': content})]))
                break

            self.context.add_context(self.session_id, Message(role='assistant', content=[Part(type='text', data={'text': content})] if content else None, tool_calls=[ToolCall(id=c.id, name=c.name, args=c.args or {}) for c in calls.values()] or []) )
                
            for result in handle_tool_calls(calls) or []:
                self.context.add_context(self.session_id , Message(role='tool', content=[Part(type='text', data={'text': result.result})], tool_call_id=result.id))