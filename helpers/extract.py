import zipfile
import os

def unzip_file(zip_path, extract_to):
    """
    Dézipper le projet spring dans le dossier data.
    
    :param zip_path: Chemin vers le projet ZIP.
    :param extract_to: Dossier où extraire les fichiers.
    """
    # Vérifier si le fichier ZIP existe
    if not os.path.exists(zip_path):
        print("none")
        return 

    # Créer le dossier cible s'il n'existe pas
    os.makedirs(extract_to, exist_ok=True)

    # Extraire le contenu du fichier ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

