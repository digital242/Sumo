"""Model engines: the layer that turns messages into completions."""

from sumo.engine.base import Engine, Message
from sumo.engine.ollama import OllamaEngine
from sumo.engine.echo import EchoEngine
from sumo.engine.factory import build_engine

__all__ = ["Engine", "Message", "OllamaEngine", "EchoEngine", "build_engine"]
