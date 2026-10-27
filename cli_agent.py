from colorama import Fore, init  
from agent import Agent, AgentConfig                                                    
import providers
from context.simple import SimpleContext  
import tools

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

print ("Please Select your model:") 

x = 0  
models = {}
for m in prov['models']:
    x = x + 1                
    print (f"{x}. {m}")
    models[x] = m

model_selection = int(input())

model = models[model_selection]

sys_prompt = 'you are Friday. A helpful, however snarky and sarcastic, assistant. Provide quick brief answers   unless a longer explaination is specifically warranted.' 

agentConfig = AgentConfig(prov, model, 'default', SimpleContext(), sys_prompt)

tools.load(agentConfig)

agnt = Agent(agentConfig)                 

while True:
    thinking = False
    replying = False
    using_tool = False                                                
    user_input = input(Fore.GREEN + '\n>>> ')   
    try:                                                
        for a in agnt.chat(user_input):
            behavior = a['behavior']
            content = a['content']
            
            if behavior == 'thinking':
                if not thinking:
                    thinking = True
                    replying = False
                    using_tool = False
                    print (Fore.LIGHTRED_EX + '\nthinking> ', end="")
                print (Fore.LIGHTRED_EX + content, end="")


            if behavior == 'replying':
                if not replying:
                    thinking = False
                    replying = True
                    using_tool = False
                    print (Fore.CYAN + '\nagent> ', end="")
                print (Fore.CYAN + content, end="")

            if behavior == 'tool call':
                if not using_tool:
                    thinking = False
                    replying = False
                    using_tool = True
                    print (Fore.LIGHTYELLOW_EX + "\ntool> ", end="")
                print (Fore.LIGHTYELLOW_EX + f'{a['tool'] or ""} > {content or "no content"}', end="")

    except KeyboardInterrupt:
        pass