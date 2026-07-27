"""Local model engine backed by Ollama.

Ollama exposes an HTTP API on ``localhost:11434`` by default. We talk to it
with the standard library only (``urllib``) so Sumo's core stays
dependency-free. If the server is down, :meth:`available` returns ``False``
and callers fall back to the echo engine.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import List

from sumo.engine.base import Message, to_payload

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2"


class OllamaEngine:
    name = "ollama"

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        host: str = DEFAULT_HOST,
        timeout: float = 120.0,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def available(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.host}/api/tags")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                return resp.status == 200
        except (urllib.error.URLError, OSError, ValueError):
            return False

    def chat(self, messages: List[Message], **options) -> str:
        body = {
            "model": options.get("model", self.model),
            "messages": to_payload(messages),
            "stream": False,
        }
        if "temperature" in options:
            body["options"] = {"temperature": options["temperature"]}

        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return payload.get("message", {}).get("content", "").strip()
