from collections import deque
from context import ContextProvider

NAME = 'simple'

def make_context():
    return SimpleContext()

class SimpleContext(ContextProvider):
    def __init__(self, max_length = 150):
        self.memory = deque(maxlen=max_length)

    def get_context(self):
        return self.memory

    def add_context(self, role, content, tool_calls= None):
        if not tool_calls:
            self.memory.append({'role': role, 'content': content})
            return
        self.memory.append({'role': role, 'content': content, 'tool_calls': tool_calls})

    def add_tool_result(self, tool_call_id, content):
        self.memory.append({"role": "tool", "tool_call_id": tool_call_id, "content": content})

