from dataclasses import dataclass, field
from typing import List, Dict, Optional
from helpers.utils import Utils
from models.attribute_model import Attribute
from models.method_model import Method


@dataclass
class Class(object):
    name: str
    attributes: List[Attribute]
    methods: List[Method]
    aggregations: List[Attribute]
    compositions: List[Attribute]
    parent: Optional[str]

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
