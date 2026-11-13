from collections.abc import Iterator
from ..core.interfaces import SessionManager, MemoryManager,SkillManager, Toolbox, ToolboxAdvanced
from ..messages import Message, Part, AgentMessage
from ..utils import count_tokens
from ..skill_managers import DefaultSkillManager
from ..memory_managers import SimpleMemoryManager
from .. agent import Agent


class DefaultSessionManager(SessionManager):
    def __init__(self,
                 agent: Agent,
                 system_prompt: str = '',
                 memory_manager: MemoryManager | None = None, 
                 skill_manager: SkillManager | None = None, 
                 toolbox: Toolbox | None = None,
                 max_tokens: int = 32_000,
                 max_rounds: int = 10):
        self.agent: Agent = agent
        self.system_prompt: str = system_prompt
        self.memory_manager = memory_manager or SimpleMemoryManager()
        self.skill_manager: SkillManager = skill_manager or DefaultSkillManager()
        self.toolbox: Toolbox = toolbox
        if self.toolbox:
            if isinstance(self.toolbox, ToolboxAdvanced):
                print ('advanced toolbox')
                self.toolbox.set_session(self)
            self.toolbox.load()
        self.max_tokens = max_tokens
        self.max_rounds = max_rounds

    def _add_context(self, message):
        self.memory_manager.add_context(message)
        while True:
            if count_tokens(self._get_context(), self._tools()) > self.max_tokens:
                self.memory_manager.trim_context()
                continue
            break
        
    def _get_context(self):
        system = f'{self.system_prompt}\n{self.skill_manager.skills()}'
        system_prompt_message = Message(role='system', content=[Part(type='text', data={'text':system})])
        return [system_prompt_message] + self.memory_manager.get_context()
    
    def _has_tools(self) -> bool:
        return self.toolbox is not None

    def _tools(self) -> str | None:
        if self._has_tools():
            return self.toolbox.schemas()
        return None

    def handle_user_message(self, message: Message) -> Iterator[AgentMessage]:        
        self._add_context(message)
        tool_calls = None
        for _ in range(self.max_rounds):
            context = self._get_context()
            for agent_message in self.agent.process_context(context, self._tools()):
                if agent_message.behavior == 'message':
                    self._add_context(agent_message.message)
                    tool_calls = agent_message.message.tool_calls

                yield agent_message

            if not tool_calls:
                break

            if self._has_tools():
                for result in self.toolbox.handle_tool_calls(tool_calls):
                    self._add_context(Message(role='tool', content=[Part(type='text', data={'text': result.result})], tool_call_id=result.id))

                    
