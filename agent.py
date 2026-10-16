from collections import deque

class agent:
    def __init__(self, provider, sys_prompt, context_length):
        self.prov = provider
        self.context = deque(maxlen=context_length)
        self.sys_prompt = sys_prompt

    def chat(self, message):
        self.context.append({'role': 'user', 'content': user})
        try:
            stream = self.prov["client"].chat.completions.create(
                model="Gemma4 12b", 
                messages=[{'role': 'system', 'content': self.sys_prompt}] + list(self.context),
                stream=True)

            thinking, answering = False, False

            for chunk in stream:        
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                # reasoning text (llama-server: reasoning_content, some APIs: reasoning). Not saved to history.
                extra = getattr(delta, "model_extra", None) or {}
                rtext = getattr(delta, "reasoning_content", None) or extra.get("reasoning_content")or extra.get ("reasoning")
                if rtext:
                    if not thinking:
                        print (Fore.LIGHTRED_EX + '\nthinking> ')
                        thinking = True
                        answering = False
                    print (Fore.LIGHTRED_EX + rtext, end= "")
                if delta.content:
                    if not answering:
                        print (Fore.CYAN + '\nagent> ', end="")
                        thinking = False
                        answering = True

                    print (Fore.CYAN + delta.content, end= "")

                    self.context.append({'role': 'assistant', 'content': delta.content})

        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    from colorama import Fore, init
    import providers

    init(autoreset=True)

    providers.load()

    print ("Please Select your provider:")

    x = 0
    provs = {}
    for p in providers.summary():
        x = x + 1
        print (f"{x}. {p['id']}")
        provs[x] = p['id']

    selection = int(input())

    prov = providers.PROVIDERS[provs[selection]]

    print (prov)

    sys_prompt = 'you are Friday. A helpful, however snarky and sarcastic, assistant. Provide quick brief answers   unless a longer explaination is specifically warranted.'

    agnt = agent(prov, sys_prompt, 150)

    while True:
        user = input(Fore.GREEN + '\n>>> ')
        agnt.chat(user)