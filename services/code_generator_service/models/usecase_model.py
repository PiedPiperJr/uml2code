from dataclasses import dataclass
from typing import List, Literal

from helpers.utils import Utils
from models.dto_model import Dto
from models.repository_model import Repository
from models.resource_model import Resource
from models.scenario_model import Scenario
from models.service_model import Service


@dataclass
class UseCase:
    name: str
    action: Literal["POST", "GET", "PUT", "PATCH", "DELETE"]
    actors: List[str]
    scenarios: Scenario
    preconditions: List[str]
    postconditions: List[str]

    # After interpratation
    dto: Dto
    uses: List['UseCase']
    extends: List['UseCase']
    include: List['UseCase']
    services: List[Service]
    resource: Resource
    repositories: List[Repository]

    @classmethod
    def capitalize(cls):
        Utils.capitalize(cls(name=Utils.capitalize(cls.name)))
