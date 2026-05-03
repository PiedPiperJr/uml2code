import re

from core.ir.sequence_diagram import SeqMessage, SeqParticipant, SequenceDiagram

_PARTICIPANT_KINDS = frozenset([
    'participant', 'actor', 'boundary', 'control',
    'entity', 'database', 'collections', 'queue',
])

# participant "Full Name" as alias  |  participant Name  |  actor Name as A
_PARTICIPANT_RE = re.compile(
    r'^(?P<kind>' + '|'.join(_PARTICIPANT_KINDS) + r')\s+'
    r'(?:"(?P<qname>[^"]+)"|(?P<name>[A-Za-z_]\w*))'
    r'(?:\s+as\s+(?P<alias>[A-Za-z_]\w*))?$',
    re.IGNORECASE,
)

# Explicit arrow forms, longest first to avoid partial matches
_KNOWN_ARROWS = ['-->>', '->>', '-->', '-x', '->', '<--', '<<--', '<-']
_ARROW_PAT = '|'.join(re.escape(a) for a in _KNOWN_ARROWS)

# Sender arrow Receiver [: label]
_MESSAGE_RE = re.compile(
    rf'^(?P<sender>[A-Za-z_]\w*)'
    rf'\s*(?P<arrow>{_ARROW_PAT})'
    rf'\s*(?P<receiver>[A-Za-z_]\w*)'
    rf'(?:\s*:\s*(?P<label>.+))?$'
)


class SequenceParser:
    """Parses a PlantUML sequence-diagram block into a SequenceDiagram."""

    def parse(self, lines: list[str]) -> SequenceDiagram:
        diagram   = SequenceDiagram()
        known: set[str] = set()

        for line in lines:
            # Participant / actor declaration
            m = _PARTICIPANT_RE.match(line)
            if m:
                name  = m.group('qname') or m.group('name')
                alias = m.group('alias') or name
                kind  = m.group('kind').lower()
                diagram.participants.append(SeqParticipant(name=name, alias=alias, kind=kind))
                known.add(alias)
                continue

            # Message
            m = _MESSAGE_RE.match(line)
            if m:
                sender   = m.group('sender')
                receiver = m.group('receiver')
                label    = (m.group('label') or '').strip()
                arrow    = m.group('arrow')

                # Auto-register participants that were not declared explicitly
                for p in (sender, receiver):
                    if p not in known:
                        diagram.participants.append(SeqParticipant(name=p, alias=p))
                        known.add(p)

                diagram.messages.append(
                    SeqMessage(sender=sender, receiver=receiver, label=label, arrow=arrow)
                )

        return diagram
