#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from tinyagent.core.interfaces import SkillManagerDynamic

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
            if session.skill_manager and isinstance(session.skill_manger, SkillManagerSkillMaker):
                session.skill_manager.create_skill(skill_name, description, text)
                return f'{skill_name} created'
            return 'Current skill manager does not implement SkillManagerSkillMaker'
        except Exception as e:
            return f"Couldn't create {skill_name}: {e}"

    return run