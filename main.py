from config import *
from utils.validators import validate_data_types
from utils.utils import dump
from converters.xml_to_json import convert_xml_to_json
from code_generators.java_pojo import write_java_files
from code_generators.java_clean import generate_clean_project
from converters.json_to_structure import convert_json_to_structure, interpret_relationships
from extractors.relationship_extractor import extract_relationships
from models.relationship_model import RelationshipType
from models.project_model import Project


def main(xml_data=None, enable_type_validation=False):
    # Lecture du fichier XML
    if xml_data is None:
        with open(XML_FILE_PATH, "r") as xml_file:
            xml_data = xml_file.read()

    # Étape 1: Conversion XML vers JSON
    initial_json_data = convert_xml_to_json(xml_data)
    dump(INITIAL_JSON_FILE_PATH, initial_json_data)

    # Étape 2: Structuration du JSON
    structured_data = convert_json_to_structure(initial_json_data)
    dump(STRUCTURED_JSON_FILE_PATH, structured_data)

    # Step 3: Extract relationships between classes (at now, only inheritance is fully managed)
    relationships = extract_relationships(structured_data)

    # Étape 4: Interprete relationships
    classes = list(structured_data["classes"].values())
    interpreted_data = interpret_relationships(classes, relationships)

    # Step 5: We check with google gemini if datatypes are good for the given language
    if enable_type_validation:
        validate_data_types(interpreted_data, GEMINI_API_KEY)

    dump(INTERPRETED_JSON_FILE_PATH, interpreted_data)

    project: Project = Project("org.enspy.4gi", interpreted_data, [])

    generate_clean_project(project, CLEAN_JAVA_APP_TEMPLATE, CLEAN_APP_FOLDER)

    # Étape 6: Code Generation
    # write_java_files(interpreted_data, SIMPLE_JAVA_CLASS_TEMPLATE, CLEAN_APP_FOLDER)


if __name__ == "__main__":
    main()
