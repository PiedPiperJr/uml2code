from core.ir.class_diagram import ClassDiagram, RelationshipKind
from core.ir.diagram_bundle import DiagramBundle
from core.ir.project_ir import IREntity, IRField, ProjectIR
from helpers.utils import capitalize


class SemanticAnalyzer:
    """
    Transforms a DiagramBundle into a target-agnostic ProjectIR.

    This stage is intentionally blind to both the input format (draw.io,
    PlantUML, Mermaid…) and the output target (Spring Boot, Django, NestJS…).
    It merges all ClassDiagrams from the bundle and resolves entity structure
    and relationships; type names are passed through as-is so each backend can
    normalize them to its own type system.
    """

    def analyze(self, bundle: DiagramBundle, package: str) -> ProjectIR:
        merged = ClassDiagram()
        for cd in bundle.class_diagrams:
            merged.classes.update(cd.classes)
            merged.relationships.extend(cd.relationships)

        ir_by_id: dict[str, IREntity] = {}

        for cls_id, uml_class in merged.classes.items():
            fields = [
                IRField(name=f.name, type=f.type, visibility=f.visibility)
                for f in uml_class.fields
            ]
            ir_by_id[cls_id] = IREntity(name=capitalize(uml_class.name), fields=fields)

        for rel in merged.relationships:
            source = ir_by_id.get(rel.source_id)
            target = ir_by_id.get(rel.target_id)
            if not source or not target:
                continue

            match rel.kind:
                case RelationshipKind.INHERITANCE | RelationshipKind.REALIZATION:
                    if source.parent is None:
                        source.parent = target
                case RelationshipKind.COMPOSITION:
                    if target not in source.compositions:
                        source.compositions.append(target)
                case RelationshipKind.AGGREGATION | RelationshipKind.ASSOCIATION:
                    if target not in source.aggregations:
                        source.aggregations.append(target)

        return ProjectIR(package=package, entities=list(ir_by_id.values()))
