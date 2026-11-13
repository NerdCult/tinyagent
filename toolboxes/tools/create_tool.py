SCHEMA = {
    "name": "create_tool",
    "description": """Creates a new tool and loads it. `code` must be a complete Python source string with imports at the top, a SCHEMA dict, and a run function. SCHEMA is OpenAI function format: name, description, and parameters ({"type": "object", "properties": {...}, "required": [...]}). SCHEMA["name"] must equal tool_name. run arguments must match the schema properties. run's return value is json.dumps'd, so return a str, dict, list, number, or bool. Do not read other tool files to learn this format.""",
    "parameters": {
        "type": "object",
        "properties": {
            "tool_name": {"type": "string"},
            "code": {"type": "string"},
        },
        "required": ["tool_name", "code"]    
    }
}

def make_session_aware_run(session):
    def run(tool_name: str, code: str) -> str:
        try:
            session.create_tool(tool_name, code)
            return f'{tool_name} created'
        except Exception as e:
            return f"Couldn't create {tool_name}: {e}"

    return run