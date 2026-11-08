from collections import deque
from .context_provider import ContextProvider
from ..messages.message import Message, Part

NAME = 'simple'

def make_context():
    return SimpleContext()

class SimpleContext(ContextProvider):
    def __init__(self, max_length: int = 150):
        self.memory = deque(maxlen=max_length)

    def set_system_prompt(self, system_prompt: str):
        self.system_prompt_message = Message(role='system', content=[Part(type='text', data={'text':system_prompt})])

    def get_context(self, session_id: str):
        return [self.system_prompt_message] + list(self.memory)

    def add_context(self, session_id: str, message: Message):
        self.memory.append(message)

    def get_session_ids(self):
        return ['default']

    def add_session_id(self, id: str):
        pass

