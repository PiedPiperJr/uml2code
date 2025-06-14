from google import genai
from config import *
import json
from typing import List, Dict
from utils.utils import dump
from models.project_model import UseCase


def use_cases_to_json(use_cases: str):
    # CONFIGURATION DE GEMINI
    client = genai.Client(api_key="AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8")

    prompt1 = f"""**Modèle de Formatage :**
                    {USECASE_PATTERN}
                **Texte à Reformater :**
                    {use_cases}
                **Consignes pour le formatage :**

                    * Identifie et établis les **relations possibles** entre les différents cas d'utilisation.
                    * Matérialise ces relations en remplissant les champs `uses` et `extends` pour chaque cas d'utilisation, conformément au modèle.
                    * Le résultat final doit être **strictement le texte reformaté**, sans aucune introduction, explication ou autre texte additionnel."""

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=prompt1,
    )
    
    prompt2 = f"""Convertit le texte (dictionnaire) suivant en JSON. Le résultat doit être *uniquement* le texte sous format JSON, sans aucun préambule, explication ou texte additionnel. 
                
                **Texte à convertir
                {str(response.to_dict())}"""


    json_response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=prompt2,
    )
    json_store = json.loads(json_response.text.replace(
        "json", "").replace("```", "").strip().replace("\n", ""))

    return json_store


def interprete_usecase(usecases: List[Dict]) -> List[UseCase]:
    """
    Cette methode permet de parser la description textuelle des cas d'utilisations 
    et remplir les autres champs liés à un cas d'utilisation
    
    Suppose que les relations 'uses' et 'extends' sont déjà déterminées par Gemini
    """
    parsed_usecases = []
    
    # Première passe : créer tous les cas d'utilisation de base
    for usecase_data in usecases:
        try:
            # Extraction des données de base du cas d'utilisation
            name = usecase_data.get('name', '').strip()
            action = determine_http_action(usecase_data)
            actors = extract_actors(usecase_data.get('actors', []))
            
            # Extraction des scénarios (principal/alternatif selon le pattern)
            scenarios = extract_scenarios(usecase_data.get('scenarios', {}))
            
            # Extraction des conditions
            preconditions = extract_conditions(usecase_data.get('preconditions', []))
            postconditions = extract_conditions(usecase_data.get('postconditions', []))
            
            # Génération des composants techniques via Gemini
            scenarios = extract_scenarios(usecase_data.get('scenarios', {}))
            dto = generate_dto(name, usecase_data, action)
            resource = generate_resource(name, dto)
            services = generate_services(name, scenarios, action)
            repositories = generate_repositories(name, dto, action)
            
            # Relations entre cas d'utilisation (vides pour l'instant)
            uses = []  # Sera rempli dans la seconde passe
            extends = []  # Sera rempli dans la seconde passe  
            include = []  # Pattern ne mentionne pas include, on le laisse vide
            
            # Création de l'objet UseCase
            usecase = UseCase(
                name=name,
                action=action,
                actors=actors,
                scenarios=scenarios,
                preconditions=preconditions,
                postconditions=postconditions,
                dto=dto,
                uses=uses,
                extends=extends,
                include=include,
                services=services,
                resource=resource,
                repositories=repositories
            )
            
            parsed_usecases.append(usecase)
            
        except Exception as e:
            print(f"Erreur lors du parsing du cas d'utilisation {usecase_data}: {e}")
            continue
    
    # Seconde passe : résoudre les relations entre cas d'utilisation
    resolve_usecase_relationships(parsed_usecases, usecases)
    
    return parsed_usecases


