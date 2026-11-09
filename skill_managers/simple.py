import os, json
from .skill_manager import SkillManager

DEFAULT_SKILLS_PATH = os.path.dirname(__file__) + './skills'

class SimpleSkillManager(SkillManager):
    def __init__(self, skill_folder: str = DEFAULT_SKILLS_PATH):
        self.skills_folder = skill_folder
        self.menu_preamble = 'Provided below are the available skills in this environment. To have it loaded into the context use the load_skill tools providing the name of the skill to load. Use unload_skill if a skill is no longer needed.'
        self.menu = {}
        self.loaded_skills = {}
        self.reload_skills()

    def set_skills_folder(self, path: str):
        self.skills_folder = path
        self.reload_skills

    def reload_skills(self):
        self.loaded_skills.clear()

    def skills(self):
        accumulater = ""
        for text in self.loaded_skills.items():
            accumulater = f'{accumulater}\n {text}'
        current = f"{self.menu_preamble}\n { accumulater }"
        return current

    def load_skill(self, skill_name):
        self.get_skill_from_file(f'{self.skills_folder}/{skill_name}')

    def unload_skill(self, skill_name):
        self.loaded_skills.pop(skill_name)

    def get_skill_from_file(self,file_path: str):
        pass