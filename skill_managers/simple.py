import os, json
from pathlib import Path
from .skill_manager import SkillManager

DEFAULT_SKILLS_PATH = os.path.dirname(__file__) + '/skills'

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
        for file in Path(self.skills_folder).glob("*.json"):
            self.add_skill_to_menu(file.name)

    def skills(self):
        accumulater = f'{self.menu_preamble}\n available skills:'
        for name, description in self.menu.items():
            accumulater = f'{accumulater}\n {name}: {description}'

        accumulater = f'{accumulater}\n loaded skills:'
        for name, text in self.loaded_skills.items():
            accumulater = f'{accumulater}\n {name}: {text}'
        return accumulater

    def load_skill(self, skill_name: str):
        with open(file=f'{self.skills_folder}/{skill_name}') as f:
            t = f.read().strip()
            s = json.loads(t)
            self.loaded_skills[skill_name] = s['text']

    def unload_skill(self, skill_name: str):
        self.loaded_skills.pop(skill_name)

    def add_skill_to_menu(self, skill_name: str):
        with open(file=f'{self.skills_folder}/{skill_name}') as f:
            t = f.read().strip()
            s = json.loads(t)
            self.menu[skill_name] = s['description']
