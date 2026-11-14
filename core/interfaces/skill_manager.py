#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from typing import Protocol, runtime_checkable

@runtime_checkable
class SkillManager(Protocol):
    ''' Provide the skills to the context '''
    def skills(self) -> str: ...
    ''' returns a str containing the skills'''
    def reload_skills(self): ...
    ''' reloads the skills allowing skills to be added without restarting the session '''

@runtime_checkable
class SkillManagerDynamic(SkillManager, Protocol):
    ''' Extends SkillManager to allow specific skills to be loaded, unloaded. SkillManager.skills() should return a menu of names and descriptions for available skills and how to load and unload them. requires having load_skill and unload_skill tools in the Toolbox used in the session. These tools should be explained in their tool descriptions and in the skill menu. '''

    def load_skill(self, skill_name: str): ...
    ''' allows the session to load a skill from the skill menu on demand when paired with the appropriate tool in the toolbox.'''

    def unload_skill(self, skill_name: str): ...
    ''' allows the session to unload a skill previously loaded from the skill menu on demand when paired with the appropriate tool in the toolbox.'''

@runtime_checkable
class SkillManagerSkillMaker(SkillManagerDynamic, Protocol):
    ''' Extends SkillManagerDynamic, adding a create_skill() method. Requires a partner tool in the Toolbox used in the session.'''

    def create_skill(self, skill_name: str, description: str, text: str): ...
    ''' allows the session to create a new skill when paired with the appropriate tool in the toolbox. the new skill should be made available in the menu'''