from tinyagent.core.interfaces import SkillManagerDynamic

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

def make_session_aware_run(session):
    def run(skill_name: str) -> str:
        try:
            if session.skill_manager and isinstance(session.skill_manager, SkillManagerDynamic):
                session.unload_skill(skill_name)
                return f'{skill_name} unloaded'
            return 'Current skill manager does not implement SkillManagerDynamic'
        except Exception as e:
            return f"Couldn't unload {skill_name}: {e}"

    return run