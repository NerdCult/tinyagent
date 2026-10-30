from tool_handler import handle_tool_calls
import tools
from config import AgentConfig

MAX_TOOL_CALLS = 10

class Agent:
    def __init__(self, agentConfig: AgentConfig):
        self.prov = agentConfig.provider
        self.sys_prompt = agentConfig.system_prompt
        self.context = agentConfig.context
        self.session_id = agentConfig.session_id

    def chat(self, message: str):
        self.context.add_context(self.session_id , 'user', message)
        for _ in range(MAX_TOOL_CALLS ):

            messages=[{'role': 'system', 'content': self.sys_prompt}] + self.context.get_context(self.session_id )

            events = self.prov.chat(messages, tools.schemas())

            content, calls = "", {}
            for event in events: 
                if event.event_type  == "done":
                    continue

                if event.event_type == "thinking":
                    yield { 'behavior': 'thinking', 'content': event.content}

                if event.event_type == "content":
                    yield { 'behavior': 'replying', 'content': event.content}
                    content = content + event.content

                if event.event_type == "tool_call":
                    calls = event.tool_calls
                    for call in calls.values():
                        yield{ 'behavior': 'tool call', 'tool': call.name,'content' : f"\n`{call.args}`\n"}

            if not calls:
                self.context.add_context(self.session_id , 'assistant', content)
                break


            self.context.add_context(self.session_id, 'assistant', content,  [{"id": c.id , "type": "function",
                 "function": {"name": c.name, "arguments": c.args or "{}"}}
                for c in calls.values()] or [])
                
            for result in handle_tool_calls(calls) or []:
                self.context.add_tool_result(self.session_id , result.id, result.result)