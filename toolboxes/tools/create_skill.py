SCHEMA = {
    "name": "create_skill",
    "description": "Use to create a skill to be added to the available skills into the session context.",
    "parameters": {
        "type": "object",
        "properties": {
            "skill_name": {"type": "string"},
            "description": {"type": "string"},
            "text": {"type": "string"}},
        "required": ["skill_name", "description", "text"],
    },
}

def make_session_aware_run(session):
    def run(skill_name: str, description: str, text: str) -> str:
        try:
            session.create_skill(skill_name, description, text)
            return f'{skill_name} created'
        except Exception as e:
            return f"Couldn't create {skill_name}: {e}"

    return run