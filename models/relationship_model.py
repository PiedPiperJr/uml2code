from dataclasses import dataclass

@dataclass
class Relationship:
    name: str
    source: str
    target: str
    edge: str
    style: str
    type: str
    multiplicity: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Relationship':
        return cls(**data)