def determine_http_action(usecase_data: Dict) -> str:
    """Détermine l'action HTTP basée sur le nom et les scénarios du cas d'utilisation"""
    name = usecase_data.get('name', '').lower()
    scenarios = usecase_data.get('scenarios', {})
    
    # Récupérer le scénario principal selon le pattern YAML
    principal_scenario = scenarios.get('principal', [])
    if isinstance(principal_scenario, list):
        principal_text = ' '.join(principal_scenario).lower()
    else:
        principal_text = str(principal_scenario).lower()
    
    # Mots-clés pour déterminer l'action HTTP
    create_keywords = ['crée', 'créer', 'ajouter', 'nouveau', 'enregistrer', 'sauvegarder', 'create', 'add', 'insert', 'register', 'submit']
    update_keywords = ['modifie', 'modifier', 'mettre à jour', 'éditer', 'changer', 'update', 'modify', 'edit', 'change']
    delete_keywords = ['supprimer', 'supprime', 'effacer', 'retirer', 'delete', 'remove', 'cancel']
    
    if any(keyword in name or keyword in principal_text for keyword in create_keywords):
        return 'POST'
    elif any(keyword in name or keyword in principal_text for keyword in update_keywords):
        return 'PUT'
    elif any(keyword in name or keyword in principal_text for keyword in delete_keywords):
        return 'DELETE'
    else:
        return 'GET'  # Par défaut pour consultation/recherche


def extract_actors(actors_data) -> List[str]:
    """Extrait et nettoie la liste des acteurs"""
    if isinstance(actors_data, list):
        return [actor.strip() for actor in actors_data if actor.strip()]
    elif isinstance(actors_data, str):
        return [actor.strip() for actor in actors_data.split(',') if actor.strip()]
    return []


def extract_scenarios(scenarios_data: Dict) -> Scenario:
    """Extrait les scénarios principal et alternatifs selon le pattern YAML"""
    main = []
    alternative = []
    
    if isinstance(scenarios_data, dict):
        # Le pattern utilise 'principal' et 'alternatif'
        main = scenarios_data.get('principal', [])
        alternative = scenarios_data.get('alternatif', [])
        
        # Fallback pour autres variantes possibles
        if not main:
            main = scenarios_data.get('main', [])
        if not alternative:
            alternative = scenarios_data.get('alternative', [])
    
    # S'assurer que ce sont des listes
    if isinstance(main, str):
        main = [main]
    if isinstance(alternative, str):
        alternative = [alternative]
        
    return Scenario(main=main, alternative=alternative)


def extract_conditions(conditions_data) -> List[str]:
    """Extrait et nettoie les conditions (pré/post)"""
    if isinstance(conditions_data, list):
        return [condition.strip() for condition in conditions_data if condition.strip()]
    elif isinstance(conditions_data, str):
        return [condition.strip() for condition in conditions_data.split('.') if condition.strip()]
    return []


def generate_dto(name: str, usecase_data: Dict, action: str) -> Dto:
    """Génère le DTO basé sur le cas d'utilisation en utilisant Gemini"""
    dto_name = f"{capitalize(name)}Dto"
    
    # Utiliser la fonction d'extraction des scénarios déjà définie
    scenarios = extract_scenarios(usecase_data.get('scenarios', {}))
    
    # Générer les attributs via Gemini
    attributes = generate_dto_attributes_with_gemini(name, usecase_data, scenarios, action)
    
    return Dto(name=dto_name, attributes=attributes)


