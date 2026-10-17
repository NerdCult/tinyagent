from collections import deque

NAME = 'simple'

def make_context():
    return SimpleContext()

class SimpleContext:
    def __init__(self):
        self.memory = deque(maxlen=150)


    def get_context(self):
        return self.memory

    def add_context(self, role, content):
        self.memory.append({'role': role, 'content': content})
