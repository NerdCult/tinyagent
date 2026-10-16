"""xAI Grok API. Key is read from keys/grok (never commit that folder)."""
from openai import OpenAI
from providers import read_key

NAME = "Grok (xAI API)"

def make_client():
    return OpenAI(base_url="https://api.x.ai/v1", api_key=read_key("grok"), timeout=600)

def list_models(client):
    ids = [m.id for m in client.models.list().data]
    return sorted(i for i in ids if "image" not in i and "imagine" not in i)