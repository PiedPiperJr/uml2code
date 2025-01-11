from config import *
from typing import Dict
from models.relationship_model import RelationshipType


def inject_relationships(interpreted_data: Dict, relationships: Dict) -> None:
    for class_data in interpreted_data:
        list_used: bool = False
        class_data['aggregations'] = []
        class_data['compositions'] = []

        for relationship in relationships:
            if class_data['type'] == "class" and class_data['name'].lower() == relationship.source_name.lower():
                match(relationship._type):
                    case RelationshipType.INHERITANCE:
                        class_data['parent'] = relationship.target_name

                    case RelationshipType.AGGREGATION:
                        class_data['aggregations'].append({'visibility':'private', 
                                                        'type':relationship.target_name.capitalize(),
                                                        'name':relationship.target_name.lower() + 's'})

                    case RelationshipType.COMPOSITION:
                        class_data['compositions'].append({'visibility':'private', 
                                                        'type':relationship.target_name.capitalize(),
                                                        'name':relationship.target_name.lower() + 's'})
                    
                    case RelationshipType.ATTRIBUTE:
                        class_data['attributes'].append({'visibility':'private', 
                                                        'type':relationship.target_name.capitalize(),
                                                        'name':relationship.target_name.lower()})

                    case RelationshipType.NONE:
                        pass

                list_used = True

        if list_used:
            class_data['import_list'] = True