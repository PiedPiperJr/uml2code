from typing import Dict, Tuple
import google.generativeai as genai


class Validators:
    @staticmethod
    def is_class(object: Dict, sub_root_id: str) -> bool:
        return (
            object.get("@vertex") and
            object.get("@parent") == sub_root_id
        )

    @staticmethod
    def is_relation(object: Dict, sub_root_id: str) -> bool:
        return (
            object.get("@parent") == sub_root_id and
            object.get("@source") and
            object.get("@target")
        )

    @staticmethod
    def is_attribute(object: Dict, sub_root_id: str) -> bool:
        return (
            object.get("@parent") and
            object.get("@parent") != sub_root_id and
            object.get("@vertex") and
            object.get("@value")
        )

    @staticmethod
    def is_method(object: Dict, sub_root_id: str) -> bool:
        if not Validators.is_attribute(object, sub_root_id):
            return False
        value: str = object.get("@value", "")
        return "(" in value and ")" in value


    @staticmethod
    def is_relationship_argument(parent: str, relationships: Dict) -> Tuple[bool, str]:
        for relationship in relationships.keys():
            if relationship == parent :
                return True, relationship
            
        return False, None