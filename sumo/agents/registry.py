"""Map agent names to classes so the CLI can spin them up by name."""

from __future__ import annotations

from typing import Dict, Optional, Type

from sumo.agents.base import Agent
from sumo.agents.chat import ChatAgent
from sumo.agents.morning import MorningAgent
from sumo.agents.react import ReActAgent
from sumo.engine.base import Engine
from sumo.skills.catalog import Catalog

AGENTS: Dict[str, Type[Agent]] = {
    ChatAgent.name: ChatAgent,
    ReActAgent.name: ReActAgent,
    MorningAgent.name: MorningAgent,
}


def build_agent(
    name: str, engine: Engine, catalog: Optional[Catalog] = None
) -> Agent:
    try:
        cls = AGENTS[name]
    except KeyError:
        raise ValueError(
            f"unknown agent {name!r}; available: {', '.join(sorted(AGENTS))}"
        )
    return cls(engine, catalog)
