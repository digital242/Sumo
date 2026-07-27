"""The ``sumo`` command-line interface.

Usage examples::

    sumo doctor                 # show which engine is available
    sumo chat "what's 12 * 8?"  # one-shot chat
    sumo chat                   # interactive REPL
    sumo run react "what time is it, then add 2 and 3"
    sumo morning                # today's briefing
    sumo skills                 # list the skill catalog
    sumo agents                 # list available agents
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from sumo import __version__, config
from sumo.agents.registry import AGENTS, build_agent
from sumo.engine.factory import build_engine
from sumo.skills.catalog import default_catalog


def _engine_and_catalog():
    cfg = config.load()
    return build_engine(cfg), default_catalog(), cfg


def cmd_doctor(_args) -> int:
    engine, catalog, cfg = _engine_and_catalog()
    print(f"sumo {__version__}")
    print(f"engine:   {engine.name} (available={engine.available()})")
    print(f"model:    {cfg['model']}")
    print(f"host:     {cfg['host']}")
    print(f"agents:   {', '.join(sorted(AGENTS))}")
    print(f"skills:   {', '.join(catalog.names())}")
    if engine.name == "echo":
        print(
            "\nNo local model reachable. Install Ollama and run "
            "`ollama run llama3.2` to enable real reasoning.",
            file=sys.stderr,
        )
    return 0


def cmd_agents(_args) -> int:
    for name, cls in sorted(AGENTS.items()):
        print(f"{name:10s} {cls.description}")
    return 0


def cmd_skills(_args) -> int:
    print(default_catalog().describe())
    return 0


def cmd_chat(args) -> int:
    engine, catalog, _ = _engine_and_catalog()
    agent = build_agent("chat", engine, catalog)

    if args.prompt:
        print(agent.run(" ".join(args.prompt)).answer)
        return 0

    print("sumo chat — Ctrl-D or 'exit' to quit.")
    while True:
        try:
            line = input("you> ").strip()
        except EOFError:
            print()
            break
        if line in ("exit", "quit"):
            break
        if not line:
            continue
        print("sumo>", agent.run(line).answer)
    return 0


def cmd_run(args) -> int:
    engine, catalog, _ = _engine_and_catalog()
    try:
        agent = build_agent(args.agent, engine, catalog)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    result = agent.run(" ".join(args.goal))
    print(result.answer)
    if args.trace and result.trace:
        print("\n--- trace ---", file=sys.stderr)
        for step in result.trace:
            print(step, file=sys.stderr)
    return 0


def cmd_morning(args) -> int:
    engine, catalog, _ = _engine_and_catalog()
    agent = build_agent("morning", engine, catalog)
    result = agent.compose(tasks=args.task, note=args.note)
    print(result.answer)
    return 0


def cmd_config(args) -> int:
    cfg = config.load()
    if args.set:
        for pair in args.set:
            if "=" not in pair:
                print(f"ignoring {pair!r}: expected key=value", file=sys.stderr)
                continue
            key, value = pair.split("=", 1)
            cfg[key] = value
        path = config.save(cfg)
        print(f"saved {path}")
    else:
        for key, value in cfg.items():
            print(f"{key} = {value}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sumo", description="Local-first personal AI.")
    parser.add_argument("--version", action="version", version=f"sumo {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("doctor", help="show engine/model status").set_defaults(func=cmd_doctor)
    sub.add_parser("agents", help="list available agents").set_defaults(func=cmd_agents)
    sub.add_parser("skills", help="list the skill catalog").set_defaults(func=cmd_skills)

    p_chat = sub.add_parser("chat", help="chat with Sumo")
    p_chat.add_argument("prompt", nargs="*", help="one-shot prompt; omit for a REPL")
    p_chat.set_defaults(func=cmd_chat)

    p_run = sub.add_parser("run", help="run a named agent on a goal")
    p_run.add_argument("agent", help="agent name (see `sumo agents`)")
    p_run.add_argument("goal", nargs="+", help="the goal / task")
    p_run.add_argument("--trace", action="store_true", help="print the reasoning trace")
    p_run.set_defaults(func=cmd_run)

    p_morning = sub.add_parser("morning", help="today's briefing")
    p_morning.add_argument("--task", action="append", help="a task for today (repeatable)")
    p_morning.add_argument("--note", help="a freeform note about the day")
    p_morning.set_defaults(func=cmd_morning)

    p_config = sub.add_parser("config", help="show or set configuration")
    p_config.add_argument("--set", action="append", metavar="KEY=VALUE", help="set a value")
    p_config.set_defaults(func=cmd_config)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
