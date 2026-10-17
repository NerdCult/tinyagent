from collections import deque

class Agent:
    def __init__(self, provider, context, sys_prompt, context_length):
        self.prov = provider
        self.sys_prompt = sys_prompt
        self.context = context

    def chat(self, message, model):
        self.context.add_context('user', message)
        
        stream = self.prov["client"].chat.completions.create(
            model=model, 
            messages=[{'role': 'system', 'content': self.sys_prompt}] + list(self.context.get_context()),
            stream=True)

        content = ""

        for chunk in stream:        
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            # reasoning text (llama-server: reasoning_content, some APIs: reasoning). Not saved to history.
            extra = getattr(delta, "model_extra", None) or {}
            rtext = getattr(delta, "reasoning_content", None) or extra.get("reasoning_content")or extra.get ("reasoning")

            if rtext:
                yield { 'behavior': 'thinking', 'content': rtext}

            if delta.content:
                yield { 'behavior': 'replying', 'content': delta.content}
                content = content + delta.content
        
        self.context.add_context('assistant', content)

