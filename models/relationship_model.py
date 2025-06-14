from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple



@dataclass
class RelationshipType(Enum):
    NONE = 0
    INTERFACE = 1
    INHERITANCE = 2
    AGGREGATION = 3
    COMPOSITION = 4
    ATTRIBUTE = 5
    DEPENDENCY = 6
    ASSOCIATION = 7


@dataclass
class Relationship:
    name: str
    source: str
    target: str
    _type: RelationshipType
    source_name: str
    target_name: str
    source_role: Optional[str]
    target_role: Optional[str]
    source_multiplicity: Optional[Tuple[int, int]]
    target_multiplicity: Optional[Tuple[int, int]]
    is_navigable_to_source: bool = False 
    is_navigable_to_target: bool = False
    args: List[Dict] = field(default_factory=list)
