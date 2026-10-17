from colorama import Fore, init  
from agent import Agent                                                     
import providers
import context    

init(autoreset=True)   

providers.load()
context.load()               

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

print ('Please select a context tracker:')
x = 0
contexts = {}
for c in context.summary():
    x = x + 1
    contexts[x] = c['name']
    print (x, c['name'])

context_selection = int(input())

context_provider = context.CONTEXTS[contexts[context_selection]]['context']

sys_prompt = 'you are Friday. A helpful, however snarky and sarcastic, assistant. Provide quick brief answers   unless a longer explaination is specifically warranted.' 

print (f'Current system prompt:\n{sys_prompt}\npress enter to keep or type a new system prompt:')

new_sp = input()

if new_sp != '':
    sys_prompt = new_sp

agnt = Agent(prov, context_provider, sys_prompt, 150)                 
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