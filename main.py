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
from converters.use_cases_converter import use_cases_to_json
import json

def main(usc = None, use_cases_data: str = None, xml_data: str = None,  enable_type_validation: bool = False):
    # Lecture du fichier XML
    if use_cases_data is None:
        with open(USECASE_EXAMPLE_FILE_PATH, "r") as file:
            use_cases_data = file.read()

    if xml_data is None:
        with open(XML_FILE_PATH, "r") as xml_file:
            xml_data = xml_file.read()

    # TODO remove usc in prod
    class_diagram_interpretation = class_diagram_interpreter(xml_data, False)
    if usc is None:
        use_case_interpretation = use_cases_to_json(use_cases_data)["useCases"]
        dump(USECASES_JSON_FILE_PATH, use_case_interpretation)
    else:
        use_case_interpretation = usc


    project: Project = Project(
        "org.enspy.4gi", class_diagram_interpretation, use_case_interpretation)
    
    dump(PROJECT_JSON_FILE_PATH, {
         "route": project.route, "classes": project.classes, "usecases": project.useCases})
    
    generate_clean_project(project, CLEAN_JAVA_APP_TEMPLATE, CLEAN_APP_FOLDER)
    # write_java_files(interpreted_data, SIMPLE_JAVA_CLASS_TEMPLATE, CLEAN_APP_FOLDER)


def class_diagram_interpreter(xml_data, enable_type_validation: bool = False):
    initial_json_data = convert_xml_to_json(xml_data)
    dump(INITIAL_JSON_FILE_PATH, initial_json_data)
    structured_data = convert_json_to_structure(initial_json_data)
    dump(STRUCTURED_JSON_FILE_PATH, structured_data)
    relationships = extract_relationships(structured_data)
    classes = list(structured_data["classes"].values())
    interpreted_data = interpret_relationships(classes, relationships)

    if enable_type_validation:
        validate_data_types(interpreted_data, GEMINI_API_KEY)

    dump(INTERPRETED_JSON_FILE_PATH, interpreted_data)

    return interpreted_data


if __name__ == "__main__":

    with open(USECASES_JSON_FILE_PATH, 'r') as f:
        usecase = json.loads(f.read())
    

    main(usc = usecase)
