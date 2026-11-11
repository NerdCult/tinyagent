from collections.abc import Iterator
from .context_manager import ContextManager
from ..messages.message import Message, Part, user_message
from ..messages.tool_call_result import ToolCallResult
from ..messages.token_calculator import count_tokens
from ..skill_managers.skill_manager import SkillManager
from ..toolboxes.toolbox import Toolbox


class SimpleContextManager(ContextManager):
    def __init__(self, skill_manager: SkillManager, toolbox: Toolbox | None = None, max_tokens: int = 32_000):
        self.memory: list = []
        self.max_tokens = max_tokens
        self.skill_manager: SkillManager = skill_manager
        self.toolbox: Toolbox = toolbox
        if self.toolbox:
            self.toolbox.load(self)
        self.system_prompt: str = ''

    def set_system_prompt(self, system_prompt: str):
        self.system_prompt = system_prompt

    def get_context(self) -> list[Message]:
        system = f'{self.system_prompt}\n{self.skill_manager.skills()}'
        system_prompt_message = Message(role='system', content=[Part(type='text', data={'text':system})])
        return [system_prompt_message] + list(self.memory)

    def add_context(self, message: Message):
        self.memory.append(message)
        self._trim_context()

    def _trim_context(self):
        dropped_tool_call_ids: set[str] = set()

        def pop_front():
            popped = self.memory.pop(0)
            if popped.tool_calls:
                dropped_tool_call_ids.update(tc.id for tc in popped.tool_calls)

        while count_tokens(self.get_context(), self.tools() if self.has_tools() else None) > self.max_tokens:
            pop_front()

        while self.memory and self.memory[0].role != 'user':
            pop_front()

        if dropped_tool_call_ids:
            self.memory = [ m for m in self.memory if m.tool_call_id not in dropped_tool_call_ids]

        if not self.memory or len(self.memory) == 0:
            self.memory.append(user_message('run away context trimming, deleted that whole context!'))
        

    def load_skill(self, skill_name):
        self.skill_manager.load_skill(skill_name=skill_name)
        
    def unload_skill(self, skill_name):
        self.skill_manager.unload_skill(skill_name=skill_name)

    def create_skill(self, skill_name, description, text):
        self.skill_manager.create_skill(skill_name, description, text)

    def has_tools(self) -> bool:
        return self.toolbox is not None

    def create_tool(self, tool_name, code):
        if self.has_tools():
            self.toolbox.create_tool(tool_name=tool_name, code=code, context=self)

    def tools(self) -> str:
        return self.toolbox.schemas()

    def handle_tool_calls(self, calls) -> Iterator[ToolCallResult]:
        for c in calls.values():
            try:
                out = self.toolbox.run_tool(c.name, c.args)
            except Exception as e:
                out = f"error: {type(e).__name__}: {e}"
            yield ToolCallResult(id=c.id, result=out)