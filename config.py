import os

# Type checker AI
GEMINI_API_KEY = ""

# Chemins de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
GENERATED_APP_DIR = os.path.join(BASE_DIR, "api\data")
GENERATED_APP_PATH = os.path.join(GENERATED_APP_DIR,"demo.zip")
UNZIP_DIR = os.path.join(GENERATED_APP_DIR,'demo')
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES_JAVA_DIR = os.path.join(TEMPLATES_DIR,"java")
# Chemins des fichiers
XML_FILE_PATH = os.path.join(DATA_DIR, "class-diagram-example.drawio")
INITIAL_JSON_FILE_PATH = os.path.join(DATA_DIR, "json_files", "[0] - initial_diagram.json")
STRUCTURED_JSON_FILE_PATH = os.path.join(DATA_DIR, "json_files", "[1] - structured_diagram.json")
INTERPRETED_JSON_FILE_PATH = os.path.join(DATA_DIR, "json_files", "[2] - interpreted_diagram.json")
APP_FOLDER = os.path.join(DATA_DIR, "generated_app")

# Templates
SIMPLE_JAVA_CLASS_TEMPLATE = os.path.join(TEMPLATES_DIR, "java", "simple_class.html")