from collections import deque

NAME = 'simple'

def make_context():
    return SimpleContext()

class SimpleContext:
    def __init__(self):
        self.memory = deque(maxlen=10)

    def get_context(self):
        return self.memory

    def add_context_with_tool_calls(self, role, content, tool_calls):
        self.memory.append({'role': role, 'content': content, 'tool_calls': tool_calls})
        
    def add_context(self, role, content):
        self.memory.append({'role': role, 'content': content})

    def add_tool_result(self, tool_call_id, content):
        self.memory.append({"role": "tool", "tool_call_id": tool_call_id, "content": content})

    def reset(self, max_length=10):
        self.memory.clear()
        self.memory = deque(maxlen=max_length)
