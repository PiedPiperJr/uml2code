from dataclasses import dataclass, field
from typing import List, Dict, Optional
from helpers.utils import Utils
from models.attribute_model import Attribute
from models.interpreted_relationship_model import InterpretedRelationShip
from models.method_model import Method


@dataclass
class Class(object):
    name: str
    attributes: List[Attribute]
    methods: List[Method]
    aggregations: List[Attribute]
    compositions: List[Attribute]
    parent: Optional[str]
    implements: List[str] = field(default_factory=list)
    oneToManyRelationships: List[InterpretedRelationShip] = field(default_factory=list)
    manyToOneRelationships: List[InterpretedRelationShip] = field(default_factory=list)
    manyToManyRelationships: List[InterpretedRelationShip] = field(default_factory=list)
    oneToOneRelationships: List[InterpretedRelationShip] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Class':
        instance = cls(name=data['name'])
        instance.attributes = [Attribute(**attr)
                               for attr in data['attributes']]
        instance.methods = [Method(**method) for method in data['methods']]
        return instance

    @classmethod
    def capitalize(cls):
        cls(name=Utils.capitalize(cls.name))
