import os

# Chemins de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Chemins des fichiers
XML_FILE_PATH = os.path.join(DATA_DIR, "class-diagram-example.drawio")
INITIAL_JSON_FILE_PATH = os.path.join(DATA_DIR, "json_files", "[0] - initial_diagram.json")
STRUCTURED_JSON_FILE_PATH = os.path.join(DATA_DIR, "json_files", "[1] - structured_diagram.json")
INTERPRETED_JSON_FILE_PATH = os.path.join(DATA_DIR, "json_files", "[2] - interpreted_diagram.json")
APP_FOLDER = os.path.join(DATA_DIR, "generated_app")

# Templates
SIMPLE_JAVA_CLASS_TEMPLATE = os.path.join(TEMPLATES_DIR, "java", "simple_class.html")
