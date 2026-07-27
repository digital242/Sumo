"""Built-in skills shipped with Sumo.

These are intentionally small and offline. They demonstrate the skill
contract and give the ReAct agent something real to call without needing
any network access.
"""

from __future__ import annotations

import ast
import datetime as _dt
import operator as _op

from sumo.skills.base import Skill, SkillResult

# --- calculator -----------------------------------------------------------

_ALLOWED_BINOPS = {
    ast.Add: _op.add,
    ast.Sub: _op.sub,
    ast.Mult: _op.mul,
    ast.Div: _op.truediv,
    ast.FloorDiv: _op.floordiv,
    ast.Mod: _op.mod,
    ast.Pow: _op.pow,
}
_ALLOWED_UNARY = {ast.UAdd: _op.pos, ast.USub: _op.neg}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        return _ALLOWED_BINOPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
        return _ALLOWED_UNARY[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


def _calculator(argument: str) -> SkillResult:
    tree = ast.parse(argument.strip(), mode="eval")
    value = _eval(tree.body)
    return SkillResult(ok=True, output=str(value))


def _clock(argument: str) -> SkillResult:
    now = _dt.datetime.now().astimezone()
    return SkillResult(ok=True, output=now.strftime("%Y-%m-%d %H:%M:%S %Z"))


def _echo(argument: str) -> SkillResult:
    return SkillResult(ok=True, output=argument)


BUILTIN_SKILLS = [
    Skill(
        name="calculator",
        description="Evaluate an arithmetic expression, e.g. '2 * (3 + 4)'.",
        run=_calculator,
    ),
    Skill(
        name="clock",
        description="Return the current local date and time.",
        run=_clock,
    ),
    Skill(
        name="echo",
        description="Repeat the argument back. Useful for testing.",
        run=_echo,
    ),
]
