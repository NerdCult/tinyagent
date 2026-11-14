#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

import os
from pathlib import Path
from ..core.interfaces import SkillManager

SKILL_SUFFIXES = ('.md', '.json')


class SimpleSkillManager(SkillManager):
    '''
    Implements all the Skill Manger options. 
    skills() returns a menu of available skill names and descriptions and how to use tools to load and unload skills as well as create new skills.

    '''
    def __init__(self, skill_folder: str = f'{os.getcwd()}/skills'):
        self.skills_folder = Path(skill_folder)
        self.skills_all = ''
        Path(skill_folder).mkdir(parents=True, exist_ok=True)
        self.reload_skills()

    def reload_skills(self):
        self.skills_all = ''
        
        for path in sorted(self.skills_folder.iterdir(), key=lambda p: (p.stem, p.suffix == '.md')):
            with open(path, 'r') as f:
                self.skills_all = f'{self.skills_all} \n\n{path.stem}:\n{f.read()}'

    def skills(self) -> str:
        return self.skills_all
