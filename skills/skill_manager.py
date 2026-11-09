import abc

class SkillManger(abc.ABC):
    @abc.abstractmethod
    def skill_menu(self):
        pass

    @abc.abstractmethod
    def load_skill(self, skill_name: str):
        pass

    @abc.abstractmethod
    def unload_skill(self, skill_name: str):
        pass