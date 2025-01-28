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
      - "postconditionLes informations de l'utilisateur sont mises à jour."
    scenarios:
      principal:
        - "L'administrateur recherche un utilisateur."
        - "L'administrateur modifie les informations de l'utilisateur."
        - "Le système enregistre les modifications."
      alternatif:
        - "L'administrateur tente de supprimer un utilisateur administrateur."
        - "Le système refuse la demande."
        
    extends:
      name: "Titre du cas d'utilisation B, de la liste, qui est une option de A (qui étend A)"
      name: "Titre du cas d'utilisation C, de la liste, qui est une option de A (qui étend A)"
      ...
      
    include:
      name: "Titre du cas d'utilisation D, de la liste, qui est une sous-partie de A"
      name: "Titre du cas d'utilisation E, de la liste, qui est une sous-partie de A"
      ...

    dto:
      name: "NomDuDto"
      attributes:
        attribute:
          name: "nomAttribut"
          visibility: "public|private|protected"
          type: "typeAttribut"
          decorators:
            -decorator:
              name: "nomDecorateur"
              message: "messageDecorateur"
        attribute:
          name: "autreAttribut"
          visibility: "public|private|protected"
          type: "typeAttribut"
          decorators:
            decorator:
              name: "nomDecorateur"
              message: "messageDecorateur"
        ...
      name: "AutreDto"
      attributes:
        attribute:
          name: "nomAttribut"
          visibility: "public|private|protected"
          type: "typeAttribut"
          decorators:
            decorator:
              name: "nomDecorateur"
              message: "messageDecorateur"
        attribute:
          name: "autreAttribut"
          visibility: "public|private|protected"
          type: "typeAttribut"
          decorators:
            -decorator:
              name: "nomDecorateur"
              message: "messageDecorateur"
        ...
      ...
    resource:
      name: "ResourceName"
      attributes:
        name: "NomAttribut"
        visibility: "public|private|protected"
        type: "attributType"
              
        name: "autreAttribut"
        visibility: "public|private|protected"
        type: "attributType"
        ...
    services:

      name: "ServiceName"
      methods:

        name: "methodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
          
        name: "autreMethodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
        ...
      
      name: "autreNomService"
      methods:

        name: "methodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
          
        name: "autreMethodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
        ...

    repositories:

      entity: "NomEntité"
      methods:

        name: "methodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
          
      entity: "AutreNomEntité"
      methods:

        name: "methodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
  
  - name: "Le titre d'un autre cas d'utilisation"
    actors:
      - "Acteur 3"
      - "Acteur 4"
    preconditions:
      - "L'administrateur doit être authentifié."
    postconditions:
      - "postconditionLes informations de l'utilisateur sont mises à jour."
    scenarios:
      principal:
        - "L'administrateur recherche un utilisateur."
        - "L'administrateur modifie les informations de l'utilisateur."
        - "Le système enregistre les modifications."
      alternatif:
        - "L'administrateur tente de supprimer un utilisateur administrateur."
        - "Le système refuse la demande."
        
    extends:
      name: "Titre du cas d'utilisation B, de la liste, qui est une option de A (qui étend A)"
      name: "Titre du cas d'utilisation C, de la liste, qui est une option de A (qui étend A)"
      ...
      
    include:
      name: "Titre du cas d'utilisation D, de la liste, qui est une sous-partie de A"
      name: "Titre du cas d'utilisation E, de la liste, qui est une sous-partie de A"
      ...

    dto:
      name: "NomDuDto"
      attributes:
        attribute:
          name: "nomAttribut"
          visibility: "public|private|protected"
          type: "typeAttribut"
          decorators:
            -decorator:
              name: "nomDecorateur"
              message: "messageDecorateur"
        attribute:
          name: "autreAttribut"
          visibility: "public|private|protected"
          type: "typeAttribut"
          decorators:
            decorator:
              name: "nomDecorateur"
              message: "messageDecorateur"
        ...
      name: "AutreDto"
      attributes:
        attribute:
          name: "nomAttribut"
          visibility: "public|private|protected"
          type: "typeAttribut"
          decorators:
            decorator:
              name: "nomDecorateur"
              message: "messageDecorateur"
        attribute:
          name: "autreAttribut"
          visibility: "public|private|protected"
          type: "typeAttribut"
          decorators:
            -decorator:
              name: "nomDecorateur"
              message: "messageDecorateur"
        ...
      ...
    resource:
      name: "ResourceName"
      attributes:
        name: "NomAttribut"
        visibility: "public|private|protected"
        type: "attributType"
              
        name: "autreAttribut"
        visibility: "public|private|protected"
        type: "attributType"
        ...
    services:

      name: "ServiceName"
      methods:

        name: "methodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
          
        name: "autreMethodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
        ...
      
      name: "autreNomService"
      methods:

        name: "methodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
          
        name: "autreMethodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
        ...

    repositories:

      entity: "NomEntité"
      methods:

        name: "methodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
          
      entity: "AutreNomEntité"
      methods:

        name: "methodName"
        visibility: "public|private|protected"
        type: "returnType"
        args:

          name: "argName"
          visibility: "public|private|protected"
          type: "argType"
  ...

"""