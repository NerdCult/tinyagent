"""xAI Grok API. Key is read from keys/grok (never commit that folder)."""
from openai import OpenAI
from connections import read_key
from providers.open_ai_provider import OpenAIProvider

NAME = "Grok (xAI API)"

def make_client():
    return OpenAI(base_url="https://api.x.ai/v1", api_key=read_key("grok"), timeout=600)

def list_models(client):
    ids = [m.id for m in client.models.list().data]
    return sorted(i for i in ids if "image" not in i and "imagine" not in i)


def make_provider(client, model_name):
    return OpenAIProvider(client, model_name)
