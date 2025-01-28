from dataclasses import dataclass, field
from typing import List, Literal
from models.class_model import Class
from utils.utils import capitalize


@dataclass
class Decorator:
    name: str
    message: str


@dataclass
class Arg:
    visibility: Literal["public", "private", "protected"]
    name: str
    type: str


@dataclass
class DtoAttribute(Arg):
    decorators: List[Decorator]


@dataclass
class Dto:
    name: str
    attributes: List[DtoAttribute]


@dataclass
class Method:
    name: str
    args: List[Arg]
    type: str
    visibility: Literal["public", "private", "protected"]


@dataclass
class Service:
    name: str
    methods: List[Method]


@dataclass
class Repository:
    entity: str
    methods: List[Method]


@dataclass
class Resource:
    name: str
    attributes: List[Arg]

@dataclass
class Scenario:
    main: List[str]
    alternative: List[str]

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
    extends: List['UseCase']
    include: List['UseCase']
    services: List[Service]
    resource: Resource
    repositories: List[Repository]

    @classmethod
    def capitalize(cls):
        capitalize(cls(name=capitalize(cls.name)))

    
@dataclass
class Project:
    route: str
    classes: List[Class]
    useCases: List[UseCase]

    
