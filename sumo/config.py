"""Sumo configuration.

Config is a small JSON file at ``~/.sumo/config.json``. Everything has a
sane default, so Sumo runs with no config at all. Environment variables
(``SUMO_ENGINE``, ``SUMO_MODEL``, ``SUMO_HOST``) override the file.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

CONFIG_DIR = Path(os.environ.get("SUMO_HOME", Path.home() / ".sumo"))
CONFIG_PATH = CONFIG_DIR / "config.json"

DEFAULTS: Dict[str, Any] = {
    "engine": "auto",          # auto | ollama | echo
    "model": "llama3.2",
    "host": "http://localhost:11434",
}


def load() -> Dict[str, Any]:
    config = dict(DEFAULTS)
    if CONFIG_PATH.exists():
        try:
            config.update(json.loads(CONFIG_PATH.read_text()))
        except (json.JSONDecodeError, OSError):
            pass  # a broken config file should never break the CLI

    # Environment overrides win.
    for key, env in (("engine", "SUMO_ENGINE"), ("model", "SUMO_MODEL"), ("host", "SUMO_HOST")):
        if os.environ.get(env):
            config[key] = os.environ[env]
    return config


def save(config: Dict[str, Any]) -> Path:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")
    return CONFIG_PATH
