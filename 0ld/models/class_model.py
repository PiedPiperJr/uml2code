from dataclasses import dataclass, field
from typing import List, Dict
from utils.utils import capitalize

@dataclass
class Attribute:
    visibility: str
    name: str
    type: str

@dataclass
class Method:
    visibility: str
    name: str
    type: str
    args: List[str]

@dataclass
class Class:
    name: str
    type: str = "classe"
    attributes: List[Attribute] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Class':
        instance = cls(name=data['name'])
        instance.attributes = [Attribute(**attr) for attr in data['attributes']]
        instance.methods = [Method(**method) for method in data['methods']]
        return instance

    @classmethod
    def capitalize(cls):
        capitalize(cls(name=capitalize(cls.name)))