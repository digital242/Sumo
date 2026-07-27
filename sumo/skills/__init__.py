"""The skill catalog.

A *skill* is a small, named capability an agent can invoke by name — a
calculator, a clock, a note-taker. Skills are the units Sumo agents
discover and call. They are plain Python callables wrapped with metadata so
they can be listed, described, and dispatched uniformly.
"""

from sumo.skills.base import Skill, SkillResult
from sumo.skills.catalog import Catalog, default_catalog

__all__ = ["Skill", "SkillResult", "Catalog", "default_catalog"]
