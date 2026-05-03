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
        instance = cls(name=data['name'],
                       attributes=[],
                       methods=[],
                       aggregations=[],
                       compositions=[],
                       parent=data.get('parent'),
                       implements=data.get('implements', []))
        instance.attributes = [Attribute(**attr) for attr in data.get('attributes', [])]
        instance.methods = [Method(**method) for method in data.get('methods', [])]
        instance.aggregations = [Attribute(**attr) for attr in data.get('aggregations', [])]
        instance.compositions = [Attribute(**attr) for attr in data.get('compositions', [])]
        instance.parent = data.get('parent')
        instance.implements = data.get('implements', [])
        instance.oneToManyRelationships = [
            InterpretedRelationShip(rel["role"], rel["comodel"], rel["mapped_by_property"]) for rel in data.get('oneToManyRelationships', [])
        ]
        instance.manyToOneRelationships = [
            InterpretedRelationShip(rel["role"], rel["comodel"], rel["mapped_by_property"]) for rel in data.get('manyToOneRelationships', [])
        ]
        instance.manyToManyRelationships = [
            InterpretedRelationShip(rel["role"], rel["comodel"], rel["mapped_by_property"]) for rel in data.get('manyToManyRelationships', [])
        ]
        instance.oneToOneRelationships = [
            InterpretedRelationShip(rel["role"], rel["comodel"], rel["mapped_by_property"]) for rel in data.get('oneToOneRelationships', [])
        ]
        return instance

    @classmethod
    def capitalize(cls):
        cls(name=Utils.capitalize(cls.name))
