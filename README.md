# Sumo

**A local-first personal AI that runs on your own devices.**

Sumo is a small framework for building personal AI agents that run *on your
machine* by default — talking to a local model server (Ollama) and only
reaching for the cloud when you explicitly ask. It's inspired by
[OpenJarvis](https://github.com/open-jarvis/OpenJarvis): the premise that
local models are now good enough to handle the large majority of everyday
chat and reasoning, so your personal AI doesn't need to send everything to
someone else's server.

The core has **zero third-party dependencies** — a fresh clone runs on the
Python standard library alone. When no local model is reachable, Sumo falls
back to an offline "echo" engine so every command still works.

---

## Install

**One command** (clones, installs the `sumo` command, and checks your setup):

```bash
curl -fsSL https://raw.githubusercontent.com/digital242/sumo/main/install.sh | bash
```

**From a checkout** — pick whichever you like:

```bash
git clone https://github.com/digital242/sumo.git
cd sumo

./install.sh          # guided setup
# or
make install          # just install the `sumo` command
# or
pip install -e .       # the plain pip way
```

Or run it straight from the source tree without installing anything:

```bash
python3 -m sumo.cli doctor
```

Common tasks are wrapped in the `Makefile` — run `make help` to see them
(`make test`, `make chat`, `make doctor`, `make run AGENT=react GOAL="..."`).

## Enable real reasoning (Ollama)

Sumo is local-first. Point it at a running [Ollama](https://ollama.com):

```bash
# install Ollama, then pull and run a small local model
ollama run llama3.2
```

Sumo auto-detects Ollama on `http://localhost:11434`. Check with:

```bash
sumo doctor
```

If you see `engine: ollama (available=True)`, you're reasoning locally.

## Quick start

```bash
sumo chat "summarize what a REST API is in two sentences"
sumo chat                       # interactive REPL
sumo run react "what time is it, then add 2 and 3" --trace
sumo morning --task "review PR" --task "call the plumber"
sumo skills                     # list the skill catalog
sumo agents                     # list available agents
```

## Concepts

Sumo is built from three small, composable layers.

### Engines — `sumo/engine`
An engine turns a conversation into a reply. Ships with:

| Engine   | What it is                                            |
|----------|-------------------------------------------------------|
| `ollama` | Local model server, talked to over `urllib` (no deps) |
| `echo`   | Offline fallback; deterministic, never hits the network |

`build_engine()` picks the best available one automatically.

### Skills — `sumo/skills`
A **skill** is a named capability an agent can invoke by name. Built-ins:
`calculator`, `clock`, `echo`. Skills are plain callables wrapped with
metadata, registered in a `Catalog` that agents query and dispatch against.

Add your own:

```python
from sumo.skills import Skill, SkillResult, default_catalog

def weather(arg: str) -> SkillResult:
    return SkillResult(ok=True, output="it's sunny")

catalog = default_catalog()
catalog.register(Skill("weather", "Look up the weather.", weather))
```

### Agents — `sumo/agents`
An **agent** is a strategy for turning a goal into an answer using an engine
and (optionally) the skill catalog.

| Agent     | Strategy                                              |
|-----------|-------------------------------------------------------|
| `chat`    | Conversational assistant with history                 |
| `react`   | Thought → Action → Observation loop over skills       |
| `morning` | Scheduled daily briefing from date + tasks            |

## Configuration

Config lives at `~/.sumo/config.json` (override the dir with `SUMO_HOME`).
Everything has a default, so Sumo runs with no config at all.

```bash
sumo config                          # show current config
sumo config --set model=qwen2.5      # pick a different local model
sumo config --set engine=echo        # force the offline engine
```

Environment overrides: `SUMO_ENGINE`, `SUMO_MODEL`, `SUMO_HOST`.

## Project layout

```
sumo/
  cli.py            # the `sumo` command
  config.py         # ~/.sumo/config.json
  engine/           # ollama + echo engines, auto-selection
  skills/           # skill contract, catalog, built-ins
  agents/           # chat, react, morning + registry
tests/              # offline test suite (runs against the echo engine)
```

## Development

```bash
pip install -e ".[dev]"
pytest -q
```

## License

Apache-2.0. See [LICENSE](LICENSE).
