
from dataclasses import dataclass
from typing import List

from models.method_model import Method


@dataclass
class Repository:
    entity: str
    methods: List[Method]
