"""A dependency-free fallback engine.

The echo engine never touches the network. It is what Sumo falls back to
when no local model server is reachable, so the CLI and the test-suite work
on a bare clone. It produces deterministic, obviously-synthetic replies.
"""

from __future__ import annotations

from typing import List

from sumo.engine.base import Message


class EchoEngine:
    name = "echo"

    def available(self) -> bool:
        return True

    def chat(self, messages: List[Message], **options) -> str:
        last_user = next(
            (m.content for m in reversed(messages) if m.role == "user"),
            "",
        )
        if not last_user:
            return "[sumo:echo] Nothing to respond to yet."
        return (
            "[sumo:echo] No local model is running, so I can't reason about "
            f"this yet. You said: {last_user!r}. Start Ollama (see the README) "
            "and I'll answer for real."
        )
