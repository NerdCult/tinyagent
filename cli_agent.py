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

sys_prompt = 'you are Friday. A helpful, however snarky and sarcastic, assistant. Provide quick brief answers   unless a longer explaination is specifically warranted.'   
         
agnt = Agent(prov, sys_prompt, 150)                 

while True:                                                                               
    user = input(Fore.GREEN + '\n>>> ')                                                   
    agnt.chat(user)                                                                       