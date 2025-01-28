from typing import List, Literal
from dataclasses import dataclass
from helpers.utils import Utils
from models.class_model import Class
from models.usecase_model import UseCase


@dataclass
class Project:
    route: str
    classes: List[Class]
    useCases: List[UseCase]
