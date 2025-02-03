from typing import Dict
from dataclasses import dataclass

@dataclass
class Attribute:
    visibility: str
    name: str
    _type: str

    def to_dict(self) -> Dict:
        return {
            'visibility': self.visibility,
            'name': self.name,
            '_type': self._type
        }