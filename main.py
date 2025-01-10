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
    main()