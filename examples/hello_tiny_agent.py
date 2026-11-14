#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from tinyagent import openai_agent_runtime, cli

#configure your connection

URL = 'https://api.openai.com/v1'   # or your preferred endpoint
MODEL = 'gpt-4o-mini'               # or whatever you prefer
KEY = 'your-key-here'

#Create a basic instance of AgentRuntime
# use anthropic_agent_runtime if you want to connect to their api
runtime = openai_agent_runtime(url=URL, model=MODEL, key=KEY)

#Launch the command line interface to interact with the AgentRuntime runtime. output is color-coded green -> user, red -> agent thinking, yellow -> tool calls, blue -> agent reply
cli(runtime)