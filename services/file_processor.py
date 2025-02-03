import os
import sys
import shutil
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List, Optional, Literal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "code_generator_service")))

from lexer.lexer import Lexer # type: ignore
from helpers.utils import Utils  # type: ignore
from models.class_model import Class  # type: ignore
from models.project_model import Project  # type: ignore
from semantic_analyzer.semantic_analyzer import SemanticAnalyzer  # type: ignore
from code_generator.clean.clean_code_generator import CleanCodeGenerator  # type: ignore


def process_file(diagram_path: str,
                 ouput_dir: str,
                 zip_name: str,
                 folder_to_zip: Optional[str] = None,
                 language: Optional[Literal['laravel', 'springboot']] = 'springboot',
                 package_name: Optional[str] = None) -> str:
    
    # load the diagram
    diagram = Path(diagram_path)

    # call the lexer
    lexer = Lexer(diagram.read_text("utf-8"))
    lexer_result = lexer.execute()
    
    # call the semantic analyzer
    semantic_analyzer = SemanticAnalyzer(lexer_result)
    classes = semantic_analyzer.execute()

    if language == 'springboot':
        if not package_name is None:
            return generate_springboot(classes, package_name, ouput_dir, zip_name, folder_to_zip)
        else:
            raise Exception("Package name is required for Spring Boot projects")
        
    elif language == 'laravel':
        return generate_laravel(classes, ouput_dir, zip_name)
    
    else:
        raise Exception(f"Unsupported language: {language}. Supported languages are 'laravel' and 'springboot'")


def generate_laravel(classes: List[Class], ouput_dir: str, zip_name: str, folder_to_zip: Optional[str] = None) -> str:
    class_data_file_path = os.path.join(ouput_dir, 'class_data.json')
    Utils.dump(class_data_file_path, [_class.to_dict() for _class in classes])
    
    folder_to_zip = ouput_dir if folder_to_zip is None else folder_to_zip
    zip_path = zip_folder(folder_to_zip, zip_name)
    os.remove(class_data_file_path)
    
    return zip_path


def generate_springboot(classes: List[Class], package_name: str, ouput_dir: str, zip_name: str, folder_to_zip: Optional[str] = None) -> str:
    project = Project(package_name, classes, [])
    template_path = os.path.join(os.getcwd(), 'services', "code_generator_service/templates/java-clean")
    clean_generator = CleanCodeGenerator(project, template_path, ouput_dir)
    clean_generator.execute()

    folder_to_zip = ouput_dir if folder_to_zip is None else folder_to_zip
    return zip_folder(folder_to_zip, zip_name)


def zip_folder(dir: str, zip_name: str) -> str:
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, zip_name+'.zip')
    
    base_path = os.path.abspath(dir)
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.make_archive(tmp_file.name, 'zip', base_path)
        shutil.move(f"{tmp_file.name}.zip", zip_path)
    
    return zip_path


def copy_tree(source_folder: str, destination_folder: str):
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        destination_item = os.path.join(destination_folder, item)
        
        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)  # Copy subdirectories
        else:
            shutil.copy2(source_item, destination_item)  # Copy files
            
            
def update_pomxl(path: str) -> None:
    # Load the existing pom.xml file
    tree = ET.parse(path)
    root = tree.getroot()

    # Define the new dependencies to be added
    new_dependencies = [
        {
            'groupId': 'com.fasterxml.jackson.datatype',
            'artifactId': 'jackson-datatype-jsr310',
            'version': '2.17.2'
        },
        {
            'groupId': 'org.springdoc',
            'artifactId': 'springdoc-openapi-starter-webmvc-ui',
            'version': '2.5.0'
        },
        {
            'groupId': 'com.fasterxml.jackson.core',
            'artifactId': 'jackson-core',
        }
    ]

    # Remove namespace prefixes from all elements
    def remove_namespace_prefix(element):
        # Remove the namespace prefix from the tag
        if '}' in element.tag:
            element.tag = element.tag.split('}', 1)[1]  # Strip namespace prefix
        # Remove namespace prefixes from child elements
        for child in element:
            remove_namespace_prefix(child)

    # Remove namespace prefixes from the root and all its children
    remove_namespace_prefix(root)

    # Find the <dependencies> tag
    dependencies = root.find('dependencies')

    if dependencies is None:
        raise ValueError("Could not find <dependencies> element in the XML file.")

    # Add the new dependencies to the <dependencies> section
    for dep in new_dependencies:
        dep_element = ET.SubElement(dependencies, 'dependency')

        group_id = ET.SubElement(dep_element, 'groupId')
        group_id.text = dep['groupId']

        artifact_id = ET.SubElement(dep_element, 'artifactId')
        artifact_id.text = dep['artifactId']

        if 'version' in dep:
            version = ET.SubElement(dep_element, 'version')
            version.text = dep['version']

    # Save the modified XML back to the pom.xml file without namespaces
    tree.write(path, encoding='UTF-8', xml_declaration=True)
    