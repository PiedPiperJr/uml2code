from dataclasses import dataclass
from typing import List
from models.attribute_model import Attribute


@dataclass
class Resource:
    name: str
    attributes: List[Attribute]
