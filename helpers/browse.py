import os
from jinja2 import Template
from config import TEMPLATES_JAVA_DIR
from converters.structure_to_code import generate_java_code
from typing import List, Dict


def to_camel_case(name: str) -> str:
    """
    Convert a file or folder name to CamelCase.

    :param name: Name to convert.
    :return: Name in CamelCase.
    """
    base_name, ext = os.path.splitext(name)
    camel_case_name = ''.join(word.capitalize() for word in base_name.split('_'))
    return camel_case_name + ext


def recreate_folders_and_generate_java_code(
    source_dir: str,
    destination_dir: str,
    interpreted_data: List[Dict]
):
    """
    Browse a source directory, recreate its structure in the destination,
    and generate Java code files using templates.

    :param source_dir: Source directory to browse.
    :param destination_dir: Destination directory to recreate structure and files.
    :param interpreted_data: Data to use for generating Java classes.
    """
    if not os.path.exists(source_dir):
        print(f"The source directory '{source_dir}' does not exist.")
        return

    for root, dirs, files in os.walk(source_dir):
        # Compute the relative path to preserve the structure
        relative_path = os.path.relpath(root, source_dir)
        destination_path = os.path.join(destination_dir, relative_path)
        os.makedirs(destination_path, exist_ok=True)

        # Process files in the current directory
        for file_name in files:
            # Convert to CamelCase for destination filenames

            # Locate the corresponding template
            template_path = os.path.join(TEMPLATES_JAVA_DIR, relative_path, file_name)
            if not os.path.exists(template_path):
                print(template_path)
                print(f"Template not found for {file_name}, skipping...")
                continue

            # Read the template and generate Java code
            with open(template_path, 'r') as template_file:
                template = Template(template_file.read())
            print(interpreted_data)
            for class_data in interpreted_data:
                java_code = generate_java_code(class_data, template)
                java_code = generate_java_code(class_data, template)
                # Destination path for the generated Java file
                camel_case_name = to_camel_case(f"{class_data['name'].capitalize()}.java")
                dest_path = os.path.join(destination_path, camel_case_name)

                # Write the generated Java code to the destination file
                with open(dest_path, 'w') as java_file:
                    java_file.write(java_code)
                    print(f"Generated Java file: {dest_path}")
