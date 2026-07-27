"""Pick the best available engine for the current machine."""

from __future__ import annotations

from sumo.engine.base import Engine
from sumo.engine.echo import EchoEngine
from sumo.engine.ollama import DEFAULT_HOST, DEFAULT_MODEL, OllamaEngine


def build_engine(config=None) -> Engine:
    """Return a ready-to-use engine.

    Sumo is local-first: it prefers a running local model server and only
    falls back to the offline echo engine when nothing else is reachable.
    """
    config = config or {}
    engine_name = config.get("engine", "auto")

    if engine_name in ("ollama", "auto"):
        ollama = OllamaEngine(
            model=config.get("model", DEFAULT_MODEL),
            host=config.get("host", DEFAULT_HOST),
        )
        if ollama.available():
            return ollama
        if engine_name == "ollama":
            # Explicitly requested but unreachable: still return it so the
            # error surfaces where the user asked for it.
            return ollama

    return EchoEngine()
