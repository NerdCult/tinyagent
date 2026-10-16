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

while True:
    user = input()
    response = prov["client"].chat.completions.create(
                    model="Gemma4 12b", messages=[
                        {"role": "user", "content": user}
                    ])

    print (response.choices[0].message.content)