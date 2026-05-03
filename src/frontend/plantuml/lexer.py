import re

_BLOCK_RE       = re.compile(r'@startuml\b[^\n]*\n(.*?)@enduml', re.DOTALL | re.IGNORECASE)
_INLINE_COMMENT = re.compile(r"'.*$")
_BLOCK_COMMENT  = re.compile(r"/'\s*.*?\s*'/", re.DOTALL)


class PlantUMLLexer:
    """Splits a PlantUML source file into cleaned line-lists, one per @startuml block."""

    def tokenize(self, source: str) -> list[list[str]]:
        source = _BLOCK_COMMENT.sub('', source)
        blocks = []
        for match in _BLOCK_RE.finditer(source):
            lines = []
            for raw in match.group(1).splitlines():
                line = _INLINE_COMMENT.sub('', raw).strip()
                if line:
                    lines.append(line)
            if lines:
                blocks.append(lines)
        return blocks
