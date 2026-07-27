"""A scheduled morning-digest agent.

Given a few facts about the day (date, weather, a task list), it asks the
local model to compose a short spoken-style briefing. With no model running
it still produces a usable plain-text digest from the raw inputs.
"""

from __future__ import annotations

import datetime as _dt
from typing import Optional, Sequence

from sumo.agents.base import Agent, AgentResult

SYSTEM_PROMPT = (
    "You are Sumo's morning digest. Compose a warm, 4-6 sentence spoken "
    "briefing for the user's day. Lead with the date, then the most "
    "important tasks, then a closing note. No markdown, no lists."
)


class MorningAgent(Agent):
    name = "morning"
    description = "Compose a short daily briefing."

    def run(self, goal: str) -> AgentResult:
        # ``goal`` is treated as an optional freeform note about the day.
        return self.compose(note=goal or None)

    def compose(
        self,
        tasks: Optional[Sequence[str]] = None,
        note: Optional[str] = None,
    ) -> AgentResult:
        today = _dt.date.today().strftime("%A, %B %d, %Y")
        tasks = list(tasks or [])
        facts = [f"Date: {today}"]
        if tasks:
            facts.append("Tasks: " + "; ".join(tasks))
        if note:
            facts.append("Note: " + note)
        user = "\n".join(facts)

        reply = self._ask(SYSTEM_PROMPT, user)
        return AgentResult(answer=reply, trace=facts)
