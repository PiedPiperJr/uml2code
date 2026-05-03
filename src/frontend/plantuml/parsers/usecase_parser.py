import re

from core.ir.usecase_diagram import Actor, UseCase, UseCaseDiagram, UseCaseLink

# actor Name  |  actor "Full Name" as alias
_ACTOR_RE = re.compile(
    r'^actor\s+(?:"(?P<qname>[^"]+)"|(?P<name>[A-Za-z_]\w*))'
    r'(?:\s+as\s+(?P<alias>[A-Za-z_]\w*))?$',
    re.IGNORECASE,
)

# usecase "Name" as alias  |  usecase (Name) as alias  |  (Name) as alias  |  (Name)
_UC_RE = re.compile(
    r'^(?:usecase\s+)?(?:"(?P<qname>[^"]+)"|\((?P<pname>[^)]+)\))'
    r'(?:\s+as\s+(?P<alias>[A-Za-z_]\w*))?$',
    re.IGNORECASE,
)

# Source <arrow> Target [: label]
_LINK_RE = re.compile(
    r'^(?P<source>[A-Za-z_]\w*)'
    r'\s+(?P<arrow>\S+)'
    r'\s+(?P<target>[A-Za-z_]\w*)'
    r'(?:\s*:\s*(?P<label>.+))?$',
)


def _link_kind(arrow: str, label: str) -> str:
    label_lc = label.lower()
    if 'include' in label_lc:
        return 'include'
    if 'extend' in label_lc:
        return 'extend'
    if '|>' in arrow or '<|' in arrow:
        return 'generalize'
    return 'triggers'


class UseCaseParser:
    """Parses a PlantUML use-case diagram block into a UseCaseDiagram."""

    def parse(self, lines: list[str]) -> UseCaseDiagram:
        diagram = UseCaseDiagram()

        for line in lines:
            # Actor declaration
            m = _ACTOR_RE.match(line)
            if m:
                name = m.group('qname') or m.group('name')
                key  = m.group('alias') or name
                diagram.actors[key] = Actor(name=name)
                continue

            # Use-case declaration
            m = _UC_RE.match(line)
            if m:
                name = (m.group('qname') or m.group('pname') or '').strip()
                key  = m.group('alias') or name
                diagram.usecases[key] = UseCase(name=name, alias=key)
                continue

            # Relationship
            m = _LINK_RE.match(line)
            if m:
                source = m.group('source')
                target = m.group('target')
                label  = (m.group('label') or '').strip()
                arrow  = m.group('arrow')
                kind   = _link_kind(arrow, label)
                diagram.links.append(
                    UseCaseLink(source=source, target=target, kind=kind, label=label)
                )

        return diagram
