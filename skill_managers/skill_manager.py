import abc

class SkillManager(abc.ABC):
    @abc.abstractmethod
    def skills(self):
        pass

    @abc.abstractmethod
    def reload_skills(self):
        pass

    @abc.abstractmethod
    def load_skill(self, skill_name: str):
        pass

    @abc.abstractmethod
    def unload_skill(self, skill_name: str):
        pass

    @abc.abstractmethod
    def create_skill(self, skill_name: str, description: str, text: str):
        pass