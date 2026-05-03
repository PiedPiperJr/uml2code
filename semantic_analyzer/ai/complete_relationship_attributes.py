import json
from typing import Dict, Any, Optional, Tuple
from enum import Enum
import logging
from openai import OpenAI

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def complete_relationship_attributes(class1: Dict[str, Any], class2: Dict[str, Any], 
                          partial_relationship: Dict[str, Any]) -> Dict[str, Any]:
    """
    Complète une relation UML entre deux classes en utilisant un LLM.
    
    Args:
        class1: Premier objet classe au format dictionnaire
        class2: Second objet classe au format dictionnaire
        partial_relationship: Relation partielle au format dictionnaire
        
    Returns:
        Dict[str, Any]: Relation complétée au format JSON
    """
    # Initialiser le client OpenAI pour OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    
    # Construire le prompt pour le LLM
    prompt = f"""
    Tu es un expert en UML et en modélisation de données. Ton travail est d'analyser deux classes et une relation partielle 
    pour compléter tous les attributs manquants dans la relation en utilisant la logique et les connaissances d'UML.
    
    Voici les deux classes:
    
    CLASSE 1:
    {json.dumps(class1, indent=2)}
    
    CLASSE 2:
    {json.dumps(class2, indent=2)}
    
    Voici la relation partielle entre ces classes:
    {json.dumps(partial_relationship, indent=2)}
    
    Complète tous les attributs manquants ou marqués comme Optional dans la relation selon cette structure:
    ```
    class Relationship:
        name: str
        source: str
        target: str
        _type: RelationshipType  # conserve la valeur existante
        source_name: str
        target_name: str
        source_role: Optional[str] # à completer si absente avec une valeur sans espace
        target_role: Optional[str] # à completer si absente avec une valeur sans espace
        source_multiplicity: Optional[Tuple[int, int]]  # Tuple comme [min, max], par exemple [0, 1], [1, 1], [0, n], etc.
        target_multiplicity: Optional[Tuple[int, int]]
        is_navigable_to_source: bool
        is_navigable_to_target: bool
    ```
    
    Analyse les attributs des classes, leurs relations et leurs géométries pour déduire les valeurs manquantes.
    Ta réponse doit être un objet JSON valide et complet respectant exactement la structure ci-dessus. 
    N'ajoute aucun texte explicatif, seul le JSON est attendu.
    """

    logging.info("Envoi de la requête au LLM...")
    
    try:
        completion = client.chat.completions.create(
            model="mistralai/devstral-small:free",
            messages=[
                {"role": "system", "content": "Tu es un expert en UML et modélisation de données qui analyse et complète des relations entre classes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Réduire la température pour obtenir des réponses plus déterministes
        )
        
        response_text = completion.choices[0].message.content.strip()
        logging.info("Réponse reçue du LLM")
        
        # Tenter d'extraire le JSON de la réponse (au cas où il y aurait du texte autour)
        try:
            # Vérifier si la réponse est entourée de délimiteurs de code
            if "```json" in response_text or "```" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    response_text = response_text[json_start:json_end]
            
            completed_relationship = json.loads(response_text)
            
            # Vérifier que tous les champs requis sont présents
            required_fields = ["name", "source", "target", "_type", "source_name", "target_name", 
                               "source_role", "target_role", "source_multiplicity", "target_multiplicity", 
                               "is_navigable_to_source", "is_navigable_to_target"]
            
            for field in required_fields:
                if field not in completed_relationship:
                    raise ValueError(f"Champ manquant dans la réponse: {field}")
            
            # Conserver le type de relation d'origine s'il existe
            if "_type" in partial_relationship:
                completed_relationship["_type"] = partial_relationship["_type"]
                
            logging.info("Relation complétée avec succès")
            return completed_relationship
            
        except json.JSONDecodeError as e:
            logging.error(f"Erreur lors du décodage du JSON: {e}")
            logging.error(f"Réponse brute: {response_text}")
            # En cas d'erreur, on essaie une deuxième fois en demandant explicitement un JSON valide
            return retry_with_explicit_json(client, class1, class2, partial_relationship)
            
    except Exception as e:
        logging.error(f"Erreur lors de l'appel au LLM: {e}")
        raise

def retry_with_explicit_json(client, class1, class2, partial_relationship):
    """Fonction de secours pour réessayer avec une demande explicite de JSON"""
    logging.info("Tentative de récupération avec une demande explicite de JSON...")
    
    retry_prompt = f"""
    Je n'ai pas pu parser ta dernière réponse comme un JSON valide.
    
    Analyse ces deux classes et la relation partielle:
    
    CLASSE 1: {json.dumps(class1)}
    CLASSE 2: {json.dumps(class2)}
    RELATION: {json.dumps(partial_relationship)}
    
    Retourne UNIQUEMENT un objet JSON avec cette structure exacte, sans aucun texte explicatif:
    {{
        "name": string,
        "source": string,
        "target": string,
        "_type": string (conserver la valeur existante),
        "source_name": string,
        "target_name": string,
        "source_role": string, (non nulle et sans espace)
        "target_role": string, (non nulle et sans espace)
        "source_multiplicity": [int, int], (non nulle et sans espace)
        "target_multiplicity": [int, int], (non nulle et sans espace)
        "is_navigable_to_source": boolean,
        "is_navigable_to_target": boolean
    }}
    """
    
    completion = client.chat.completions.create(
        model="mistralai/devstral-small:free",
        messages=[
            {"role": "system", "content": "Tu es un expert en UML qui génère des réponses en JSON pur."},
            {"role": "user", "content": retry_prompt}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}  # Forcer un format de réponse JSON
    )
    
    response_text = completion.choices[0].message.content.strip()
    
    try:
        completed_relationship = json.loads(response_text)
        logging.info("Récupération réussie")
        return completed_relationship
    except json.JSONDecodeError as e:
        logging.error(f"Échec de la récupération: {e}")
        raise ValueError(f"Impossible d'obtenir une réponse JSON valide: {e}")