def generate_dto_attributes_with_gemini(name: str, usecase_data: Dict, scenarios: Scenario, action: str) -> List[DtoAttribute]:
    """Génère les attributs du DTO en utilisant Gemini pour l'analyse contextuelle"""
    
    client = genai.Client(api_key="AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8")
    
    # Préparer le contexte pour Gemini
    context = {
        "nom_cas_utilisation": name,
        "action_http": action,
        "acteurs": usecase_data.get('actors', []),
        "scenario_principal": scenarios.main,
        "scenario_alternatif": scenarios.alternative,
        "preconditions": usecase_data.get('preconditions', []),
        "postconditions": usecase_data.get('postconditions', [])
    }
    
    prompt = f"""Analyse le cas d'utilisation suivant et génère les attributs appropriés pour un DTO Java Spring Boot.

            **Contexte du cas d'utilisation :**
            {json.dumps(context, ensure_ascii=False, indent=2)}

            **Instructions :**
            1. Identifie les attributs pertinents basés sur les scénarios et le contexte métier
            2. Détermine le type Java approprié pour chaque attribut
            3. Choisis les décorateurs de validation appropriés selon l'action HTTP
            4. Ajoute un attribut 'id' de type 'Long' si nécessaire pour les actions GET/PUT/DELETE

            **Format de réponse attendu (JSON uniquement) :**
            [
            {{
                "name": "nom_attribut",
                "type": "TypeJava",
                "visibility": "private",
                "decorators": [
                {{
                    "name": "NomDecorateur",
                    "message": "Message de validation"
                }}
                ]
            }}
            ]

            Réponds uniquement avec le JSON, sans explication, ni texe superflus."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=prompt,
        )
        
        # Nettoyer la réponse et parser le JSON
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        attributes_data = json.loads(json_text)
        
        # Convertir en objets DtoAttribute
        dto_attributes = []
        for attr_data in attributes_data:
            decorators = [
                Decorator(name=dec["name"], message=dec["message"]) 
                for dec in attr_data.get("decorators", [])
            ]
            
            dto_attributes.append(DtoAttribute(
                visibility=attr_data.get("visibility", "private"),
                name=attr_data["name"],
                type=attr_data["type"],
                decorators=decorators
            ))
        
        return dto_attributes
        
    except Exception as e:
        print(f"Erreur lors de la génération des attributs DTO avec Gemini: {e}")
        return [
            DtoAttribute(
                visibility="private",
                name="id" if action in ['GET', 'PUT', 'DELETE'] else "name",
                type="Long" if action in ['GET', 'PUT', 'DELETE'] else "String",
                decorators=[Decorator(name="NotNull", message="Field is required")]
            )
        ]


def generate_resource(name: str, dto: Dto) -> Resource:
    """Génère la ressource REST basée sur le DTO"""
    resource_name = f"{capitalize(name)}Resource"
    
    attributes = []
    for dto_attr in dto.attributes:
        attributes.append(Arg(
            visibility="private",
            name=dto_attr.name,
            type=dto_attr.type
        ))
    
    return Resource(name=resource_name, attributes=attributes)


def generate_services(name: str, scenarios: Scenario, action: str) -> List[Service]:
    """Génère les services nécessaires pour le cas d'utilisation en utilisant Gemini"""
    service_name = f"{capitalize(name)}Service"
    
    # Générer les méthodes via Gemini
    methods = generate_service_methods_with_gemini(name, scenarios, action)
    
    return [Service(name=service_name, methods=methods)]


