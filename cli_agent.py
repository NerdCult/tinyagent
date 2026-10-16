from colorama import Fore, init  
from agent import Agent                                                     
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

agnt = Agent(prov, sys_prompt, 150)                 
thinking = False
replying = False
while True:                                                                               
    user_input = input(Fore.GREEN + '\n>>> ')   
    try:                                                
        for a in agnt.chat(user_input, model):
            if a['behavior'] == 'thinking':
                if not thinking:
                    thinking = True
                    replying = False
                    print (Fore.LIGHTRED_EX + '\nthinking> ', end="")
                print (Fore.LIGHTRED_EX + a['content'], end="")


            if a['behavior'] == 'replying':
                if not replying:
                    thinking = False
                    replying = True
                    print (Fore.CYAN + '\nagent> ', end="")
                print (Fore.CYAN + a['content'], end="")

    except KeyboardInterrupt:
        pass