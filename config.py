from .core.interfaces.context_manager import ContextManager
from .core.interfaces.provider import Client

class AgentConfig:
    client: Client
    context: ContextManager
    
    def __init__(self, client: Client, context: ContextManager):
        self.client = client
        self.context = context