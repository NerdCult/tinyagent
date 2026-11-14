**UNDER CONSTRUCTION** — Early preview. Things will break. Feedback welcome.

**License:** This software is released under the [PolyForm Noncommercial License 1.0.0](LICENSE). You're free to use it for personal, educational, research, and non-commercial projects.

Want to use it commercially, in a product, or at scale? No problem — just reach out. I'm happy to grant **free short-term evaluation licenses** to companies for testing and prototyping, and long-term licenses can be negotiated.

### Creators & Influencers
If you're a YouTuber, TikToker, blogger, or anyone who makes tech content, feel free to build showcases, reviews, tutorials, or crazy demos with TinyAgent. Just point your viewers to the repo. I'll happily provide a free license if you want one for peace of mind.

Email me at gbdenney84@gmail.com to inquire about a license (or open a GitHub issue).

For full legal terms, see the [LICENSE](LICENSE) file. Commercial use or uses outside the license always requires explicit written approval from the copyright holder (Gene B. Denney).

## Quick Start: Hello TinyAgent

The sample below runs a simple command-line chat interface.

`DefaultAgentRuntime` can accept a Skill Manager and a Toolbox.  
- `BasicToolbox` lets you browse/read files, search the web, and load/unload skills.  
- `AdvancedToolbox` adds file writing, deletion, tool creation, and skill creation.  
**USE THE ADVANCED TOOLBOX WITH CAUTION — THERE ARE NO HARD BUILT-IN GUARDRAILS.**

```python
from tinyagent import *

URL = 'https://api.openai.com/v1'   # or your preferred endpoint
KEY = 'your-key-here'
MODEL = 'gpt-4o-mini'               # or whatever you prefer

session = DefaultAgentRuntime(
    DefaultApiAggregator(create_openai_client(URL, MODEL, KEY))
)

cli(session)
```

1. Save this as `hello_tiny_agent.py`
2. Update the URL, KEY, and MODEL
3. (Optional) Swap `create_openai_client` for `create_anthropic_client` if preferred
4. Run it: `python hello_tiny_agent.py`

When you see the `>>>` prompt, type your message and hit Enter.

**Note:** Gemini's OpenAI-compatible API (currently in beta) works for basic chat but tools are currently broken due to a quirk in their beta implementation.