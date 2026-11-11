SCHEMA = {
    "name": "load_skill",
    "description": "Use to load a skill from the available skills into the session context.",
    "parameters": {
        "type": "object",
        "properties": {
            "skill_name": {"type": "string"}},
        "required": ["skill_name"],
    },
}

def get_context_aware_run(context):
    def run(skill_name: str) -> str:
        try:
            context.load_skill(skill_name)
            return f'{skill_name} loaded'
        except Exception as e:
            return f"Couldn't read {skill_name}: {e}"

    return run