def generate_service_methods_with_gemini(name: str, scenarios: Scenario, action: str) -> List[Method]:
    """Génère les méthodes de service en utilisant Gemini pour l'analyse contextuelle"""
    import google as genai
    
    client = genai.Client(api_key="AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8")
    
    context = {
        "nom_cas_utilisation": name,
        "action_http": action,
        "scenario_principal": scenarios.main,
        "scenario_alternatif": scenarios.alternative
    }
    
    prompt = f"""Analyse le cas d'utilisation suivant et génère les méthodes appropriées pour un Service Java Spring Boot.

                **Contexte du cas d'utilisation :**
                {json.dumps(context, ensure_ascii=False, indent=2)}

                **Instructions :**
                1. Génère les méthodes de service basées sur l'action HTTP et les scénarios
                2. Utilise des noms de méthodes significatifs selon le contexte métier
                3. Détermine les arguments et types de retour appropriés
                4. Toutes les méthodes doivent être publiques

                **Types Java courants à utiliser :**
                - String, Long, Integer, Boolean
                - LocalDateTime pour les dates
                - List<...> pour les collections
                - {capitalize(name)}Dto pour le DTO principal
                - void pour les méthodes sans retour

                **Format de réponse attendu (JSON uniquement) :**
                [
                {{
                    "name": "nomMethode",
                    "visibility": "public",
                    "type": "TypeRetour",
                    "args": [
                    {{
                        "name": "nomArgument",
                        "type": "TypeArgument",
                        "visibility": "public"
                    }}
                    ]
                }}
                ]

                Réponds uniquement avec le JSON, sans explication, ni texte superflus."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=prompt,
        )
        
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        methods_data = json.loads(json_text)
        
        methods = []
        for method_data in methods_data:
            args = [
                Arg(
                    visibility=arg_data.get("visibility", "public"),
                    name=arg_data["name"],
                    type=arg_data["type"]
                )
                for arg_data in method_data.get("args", [])
            ]
            
            methods.append(Method(
                name=method_data["name"],
                args=args,
                type=method_data["type"],
                visibility=method_data.get("visibility", "public")
            ))
        
        return methods
        
    except Exception as e:
        print(f"Erreur lors de la génération des méthodes de service avec Gemini: {e}")
        # Fallback simple en cas d'erreur
        fallback_method = Method(
            name=f"process{capitalize(name)}",
            args=[Arg("public", "dto", f"{capitalize(name)}Dto")],
            type=f"{capitalize(name)}Dto" if action != 'DELETE' else "void",
            visibility="public"
        )
        return [fallback_method]


def generate_repositories(name: str, dto: Dto, action: str) -> List[Repository]:
    """Génère les repositories nécessaires en utilisant Gemini"""
    entity_name = f"{capitalize(name)}Entity"
    
    # Générer les méthodes via Gemini
    methods = generate_repository_methods_with_gemini(name, dto, action, entity_name)
    
    return [Repository(entity=entity_name, methods=methods)]


def generate_repository_methods_with_gemini(name: str, dto: Dto, action: str, entity_name: str) -> List[Method]:
    """Génère les méthodes de repository en utilisant Gemini pour l'analyse contextuelle"""
    import google as genai
    
    client = genai.Client(api_key="AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8")
    
    dto_attributes = [
        {"name": attr.name, "type": attr.type} 
        for attr in dto.attributes
    ]
    
    context = {
        "nom_cas_utilisation": name,
        "action_http": action,
        "nom_entite": entity_name,
        "attributs_dto": dto_attributes
    }
    
    prompt = f"""Analyse le cas d'utilisation suivant et génère les méthodes appropriées pour un Repository JPA Spring Boot.

                **Contexte du cas d'utilisation :**
                {json.dumps(context, ensure_ascii=False, indent=2)}

                **Instructions :**
                1. Génère les méthodes de repository basées sur l'action HTTP et les attributs disponibles
                2. Inclus les méthodes JPA standard (save, findById, findAll, deleteById selon l'action)
                3. Ajoute des méthodes de recherche personnalisées basées sur les attributs pertinents
                4. Utilise les conventions Spring Data JPA pour les noms de méthodes
                5. Toutes les méthodes doivent être publiques

                **Types Java courants à utiliser :**
                - {entity_name} pour l'entité
                - Optional<{entity_name}> pour les recherches par ID
                - List<{entity_name}> pour les collections
                - Les types des attributs pour les paramètres de recherche

                **Méthodes JPA standard à considérer :**
                - save, findById, findAll, deleteById, existsById

                **Format de réponse attendu (JSON uniquement) :**
                [
                {{
                    "name": "nomMethode",
                    "visibility": "public",
                    "type": "TypeRetour",
                    "args": [
                    {{
                        "name": "nomArgument",
                        "type": "TypeArgument",
                        "visibility": "public"
                    }}
                    ]
                }}
                ]

                Réponds uniquement avec le JSON, sans explication, ni texte superflus."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=prompt,
        )
        
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        methods_data = json.loads(json_text)
        
        methods = []
        for method_data in methods_data:
            args = [
                Arg(
                    visibility=arg_data.get("visibility", "public"),
                    name=arg_data["name"],
                    type=arg_data["type"]
                )
                for arg_data in method_data.get("args", [])
            ]
            
            methods.append(Method(
                name=method_data["name"],
                args=args,
                type=method_data["type"],
                visibility=method_data.get("visibility", "public")
            ))
        
        return methods
        
    except Exception as e:
        print(f"Erreur lors de la génération des méthodes de repository avec Gemini: {e}")
        fallback_methods = [
            Method(
                name="save",
                args=[Arg("public", "entity", entity_name)],
                type=entity_name,
                visibility="public"
            ),
            Method(
                name="findById",
                args=[Arg("public", "id", "Long")],
                type=f"Optional<{entity_name}>",
                visibility="public"
            )
        ]
        return fallback_methods


def resolve_usecase_relationships(usecases: List[UseCase], original_data: List[Dict]):
    """Résout les relations entre cas d'utilisation basées sur les données Gemini"""
    usecase_map = {uc.name.lower().strip(): uc for uc in usecases}
    
    for i, usecase in enumerate(usecases):
        if i >= len(original_data):
            continue
            
        original = original_data[i]
        uses_data = original.get('uses', '')
        if uses_data and isinstance(uses_data, str):
            # Chercher des noms de cas d'utilisation dans le texte 'uses'
            uses_names = find_referenced_usecases(uses_data, usecase_map)
            usecase.uses = [usecase_map[name] for name in uses_names if name in usecase_map]
        
        extends_data = original.get('extends', '')
        if extends_data and isinstance(extends_data, str):
            extends_names = find_referenced_usecases(extends_data, usecase_map.keys())
            usecase.extends = [usecase_map[name] for name in extends_names if name in usecase_map]


