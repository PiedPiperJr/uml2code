from core.ir.er_diagram import ERDiagram, RelationshipKind
from core.ir.project_ir import IREntity, IRField, ProjectIR
from helpers.utils import capitalize

# Maps common type aliases to canonical Java types
_JAVA_TYPE_MAP: dict[str, str] = {
    'int':       'Integer',
    'integer':   'Integer',
    'string':    'String',
    'str':       'String',
    'bool':      'Boolean',
    'boolean':   'Boolean',
    'float':     'Float',
    'double':    'Double',
    'long':      'Long',
    'char':      'Character',
    'byte':      'Byte',
    'short':     'Short',
    'void':      'void',
    'date':      'LocalDate',
    'datetime':  'LocalDateTime',
    'timestamp': 'LocalDateTime',
    'uuid':      'UUID',
    'object':    'Object',
    'list':      'List',
    'set':       'Set',
    'map':       'Map',
}


def _normalize_type(raw: str) -> str:
    stripped = raw.strip()
    return _JAVA_TYPE_MAP.get(stripped.lower(), stripped)


class SemanticAnalyzer:
    """Transforms an ERDiagram AST into a target-agnostic ProjectIR."""

    def analyze(self, diagram: ERDiagram, package: str) -> ProjectIR:
        ir_by_id: dict[str, IREntity] = {}

        # Build one IREntity per diagram entity
        for entity_id, er_entity in diagram.entities.items():
            fields = [
                IRField(
                    name=er_entity.name,
                    type=_normalize_type(f.type),
                    visibility=f.visibility,
                )
                for f in er_entity.fields
            ]
            # Fix: use f.name not er_entity.name for each field
            fields = [
                IRField(name=f.name, type=_normalize_type(f.type), visibility=f.visibility)
                for f in er_entity.fields
            ]
            ir_by_id[entity_id] = IREntity(name=capitalize(er_entity.name), fields=fields)

        # Apply relationships
        for rel in diagram.relationships:
            source = ir_by_id.get(rel.source_id)
            target = ir_by_id.get(rel.target_id)
            if not source or not target:
                continue

            match rel.kind:
                case RelationshipKind.INHERITANCE:
                    if source.parent is None:  # first wins
                        source.parent = target
                case RelationshipKind.COMPOSITION:
                    if target not in source.compositions:
                        source.compositions.append(target)
                case RelationshipKind.AGGREGATION | RelationshipKind.ASSOCIATION:
                    if target not in source.aggregations:
                        source.aggregations.append(target)

        return ProjectIR(package=package, entities=list(ir_by_id.values()))
