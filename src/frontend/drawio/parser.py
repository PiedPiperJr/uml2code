import re
from typing import Optional

from core.ir.er_diagram import (
    ERDiagram, EREntity, ERField, ERMethod, ERParam, ERRelationship, RelationshipKind,
)
from helpers.utils import capitalize

_VISIBILITY_MAP = {'+': 'public', '-': 'private', '#': 'protected', '~': 'package'}

# Supports generics: List<String>, Map<K,V>, Optional<T>, etc.
_TYPE_RE = r'[a-zA-Z_][a-zA-Z0-9_<>,\s\[\]]*'

_FIELD_RE = re.compile(
    rf'(?P<vis>[+#\-~])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?P<type>{_TYPE_RE})'
)
_METHOD_RE = re.compile(
    rf'(?P<vis>[+#\-~])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*\((?P<params>[^)]*)\)\s*:\s*(?P<type>{_TYPE_RE})'
)


def _visibility(symbol: str) -> str:
    return _VISIBILITY_MAP.get(symbol, 'public')


def _parse_param(raw: str) -> Optional[ERParam]:
    raw = raw.strip()
    if not raw:
        return None
    parts = raw.split()
    if len(parts) >= 2:
        return ERParam(name=parts[1], type=parts[0])
    return ERParam(name=parts[0], type='Object')


def _parse_field(value: str) -> Optional[ERField]:
    m = _FIELD_RE.match(value.strip())
    if not m:
        return None
    return ERField(
        name=m.group('name').strip(),
        type=m.group('type').strip(),
        visibility=_visibility(m.group('vis')),
    )


def _parse_method(value: str) -> Optional[ERMethod]:
    m = _METHOD_RE.match(value.strip())
    if not m:
        return None
    params = [p for p in (_parse_param(p) for p in m.group('params').split(',')) if p]
    return ERMethod(
        name=m.group('name').strip(),
        return_type=m.group('type').strip(),
        visibility=_visibility(m.group('vis')),
        params=params,
    )


def _interpret_style(style: str) -> RelationshipKind:
    style = style.lower()
    m = re.search(r'endarrow=([^;]+)', style)
    if not m:
        return RelationshipKind.NONE

    arrow = m.group(1).strip()

    if arrow == 'block':
        return RelationshipKind.INHERITANCE

    if arrow == 'diamondthin':
        fill_m = re.search(r'endfill=([^;]+)', style)
        if fill_m and fill_m.group(1).strip() not in ('0', 'false', ''):
            return RelationshipKind.COMPOSITION
        return RelationshipKind.AGGREGATION

    if arrow in ('open', 'classic', 'classicthin', 'openasync'):
        return RelationshipKind.ASSOCIATION

    return RelationshipKind.NONE


class DrawIOParser:
    """Builds an ERDiagram AST from a flat list of draw.io cell dicts."""

    def parse(self, cells: list[dict]) -> ERDiagram:
        diagram = ERDiagram()
        root_id, sub_root_id = self._find_roots(cells)

        # O(1) lookup by cell id
        cell_index: dict[str, dict] = {c.get('@id'): c for c in cells if c.get('@id')}

        # Pass 1: extract entities
        for cell in cells:
            if self._is_entity(cell, sub_root_id):
                entity = EREntity(
                    id=cell['@id'],
                    name=capitalize(cell.get('@value', '').strip()),
                )
                diagram.entities[entity.id] = entity

        # Pass 2: extract fields and methods
        for cell in cells:
            parent_id = cell.get('@parent')
            if parent_id not in diagram.entities:
                continue
            value = cell.get('@value', '').strip()
            if not value:
                continue

            if '(' in value and ')' in value:
                method = _parse_method(value)
                if method:
                    diagram.entities[parent_id].methods.append(method)
            else:
                field = _parse_field(value)
                if field:
                    diagram.entities[parent_id].fields.append(field)

        # Pass 3: extract relationships
        for cell in cells:
            if not self._is_relationship(cell, sub_root_id):
                continue

            source_id = self._resolve_to_entity(cell.get('@source', ''), cell_index, diagram.entities)
            target_id = self._resolve_to_entity(cell.get('@target', ''), cell_index, diagram.entities)

            if not source_id or not target_id or source_id == target_id:
                continue

            kind = _interpret_style(cell.get('@style', ''))
            if kind == RelationshipKind.NONE:
                continue

            diagram.relationships.append(ERRelationship(
                source_id=source_id,
                target_id=target_id,
                kind=kind,
                label=cell.get('@value', ''),
            ))

        return diagram

    def _find_roots(self, cells: list[dict]) -> tuple[str, str]:
        root_id = next((c['@id'] for c in cells if len(c) == 1 and '@id' in c), None)
        sub_root_id = next(
            (c['@id'] for c in cells if len(c) == 2 and c.get('@parent') == root_id),
            None,
        )
        return root_id, sub_root_id

    def _is_entity(self, cell: dict, sub_root_id: str) -> bool:
        return bool(cell.get('@vertex')) and cell.get('@parent') == sub_root_id

    def _is_relationship(self, cell: dict, sub_root_id: str) -> bool:
        return (
            cell.get('@parent') == sub_root_id
            and bool(cell.get('@source'))
            and bool(cell.get('@target'))
        )

    def _resolve_to_entity(self, cell_id: str, cell_index: dict, entities: dict) -> str:
        """Walk the parent chain until an entity is found."""
        visited: set[str] = set()
        current = cell_id
        while current and current not in visited:
            if current in entities:
                return current
            visited.add(current)
            parent = (cell_index.get(current) or {}).get('@parent')
            current = parent
        return ''
