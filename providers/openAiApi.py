"""Local llama-server (run_llama.bat)."""
from openai import OpenAI

NAME = "Local (llama-server)"
DEFAULT_MODEL = "gemma4-12b"


def make_client():
    return OpenAI(base_url="http://localhost:8080/v1", api_key="llama-server", timeout=600) 

def list_models(client):
    ids = [m.id for m in client.models.list().data]
    return sorted(i for i in ids if "image" not in i and "imagine" not in i)