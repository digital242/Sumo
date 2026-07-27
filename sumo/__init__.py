"""Sumo: a local-first personal AI framework.

Sumo runs personal AI agents primarily on your own devices. It talks to a
local model server (Ollama by default) and only reaches for the cloud when
you explicitly ask it to. The core has no third-party dependencies, so a
fresh clone runs on the Python standard library alone.
"""

__version__ = "0.1.0"

from sumo.engine.base import Engine, Message
from sumo.agents.base import Agent, AgentResult

__all__ = ["Engine", "Message", "Agent", "AgentResult", "__version__"]
