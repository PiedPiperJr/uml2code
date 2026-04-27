from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IRField:
    name: str
    type: str
    visibility: str = "private"


@dataclass
class IREntity:
    name: str
    fields: list[IRField] = field(default_factory=list)
    parent: Optional[IREntity] = None
    compositions: list[IREntity] = field(default_factory=list)
    aggregations: list[IREntity] = field(default_factory=list)

    @property
    def is_root(self) -> bool:
        return self.parent is None


@dataclass
class ProjectIR:
    package: str
    entities: list[IREntity] = field(default_factory=list)
