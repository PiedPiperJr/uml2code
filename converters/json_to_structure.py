from typing import Dict, List, Tuple
from utils.validators import is_class, is_relation, is_attribute, is_method
from utils.parsers import parse_attribute_value, parse_method_value, interpret_visibility
from models.relationship_model import RelationshipType


def find_root_ids(json_data: List[Dict]) -> Tuple[str, str]:
    """Trouve les IDs root et sub_root"""
    root_id = next((cell["@id"] for cell in json_data if len(cell.keys()) == 1), None)
    sub_root_id = next((cell["@id"] for cell in json_data 
                       if len(cell.keys()) == 2 and cell.get("@parent") == root_id), None)
    return root_id, sub_root_id

def create_class_structure(mxcell: Dict) -> Dict:
    return {
        "name": mxcell.get("@value"),
        "type": "class",
        "attributes": [],
        "methods": []
    }

def create_relationship_structure(mxcell: Dict) -> Dict:
    return {
        "name": mxcell.get("@value"),
        "source": mxcell.get("@source"),
        "target": mxcell.get("@target"),
        "edge": mxcell.get("@edge"),
        "style": mxcell.get("@style"),
        "type": "",
        "multiplicity": ""
    }

def fix_relationship_attribs(relationship: Dict, initial_json_data: List[Dict]) -> None:
    # fix bad source and target in relationships 
    for mxcell in initial_json_data:
        parent = mxcell.get('@parent')
        if relationship['source'].lower() == mxcell.get('@id'):
            relationship['source'] = parent if not parent is None else relationship['source']

        if relationship['target'].lower() == mxcell.get('@id'):
            relationship['target'] = parent if not parent is None else relationship['target']

def convert_json_to_structure(initial_json_data: List[Dict]) -> Dict:
    """Convertit le JSON initial en structure hiérarchique"""
    structured_data = {"classes": {}, "relationships": []}
    root_id, sub_root_id = find_root_ids(initial_json_data)
    
    # Premier passage : classes et relations
    remaining_cells = []
    for mxcell in initial_json_data:
        if mxcell.get("@id") in [root_id, sub_root_id]:
            continue
            
        if is_class(mxcell, sub_root_id):
            structured_data["classes"][mxcell.get("@id")] = create_class_structure(mxcell)
        elif is_relation(mxcell, sub_root_id):
            relationship = create_relationship_structure(mxcell)
            fix_relationship_attribs(relationship, initial_json_data)
            structured_data["relationships"].append(relationship)
        else:
            remaining_cells.append(mxcell)
    
    # Deuxième passage : attributs et méthodes
    for mxcell in remaining_cells:
        parent_id = mxcell.get("@parent")
        if parent_id not in structured_data["classes"]:
            continue
            
        if is_method(mxcell, sub_root_id):
            visibility, name, type_, _args = parse_method_value(mxcell.get("@value", ""))
            args = []
            for arg in _args:
                values = arg.strip().split()
                if len(values) >= 2:
                    args.append({'type':values[0], 'name':values[1]})
                else:
                    args.append({'type':'Object', 'name':values[0]})

            structured_data["classes"][parent_id]["methods"].append({
                "visibility": interpret_visibility(visibility),
                "name": name.strip(),
                "type": type_.strip(),
                "args": args
            })

        elif is_attribute(mxcell, sub_root_id):
            visibility, name, type_ = parse_attribute_value(mxcell.get("@value", ""))
            structured_data["classes"][parent_id]["attributes"].append({
                "visibility": interpret_visibility(visibility),
                "name": name.strip(),
                "type": type_.strip()
            })
    
    return structured_data


def interpret_relationships(interpreted_data, relationships):
    _interpreted_data = interpreted_data
    for class_data in _interpreted_data:
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

    return _interpreted_data