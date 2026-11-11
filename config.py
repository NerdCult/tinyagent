from .context_managers.context_manager import ContextManager
from .api_providers.provider import Client

class AgentConfig:
    client: Client
    context: ContextManager
    
    def __init__(self, client: Client, context: ContextManager):
        self.client = client
        self.context = context