from typing import Protocol

class SkillManager(Protocol):
    def skills(self):
        pass

    def reload_skills(self):
        pass

    def load_skill(self, skill_name: str):
        pass

    def unload_skill(self, skill_name: str):
        pass

    def create_skill(self, skill_name: str, description: str, text: str):
        pass