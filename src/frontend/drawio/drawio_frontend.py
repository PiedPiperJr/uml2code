from core.ir.er_diagram import ERDiagram
from core.ports.frontend_port import IFrontend
from frontend.drawio.lexer import DrawIOLexer
from frontend.drawio.parser import DrawIOParser


class DrawIOFrontend(IFrontend):
    """Facade that wires the DrawIO lexer and parser behind the IFrontend port."""

    def __init__(self):
        self._lexer = DrawIOLexer()
        self._parser = DrawIOParser()

    def parse(self, source: str) -> ERDiagram:
        cells = self._lexer.tokenize(source)
        return self._parser.parse(cells)
