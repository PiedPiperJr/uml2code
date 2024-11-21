from enum import Enum
from dataclasses import dataclass

class RelationshipType(Enum):
    NONE = 0
    INTERFACE = 1
    INHERITANCE = 2
    AGGREGATION = 3
    COMPOSITION = 4
    ATTRIBUTE = 5

@dataclass
class Relationship:
    name: str
    source: str
    target: str
    _type: RelationshipType
    source_name: str
    target_name: str