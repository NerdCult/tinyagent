from .anthropic_provider import AnthropicClient, AnthropicProvider
from .open_ai_provider import OpenAIClient, OpenAIProvider

__all__=[
    'AnthropicClient',
    'AnthropicProvider',
    'OpenAIClient',
    'OpenAIProvider'
]

def create_openai_client(url: str, model: str, key: str):
    return OpenAIProvider(url, key).make_client(model)


def create_anthropic_client(url: str, model: str, key: str):
    return AnthropicProvider(url, key).make_client(model)