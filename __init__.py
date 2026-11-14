#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from .cli import cli
from .api_providers import create_openai_client, create_anthropic_client, OpenAIProvider, OpenAIClient, AnthropicProvider, AnthropicClient
from .agent_runtimes import DefaultAgentRuntime
from .api_aggregators import DefaultApiAggregator
from .toolboxes import BasicToolbox
from .core.interfaces import MemoryManager, Toolbox, SkillManager
from .memory_managers import SimpleMemoryManager
from.api_aggregators import DefaultApiAggregator
        

def openai_agent_runtime(url: str, 
                         model: str, 
                         key: str = 'no key', 
                         system_prompt: str = '', 
                         memory_manager: MemoryManager | None = None,
                         skill_manager: SkillManager | None = None,
                         toolbox: Toolbox | None = None,
                         max_tokens: int = 32_000,
                         max_rounds: int = 10):

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

    return DefaultAgentRuntime(
        api_aggregator= DefaultApiAggregator(client=create_anthropic_client(url=url, model=model, key=key)),
        system_prompt=system_prompt,
        memory_manager=memory_manager or SimpleMemoryManager(),
        skill_manager=skill_manager,
        toolbox=toolbox,
        max_tokens=max_tokens,
        max_rounds=max_rounds
    )

__all__ = [
    'cli',
    'create_openai_client', 
    'openai_agent_runtime',
    'create_anthropic_client', 
    'anthropic_agent_runtime',
    'OpenAIProvider', 
    'OpenAIClient', 
    'AnthropicProvider', 
    'AnthropicClient',
    'DefaultAgentRuntime',
    'DefaultApiAggregator',
    'BasicToolbox'
]