from collections import deque
import providers

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

context = deque(maxlen=150)
sys_prompt = 'you are Friday. A helpful, however snarky and sarcastic, assistant. Provide quick brief answers unless a longer explaination is specifically warranted.'

while True:
    user = input('>>>')
    context.append({'role': 'user', 'content': user})
    response = prov["client"].chat.completions.create(
                    model="Gemma4 12b", 
                    messages=[{'role': 'system', 'content': sys_prompt}] + list(context))

    context.append({'role': 'assistant', 'content': response.choices[0].message.content})
    print ('agent>', response.choices[0].message.content)