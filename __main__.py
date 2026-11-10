from pathlib import Path
from .agent import Agent
from .config import AgentConfig
from .context.simple import SimpleContext 
from .providers.open_ai import OpenAiProvider
from .skill_managers.simple import SimpleSkillManager
from . import tools 
from . import OPEN_AI_URLS, cli

if __name__ == '__main__':
    print ('Welcome to the TinyAgent demo CLI.')
    api_selection = int(input ("Please Select your api type:\n1. OpenAI\n2. Anthropic\n")) 

    if api_selection == 1:
        x = 0
        urls = {}

        print ('Please select url or enter 0 to manually enter: ')
        for api in OPEN_AI_URLS:
            x = x +1
            urls[x] = {'name': api, 'url':OPEN_AI_URLS[api]}
            print (f'{x}. {api}: {OPEN_AI_URLS[api]}')  

    else:
        print ('Only OpenAI currently supported')
        exit()

    url_selection = int (input ())
    if url_selection == 0:
        url = input ('Please enter the desired url (ex. https://127.0.0.1:8080/v1): ')
        key = input ('Please enter your api key or hit enter if one is not needed: ')
    else:
        url = urls[url_selection]['url']
    
        key_path = f'./keys/{urls[url_selection]['name']}'

        print (f'Checking for key file at {key_path}')

        if Path.is_file(key_path):
            with open(key_path, encoding="utf-8") as f:
                key = f.read().strip()
        else:
            key = input ('Key file was not found, Please enter your key or just hit enter if no key is needed:')  or 'no key'
        
    if api_selection == 1:
        provider = OpenAiProvider(url, key)

    print ("Please Select your model:") 

    x = 0  
    models = {}
    for m in provider.list_models():
        x = x + 1                
        print (f"{x}. {m}")
        models[x] = m

    model_selection = int(input())

    model = models[model_selection]

    client = provider.make_client(model)

    sys_prompt = 'You are Friday. A helpful, however snarky and sarcastic, assistant. Provide quick brief answers unless a longer explaination is specifically warranted. If a longer explaination is warranted, open with a TL;DR summary, sticking to the helpful however snarky and saracastic persona. Following the TL;DR provide the complete answer in a direct, state the facts manner.' 

    print (f'default system prompt: {sys_prompt}')

    new_sys_prompt = input ('Enter a new system prompt or hit enter to accept default: ') or sys_prompt

    context = SimpleContext(skill_manager=SimpleSkillManager(), max_length=50)
    context.set_system_prompt(sys_prompt)
    agentConfig = AgentConfig(client, 'default', context)

    tools.load(agentConfig)

    agnt = Agent(agentConfig)                 

    cli(agnt)