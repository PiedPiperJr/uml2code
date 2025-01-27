from dataclasses import dataclass

@dataclass
class Attribute:
    visibility: str
    name: str
    _type: str