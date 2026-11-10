import os, json
from pathlib import Path
from .skill_manager import SkillManager

DEFAULT_SKILLS_PATH = os.path.dirname(__file__) + '/skills'

class SimpleSkillManager(SkillManager):
    def __init__(self, skill_folder: str = DEFAULT_SKILLS_PATH):
        self.skills_folder: str = skill_folder
        self.menu_preamble: str = 'Provided below are the available skills in this environment. To have it loaded into the context use the load_skill tools providing the name of the skill to load. Use unload_skill if a skill is no longer needed.'
        self.menu: str = ''
        self.loaded_skills: dict = {}
        self.reload_skills()

    def reload_skills(self):
        self.menu = ''
        for file in Path(self.skills_folder).glob("*.json"):
            self.add_skill_to_menu(file.name)

    def skills(self):
        accumulater = f'{self.menu_preamble}\n available skills:\n{self.menu}'

        accumulater = f'{accumulater}\n loaded skills:'
        for name, text in self.loaded_skills.items():
            accumulater = f'{accumulater}\n {name}: {text}'
        return accumulater

    def load_skill(self, skill_name: str):
        if skill_name.endswith('.json'):
            sn = skill_name
        else:
            sn = skill_name + '.json'
        with open(file=f'{self.skills_folder}/{sn}') as f:
            t = f.read().strip()
            s = json.loads(t)
            self.loaded_skills[sn] = s['text']

    def unload_skill(self, skill_name: str):
        if skill_name.endswith('.json'):
            sn = skill_name
        else:
            sn = skill_name + '.json'
        self.loaded_skills.pop(sn)

    def add_skill_to_menu(self, skill_name: str):
        with open(file=f'{self.skills_folder}/{skill_name}') as f:
            t = f.read().strip()
            s = json.loads(t)
            self.menu = self.menu + f'\n{skill_name} = {s["description"]}'

    def create_skill(self, skill_name: str, description: str, text: str):
        if skill_name.endswith('.json'):
            sn = skill_name
        else:
            sn = skill_name + '.json'
        with open(f'{self.skills_folder}/{sn}',mode='w') as f:
            skill = {'description': description, 'text': text}
            f.write(json.dumps(skill))
        self.reload_skills()
