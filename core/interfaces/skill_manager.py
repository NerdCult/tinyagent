from typing import Protocol, runtime_checkable

@runtime_checkable
class SkillManager(Protocol):
    ''' Provide the skills to the context '''
    def skills(self): ...
    def reload_skills(self): ...

@runtime_checkable
class SkillManagerDynamic(SkillManager, Protocol):
    ''' Extends SkillManager to allow specific skills to be loaded, unloaded. skills() should return a menu of names and descriptions for available skills and how to load and unload them. requires having load_skill and unload_skill tools in the Toolbox used in the session. These tools should be explained in their description and in the skill menu. '''

    def load_skill(self, skill_name: str): ...

    def unload_skill(self, skill_name: str): ...

@runtime_checkable
class SkillManagerSkillMaker(SkillManagerDynamic, Protocol):
    ''' Extends SkillManager, adding a create_skill() method. Requires a matching skill in the Toolbox used in the session.'''

    def create_skill(self, skill_name: str, description: str, text: str): ...