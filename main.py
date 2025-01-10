<<<<<<< HEAD
from config import *
from utils.validators import validate_data_types
from converters.xml_to_json import convert_xml_to_json
from converters.structure_to_code import write_java_files
from injectors.relationship_injector import inject_relationships
from converters.json_to_structure import convert_json_to_structure
from extractors.relationship_extractor import extract_relationships

def main():
    # Lecture du fichier XML
    with open(XML_FILE_PATH, "r") as xml_file:
        xml_data = xml_file.read()
    
    # Étape 1: Conversion XML vers JSON
    initial_json_data = convert_xml_to_json(xml_data)
    
    # Étape 2: Structuration du JSON
    structured_data = convert_json_to_structure(initial_json_data)
    
    # Step 3: Extract relationships between classes (at now, only heritage is fully managed)
    relationships = extract_relationships(structured_data)
    
    # Étape 4: Code generation
    interpreted_data = list(structured_data["classes"].values())
    # Step 4.5: We check with google gemini if datatypes are good for the given language
    validate_data_types(interpreted_data, GEMINI_API_KEY)

    # Step 6: Adding relationships to interpreted datas
    inject_relationships(interpreted_data, relationships)

    # Étape 5: Génération du code
    write_java_files(interpreted_data, SIMPLE_JAVA_CLASS_TEMPLATE, APP_FOLDER)

if __name__ == "__main__":
=======
import json
from config import *
from utils.validators import validate_data_types
from converters.xml_to_json import convert_xml_to_json
from converters.structure_to_code import write_java_files
from converters.json_to_structure import convert_json_to_structure
from extractors.relationship_extractor import extract_relationships
from models.relationship_model import RelationshipType

def main():
    # Lecture du fichier XML
    with open(XML_FILE_PATH, "r") as xml_file:
        xml_data = xml_file.read()
    
    # Étape 1: Conversion XML vers JSON
    initial_json_data = convert_xml_to_json(xml_data)
    with open(INITIAL_JSON_FILE_PATH, 'w') as f:
        json.dump(initial_json_data, f, indent=4)
    
    # Étape 2: Structuration du JSON
    structured_data = convert_json_to_structure(initial_json_data)
    with open(STRUCTURED_JSON_FILE_PATH, 'w') as f:
        json.dump(structured_data, f, indent=4)
    
    # Step 3: Extract relationships between classes (at now, only heritage is fully managed)
    relationships = extract_relationships(structured_data)
    
    # Étape 4: Code generation
    interpreted_data = list(structured_data["classes"].values())
    # Step 4.5: We check with google gemini if datatypes are good for the given language
    # validate_data_types(interpreted_data, GEMINI_API_KEY)
    # dump. . .
    with open(INTERPRETED_JSON_FILE_PATH, 'w') as f:
        json.dump(interpreted_data, f, indent=4)

    # Step 6: Adding relationships to interpreted datas
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

    # Étape 5: Génération du code
    write_java_files(interpreted_data, SIMPLE_JAVA_CLASS_TEMPLATE, APP_FOLDER)

if __name__ == "__main__":
>>>>>>> d598bcdb5763c0553a737c71d46b5b100a15560d
    main()