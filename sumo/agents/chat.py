"""A single-turn / multi-turn chat agent."""

from __future__ import annotations

from typing import List

from sumo.agents.base import Agent, AgentResult
from sumo.engine.base import Message

SYSTEM_PROMPT = (
    "You are Sumo, a helpful personal AI assistant running locally on the "
    "user's own device. Be concise, direct, and practical."
)


class ChatAgent(Agent):
    name = "chat"
    description = "Plain conversational assistant."

    def __init__(self, engine, catalog=None) -> None:
        super().__init__(engine, catalog)
        self._history: List[Message] = [Message("system", SYSTEM_PROMPT)]

    def run(self, goal: str) -> AgentResult:
        self._history.append(Message("user", goal))
        reply = self.engine.chat(self._history)
        self._history.append(Message("assistant", reply))
        return AgentResult(answer=reply)

    def reset(self) -> None:
        self._history = [Message("system", SYSTEM_PROMPT)]
