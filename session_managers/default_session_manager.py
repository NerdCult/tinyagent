from ..core.interfaces import SessionManager, MemoryManager,SkillManager, SkillManagerSkillMaker, SkillManagerDynamic, Toolbox, ToolboxAdvanced
from ..messages import Message, Part
from ..utils import count_tokens
from ..skill_managers import DefaultSkillManager
from ..memory_managers import SimpleMemoryManager


class DefaultSessionManager(SessionManager):
    def __init__(self,
                 system_prompt: str = '',
                 memory_manager: MemoryManager | None = None, 
                 skill_manager: SkillManager | None = None, 
                 toolbox: Toolbox | None = None,
                 max_tokens: int = 32_000):
        self.system_prompt: str = system_prompt
        self.memory_manager = memory_manager or SimpleMemoryManager()
        self.skill_manager: SkillManager = skill_manager or DefaultSkillManager()
        self.toolbox: Toolbox = toolbox
        if self.toolbox:
            if isinstance(self.toolbox, ToolboxAdvanced):
                self.toolbox.set_session(self)
            self.toolbox.load()
        self.max_tokens = max_tokens

    def add_context(self, message):
        self.memory_manager.add_context(message=message)
        while True:
            if count_tokens(self.get_context(), self.tools()) > self.max_tokens:
                self.memory_manager.trim_context()
                continue
            break
        
    def get_context(self):
        system = f'{self.system_prompt}\n{self.skill_manager.skills()}'
        system_prompt_message = Message(role='system', content=[Part(type='text', data={'text':system})])
        return [system_prompt_message] + self.memory_manager.get_context()
               

    def load_skill(self, skill_name):
        if isinstance(self.skill_manager, SkillManagerDynamic):
            self.skill_manager.load_skill(skill_name=skill_name)
        
    def unload_skill(self, skill_name):        
        if isinstance(self.skill_manager, SkillManagerDynamic):
            self.skill_manager.unload_skill(skill_name=skill_name)

    def create_skill(self, skill_name, description, text):
        if isinstance(self.skill_manager, SkillManagerSkillMaker):
            self.skill_manager.create_skill(skill_name, description, text)

    def has_tools(self) -> bool:
        return self.toolbox is not None

    def create_tool(self, tool_name, code):
        if self.has_tools() and isinstance(self.toolbox, ToolboxAdvanced):
            self.toolbox.create_tool(tool_name=tool_name, code=code)

    def tools(self) -> str | None:
        if self.has_tools():
            return self.toolbox.schemas()

    def handle_tool_calls(self, calls):
        if self.has_tools():
            for result in self.toolbox.handle_tool_calls(calls):
                self.memory_manager.add_context(Message(role='tool', content=[Part(type='text', data={'text': result.result})], tool_call_id=result.id))