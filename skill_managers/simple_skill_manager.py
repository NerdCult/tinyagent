import json
from pathlib import Path
from .skill_manager import SkillManager

DEFAULT_SKILLS_PATH = Path(__file__).parent / 'skills'
SKILL_SUFFIXES = ('.md', '.json')


def skill_name_of(skill_name: str) -> str:
    """Normalize a skill name: drop any directory part and a known suffix."""
    name = Path(skill_name).name
    for suffix in SKILL_SUFFIXES:
        if name.endswith(suffix):
            return name[:-len(suffix)]
    return name


def parse_skill(path: Path) -> tuple[str, str]:
    """Return (description, text) for a .md (front matter) or .json skill."""
    raw = path.read_text(encoding='utf-8').strip()
    if path.suffix == '.json':
        data = json.loads(raw)
        return data['description'], data['text']

    description, body = '', raw
    parts = raw.split('---', 2)
    if raw.startswith('---') and len(parts) == 3:
        _, header, body = parts
        for line in header.strip().splitlines():
            key, _, value = line.partition(':')
            if key.strip() == 'description':
                description = value.strip()
    return description, body.strip()


class SimpleSkillManager(SkillManager):
    def __init__(self, skill_folder: str | Path = DEFAULT_SKILLS_PATH):
        self.skills_folder = Path(skill_folder)
        self.menu_preamble: str = 'Provided below are the available skills in this environment. To have it loaded into the context use the load_skill tools providing the name of the skill to load. Use unload_skill if a skill is no longer needed.'
        self.available: dict[str, Path] = {}  # name -> file
        self.menu: str = ''
        self.loaded_skills: dict[str, str] = {}
        self.reload_skills()

    def reload_skills(self):
        self.available = {}
        lines = []
        # sorted + .md after .json means a .md wins if both exist for the same name
        for path in sorted(self.skills_folder.iterdir(), key=lambda p: (p.stem, p.suffix == '.md')):
            if path.suffix in SKILL_SUFFIXES:
                self.available[path.stem] = path
        for name, path in self.available.items():
            lines.append(f'{name} = {parse_skill(path)[0]}')
        self.menu = '\n'.join(lines)

    def skills(self):
        loaded = ''.join(f'\n {name}: {text}' for name, text in self.loaded_skills.items())
        return f'{self.menu_preamble}\n available skills:\n{self.menu}\n loaded skills:{loaded}'

    def _resolve(self, skill_name: str) -> str:
        name = skill_name_of(skill_name)
        if name not in self.available:
            raise KeyError(f'unknown skill: {skill_name}')
        return name

    def load_skill(self, skill_name: str):
        name = self._resolve(skill_name)
        self.loaded_skills[name] = parse_skill(self.available[name])[1]

    def unload_skill(self, skill_name: str):
        self.loaded_skills.pop(self._resolve(skill_name))

    def create_skill(self, skill_name: str, description: str, text: str):
        name = skill_name_of(skill_name)
        if not name:
            raise ValueError('skill_name must not be empty')
        # the description lives on one front matter line
        description = ' '.join(description.split())
        (self.skills_folder / f'{name}.md').write_text(
            f'---\ndescription: {description}\n---\n{text}\n', encoding='utf-8')
        self.reload_skills()
