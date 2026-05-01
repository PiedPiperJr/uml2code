from dataclasses import dataclass, field
from enum import Enum


class RelationshipKind(Enum):
    INHERITANCE = "INHERITANCE"
    COMPOSITION = "COMPOSITION"
    AGGREGATION = "AGGREGATION"
    ASSOCIATION = "ASSOCIATION"
    NONE = "NONE"


@dataclass
class ERParam:
    name: str
    type: str


@dataclass
class ERMethod:
    name: str
    return_type: str
    visibility: str
    params: list[ERParam] = field(default_factory=list)


@dataclass
class ERField:
    name: str
    type: str
    visibility: str = "public"


@dataclass
class EREntity:
    id: str
    name: str
    fields: list[ERField] = field(default_factory=list)
    methods: list[ERMethod] = field(default_factory=list)


@dataclass
class ERRelationship:
    source_id: str
    target_id: str
    kind: RelationshipKind
    label: str = ""


@dataclass
class ERDiagram:
    entities: dict[str, EREntity] = field(default_factory=dict)
    relationships: list[ERRelationship] = field(default_factory=list)
