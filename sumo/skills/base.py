"""Skill primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class SkillResult:
    ok: bool
    output: str

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.output


@dataclass
class Skill:
    """A named capability an agent can invoke.

    ``run`` takes a single string argument (the agent's request to the
    skill) and returns a :class:`SkillResult`.
    """

    name: str
    description: str
    run: Callable[[str], SkillResult]

    def invoke(self, argument: str) -> SkillResult:
        try:
            return self.run(argument)
        except Exception as exc:  # skills must never crash the agent loop
            return SkillResult(ok=False, output=f"skill {self.name!r} failed: {exc}")
