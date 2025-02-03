from dataclasses import dataclass, field
from typing import List, Dict, Optional
from helpers.utils import Utils
from models.attribute_model import Attribute
from models.method_model import Method



@dataclass
class Class(object):
    name: str
    attributes: List[Attribute] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)
    aggregations: List[Attribute] = field(default_factory=list)
    compositions: List[Attribute] = field(default_factory=list)
    parent: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Class':
        instance = cls(name=data['name'])
        instance.attributes = [Attribute(**attr)
                            for attr in data['attributes']]
        instance.methods = [Method(**method) for method in data['methods']]
        return instance

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'attributes': [attr.to_dict() for attr in self.attributes],
            'methods': [method.to_dict() for method in self.methods],
            'aggregations': [agg.to_dict() for agg in self.aggregations],
            'compositions': [comp.to_dict() for comp in self.compositions],
            'parent': self.parent
        }
