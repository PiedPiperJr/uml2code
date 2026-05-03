from dataclasses import dataclass, field


@dataclass
class Actor:
    name: str


@dataclass
class UseCase:
    name:  str
    alias: str = ""


@dataclass
class UseCaseLink:
    source: str
    target: str
    kind:   str  # "triggers" | "include" | "extend" | "generalize"
    label:  str = ""


@dataclass
class UseCaseDiagram:
    actors:    dict[str, Actor]    = field(default_factory=dict)
    usecases:  dict[str, UseCase]  = field(default_factory=dict)
    links:     list[UseCaseLink]   = field(default_factory=list)
