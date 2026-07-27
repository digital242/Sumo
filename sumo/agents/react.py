"""A ReAct-style agent: Thought -> Action -> Observation loops.

The agent reasons in natural language and calls skills from the catalog by
emitting lines shaped like::

    Action: <skill_name> | <argument>

When it is ready to answer it emits::

    Final: <answer>

The loop parses those lines, runs the skill, feeds the observation back,
and repeats up to ``max_steps``. Parsing is deliberately forgiving so the
loop degrades gracefully with small local models.
"""

from __future__ import annotations

import re
from typing import Optional

from sumo.agents.base import Agent, AgentResult
from sumo.engine.base import Message
from sumo.skills.catalog import Catalog, default_catalog

_ACTION_RE = re.compile(r"^\s*Action:\s*([\w-]+)\s*\|\s*(.*)$", re.IGNORECASE)
_FINAL_RE = re.compile(r"^\s*Final:\s*(.*)$", re.IGNORECASE | re.DOTALL)


def _system_prompt(catalog: Catalog) -> str:
    return (
        "You are Sumo, a reasoning agent that can call skills.\n"
        "Available skills:\n"
        f"{catalog.describe()}\n\n"
        "On each turn, either call a skill or give a final answer.\n"
        "To call a skill, output exactly one line:\n"
        "  Action: <skill_name> | <argument>\n"
        "To finish, output exactly one line:\n"
        "  Final: <your answer>\n"
        "Think briefly before acting, but keep it short."
    )


class ReActAgent(Agent):
    name = "react"
    description = "Reasoning agent that invokes skills in a loop."

    def __init__(self, engine, catalog: Optional[Catalog] = None, max_steps: int = 6):
        super().__init__(engine, catalog or default_catalog())
        self.max_steps = max_steps

    def run(self, goal: str) -> AgentResult:
        assert self.catalog is not None
        messages = [
            Message("system", _system_prompt(self.catalog)),
            Message("user", goal),
        ]
        trace = []

        for _ in range(self.max_steps):
            reply = self.engine.chat(messages)
            messages.append(Message("assistant", reply))

            final = _FINAL_RE.search(reply)
            if final:
                trace.append(f"final: {final.group(1).strip()}")
                return AgentResult(answer=final.group(1).strip(), trace=trace)

            action = _ACTION_RE.search(reply)
            if not action:
                # No parseable step: treat the whole reply as the answer.
                trace.append("no-action; returning raw reply")
                return AgentResult(answer=reply.strip(), trace=trace)

            skill_name, argument = action.group(1), action.group(2).strip()
            result = self.catalog.invoke(skill_name, argument)
            observation = f"Observation: {result.output}"
            trace.append(f"{skill_name}({argument!r}) -> {result.output}")
            messages.append(Message("user", observation))

        return AgentResult(
            answer="[sumo] stopped: reached max reasoning steps.", trace=trace
        )
