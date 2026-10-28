import tools, threading

MAX_TOOL_CALLS = 10

class Agent:
    def __init__(self, agentConfig: AgentConfig):
        self.prov = agentConfig.provider
        self.sys_prompt = agentConfig.system_prompt
        self.context = agentConfig.context
        self.session_id = agentConfig.session_id

    def chat(self, message: string):
        self.context.add_context(self.session_id , 'user', message)
        for _ in range(MAX_TOOL_CALLS ):

            messages=[{'role': 'system', 'content': self.sys_prompt}] + self.context.get_context(self.session_id )

            events = self.prov.chat(messages, tools.schemas())

            content, calls = "", {}
            for event in events: 
                if event.event_type  == "done":
                    return

                if event.event_type == "thinking":
                    yield { 'behavior': 'thinking', 'content': event.content}

                if event.event_type == "content":
                    yield { 'behavior': 'replying', 'content': event.content}
                    content = content + event.content

            self.context.add_context(self.session_id , 'assistant', content)
            break

            #     for tc in event.tool_calls or []:
            #         c = calls.setdefault(tc.index, {"id": "", "name": "", "args": ""})
            #         if tc.id: c["id"] = tc.id
            #         if tc.function and tc.function.name: c["name"] += tc.function.name
            #         if tc.function and tc.function.arguments: c["args"] += tc. function.arguments

            # if not calls:
            #     self.context.add_context(self.session_id , 'assistant', content)
            #     break
        
            # ordered = [calls[i] for i in sorted(calls)]

            # self.context.add_context(self.session_id, 'assistant', content,  [{"id": c["id"] or f"call_{i}", "type": "function",
            #      "function": {"name": c["name"], "arguments": c["args"] or "{}"}}
            #     for i, c in enumerate(ordered)] or [])
            
            # for i, c in enumerate(ordered):
            #     yield { 'behavior': 'tool call', 'tool': c['name'],'content' : {f"\n`[{c['name']}: {c['args']}]`\n"}}
            #     box = {}
            #     def _run(name=c["name"], args=c["args"], box=box):
            #         box["out"] = tools.run_tool(name, args)
            #     worker = threading.Thread(target=_run, daemon=True)
            #     worker.start()
            #     while worker.is_alive():
            #         worker.join(0.25)
            #     self.context.add_tool_result(self.session_id , c["id"] or f"call_{i}", box.get("out", ""))
