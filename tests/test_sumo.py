"""Tests that run fully offline against the echo engine."""

from sumo.agents.registry import build_agent
from sumo.engine.base import Message
from sumo.engine.echo import EchoEngine
from sumo.engine.factory import build_engine
from sumo.skills.catalog import default_catalog


def test_echo_engine_available():
    engine = EchoEngine()
    assert engine.available()
    reply = engine.chat([Message("user", "hi")])
    assert "hi" in reply


def test_factory_falls_back_to_echo_when_offline():
    # A host that will never resolve forces the fallback path.
    engine = build_engine({"engine": "auto", "host": "http://127.0.0.1:1"})
    assert engine.name == "echo"


def test_calculator_skill():
    catalog = default_catalog()
    result = catalog.invoke("calculator", "2 * (3 + 4)")
    assert result.ok
    assert result.output == "14"


def test_calculator_rejects_bad_input():
    catalog = default_catalog()
    result = catalog.invoke("calculator", "__import__('os')")
    assert not result.ok


def test_unknown_skill():
    catalog = default_catalog()
    result = catalog.invoke("nope", "x")
    assert not result.ok


def test_react_agent_final_answer():
    # The echo engine never emits a "Final:" line, so the agent returns the
    # raw reply on the first step — exercising the no-action path.
    engine = EchoEngine()
    agent = build_agent("react", engine, default_catalog())
    result = agent.run("what is 2+2?")
    assert result.answer
    assert result.trace


def test_chat_agent_roundtrip():
    engine = EchoEngine()
    agent = build_agent("chat", engine)
    result = agent.run("hello there")
    assert "hello there" in result.answer


def test_morning_agent_includes_date():
    engine = EchoEngine()
    agent = build_agent("morning", engine)
    result = agent.compose(tasks=["ship sumo"], note="feeling good")
    assert any("Date:" in step for step in result.trace)
    assert any("ship sumo" in step for step in result.trace)
