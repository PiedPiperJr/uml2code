import google.generativeai as genai
from config import *
import json
from typing import List, Dict
from utils.utils import dump
from models.project_model import UseCase, Dto, Scenario, Method, Arg, DtoAttribute, Repository, Resource, Decorator, Service
from copy import deepcopy
from typing import List, Literal, Dict, Any, Optional
from dataclasses import dataclass


def use_cases_to_json(use_cases: str):
    # CONFIGURATION DE GEMINI
    genai.configure(api_key="AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8")
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    prompt = f"""convertit ce fichier texte {use_cases} sous ce format: 
    {USECASE_PATTERN},correspondant pour le cas d'utilisation donné,
    les différentes données présentent sur le format, sans aucun texte
    superflux.Base toi sur les préconditions et les postcondtions de
    tous les cas d'utilisations de la liste, et tout autre chsoe pouvant
    être utile. Si tu ne trouves pas quelque chose tu mets None. Tous ce
    qui est au plurile corespond à une liste dont les éléments sont listé
    en dessosu (avec indentation). Enlève les whitespacecs dans tes réponses.
    Suis rigoureusement le format donné. Je précise qu'avant toute utilisation
    au système, il faut s'authentifier. Ensuite convertit en JSON. Mets le nom
    des uses cases sous la forme camelcase de java. Je précise que resource 
    correspond à ce qe produit le cas d'utiisation, donc, n'est pas un iterable"""

    response = model.generate_content(prompt)

    json_response = model.generate_content(
        "convertit " + str(response.to_dict()) + "sous format JSON et donne moi uniquement le json")

    json_store = json.loads(json_response.text.replace(
        "json", "").replace("```", "").strip().replace("\n", ""))

    return json_store


def determine_http_action(name: str, scenario: Scenario) -> Literal["POST", "GET", "PUT", "PATCH", "DELETE"]:
    """
    Détermine l'action HTTP basée sur le nom du use case et son scénario.
    """
    name_lower = name.lower()
    main_steps = ' '.join(scenario.main).lower()
    
    if any(word in name_lower or word in main_steps for word in ['créer', 'ajouter', 'create', 'nouveau']):
        return "POST"
    elif any(word in name_lower or word in main_steps for word in ['modifier', 'mettre à jour', 'update']):
        return "PUT"
    elif any(word in name_lower or word in main_steps for word in ['supprimer', 'delete']):
        return "DELETE"
    elif any(word in name_lower or word in main_steps for word in ['obtenir', 'afficher', 'lire', 'consulter', 'rechercher']):
        return "GET"
    elif any(word in name_lower or word in main_steps for word in ['patch', 'modifier partiellement']):
        return "PATCH"
    
    return "GET"

def interprete_usecase(usecases: Dict) -> List[UseCase]:
    """
        Cette methode permet de parser la description textuelle des cas d(utilisations (retourné pas la fonction just au dessus))
        et remplir les autres champs liés à un cas d'utilisation
        
        Regarder la structure du type UseCase pour plus d'infos !        
    """
    useCases : List[UseCase] = list()
    if "useCases" in usecases.keys() :
        nameOfUseCase = "useCases"
    elif "use_cases" in usecases.keys():
        nameOfUseCase = "use_cases"
    for case in usecases[nameOfUseCase]:
        # Parsing des extends
        extends_list = []
        if 'extends' in case:
            if case['extends'] is not None:
                for extend in case['extends']:
                    # Ici on stocke juste les noms car on n'a pas accès aux autres UseCases
                    extends_list.append(extend)

        # Parsing des includes
        include_list = []
        if 'include' in case:
            if case['include'] is not None:
                for include in case['include']:
                    include_list.append(include)

        # Parsing des DTOs
        dto = []
        if 'dto' in case:
            dto_datas = case['dto']
            attributes = []
            for dto_data in dto_datas:
                for attr in dto_data.get('attributes', {}):
                    decorators = []
                    if 'decorators' in attr:
                        dec_data = attr['decorators']
                        if isinstance(dec_data, list):
                            for d in dec_data:
                                decorators.append(Decorator(
                                    name=d['decorator']['name'],
                                    message=d['decorator'].get('message', '')
                                ))
                        else:
                            decorators.append(Decorator(
                                name=dec_data['decorator']['name'],
                                message=dec_data['decorator'].get('message', '')
                            ))
                    
                    attributes.append(DtoAttribute(
                        name=attr['name'],
                        visibility=attr['visibility'],
                        type=attr['type'],
                        decorators=decorators
                    ))
            
                dto.append(Dto(name=dto_data['name'], attributes=attributes))

        # Parsing de la Resource
        resource = None
        if 'resource' in case:
            res_data = case['resource']
            attributes = []
            if res_data is not None:
                for attr in res_data.get('attributes', []):
                    attributes.append(Arg(
                        name=attr['name'],
                        visibility=attr['visibility'],
                        type=attr['type']
                    ))
                resource = Resource(name=res_data['name'], attributes=attributes)

        # Parsing des Services
        services = []
        if 'services' in case:
            services_data = case['services']
            for service_data in services_data if isinstance(services_data, list) else [services_data]:
                methods = []
                for method_data in service_data.get('methods', []):
                    args = []
                    for arg_data in method_data.get('args', []):
                        args.append(Arg(
                            name=arg_data['name'],
                            visibility=arg_data['visibility'],
                            type=arg_data['type']
                        ))
                    methods.append(Method(
                        name=method_data['name'],
                        visibility=method_data['visibility'],
                        type=method_data['type'],
                        args=args
                    ))
                services.append(Service(name=service_data['name'], methods=methods))

        # Parsing des Repositories
        repositories = []
        if 'repositories' in case:
            repos_data = case['repositories']
            for repo_data in repos_data if isinstance(repos_data, list) else [repos_data]:
                methods = []
                for method_data in repo_data.get('methods', []):
                    args = []
                    for arg_data in method_data.get('args', []):
                        args.append(Arg(
                            name=arg_data['name'],
                            visibility=arg_data['visibility'],
                            type=arg_data['type']
                        ))
                    methods.append(Method(
                        name=method_data['name'],
                        visibility=method_data['visibility'],
                        type=method_data['type'],
                        args=args
                    ))
                repositories.append(Repository(
                    entity=repo_data['entity'],
                    methods=methods
                ))

        # Parsing du scénario
        scenario = Scenario(
            main=case.get('scenarios', {}).get('principal', []),
            alternative=case.get('scenarios', {}).get('alternatif', [])
        )

        # Détermination de l'action HTTP
        action = determine_http_action(case['name'], scenario)

        # Construction de l'objet UseCase final
        useCases.append(UseCase(
            name=case['name'],
            action=action,
            actors=case.get('actors', []),
            scenarios=scenario,
            preconditions=case.get('preconditions', []),
            postconditions=case.get('postconditions', []),
            dto=dto,
            extends=extends_list,
            include=include_list,
            services=services,
            resource=resource,
            repositories=repositories
        ))
    
    return useCases