def find_referenced_usecases(usecase: UseCase, all_usecases: Dict[str, UseCase]) -> List[UseCase]:
    """
    Utilise Gemini 2.5 Flash pour identifier intelligemment les relations 
    entre cas d'utilisation basées sur l'analyse sémantique du contenu
    """
    
    client = genai.Client(api_key="AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8")
    
    usecase_context = {
        "nom": usecase.name,
        "action_http": usecase.action,
        "acteurs": usecase.actors,
        "scenario_principal": usecase.scenarios.main if usecase.scenarios else [],
        "scenario_alternatif": usecase.scenarios.alternative if usecase.scenarios else [],
        "preconditions": usecase.preconditions,
        "postconditions": usecase.postconditions
    }
    
    try:
        
        other_usecases_info = []
        usecase_objects_map = {}
        
        for uc in all_usecases:
            if uc.name != usecase.name:  # Exclure le cas d'utilisation courant
                uc_info = {
                    "nom": uc.name,
                    "action_http": uc.action,
                    "acteurs": uc.actors,
                    "scenario_principal": uc.scenarios.main if uc.scenarios else [],
                    "scenario_alternatif": uc.scenarios.alternative if uc.scenarios else [],
                    "preconditions": uc.preconditions,
                    "postconditions": uc.postconditions
                }
                other_usecases_info.append(uc_info)
                usecase_objects_map[uc.name] = uc
        
        if not other_usecases_info:
            return []
        
        # Construire le prompt pour Gemini
        analysis_context = {
            "cas_utilisation_analyse": usecase_context,
            "autres_cas_utilisation": other_usecases_info
        }
        
        prompt = f"""Analyse le cas d'utilisation suivant et identifie ses relations avec les autres cas d'utilisation disponibles.

                    **Cas d'utilisation à analyser :**
                    {json.dumps(usecase_context, ensure_ascii=False, indent=2)}

                    **Autres cas d'utilisation disponibles :**
                    {json.dumps(other_usecases_info, ensure_ascii=False, indent=2)}

                    **Instructions d'analyse :**
                    1. Identifie les relations sémantiques entre le cas d'utilisation analysé et les autres cas disponibles
                    2. Recherche les types de relations suivants :
                    - **USES** : Le cas analysé utilise/dépend d'un autre cas (invoque, nécessite, s'appuie sur)
                    - **EXTENDS** : Le cas analysé étend/spécialise un autre cas (cas particulier, variation)
                    - **INCLUDE** : Le cas analysé inclut/intègre un autre cas (contient, incorpore)
                    - **REFERENCE** : Le cas analysé fait référence à un autre cas (mentionne, lié à)

                    3. Base ton analyse sur :
                    - Les similitudes dans les acteurs
                    - Les liens logiques entre les scénarios
                    - Les dépendances dans les pré/postconditions
                    - Les mots-clés et concepts partagés
                    - La logique métier commune

                    4. Pour chaque relation identifiée, évalue la force de la relation (forte/moyenne/faible)
                    5. Ne retourne que les relations fortes et moyennes

                    **Format de réponse attendu (JSON uniquement) :**
                    {{
                    "relations_identifiees": [
                        {{
                        "nom_cas_utilisation": "nom_exact_du_cas_référencé",
                        "type_relation": "USES|EXTENDS|INCLUDE|REFERENCE",
                        "force_relation": "forte|moyenne|faible",
                        "justification": "Explication courte de la relation identifiée"
                        }}
                    ]
                    }}

                    Réponds uniquement avec le JSON, sans explication additionnelle, ni texte superflus."""

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=prompt,
        )
        
        # Parser la réponse JSON
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        analysis_result = json.loads(json_text)
        
        # Extraire les cas d'utilisation référencés
        referenced_usecases = []
        relations = analysis_result.get("relations_identifiees", [])
        
        for relation in relations:
            # Ne conserver que les relations fortes et moyennes
            if relation.get("force_relation") in ["forte", "moyenne"]:
                referenced_name = relation.get("nom_cas_utilisation")
                if referenced_name in usecase_objects_map:
                    referenced_usecases.append(usecase_objects_map[referenced_name])
        
        return referenced_usecases
        
    except Exception as e:
        print(f"Erreur lors de l'analyse des relations avec Gemini: {e}")
        # Fallback: utiliser l'ancienne méthode basique en cas d'erreur
        return fallback_find_relations(usecase, all_usecases)


