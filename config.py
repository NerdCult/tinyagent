from context.contextProvider import ContextProvider
from providers.provider import Provider

class AgentConfig:
    model: str
    session_id: str
    context: ContextProvider
    system_prompt: str
    def __init__(self, lm_provider: Provider,  session_id: str, context: ContextProvider, system_prompt: str):
        self.provider = lm_provider
        self.session_id = session_id
        self.context = context
        self.system_prompt = system_prompt