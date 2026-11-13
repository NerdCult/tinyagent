from ..core.interfaces.session_manager import SessionManager
from ..messages.message import Message, Part
from ..utils.token_calculator import count_tokens
from ..core.interfaces import MemoryManager,SkillManager, SkillManagerSkillMaker, SkillMangerDynamic, Toolbox, ToolboxAdvanced
from ..skill_managers.simple_skill_manager import SimpleSkillManager
from ..memory_managers.simple_memory_manager import SimpleMemoryManager
from ..agent import Agent


class DefaultSessionManager(SessionManager):
    def __init__(self, agent:Agent, 
                 system_prompt: str = '',
                 memory_manager: MemoryManager | None = None, 
                 skill_manager: SkillManager | None = None, 
                 toolbox: Toolbox | None = None,
                 max_tokens: int = 32_000):
        self.agent = agent
        self.system_prompt: str = system_prompt
        self.memory_manager = memory_manager or SimpleMemoryManager()
        self.skill_manager: SkillManager = skill_manager or SimpleSkillManager()
        self.toolbox: Toolbox = toolbox
        if self.toolbox:
            self.toolbox.load(self)
        self.max_tokens = max_tokens

    def chat(self, message):
        self.memory_manager.add_context(message)
        turn_messages = self.get_context()

        for agent_message in self.agent.chat(turn_messages, self.toolbox.schemas()):
            if agent_message.behavior == 'message' and agent_message.message:
                self.memory_manager.add_context(agent_message.message)

                if agent_message.message.tool_calls:
                    print ('message had tool calls')
                    for result in self.toolbox.handle_tool_calls(agent_message.message.tool_calls):
                        print (result)
                        self.memory_manager.add_context(Message(role='tool', content=[Part(type='text', data={'text': result.result})], tool_call_id=result.id))

            else:
                yield agent_message

    def get_context(self):
        memory: list[Message]
        while True:
            memory = self.memory_manager.get_context()

            system = f'{self.system_prompt}\n{self.skill_manager.skills()}'
            system_prompt_message = Message(role='system', content=[Part(type='text', data={'text':system})])
            full_context = [system_prompt_message] + memory

            if count_tokens(full_context, self.tools() if self.has_tools() else None) > self.max_tokens:
                self.memory_manager.trim_context()
                continue
            break
        return memory        

    def load_skill(self, skill_name):
        if isinstance(self.skill_manager, SkillMangerDynamic):
            self.skill_manager.load_skill(skill_name=skill_name)
        
    def unload_skill(self, skill_name):        
        if isinstance(self.skill_manager, SkillMangerDynamic):
            self.skill_manager.unload_skill(skill_name=skill_name)

    def create_skill(self, skill_name, description, text):
        if isinstance(self.skill_manager, SkillManagerSkillMaker):
            self.skill_manager.create_skill(skill_name, description, text)

    def has_tools(self) -> bool:
        return self.toolbox is not None

    def create_tool(self, tool_name, code):
        if self.has_tools() and isinstance(self.toolbox, ToolboxAdvanced):
            self.toolbox.create_tool(tool_name=tool_name, code=code, context=self)

    def tools(self) -> str:
        if self.has_tools():
            return self.toolbox.schemas()