**UNDER CONSTRUCTION**

hello Tiny Agent:

The sample code below will run a simple command line chat interface.
DefaultAgentRuntime can accept a Skill Manager and a Toolbox.
The BasicToolbox can browse/read your files, browse the web, load and unload skills (with compatible Skill Manager) .
The AdvancedToolbox adds tools to write and delete files, create new tools, and create new skills (with compatible Skill Manager). 
**USE ADVANCED TOOLBOX WITH CAUTION. THERE ARE NO HARD BUILT IN GUARDRAILS**

```
from tinyagent import *

URL = 'url'
KEY= 'your key'
MODEL = 'model name'

SYSTEM_PROMPT = 'You are "Tiny Agent". A helpful, however snarky and sarcastic, assistant. Provide quick brief answers unless a longer explaination is specifically warranted. If a longer explaination is warranted, open with a TL;DR summary, sticking to the helpful however snarky and saracastic persona. Following the TL;DR provide the complete answer in a direct, state the facts manner.'

client = create_openai_client(URL, MODEL, KEY)

session = DefaultAgentRuntime(DefaultApiAggregator(client), SYSTEM_PROMPT)

cli(session)
```

save this code to a hello_tiny_agent.py file
update with your url, key, and model name.

if appropriate swap 'create_openai_client' for 'create_anthropic_client'

from the command line run 'python hello_tiny_agent.py'

when the prompt '>>>' you can type your message and hit enter