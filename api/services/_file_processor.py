import os
import shutil
import zipfile
from helpers.extract import *
from utils.validators import validate_data_types
from converters.xml_to_json import convert_xml_to_json
from converters.structure_to_code import write_java_files
from config import SIMPLE_JAVA_CLASS_TEMPLATE, GEMINI_API_KEY
from injectors.relationship_injector import inject_relationships
from converters.json_to_structure import convert_json_to_structure
from extractors.relationship_extractor import extract_relationships


def process_file(file_path: str, artifact_name: str, gen_path: str):
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

    zip_path = "api/data/generated_app/projet.zip" #remplacer projet.zip par le nom_du_projet_zippe.zip
    extract_to = "api/data/generated_app/projet" #remplacer projet par le nom_du_projet_zippe

    # Generate Java files

    # creation du projet spring boot, 

    # dezipper le projet, 
    unzip_file(zip_path, extract_to)
    # parcourir le projet jusqu'à l'artifact, 
    base_path=extract_to + "/src/main/java/" + artifact_name
    # puis generer les domaines, infrastructures, presentation
    output_folder = os.path.join(artifact_name, "java_files")
    os.makedirs(output_folder, exist_ok=True)
    
    write_java_files(interpreted_data, SIMPLE_JAVA_CLASS_TEMPLATE, output_folder)

    # create a zip file of generated java files
    zip_name =  f"{os.path.join(artifact_name, '..', gen_path)}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zfp:
        for root, dirs, files in os.walk(output_folder):
            for  file in files:
                zfp.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(output_folder, '..')))

    shutil.rmtree(artifact_name)
    return zip_name
