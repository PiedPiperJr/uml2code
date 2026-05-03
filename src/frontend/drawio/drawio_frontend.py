from core.ir.class_diagram import ClassDiagram
from core.ir.diagram_bundle import DiagramBundle
from core.ports.frontend_port import IFrontend
from frontend.drawio.lexer import DrawIOLexer
from frontend.drawio.parser import DrawIOParser


class DrawIOFrontend(IFrontend):
    """Facade that wires the DrawIO lexer and parser behind the IFrontend port."""

    def __init__(self):
        self._lexer  = DrawIOLexer()
        self._parser = DrawIOParser()

    def parse(self, source: str) -> DiagramBundle:
        merged = ClassDiagram()
        for page_cells in self._lexer.tokenize(source):
            page = self._parser.parse(page_cells)
            merged.classes.update(page.classes)
            merged.relationships.extend(page.relationships)
        return DiagramBundle(class_diagrams=[merged])
