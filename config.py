from .context.context_provider import ContextProvider
from .providers.provider import Client

class AgentConfig:
    client: Client
    context: ContextProvider
    
    def __init__(self, client: Client, context: ContextProvider):
        self.client = client
        self.context = context