"""Agent abstraction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from sumo.engine.base import Engine, Message
from sumo.skills.catalog import Catalog


@dataclass
class AgentResult:
    answer: str
    trace: List[str] = field(default_factory=list)


class Agent:
    """Base class for Sumo agents.

    Subclasses implement :meth:`run`. The base holds the engine and an
    optional skill catalog so subclasses share a consistent constructor.
    """

    name = "agent"
    description = "abstract base agent"

    def __init__(self, engine: Engine, catalog: Optional[Catalog] = None) -> None:
        self.engine = engine
        self.catalog = catalog

    def run(self, goal: str) -> AgentResult:  # pragma: no cover - abstract
        raise NotImplementedError

    def _ask(self, system: str, user: str, **options) -> str:
        messages = [Message("system", system), Message("user", user)]
        return self.engine.chat(messages, **options)
