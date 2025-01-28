from dataclasses import dataclass
from typing import List

from models.method_model import Method


@dataclass
class Service:
    name: str
    methods: List[Method]

