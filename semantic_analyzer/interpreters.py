import re
from typing import List, Optional, Tuple
from helpers.utils import Utils
from models.class_model import Class
from models.interpreted_relationship_model import InterpretedRelationShip
from models.relationship_model import Relationship, RelationshipType
from semantic_analyzer.models_factory import ModelsFactory


class Interpreter:

    @staticmethod
    def interpret_relationship_style_old(style: str) -> RelationshipType:
        style = style.lower()
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
    def interpret_relationships_new(classes: List[Class], relationships: List[Relationship]) -> List[Relationship]:
        for relationship in relationships:
            source_class = next((cls for cls in classes if cls.name == relationship.source_name), None)
            target_class = next((cls for cls in classes if cls.name == relationship.target_name), None)

            if not source_class or not target_class:
                continue

            if RelationshipType.INHERITANCE:
                source_class.parent = target_class.name
                continue

            ## Interpretation de la relation proprement dite
            source_interpretation = Interpreter._interpret_relationship_source(relationship, source_class)

    @staticmethod
    def _interpret_relationship_source(relationship: Relationship, source_class: Class) -> InterpretedRelationShip:
        
        if relationship.source_multiplicity is not None:
            pass
        
        
        

        return None, None

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
                        case RelationshipType.INHERITANCE:
                            _class.parent = relationship.target_name

                        case RelationshipType.AGGREGATION:
                            _class.aggregations.append(attribute)

                        case RelationshipType.COMPOSITION:
                            _class.compositions.append(attribute)

                        # case RelationshipType.ATTRIBUTE:
                        #     _class.attributes.append(attribute)

                        case RelationshipType.NONE:
                            pass

        return classes
    
    @staticmethod
    def interpret_relationship_style(style_str: str, relationship_name: Optional[str]) -> Tuple[RelationshipType, Optional[str], bool, bool]:
        
        styles = Utils.parse_style_string(style_str)
        
        end_arrow = styles.get("endarrow")
        start_arrow = styles.get("startarrow")
        end_fill = styles.get("endfill", "1") == "1" 
        start_fill = styles.get("startfill", "1") == "1"
        dashed = styles.get("dashed", "0") == "1"

        stereotype = None

        if relationship_name and relationship_name.startswith("<<") and relationship_name.endswith(">>"):
            stereotype = relationship_name
            
        # Composition (losange plein)
        if start_arrow == "diamondthin" and start_fill:
            return RelationshipType.COMPOSITION, stereotype, (end_arrow == "open"), False
        if end_arrow == "diamondthin" and end_fill:
            return RelationshipType.COMPOSITION, stereotype, False, (start_arrow == "open")

        # Agrégation (losange vide)
        if start_arrow == "diamondthin" and not start_fill:
            return RelationshipType.AGGREGATION, stereotype, (end_arrow == "open"), False
        if end_arrow == "diamondthin" and not end_fill:
            return RelationshipType.AGGREGATION, stereotype, False, (start_arrow == "open")

        # Héritage (Generalization) ou Réalisation d'interface
        if end_arrow == "block" or end_arrow == "triangle": # 'triangle' est aussi commun pour l'héritage
            if dashed:
                return RelationshipType.INTERFACE, stereotype, False, False
            else:
                return RelationshipType.INHERITANCE, stereotype, False, False
            
        # Si la flèche d'héritage est à la source (moins courant mais possible dans certains outils)
        if start_arrow == "block" or start_arrow == "triangle":
            if dashed: # Moins probable pour une réalisation, mais pour être complet
                return RelationshipType.INTERFACE, stereotype, False, False
            else: # Moins probable pour un héritage, mais pour être complet
                return RelationshipType.INHERITANCE, stereotype, False, False

        # Dépendance (ligne pointillée, flèche ouverte)
        if dashed and (end_arrow == "open" or end_arrow == "classic" or end_arrow == "blockthin"): # classic/blockthin sont aussi des flèches ouvertes
            return RelationshipType.DEPENDENCY, stereotype, True, False # Dépendance est généralement dirigée
        if dashed and (start_arrow == "open" or start_arrow == "classic" or start_arrow == "blockthin"):
             return RelationshipType.DEPENDENCY, stereotype, False, True


        # Association (ligne pleine, peut avoir des flèches ouvertes pour navigabilité)
        if not dashed:
            nav_to_target = (end_arrow == "open" or end_arrow == "classic" or end_arrow == "blockthin")
            nav_to_source = (start_arrow == "open" or start_arrow == "classic" or start_arrow == "blockthin")
            
            # Si pas d'autres types identifiés, c'est une association
            return RelationshipType.ASSOCIATION, stereotype, nav_to_target, nav_to_source
            
        return RelationshipType.NONE, stereotype, False, False   