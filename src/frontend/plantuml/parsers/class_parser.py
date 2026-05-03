import re
from typing import Optional

from core.ir.class_diagram import (
    ClassDiagram, ClassField, ClassMethod, ClassParam,
    ClassRelationship, RelationshipKind, UMLClass,
)

_VISIBILITY_MAP = {'+': 'public', '-': 'private', '#': 'protected', '~': 'package'}
_TYPE_RE = r'[A-Za-z_][\w<>,\s\[\]]*'

# class / abstract class / interface / enum — with optional <<stereotype>>
_CLASS_RE = re.compile(
    r'^(?P<abstract>abstract\s+)?(?P<kind>class|interface|enum)\s+'
    r'(?P<name>[A-Za-z_]\w*)'
    r'(?:\s+<<\s*(?P<stereotype>[^>]+?)\s*>>)?'
    r'(?:\s*\{.*)?$',
    re.IGNORECASE,
)

_FIELD_RE = re.compile(
    rf'^(?P<vis>[+\-#~])\s*(?P<name>[A-Za-z_]\w*)\s*:\s*(?P<type>{_TYPE_RE})\s*$'
)

_METHOD_RE = re.compile(
    rf'^(?P<vis>[+\-#~])\s*(?P<name>[A-Za-z_]\w*)\s*\((?P<params>[^)]*)\)'
    rf'(?:\s*:\s*(?P<type>{_TYPE_RE}))?\s*$'
)

# Relationship: LeftName <arrow> RightName [: label]
_REL_RE = re.compile(
    r'^(?P<left>[A-Za-z_]\w*)'
    r'\s+(?P<arrow>[<|o*]{0,3}[-=.]{1,4}[>|o*]{0,3})'
    r'\s+(?P<right>[A-Za-z_]\w*)'
    r'(?:\s*:\s*(?P<label>.+))?$'
)

_SECTION_SEPARATORS = frozenset(['--', '==', '..', '__'])


def _visibility(sym: str) -> str:
    return _VISIBILITY_MAP.get(sym, 'public')


def _parse_param(raw: str) -> Optional[ClassParam]:
    raw = raw.strip()
    if not raw:
        return None
    if ':' in raw:
        name, _, type_ = raw.partition(':')
        return ClassParam(name=name.strip(), type=type_.strip())
    parts = raw.split()
    if len(parts) >= 2:
        return ClassParam(name=parts[-1], type=' '.join(parts[:-1]))
    return ClassParam(name=parts[0], type='Object')


def _parse_field(line: str) -> Optional[ClassField]:
    m = _FIELD_RE.match(line.strip())
    if not m:
        return None
    return ClassField(
        name=m.group('name').strip(),
        type=m.group('type').strip(),
        visibility=_visibility(m.group('vis')),
    )


def _parse_method(line: str) -> Optional[ClassMethod]:
    m = _METHOD_RE.match(line.strip())
    if not m:
        return None
    params_str = m.group('params').strip()
    params = [p for p in (_parse_param(s) for s in params_str.split(',')) if p]
    return ClassMethod(
        name=m.group('name').strip(),
        return_type=(m.group('type') or 'void').strip(),
        visibility=_visibility(m.group('vis')),
        params=params,
    )


def _parse_relationship(line: str) -> Optional[ClassRelationship]:
    m = _REL_RE.match(line.strip())
    if not m:
        return None
    left  = m.group('left')
    arrow = m.group('arrow')
    right = m.group('right')
    label = (m.group('label') or '').strip()

    reversed_, kind = _interpret_arrow(arrow)
    if kind is RelationshipKind.NONE:
        return None

    source_id, target_id = (right, left) if reversed_ else (left, right)
    return ClassRelationship(source_id=source_id, target_id=target_id, kind=kind, label=label)


def _interpret_arrow(arrow: str) -> tuple[bool, RelationshipKind]:
    """Return (reversed, kind).

    reversed=True means the semantic source/target are swapped relative to
    the textual left/right order (e.g. '<|--' means right extends left).
    """
    a = arrow

    # Inheritance / Realization — presence of '|'
    if '|' in a:
        kind = RelationshipKind.REALIZATION if '.' in a else RelationshipKind.INHERITANCE
        # '<|' at start → right is child (source), left is parent (target) → reversed
        return a.startswith('<'), kind

    # Composition — '*'
    if '*' in a:
        # '*--' diamond at left (left = whole/source); '--*' diamond at right → reversed
        return not a.startswith('*'), RelationshipKind.COMPOSITION

    # Aggregation — 'o'
    if 'o' in a:
        return not a.startswith('o'), RelationshipKind.AGGREGATION

    # Directed association / dependency
    if a.startswith('<'):
        return True, RelationshipKind.ASSOCIATION

    return False, RelationshipKind.ASSOCIATION


class ClassParser:
    """Parses a PlantUML class-diagram block into a ClassDiagram."""

    def parse(self, lines: list[str]) -> ClassDiagram:
        diagram = ClassDiagram()
        current: Optional[UMLClass] = None
        pending_rels: list[str] = []

        for line in lines:
            # ── Inside a class body ───────────────────────────────────────────
            if current is not None:
                if line.strip() == '}':
                    current = None
                elif line.strip() not in _SECTION_SEPARATORS:
                    if '(' in line:
                        m = _parse_method(line)
                        if m:
                            current.methods.append(m)
                    else:
                        f = _parse_field(line)
                        if f:
                            current.fields.append(f)
                continue

            # ── Class / interface declaration ─────────────────────────────────
            m = _CLASS_RE.match(line)
            if m:
                name = m.group('name')
                cls = UMLClass(
                    id=name,
                    name=name,
                    stereotype=(m.group('stereotype') or '').strip().lower(),
                    is_abstract=bool(m.group('abstract')),
                    is_interface=m.group('kind').lower() == 'interface',
                )
                diagram.classes[name] = cls
                if '{' in line:
                    current = cls
                continue

            # ── Defer relationships for a second pass ─────────────────────────
            if _REL_RE.match(line):
                pending_rels.append(line)

        # Second pass: resolve relationships (forward refs are now known)
        for line in pending_rels:
            rel = _parse_relationship(line)
            if rel:
                for cid in (rel.source_id, rel.target_id):
                    if cid not in diagram.classes:
                        diagram.classes[cid] = UMLClass(id=cid, name=cid)
                diagram.relationships.append(rel)

        return diagram
