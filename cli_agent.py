from colorama import Fore, init  
from agent import Agent
from config import AgentConfig                                                    
import connections
from context.simple import SimpleContext  
import tools

init(autoreset=True)   

connections.load()           

print ("Please Select your provider:")   

x = 0                                                                                     
connects = {}                                                                                
for p in connections.summary():                                                             
    x = x + 1                                                                             
    print (f"{x}. {p['id']}")                                                             
    connects[x] = p['id']           

selection = int(input())      

connection = connections.CONNECTIONS[connects[selection]]

print ("Please Select your model:") 

x = 0  
models = {}
for m in connection['models']:
    x = x + 1                
    print (f"{x}. {m}")
    models[x] = m

model_selection = int(input())

model = models[model_selection]

client = connection['make_provider'](connection['client'], model)

print('made provider')

sys_prompt = 'you are Friday. A helpful, however snarky and sarcastic, assistant. Provide quick brief answers   unless a longer explaination is specifically warranted; if longer explaination is warranted open with a TL;DR summary, sticking to the helpful however snarky and saracastic persona. following the TL;DR provide the more in depth answer in a more direct facts only manner.' 

agentConfig = AgentConfig(client, 'default', SimpleContext(), sys_prompt)

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
                print (Fore.LIGHTYELLOW_EX + f"{a['tool'] or ""} > {content or "no content"}", end="")

    except KeyboardInterrupt:
        pass