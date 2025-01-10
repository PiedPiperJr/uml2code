<<<<<<< HEAD
#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
from typing import Optional

from config import *
from converters.xml_to_json import convert_xml_to_json
from converters.json_to_structure import convert_json_to_structure
from converters.structure_to_code import write_java_files
from extractors.relationship_extractor import extract_relationships
from injectors.relationship_injector import inject_relationships
from utils.validators import validate_data_types

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert UML class diagrams to Java code",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input .drawio file"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="./generated",
        help="Output directory for generated files"
    )
    
    parser.add_argument(
        "--intermediate-dir",
        type=str,
        default="./temp",
        help="Directory for intermediate JSON files"
    )
    
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep intermediate JSON files"
    )
    
    return parser

def process_diagram(input_file: str, output_dir: str, temp_dir: str) -> Optional[str]:
    try:
        # Création des dossiers nécessaires
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        
        # Setup des chemins
        initial_json = Path(temp_dir) / "initial.json"
        structured_json = Path(temp_dir) / "structured.json"
        interpreted_json = Path(temp_dir) / "interpreted.json"
            
        # Lecture du fichier XML
        with open(input_file, "r") as xml_file:
            xml_data = xml_file.read()
        
        # Étape 1: Conversion XML vers JSON
        initial_json_data = convert_xml_to_json(xml_data)
        with open(initial_json, 'w') as f:
            json.dump(initial_json_data, f, indent=4)
        
        # Étape 2: Structuration du JSON
        structured_data = convert_json_to_structure(initial_json_data)
        with open(structured_json, 'w') as f:
            json.dump(structured_data, f, indent=4)
        
        # Step 3: Extract relationships between classes (at now, only heritage is fully managed)
        relationships = extract_relationships(structured_data)
        
        # Étape 4: Code generation
        interpreted_data = list(structured_data["classes"].values())
        # Step 4.5: We check with google gemini if datatypes are good for the given language
        validate_data_types(interpreted_data, GEMINI_API_KEY)
        # dump. . .
        with open(interpreted_json, 'w') as f:
            json.dump(interpreted_data, f, indent=4)

        # Step 6: Adding relationships to interpreted datas
        inject_relationships(interpreted_data, relationships)

        # Étape 5: Génération du code
        write_java_files(interpreted_data, SIMPLE_JAVA_CLASS_TEMPLATE, output_dir)
        
        return output_dir
        
    except Exception as e:
        return f"Error: {str(e)}"

def cleanup(temp_dir: str):
    """Supprime les fichiers temporaires"""
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

def main():
    parser = setup_parser()
    args = parser.parse_args()
    
    result = process_diagram(
        input_file=args.input_file,
        output_dir=args.output,
        temp_dir=args.intermediate_dir
    )
    
    if isinstance(result, str) and result.startswith("Error"):
        print(result)
        return 1
    
    print(f"Java files generated successfully in: {result}")
    
    if not args.keep_temp:
        cleanup(args.intermediate_dir)
    
    return 0

if __name__ == "__main__":
=======
#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
from typing import Optional

from config import *
from converters.xml_to_json import convert_xml_to_json
from converters.json_to_structure import convert_json_to_structure
from converters.structure_to_code import write_java_files

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert UML class diagrams to Java code",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input .drawio file"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="./generated",
        help="Output directory for generated files"
    )
    
    parser.add_argument(
        "--intermediate-dir",
        type=str,
        default="./temp",
        help="Directory for intermediate JSON files"
    )
    
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep intermediate JSON files"
    )
    
    return parser

def process_diagram(input_file: str, output_dir: str, temp_dir: str) -> Optional[str]:
    try:
        # Création des dossiers nécessaires
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        
        # Setup des chemins
        initial_json = Path(temp_dir) / "initial.json"
        structured_json = Path(temp_dir) / "structured.json"
        interpreted_json = Path(temp_dir) / "interpreted.json"
        
        # Lecture et conversion
        with open(input_file, "r") as xml_file:
            xml_data = xml_file.read()
        
        # Étape 1: XML → JSON
        initial_json_data = convert_xml_to_json(xml_data)
        with open(initial_json, 'w') as f:
            json.dump(initial_json_data, f, indent=4)
        
        # Étape 2: JSON → Structure
        structured_data = convert_json_to_structure(initial_json_data)
        with open(structured_json, 'w') as f:
            json.dump(structured_data, f, indent=4)
        
        # Étape 3: Interprétation
        interpreted_data = list(structured_data["classes"].values())
        with open(interpreted_json, 'w') as f:
            json.dump(interpreted_data, f, indent=4)
        
        # Étape 4: Génération Java
        write_java_files(interpreted_data, SIMPLE_JAVA_CLASS_TEMPLATE, output_dir)
        
        return output_dir
        
    except Exception as e:
        return f"Error: {str(e)}"

def cleanup(temp_dir: str):
    """Supprime les fichiers temporaires"""
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

def main():
    parser = setup_parser()
    args = parser.parse_args()
    
    result = process_diagram(
        input_file=args.input_file,
        output_dir=args.output,
        temp_dir=args.intermediate_dir
    )
    
    if isinstance(result, str) and result.startswith("Error"):
        print(result)
        return 1
    
    print(f"Java files generated successfully in: {result}")
    
    if not args.keep_temp:
        cleanup(args.intermediate_dir)
    
    return 0

if __name__ == "__main__":
>>>>>>> d598bcdb5763c0553a737c71d46b5b100a15560d
    exit(main())