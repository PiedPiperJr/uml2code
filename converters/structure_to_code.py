from typing import Dict, List
from jinja2 import Template
import os

def generate_java_code(class_data: Dict, template: Template) -> str:
    """Génère le code Java à partir des données de classe structurées"""
    return template.render(class_data=class_data)

def write_java_files(interpreted_data: List[Dict], template_path: str, output_dir: str):
    """Écrit les fichiers Java générés"""
    with open(template_path, 'r') as template_file:
        template = Template(template_file.read())
    
    os.makedirs(output_dir, exist_ok=True)
    
    for class_data in interpreted_data:
        java_code = generate_java_code(class_data, template)
        filename = f"{class_data['name'].capitalize()}.java"
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, 'w') as java_file:
            java_file.write(java_code)