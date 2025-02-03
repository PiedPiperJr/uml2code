from typing import Dict, List
from dataclasses import dataclass

from models.arg_model import Arg

@dataclass
class Method:
    visibility: str
    name: str
    _type: str
    args: List[Arg]

    def to_dict(self) -> Dict:
        return {
            'visibility': self.visibility,
            'name': self.name,
            '_type': self._type,
            'args': [arg.to_dict() for arg in self.args]
        }