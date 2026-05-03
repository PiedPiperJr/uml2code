from core.ir.diagram_bundle import DiagramBundle
from core.ports.frontend_port import IFrontend
from frontend.plantuml.detector import detect
from frontend.plantuml.lexer import PlantUMLLexer
from frontend.plantuml.parsers.class_parser import ClassParser
from frontend.plantuml.parsers.sequence_parser import SequenceParser
from frontend.plantuml.parsers.usecase_parser import UseCaseParser


class PlantUMLFrontend(IFrontend):
    """Parses a PlantUML source file into a DiagramBundle.

    Each @startuml…@enduml block is detected and dispatched to the appropriate
    parser. Multiple blocks of different types in the same file are all captured.
    """

    def __init__(self):
        self._lexer    = PlantUMLLexer()
        self._parsers  = {
            'class':    ClassParser(),
            'usecase':  UseCaseParser(),
            'sequence': SequenceParser(),
        }

    def parse(self, source: str) -> DiagramBundle:
        bundle = DiagramBundle()

        for block_lines in self._lexer.tokenize(source):
            kind = detect(block_lines)

            if kind == 'class':
                bundle.class_diagrams.append(self._parsers['class'].parse(block_lines))
            elif kind == 'usecase':
                bundle.usecase_diagrams.append(self._parsers['usecase'].parse(block_lines))
            elif kind == 'sequence':
                bundle.sequence_diagrams.append(self._parsers['sequence'].parse(block_lines))

        return bundle
