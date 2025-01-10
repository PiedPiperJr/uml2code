#parcourir le projet spring boot et generer les classes suivants la D
import os
from config import TEMPLATES_DIR
from converters.structure_to_code import *

def to_camel_case(name):
    """
    Convertit un nom de fichier ou de dossier en CamelCase.
    
    :param name: Nom à convertir.
    :return: Nom en CamelCase.
    """
    # Supprime l'extension pour manipuler uniquement le nom de base
    base_name, ext = os.path.splitext(name)
    # Convertit en CamelCase
    camel_case_name = ''.join(word.capitalize() for word in base_name.split('_'))
    # Ajoute l'extension si présente
    return camel_case_name + ext

def recreate_folders_and_files(source_dir, destination_dir, interpreted_data):
    """
    .

    :param source_dir: Dossier source à parcourir.
    :param destination_dir: Dossier où recréer la structure.
    """
    if not os.path.exists(source_dir):
        print(f"Le dossier source '{source_dir}' n'existe pas.")
        return

    for root, dirs, files in os.walk(source_dir):
        # Crée la structure relative des sous-dossiers
        relative_path = os.path.relpath(root, source_dir)
        destination_path = os.path.join(destination_dir, relative_path)
        os.makedirs(destination_path, exist_ok=True)

        # Crée les fichiers en CamelCase dans le dossier de destination
        for file_name in files:
            camel_case_name = to_camel_case(file_name)
            Template_path = os.path.join(TEMPLATES_DIR,relative_path)
            dest_path = os.path.join(destination_path,camel_case_name)
            write_java_files(interpreted_data,Template_path, dest_path)
            file_path = os.path.join(destination_path, camel_case_name)
            # Crée un fichier vide
            open(file_path, 'w').close()
            print(f"Fichier créé : {file_path}")

