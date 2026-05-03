import json
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, field
import logging
from openai import OpenAI

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def interpret_relationship(source_class: Dict[str, Any], target_class: Dict[str, Any], 
                           relationship: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Interprète une relation UML entre deux classes en termes de relations de base de données
    et modifie les classes en conséquence.
    
    Args:
        source_class: Dictionnaire représentant la classe source
        target_class: Dictionnaire représentant la classe cible
        relationship: Dictionnaire représentant la relation entre les deux classes
        
    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: Les deux classes modifiées avec les relations interprétées
    """
    # Initialiser le client OpenAI pour OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    
    # Construire le prompt pour le LLM
    prompt = f"""
    En tant qu'expert en UML et en persistance de données JPA, interprète cette relation UML et détermine le type de relation de base de données approprié.

    CLASSE SOURCE:
    ```json
    {json.dumps(source_class, indent=2)}
    ```
    
    CLASSE CIBLE:
    ```json
    {json.dumps(target_class, indent=2)}
    ```
    
    RELATION:
    ```json
    {json.dumps(relationship, indent=2)}
    ```
    
    Analyse cette relation et détermine s'il s'agit d'une relation OneToOne, OneToMany, ManyToOne ou ManyToMany entre ces deux classes.
    Regarde attentivement:
    - Les multiplicités (source_multiplicity, target_multiplicity) si disponibles
    - La navigabilité (is_navigable_to_source, is_navigable_to_target) si disponible
    - Les rôles définis (source_role, target_role)
    
    Puis, renvoie un JSON structuré comme suit:
    
    ```json
    {{
      "relationship_type": "OneToOne|OneToMany|ManyToOne|ManyToMany",
      "source_class": {{
        "relationship_type": "OneToOne|OneToMany|ManyToOne|ManyToMany",
        "role": "Nom du champ pour accéder à la classe cible",
        "comodel": "Nom de la classe cible",
        "mapped_by_property": "Propriété qui mappe cette relation dans la classe cible (null si propriétaire ou unidirectionnelle)"
      }},
      "target_class": {{
        "relationship_type": "OneToOne|OneToMany|ManyToOne|ManyToMany",
        "role": "Nom du champ pour accéder à la classe source",
        "comodel": "Nom de la classe source",
        "mapped_by_property": "Propriété qui mappe cette relation dans la classe source (null si propriétaire ou unidirectionnelle)"
      }}
    }}
    ```
    
    Exemple de réponse pour une relation OneToMany bidirectionnelle entre Author et Book:
    ```json
    {{
      "relationship_type": "OneToMany_ManyToOne",
      "source_class": {{
        "relationship_type": "OneToMany",
        "role": "books",
        "comodel": "Book",
        "mapped_by_property": "author"
      }},
      "target_class": {{
        "relationship_type": "ManyToOne",
        "role": "author",
        "comodel": "Author",
        "mapped_by_property": null
      }}
    }}
    ```
    
    Réponds uniquement avec le JSON, sans aucun texte supplémentaire.
    """
    
    logging.info(f"Analyse de la relation entre {source_class.get('name')} et {target_class.get('name')}...")
    
    try:
        # Appel au LLM
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",  # Ou un autre modèle disponible
            messages=[
                {"role": "system", "content": "Tu es un expert en UML et en mapping objet-relationnel JPA qui analyse et interprète les relations entre classes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Basse température pour des résultats déterministes
            response_format={"type": "json_object"}  # Force le format JSON
        )
        
        response_text = completion.choices[0].message.content.strip()
        logging.info("Réponse du LLM reçue")
        
        # Traiter la réponse JSON
        try:
            interpretation = json.loads(response_text)
            
            # Vérifier la structure de la réponse
            required_fields = ["relationship_type", "source_class", "target_class"]
            required_nested = ["relationship_type", "role", "comodel", "mapped_by_property"]
            
            for field in required_fields:
                if field not in interpretation:
                    raise ValueError(f"Champ manquant dans l'interprétation: {field}")
            
            for nested in ["source_class", "target_class"]:
                for field in required_nested:
                    if field not in interpretation[nested]:
                        raise ValueError(f"Champ manquant dans {nested}: {field}")
                        
            # Mettre à jour les classes avec l'interprétation
            source_class_updated = update_class_with_relationship(source_class, interpretation["source_class"])
            target_class_updated = update_class_with_relationship(target_class, interpretation["target_class"])
            
            logging.info(f"Relation interprétée avec succès: {interpretation['relationship_type']}")
            return source_class_updated, target_class_updated
            
        except json.JSONDecodeError as e:
            logging.error(f"Erreur lors du décodage du JSON: {e}")
            logging.error(f"Réponse brute: {response_text}")
            # En cas d'erreur, on réessaie avec une demande plus explicite
            return retry_with_explicit_json(client, source_class, target_class, relationship)
            
    except Exception as e:
        logging.error(f"Erreur lors de l'appel au LLM: {e}")
        raise

def update_class_with_relationship(class_dict: Dict[str, Any], interpretation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Met à jour une classe avec l'interprétation de la relation.
    
    Args:
        class_dict: Dictionnaire représentant la classe
        interpretation: Interprétation de la relation pour cette classe
        
    Returns:
        Dict[str, Any]: La classe mise à jour
    """
    # Créer un objet InterpretedRelationShip à partir de l'interprétation
    relationship_obj = {
        "role": interpretation["role"],
        "comodel": interpretation["comodel"],
        "mapped_by_property": interpretation["mapped_by_property"]
    }
    
    # Initialiser les listes de relations si elles n'existent pas
    for rel_type in ["oneToOneRelationships", "oneToManyRelationships", 
                     "manyToOneRelationships", "manyToManyRelationships"]:
        if rel_type not in class_dict:
            class_dict[rel_type] = []
    
    # Déterminer le type de relation et ajouter l'objet à la liste appropriée
    rel_type = interpretation["relationship_type"]
    
    if rel_type == "OneToOne":
        class_dict["oneToOneRelationships"].append(relationship_obj)
    elif rel_type == "OneToMany":
        class_dict["oneToManyRelationships"].append(relationship_obj)
    elif rel_type == "ManyToOne":
        class_dict["manyToOneRelationships"].append(relationship_obj)
    elif rel_type == "ManyToMany":
        class_dict["manyToManyRelationships"].append(relationship_obj)
    else:
        logging.warning(f"Type de relation inconnu: {rel_type}")
    
    return class_dict

def retry_with_explicit_json(client, source_class, target_class, relationship):
    """
    Réessaie avec une demande plus explicite pour obtenir un JSON valide.
    
    Args:
        client: Client OpenAI
        source_class, target_class, relationship: Données des classes et de la relation
        
    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: Les deux classes modifiées
    """
    logging.info("Tentative de récupération avec une demande explicite de JSON...")
    
    retry_prompt = f"""
    Je n'ai pas pu parser ta dernière réponse comme un JSON valide.
    
    Analyse ces deux classes et leur relation:
    
    SOURCE: {source_class.get('name')}
    CIBLE: {target_class.get('name')}
    RELATION: {relationship.get('name')}
    
    Détermine le type de relation entre ces classes (OneToOne, OneToMany, ManyToOne, ManyToMany).
    Retourne UNIQUEMENT ce JSON avec cette structure exacte:
    
    {{
      "relationship_type": "Type global de la relation",
      "source_class": {{
        "relationship_type": "OneToOne|OneToMany|ManyToOne|ManyToMany",
        "role": "nom_du_champ",
        "comodel": "NomDeClasse",
        "mapped_by_property": null ou "nom_propriete"
      }},
      "target_class": {{
        "relationship_type": "OneToOne|OneToMany|ManyToOne|ManyToMany",
        "role": "nom_du_champ",
        "comodel": "NomDeClasse",
        "mapped_by_property": null ou "nom_propriete"
      }}
    }}
    """
    
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=[
            {"role": "system", "content": "Tu es un expert en UML qui génère des réponses en JSON pur."},
            {"role": "user", "content": retry_prompt}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    response_text = completion.choices[0].message.content.strip()
    
    try:
        interpretation = json.loads(response_text)
        source_class_updated = update_class_with_relationship(source_class, interpretation["source_class"])
        target_class_updated = update_class_with_relationship(target_class, interpretation["target_class"])
        logging.info("Récupération réussie")
        return source_class_updated, target_class_updated
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Échec de la récupération: {e}")
        # Fallback: retourner les classes inchangées
        logging.warning("Utilisation d'une solution de secours par défaut")
        return fallback_interpretation(source_class, target_class, relationship)

def fallback_interpretation(source_class: Dict[str, Any], target_class: Dict[str, Any], 
                            relationship: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Solution de secours qui fait une interprétation basique basée sur les multiplicités.
    
    Args:
        source_class, target_class, relationship: Données des classes et de la relation
        
    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: Les deux classes modifiées
    """
    logging.info("Application de l'interprétation de secours basée sur les multiplicités")
    
    # Valeurs par défaut pour les rôles
    source_role = relationship.get("source_role") or target_class.get("name", "").lower()
    target_role = relationship.get("target_role") or source_class.get("name", "").lower()
    
    # Obtenir les multiplicités
    source_multiplicity = relationship.get("source_multiplicity", [0, 1])
    target_multiplicity = relationship.get("target_multiplicity", [0, 1])
    
    # Déterminer les types de relation en fonction des multiplicités
    source_max = source_multiplicity[1] if isinstance(source_multiplicity, list) and len(source_multiplicity) > 1 else 1
    target_max = target_multiplicity[1] if isinstance(target_multiplicity, list) and len(target_multiplicity) > 1 else 1
    
    # Si source_max ou target_max sont des chaînes comme 'n', les convertir en nombre large
    if isinstance(source_max, str) and source_max.lower() in ['n', '*', 'many']:
        source_max = 999
    if isinstance(target_max, str) and target_max.lower() in ['n', '*', 'many']:
        target_max = 999
        
    # Déterminer les types de relation
    source_type = "ManyToMany" if source_max > 1 and target_max > 1 else \
                  "OneToMany" if target_max > 1 else \
                  "ManyToOne" if source_max > 1 else \
                  "OneToOne"
                  
    target_type = "ManyToMany" if source_max > 1 and target_max > 1 else \
                  "ManyToOne" if source_max > 1 else \
                  "OneToMany" if target_max > 1 else \
                  "OneToOne"
    
    # Déterminer qui est propriétaire basé sur la navigabilité
    is_source_owner = relationship.get("is_navigable_to_target", True)
    is_target_owner = relationship.get("is_navigable_to_source", True)
    
    # Création des objets relationship
    source_rel = {
        "role": target_role,
        "comodel": target_class.get("name"),
        "mapped_by_property": source_role if not is_source_owner and is_target_owner else None
    }
    
    target_rel = {
        "role": source_role,
        "comodel": source_class.get("name"),
        "mapped_by_property": target_role if not is_target_owner and is_source_owner else None
    }
    
    # Mise à jour des classes
    source_class_updated = update_class_with_relationship(
        source_class, {"relationship_type": source_type, **source_rel})
    target_class_updated = update_class_with_relationship(
        target_class, {"relationship_type": target_type, **target_rel})
    
    return source_class_updated, target_class_updated
