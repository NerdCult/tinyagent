from collections import deque

NAME = 'simple'

def make_context():
    return SimpleContext()

class SimpleContext:
    def __init__(self):
        self.memory = deque(maxlen=10)


    def get_context(self):
        return self.memory

    def add_context(self, role, content):
        self.memory.append({'role': role, 'content': content})

    def reset(self, max_length):
        self.memory.clear()
        self.memory = deque(maxlen=max_length)
