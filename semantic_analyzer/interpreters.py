import re
from typing import List
from helpers.utils import Utils
from models.class_model import Class
from models.relationship_model import Relationship, RelationshipType
from semantic_analyzer.models_factory import ModelsFactory


class Interpreter:

    @staticmethod
    def interpret_relationship_style(style: str) -> RelationshipType:
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
                else:
                    return RelationshipType.AGREGATION

            case "open":
                return RelationshipType.ATTRIBUTE

            case _:
                return RelationshipType.NONE

    @staticmethod
    def map_visibility_symbol(visibility: str) -> str:
        match visibility:
            case '#':
                return "protected"
            case '-':
                return "private"
            case _:
                return "public"

    @staticmethod
    def interpret_visibility(classes: List[Class]):
        for _class in classes:
            # attribute type validation
            for attrib in _class.attributes:
                attrib.visibility = Interpreter.map_visibility_symbol(
                    attrib.visibility)

            # method type validation
            for method in _class.methods:
                method.visibility = Interpreter.map_visibility_symbol(
                    method.visibility)

        return classes

    @staticmethod
    def interpret_relationships(classes: List[Class], relationships: List[Relationship]) -> List[Class]:
        for _class in classes:
            _class.aggregations = []
            _class.compositions = []

            for relationship in relationships:
                if _class.name.lower() == relationship.source_name.lower():
                    attribute = ModelsFactory.build_attribute_model({'visibility': 'private',
                                                                     'type': Utils.capitalize(relationship.target_name),
                                                                     'name': relationship.target_name.lower() + 's'})
                    match(relationship._type):
                        # TODO rewrite this
                        # case RelationshipType.INHERITANCE:
                        #     _class['parent'] = relationship.target_name

                        case RelationshipType.AGGREGATION:
                            _class.aggregations.append(attribute)

                        case RelationshipType.COMPOSITION:
                            _class.compositions.append(attribute)

                        case RelationshipType.ATTRIBUTE:
                            _class['attributes'].append(attribute)

                        case RelationshipType.NONE:
                            pass

        return classes
