import os
from jinja2 import Template
from typing import Dict, List
from models.relationship_model import Relationship


def write_java_files(interpreted_data: List[Dict], template_path: str, output_dir: str):
    """Écrit les fichiers Java générés"""
    with open(template_path, 'r') as template_file:
        template = Template(template_file.read())
    
    os.makedirs(output_dir, exist_ok=True)
    
    for class_data in interpreted_data:
        java_code = template.render(class_data=class_data)
        filename = f"{class_data['name'].capitalize()}.java"
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, 'w') as java_file:
            java_file.write(java_code)