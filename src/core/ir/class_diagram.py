from dataclasses import dataclass, field
from enum import Enum


class RelationshipKind(Enum):
    INHERITANCE  = "INHERITANCE"
    REALIZATION  = "REALIZATION"
    COMPOSITION  = "COMPOSITION"
    AGGREGATION  = "AGGREGATION"
    ASSOCIATION  = "ASSOCIATION"
    NONE         = "NONE"


@dataclass
class ClassParam:
    name: str
    type: str


@dataclass
class ClassMethod:
    name: str
    return_type: str
    visibility: str
    params: list[ClassParam] = field(default_factory=list)


@dataclass
class ClassField:
    name: str
    type: str
    visibility: str = "private"


@dataclass
class UMLClass:
    id: str
    name: str
    stereotype:   str  = ""
    is_abstract:  bool = False
    is_interface: bool = False
    fields:  list[ClassField]  = field(default_factory=list)
    methods: list[ClassMethod] = field(default_factory=list)


@dataclass
class ClassRelationship:
    source_id: str
    target_id: str
    kind:  RelationshipKind
    label: str = ""


@dataclass
class ClassDiagram:
    classes:       dict[str, UMLClass]       = field(default_factory=dict)
    relationships: list[ClassRelationship]   = field(default_factory=list)
