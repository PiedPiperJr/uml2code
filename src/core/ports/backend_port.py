from abc import ABC, abstractmethod
from pathlib import Path
from core.ir.project_ir import ProjectIR


class IBackend(ABC):
    @abstractmethod
    def generate(self, ir: ProjectIR) -> list:
        ...

    @abstractmethod
    def write(self, files: list, output_dir: Path) -> None:
        ...