def fallback_find_relations(current_usecase: UseCase, all_usecases: List[UseCase]) -> List[UseCase]:
    """
    Méthode de fallback pour identifier les relations de base 
    en cas d'échec de l'analyse Gemini
    """
    referenced = []
    
    if not all_usecases:
        return referenced
    
    current_name_lower = current_usecase.name.lower()
    current_actors = [actor.lower() for actor in current_usecase.actors]
    current_scenarios_text = ""
    
    if current_usecase.scenarios:
        current_scenarios_text = " ".join(current_usecase.scenarios.main + current_usecase.scenarios.alternative).lower()
    
    for other_usecase in all_usecases:
        if other_usecase.name == current_usecase.name:
            continue
            
        # Vérifier les similarités d'acteurs
        other_actors = [actor.lower() for actor in other_usecase.actors]
        common_actors = set(current_actors) & set(other_actors)
        
        # Vérifier les références dans les scénarios
        other_name_words = other_usecase.name.lower().split()
        scenario_references = any(word in current_scenarios_text for word in other_name_words if len(word) > 3)
        
        # Relation détectée si acteurs communs OU référence dans scénarios
        if len(common_actors) > 0 or scenario_references:
            referenced.append(other_usecase)
    
    return referenced

def capitalize(text: str) -> str:
    """Capitalise la première lettre de chaque mot et supprime les espaces"""
    return ''.join(word.capitalize() for word in text.replace('-', ' ').replace('_', ' ').split())