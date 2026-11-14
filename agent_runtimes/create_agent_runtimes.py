#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from ..api_providers import create_openai_client, create_anthropic_client
from ..core.interfaces import MemoryManager, Toolbox, SkillManager
from ..memory_managers import SimpleMemoryManager
from ..api_aggregators import DefaultApiAggregator
from . import DefaultAgentRuntime

def openai_agent_runtime(url: str, 
                         model: str, 
                         key: str = 'no key', 
                         system_prompt: str = '', 
                         memory_manager: MemoryManager | None = None,
                         skill_manager: SkillManager | None = None,
                         toolbox: Toolbox | None = None,
                         max_tokens: int = 32_000,
                         max_rounds: int = 10):
    ''' helper function to simplify creating an AgentRuntime session with an OpenAI api'''
    return DefaultAgentRuntime(
        aggregator= DefaultApiAggregator(client=create_openai_client(url=url, model=model, key=key)),
        system_prompt=system_prompt,
        memory_manager=memory_manager or SimpleMemoryManager(),
        skill_manager=skill_manager,
        toolbox=toolbox,
        max_tokens=max_tokens,
        max_rounds=max_rounds
    )


def anthropic_agent_runtime(url: str, 
                         model: str, 
                         key: str = 'no key', 
                         system_prompt: str = '', 
                         memory_manager: MemoryManager | None = None,
                         skill_manager: SkillManager | None = None,
                         toolbox: Toolbox | None = None,
                         max_tokens: int = 32_000,
                         max_rounds: int = 10):
    ''' helper function to simplify creating an AgentRuntime session with the Anthropic api'''
    return DefaultAgentRuntime(
        api_aggregator= DefaultApiAggregator(client=create_anthropic_client(url=url, model=model, key=key)),
        system_prompt=system_prompt,
        memory_manager=memory_manager or SimpleMemoryManager(),
        skill_manager=skill_manager,
        toolbox=toolbox,
        max_tokens=max_tokens,
        max_rounds=max_rounds
    )
