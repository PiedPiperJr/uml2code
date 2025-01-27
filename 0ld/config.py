import os

# Type checker AI
GEMINI_API_KEY = "AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8"

# Chemins de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Chemins des fichiers
XML_FILE_PATH = os.path.join(DATA_DIR, "class-diagram-example.drawio")
USECASE_EXAMPLE_FILE_PATH = os.path.join(DATA_DIR, "use_case_example.md")
INITIAL_JSON_FILE_PATH = os.path.join(
    DATA_DIR, "json_files", "[0] - initial_diagram.json")
STRUCTURED_JSON_FILE_PATH = os.path.join(
    DATA_DIR, "json_files", "[1] - structured_diagram.json")
INTERPRETED_JSON_FILE_PATH = os.path.join(
    DATA_DIR, "json_files", "[2] - interpreted_diagram.json")
USECASES_JSON_FILE_PATH = os.path.join(
    DATA_DIR, "json_files", "[3] - interpreted_usecases.json")
PROJECT_JSON_FILE_PATH = os.path.join(
    DATA_DIR, "json_files", "[4] - project.json")
APP_FOLDER = os.path.join(DATA_DIR, "generated_app")
CLEAN_APP_FOLDER = os.path.join(DATA_DIR, "clean_app")

# Templates
SIMPLE_JAVA_CLASS_TEMPLATE = os.path.join(
    TEMPLATES_DIR, "java", "simple_class.html")
CLEAN_JAVA_APP_TEMPLATE = os.path.join(TEMPLATES_DIR, "java-clean")


USECASE_PATTERN = """

use_cases:
  - name: "Le titre du cas d'utilisation"
    actors:
      - "Acteur 1"
      - "Acteur 2"
    preconditions:
      - "L'administrateur doit être authentifié."
    postconditions:
      - "Les informations de l'utilisateur sont mises à jour."
    scenarios:
      principal:
        - "L'administrateur recherche un utilisateur."
        - "L'administrateur modifie les informations de l'utilisateur."
        - "Le système enregistre les modifications."
      alternatif:
        - "L'administrateur tente de supprimer un utilisateur administrateur."
        - "Le système refuse la demande."
  - name: "Gestion des contenus"
    actors:
      - "Auteur"
      - "Éditeur"
      - "Lecteur"
    preconditions:
      - "L'auteur doit être connecté."
    postconditions:
      - "Le contenu est publié et accessible aux lecteurs."
    scenarios:
      principal:
        - "L'auteur crée un nouveau contenu."
        - "L'éditeur valide le contenu."
        - "Le contenu est publié."
      alternatif:
        - "L'auteur soumet un contenu de mauvaise qualité."
        - "Le contenu est rejeté par l'éditeur."

"""
