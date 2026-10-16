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
while True:
    user = input('>>>')
    context.append({'role': 'user', 'content': user})
    response = prov["client"].chat.completions.create(
                    model="Gemma4 12b", messages=context)

    context.append({'role': 'assistant', 'content': response.choices[0].message.content})
    print ('agent>', response.choices[0].message.content)