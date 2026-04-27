from abc import ABC, abstractmethod
from core.ir.er_diagram import ERDiagram


class IFrontend(ABC):
    @abstractmethod
    def parse(self, source: str) -> ERDiagram:
        ...
