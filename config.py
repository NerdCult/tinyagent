from .context.context_provider import ContextProvider
from .providers.provider import Provider

class AgentConfig:
    provider: Provider
    session_id: str
    context: ContextProvider
    
    def __init__(self, lm_provider: Provider,  session_id: str, context: ContextProvider):
        self.provider = lm_provider
        self.session_id = session_id
        self.context = context