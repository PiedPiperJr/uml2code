from dataclasses import dataclass, field

from core.ir.class_diagram import ClassDiagram
from core.ir.sequence_diagram import SequenceDiagram
from core.ir.usecase_diagram import UseCaseDiagram


@dataclass
class DiagramBundle:
    """Collects every diagram parsed from a single source file.

    A frontend may populate any subset of the lists; consumers check each list
    independently. This type is the contract between the frontend layer and the
    middleend — it is intentionally source-format-agnostic.
    """
    class_diagrams:    list[ClassDiagram]    = field(default_factory=list)
    usecase_diagrams:  list[UseCaseDiagram]  = field(default_factory=list)
    sequence_diagrams: list[SequenceDiagram] = field(default_factory=list)
