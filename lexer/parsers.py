import re
from typing import Tuple, List, Dict
from models.relationship_model import RelationshipType


class Parsers:

    @staticmethod
    def parse_attribute_value(value: str) -> Tuple[str, str, str]:
        pattern = r'(?P<visibility>[+#-])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)'
        match = re.match(pattern, value)
        if match:
            return match.group("visibility"), match.group("name"), match.group("type")
        return "+", "name", "void"

    @staticmethod
    def parse_method_value(value: str) -> Tuple[str, str, str, List[str]]:
        pattern = r'(?P<visibility>[+#-])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*\((?P<args>[a-zA-Z0-9_,\s]*)\)\s*:\s*(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)'
        match = re.match(pattern, value)
        if match:
            args = [arg.strip() for arg in match.group(
                "args").split(",") if arg.strip()]
            return match.group("visibility"), match.group("name"), match.group("type"), args
        return "+", "name", "void", []
