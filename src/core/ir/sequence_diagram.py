from dataclasses import dataclass, field


@dataclass
class SeqParticipant:
    name:  str
    alias: str = ""
    # actor | participant | boundary | control | entity | database | collections
    kind:  str = "participant"


@dataclass
class SeqMessage:
    sender:   str
    receiver: str
    label:    str
    arrow:    str   # "->" | "-->" | "->>" | "-->>" | "-x" …


@dataclass
class SequenceDiagram:
    participants: list[SeqParticipant] = field(default_factory=list)
    messages:     list[SeqMessage]     = field(default_factory=list)
