from providers.provider import Provider, StreamEvent

class OpenAIProvider(Provider):
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name
    
    def chat(self, messages: list[str], tools: list[object]):
        stream = self.client.chat.completions.create(
            model=self.model_name, 
            messages=messages,
            tools=tools,
            stream=True)

        for chunk in stream:
            if not chunk.choices:
                yield StreamEvent(
                    event_type="done"
                )
            
            delta = chunk.choices[0].delta

            extra = getattr(delta, "model_extra", None) or {}
            rtext = getattr(delta, "reasoning_content", None) or extra.get  ("reasoning_content") or extra.get ("reasoning")

            if rtext:
                yield StreamEvent(
                    event_type="thinking",
                    content=rtext,
                    raw=chunk
                 )

            if delta.content:
                yield StreamEvent(
                    event_type="content",
                    content=delta.content,
                    raw=chunk
                )