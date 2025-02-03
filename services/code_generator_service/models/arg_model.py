from typing import Dict
from dataclasses import dataclass


@dataclass
class Arg:
    name: str
    _type: str

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            '_type': self._type
        }