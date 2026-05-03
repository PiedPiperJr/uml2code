import re

_CLASS_KEYWORDS    = frozenset(['class', 'interface', 'abstract', 'enum'])
_USECASE_KEYWORDS  = frozenset(['usecase'])
_SEQUENCE_KEYWORDS = frozenset(['participant', 'boundary', 'control', 'database', 'collections', 'queue'])

# Message arrow: one or more dashes/dots followed by '>' (e.g. ->, -->, ->>, -->>)
_MSG_ARROW_RE = re.compile(r'\w\s*-+[->.]*>\s*\w')


def detect(lines: list[str]) -> str:
    """Return 'class' | 'usecase' | 'sequence' based on content heuristics."""
    scores: dict[str, int] = {'class': 0, 'usecase': 0, 'sequence': 0}

    for line in lines:
        tokens = line.split()
        if not tokens:
            continue
        first = tokens[0].lower()

        if first in _SEQUENCE_KEYWORDS:
            scores['sequence'] += 3
        elif first in _USECASE_KEYWORDS:
            scores['usecase'] += 3
        elif first in _CLASS_KEYWORDS:
            scores['class'] += 3
        elif first == 'actor':
            # 'actor' appears in both use-case and sequence diagrams
            scores['usecase']  += 1
            scores['sequence'] += 1
        elif _MSG_ARROW_RE.search(line):
            scores['sequence'] += 2
        elif re.match(r'^\([^)]+\)', line):
            # Use-case shorthand: (Name) or (Name) as alias
            scores['usecase'] += 2
        elif re.search(r'\w\s+[<|o*]{0,3}[-=.]{2}[>|o*]{0,3}\s+\w', line):
            scores['class'] += 1

    return max(scores, key=lambda k: scores[k])
