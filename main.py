import json
from config import *
from converters.xml_to_json import convert_xml_to_json
from converters.json_to_structure import convert_json_to_structure
from converters.structure_to_code import write_java_files

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
    
    # Étape 3: Pour l'instant, on passe directement à la génération
    interpreted_data = list(structured_data["classes"].values())
    with open(INTERPRETED_JSON_FILE_PATH, 'w') as f:
        json.dump(interpreted_data, f, indent=4)
    
    # Étape 4: Génération du code
    write_java_files(interpreted_data, SIMPLE_JAVA_CLASS_TEMPLATE, APP_FOLDER)

if __name__ == "__main__":
    main()