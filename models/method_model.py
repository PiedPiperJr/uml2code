from typing import List
from dataclasses import dataclass

from models.arg_model import Arg

@dataclass
class Method:
    visibility: str
    name: str
    _type: str
    args: List[Arg]