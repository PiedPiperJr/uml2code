
from dataclasses import asdict
from typing import List, Tuple, Dict

from models.class_model import Class
from models.relationship_model import Relationship
from semantic_analyzer.ai.complete_relationship_attributes import complete_relationship_attributes
from semantic_analyzer.ai.interpret_relationship import interpret_relationship


class AIRelationshipInterpreter:
    
    @staticmethod
    def execute(classes: List[Class], relationships: List[Relationship]) -> Tuple[List[Class], List[Dict]]:

        for relationship in relationships:
            source_class = next(
                (cls for cls in classes if cls.name == relationship.source_name), None)
            target_class = next(
                (cls for cls in classes if cls.name == relationship.target_name), None)

            print(f"{relationship.name} : {relationship.source_name} -> {target_class}")
            if not source_class or not target_class:
                continue
            
            # On commence par completer les informations de la relation
            full_relationship = complete_relationship_attributes(asdict(source_class), asdict(target_class), asdict(relationship))
            relationships[relationships.index(relationship)] = full_relationship
            # On passe à present à l'interpretation de la relation
            source_class_updated, target_class_updated = interpret_relationship(asdict(source_class), asdict(target_class), full_relationship)


            # Mettre à jour les classes avec les nouvelles informations
            classes[classes.index(source_class)] = Class.from_dict(source_class_updated)
            classes[classes.index(target_class)] = Class.from_dict(target_class_updated)

        return classes, relationships
