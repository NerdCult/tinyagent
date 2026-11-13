from .core.interfaces.session_manager import SessionManager
from .core.interfaces.provider import Client

class AgentConfig:
    client: Client
    context: SessionManager
    
    def __init__(self, client: Client, context: SessionManager):
        self.client = client
        self.context = context