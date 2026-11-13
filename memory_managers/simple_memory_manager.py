from ..core.interfaces.memory_manager import MemoryManager
from ..messages import Message, user_message


class SimpleMemoryManager(MemoryManager):
    def __init__(self):
        self.memory: list = []

    def get_context(self) -> list[Message]:
        return self.memory

    def add_context(self, message: Message):
        self.memory.append(message)

    def trim_context(self):
        
        dropped_tool_call_ids: set[str] = set()

        def pop_front():
            popped = self.memory.pop(0)
            if popped.tool_calls:
                dropped_tool_call_ids.update(tc.id for tc in popped.tool_calls)

        pop_front()

        while self.memory and self.memory[0].role != 'user':
            pop_front()

        if dropped_tool_call_ids:
            self.memory = [ m for m in self.memory if m.tool_call_id not in dropped_tool_call_ids]

        if not self.memory or len(self.memory) == 0:
            self.memory.append(user_message('run away context trimming, deleted that whole context!'))
