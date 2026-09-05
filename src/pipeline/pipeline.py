from dataclasses import dataclass
from pathlib import Path

from core.ports.backend_port import IBackend
from core.ports.frontend_port import IFrontend
from middleend.semantic_analyzer import SemanticAnalyzer


@dataclass
class Pipeline:
    """
    Orchestrates the three stages of the transpiler:
      frontend  →  middle-end  →  backend

    Depends only on the abstract port interfaces, so any frontend or backend
    implementation can be injected without touching this class.
    """
    frontend: IFrontend
    analyzer: SemanticAnalyzer
    backend: IBackend

    def run(self, source: str, package: str, output_dir: Path) -> list:
        diagram = self.frontend.parse(source)
        ir      = self.analyzer.analyze(diagram, package)
        files   = self.backend.generate(ir)
        self.backend.write(files, output_dir)
        return files
