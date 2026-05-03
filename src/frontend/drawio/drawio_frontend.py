from core.ir.er_diagram import ERDiagram
from core.ports.frontend_port import IFrontend
from frontend.drawio.lexer import DrawIOLexer
from frontend.drawio.parser import DrawIOParser


class DrawIOFrontend(IFrontend):
    """Facade that wires the DrawIO lexer and parser behind the IFrontend port."""

    def __init__(self):
        self._lexer  = DrawIOLexer()
        self._parser = DrawIOParser()

    def parse(self, source: str) -> ERDiagram:
        merged = ERDiagram()
        for page_cells in self._lexer.tokenize(source):
            page = self._parser.parse(page_cells)
            merged.entities.update(page.entities)
            merged.relationships.extend(page.relationships)
        return merged
