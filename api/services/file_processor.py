import os
import shutil
import zipfile
from utils.validators import validate_data_types
from converters.xml_to_json import convert_xml_to_json
from converters.structure_to_code import write_java_files
from config import SIMPLE_JAVA_CLASS_TEMPLATE, GEMINI_API_KEY
from injectors.relationship_injector import inject_relationships
from converters.json_to_structure import convert_json_to_structure
from extractors.relationship_extractor import extract_relationships


def process_file(file_path: str, tmp_path: str, gen_path: str):
    # Read the .drawio
    with open(file_path, "r") as xml_file:
        xml_data = xml_file.read()

    # Conversion XML to JSON
    initial_json_data = convert_xml_to_json(xml_data)

    # JSON Structuring
    structured_data = convert_json_to_structure(initial_json_data)

    # Extract relationships
    relationships = extract_relationships(structured_data)

    # Interpret data for code generation
    interpreted_data = list(structured_data["classes"].values())

    # Validate data types
    # validate_data_types(interpreted_data, GEMINI_API_KEY)

    # Inject relationships
    inject_relationships(interpreted_data, relationships)

    # Generate Java files
    output_folder = os.path.join(tmp_path, "java_files")
    os.makedirs(output_folder, exist_ok=True)
    write_java_files(interpreted_data, SIMPLE_JAVA_CLASS_TEMPLATE, output_folder)

    # create a zip file of generated java files
    zip_name =  f"{os.path.join(tmp_path, '..', gen_path)}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zfp:
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                zfp.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(output_folder, '..')))

    shutil.rmtree(tmp_path)
    return zip_name
