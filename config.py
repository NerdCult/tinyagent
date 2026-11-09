from .context.context_provider import ContextProvider
from .providers.provider import Client

class AgentConfig:
    client: Client
    session_id: str
    context: ContextProvider
    
    def __init__(self, client: Client,  session_id: str, context: ContextProvider):
        self.client = client
        self.session_id = session_id
        self.context = context