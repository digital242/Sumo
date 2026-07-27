"""Built-in agents.

Each agent is a small strategy for turning a user goal into an answer using
an :class:`~sumo.engine.base.Engine` and, optionally, the skill catalog.
"""

from sumo.agents.base import Agent, AgentResult
from sumo.agents.chat import ChatAgent
from sumo.agents.react import ReActAgent
from sumo.agents.morning import MorningAgent
from sumo.agents.registry import AGENTS, build_agent

__all__ = [
    "Agent",
    "AgentResult",
    "ChatAgent",
    "ReActAgent",
    "MorningAgent",
    "AGENTS",
    "build_agent",
]
