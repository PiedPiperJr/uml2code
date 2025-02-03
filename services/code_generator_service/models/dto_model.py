from dataclasses import dataclass
from typing import List

from models.dto_attribute_model import DtoAttribute


@dataclass
class Dto:
    name: str
    attributes: List[DtoAttribute]
