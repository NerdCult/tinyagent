from collections import deque
from colorama import Fore, init  

class Agent:
    def __init__(self, provider, sys_prompt, context_length):
        self.prov = provider
        self.context = deque(maxlen=context_length)
        self.sys_prompt = sys_prompt

    def chat(self, message):
        self.context.append({'role': 'user', 'content': message})
        
        stream = self.prov["client"].chat.completions.create(
            model="gemma-4-12B-it-QAT-GGUF", 
            messages=[{'role': 'system', 'content': self.sys_prompt}] + list(self.context),
            stream=True)

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
                self.context.append({'role': 'assistant', 'content': delta.content})

