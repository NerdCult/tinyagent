SCHEMA = {
    "name": "unload_skill",
    "description": "Use to unload a skill from the currently loaded skills in the session context.",
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
            context.unload_skill(skill_name)
            return f'{skill_name} unloaded'
        except Exception as e:
            return f"Couldn't unload {skill_name}: {e}"

    return run