import tools, threading

tools.load()

MAX_TOOL_CALLS = 10

class Agent:
    def __init__(self, provider, context, sys_prompt):
        self.prov = provider
        self.sys_prompt = sys_prompt
        self.context = context

    def chat(self, message, model):
        self.context.add_context('user', message)
        for _ in range(MAX_TOOL_CALLS ):
            stream = self.prov["client"].chat.completions.create(
                model=model, 
                messages=[{'role': 'system', 'content': self.sys_prompt}] + list(self.context.get_context()),
                tools=tools.schemas(),
                stream=True)

            content, calls = "", {}
            for chunk in stream:        
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta

                extra = getattr(delta, "model_extra", None) or {}
                rtext = getattr(delta, "reasoning_content", None) or extra.get  ("reasoning_content") or extra.get ("reasoning")

                if rtext:
                    yield { 'behavior': 'thinking', 'content': rtext}

                if delta.content:
                    yield { 'behavior': 'replying', 'content': delta.content}
                    content = content + delta.content
                for tc in delta.tool_calls or []:
                    c = calls.setdefault(tc.index, {"id": "", "name": "", "args": ""})
                    if tc.id: c["id"] = tc.id
                    if tc.function and tc.function.name: c["name"] += tc.function.name
                    if tc.function and tc.function.arguments: c["args"] += tc. function.arguments

            if not calls:
                self.context.add_context('assistant', content)
                break
        
            ordered = [calls[i] for i in sorted(calls)]

            self.context.add_context('assistant', content,  [{"id": c["id"] or f"call_{i}", "type": "function",
                 "function": {"name": c["name"], "arguments": c["args"] or "{}"}}
                for i, c in enumerate(ordered)] or [])
            
            for i, c in enumerate(ordered):
                yield { 'behavior': 'tool call', 'tool': c['name'],'content' : {f"\n`[{c['name']}: {c['args']}]`\n"}}
                box = {}
                def _run(name=c["name"], args=c["args"], box=box):
                    box["out"] = tools.run_tool(name, args)
                worker = threading.Thread(target=_run, daemon=True)
                worker.start()
                while worker.is_alive():
                    worker.join(0.25)
                self.context.add_tool_result( c["id"] or f"call_{i}", box.get("out", ""))
