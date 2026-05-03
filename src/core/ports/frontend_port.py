from abc import ABC, abstractmethod

from core.ir.diagram_bundle import DiagramBundle


class IFrontend(ABC):
    @abstractmethod
    def parse(self, source: str) -> DiagramBundle:
        ...
