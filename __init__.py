from .cli import cli
from .api_providers import create_openai_client, create_anthropic_client, OpenAIProvider, OpenAIClient, AnthropicProvider, AnthropicClient
from .agent_runtimes import DefaultAgentRuntime
from .api_aggregators import DefaultApiAggregator
from .toolboxes import BasicToolbox

OPEN_AI_URLS = {
    "openai": "https://api.openai.com/v1",
    "grok": "https://api.x.ai/v1",
    "local": "http://127.0.0.1:8080/v1",
    "ollama": "http://127.0.0.1:11434/v1",
}

ANTHROPIC_URLS = {
    "anthropic": "https://api.anthropic.com"
}

__all__ = [
    'cli',
    'create_openai_client', 
    'create_anthropic_client', 
    'OpenAIProvider', 
    'OpenAIClient', 
    'AnthropicProvider', 
    'AnthropicClient',
    'DefaultAgentRuntime',
    'DefaultApiAggregator',
    'BasicToolbox'
]