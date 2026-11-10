from collections import deque
from .context_provider import ContextProvider
from ..messages.message import Message, Part
from ..skill_managers.skill_manager import SkillManager

NAME = 'simple'

class SimpleContext(ContextProvider):
    def __init__(self, skill_manager: SkillManager, max_length: int = 50):
        self.memory = deque(maxlen=max_length)
        self.skill_manager = skill_manager
        self.system_prompt = ''

    def set_system_prompt(self, system_prompt: str):
        self.system_prompt = system_prompt

    def get_context(self):
        system = f'{self.system_prompt}\n{self.skill_manager.skills()}'
        system_prompt_message = Message(role='system', content=[Part(type='text', data={'text':system})])
        return [system_prompt_message] + list(self.memory)

    def add_context(self, message: Message):
        self.memory.append(message)

    def load_skill(self, skill_name):
        self.skill_manager.load_skill(skill_name=skill_name)
        
    def unload_skill(self, skill_name):
        self.skill_manager.unload_skill(skill_name=skill_name)

    def create_skill(self, skill_name, description, text):
        self.skill_manager.create_skill(skill_name, description, text)