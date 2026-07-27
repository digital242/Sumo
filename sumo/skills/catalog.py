"""A registry agents query to discover and invoke skills."""

from __future__ import annotations

from typing import Dict, List, Optional

from sumo.skills.base import Skill, SkillResult
from sumo.skills.builtins import BUILTIN_SKILLS


class Catalog:
    def __init__(self, skills: Optional[List[Skill]] = None) -> None:
        self._skills: Dict[str, Skill] = {}
        for skill in skills or []:
            self.register(skill)

    def register(self, skill: Skill) -> None:
        self._skills[skill.name] = skill

    def names(self) -> List[str]:
        return sorted(self._skills)

    def get(self, name: str) -> Optional[Skill]:
        return self._skills.get(name)

    def describe(self) -> str:
        """A human/LLM-readable listing of available skills."""
        if not self._skills:
            return "(no skills registered)"
        lines = [f"- {s.name}: {s.description}" for s in self._skills.values()]
        return "\n".join(lines)

    def invoke(self, name: str, argument: str) -> SkillResult:
        skill = self.get(name)
        if skill is None:
            return SkillResult(
                ok=False, output=f"no such skill: {name!r} (have: {', '.join(self.names())})"
            )
        return skill.invoke(argument)


def default_catalog() -> Catalog:
    """A catalog preloaded with Sumo's built-in skills."""
    return Catalog(list(BUILTIN_SKILLS))
