from core.ir.er_diagram import ERDiagram, RelationshipKind
from core.ir.project_ir import IREntity, IRField, ProjectIR
from helpers.utils import capitalize


class SemanticAnalyzer:
    """
    Transforms an ERDiagram AST into a target-agnostic ProjectIR.

    This stage is intentionally blind to both the input format (draw.io,
    PlantUML, Mermaid…) and the output target (Spring Boot, Django, NestJS…).
    It only resolves entity structure and relationships; type names are passed
    through as-is so each backend can normalize them to its own type system.
    """

    def analyze(self, diagram: ERDiagram, package: str) -> ProjectIR:
        ir_by_id: dict[str, IREntity] = {}

        for entity_id, er_entity in diagram.entities.items():
            fields = [
                IRField(name=f.name, type=f.type, visibility=f.visibility)
                for f in er_entity.fields
            ]
            ir_by_id[entity_id] = IREntity(name=capitalize(er_entity.name), fields=fields)

        for rel in diagram.relationships:
            source = ir_by_id.get(rel.source_id)
            target = ir_by_id.get(rel.target_id)
            if not source or not target:
                continue

            match rel.kind:
                case RelationshipKind.INHERITANCE:
                    if source.parent is None:
                        source.parent = target
                case RelationshipKind.COMPOSITION:
                    if target not in source.compositions:
                        source.compositions.append(target)
                case RelationshipKind.AGGREGATION | RelationshipKind.ASSOCIATION:
                    if target not in source.aggregations:
                        source.aggregations.append(target)

        return ProjectIR(package=package, entities=list(ir_by_id.values()))
