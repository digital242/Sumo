"""Engine abstraction shared by every model backend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Protocol, runtime_checkable


@dataclass
class Message:
    """A single chat message.

    ``role`` is one of ``"system"``, ``"user"``, or ``"assistant"``.
    """

    role: str
    content: str

    def as_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


@runtime_checkable
class Engine(Protocol):
    """Anything that can turn a conversation into a reply.

    Backends implement :meth:`chat`. Sumo ships a local Ollama engine and a
    dependency-free echo engine used for tests and offline demos.
    """

    name: str

    def chat(self, messages: List[Message], **options) -> str:
        """Return the assistant's reply to ``messages``."""
        ...

    def available(self) -> bool:
        """Return ``True`` if this engine can currently serve requests."""
        ...


def to_payload(messages: Iterable[Message]) -> List[dict]:
    """Serialize messages into the list-of-dicts shape most APIs expect."""
    return [m.as_dict() for m in messages]
