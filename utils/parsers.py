<<<<<<< HEAD
import re
from typing import Tuple, List, Dict
from models.relationship_model import RelationshipType

def parse_attribute_value(value: str) -> Tuple[str, str, str]:
    pattern = r'(?P<visibility>[+#-])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)'
    match = re.match(pattern, value)
    if match:
        return match.group("visibility"), match.group("name"), match.group("type")
    return "+", "name", "void"

def parse_method_value(value: str) -> Tuple[str, str, str, List[str]]:
    pattern = r'(?P<visibility>[+#-])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*\((?P<args>[a-zA-Z0-9_,\s]*)\)\s*:\s*(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)'
    match = re.match(pattern, value)
    if match:
        args = [arg.strip() for arg in match.group("args").split(",") if arg.strip()]
        return match.group("visibility"), match.group("name"), match.group("type"), args
    return "+", "name", "void", []

def parse_relationship_type(style: str) -> RelationshipType:
    pattern = r"(?<=\bendarrow=)[^;]+"
    matched = re.search(pattern, style)
    if matched is None:
        return RelationshipType.NONE
    
    match(matched.group()):
        case "block":
            return RelationshipType.INHERITANCE
        
        case "diamondthin":
            fill_pattern = r"(?<=\bendfill=)[^;]+"
            fill_matched = re.search(fill_pattern, style).group()

            if (bool(fill_matched)):
                return RelationshipType.COMPOSITION
            else :
                return RelationshipType.AGREGATION
            
        case "open":
            return RelationshipType.ATTRIBUTE

        case _ :
            return RelationshipType.NONE
                
def extract_class_name_by_id(structured_data: Dict, id: str) -> str:
    for class_id in structured_data['classes'].keys():
        if class_id == id:
            return structured_data['classes'][class_id]['name']
        
    return ""

def interpret_visibility(visibility: str) -> str:
    visibility_map = {
        "+": "public",
        "#": "protected",
        "-": "private"
    }
=======
import re
from typing import Tuple, List, Dict
from models.relationship_model import RelationshipType

def parse_attribute_value(value: str) -> Tuple[str, str, str]:
    pattern = r'(?P<visibility>[+#-])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)'
    match = re.match(pattern, value)
    if match:
        return match.group("visibility"), match.group("name"), match.group("type")
    return "+", "name", "void"

def parse_method_value(value: str) -> Tuple[str, str, str, List[str]]:
    pattern = r'(?P<visibility>[+#-])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*\((?P<args>[a-zA-Z0-9_,\s]*)\)\s*:\s*(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)'
    match = re.match(pattern, value)
    if match:
        args = [arg.strip() for arg in match.group("args").split(",") if arg.strip()]
        return match.group("visibility"), match.group("name"), match.group("type"), args
    return "+", "name", "void", []

def parse_relationship_type(style: str) -> RelationshipType:
    pattern = r"(?<=\bendarrow=)[^;]+"
    matched = re.search(pattern, style)
    if matched is None:
        return RelationshipType.NONE
    
    match(matched.group()):
        case "block":
            return RelationshipType.INHERITANCE
        
        case "diamondthin":
            fill_pattern = r"(?<=\bendfill=)[^;]+"
            fill_matched = re.search(fill_pattern, style).group()

            if (bool(fill_matched)):
                return RelationshipType.COMPOSITION
            else :
                return RelationshipType.AGREGATION
            
        case "open":
            return RelationshipType.ATTRIBUTE

        case _ :
            return RelationshipType.NONE
                
def extract_class_name_by_id(structured_data: Dict, id: str) -> str:
    for class_id in structured_data['classes'].keys():
        if class_id == id:
            return structured_data['classes'][class_id]['name']
        
    return ""

def interpret_visibility(visibility: str) -> str:
    visibility_map = {
        "+": "public",
        "#": "protected",
        "-": "private"
    }
>>>>>>> d598bcdb5763c0553a737c71d46b5b100a15560d
    return visibility_map.get(visibility, "public")