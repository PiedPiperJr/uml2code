import google.generativeai as genai
from config import *
import json
from typing import List, Dict
from utils.utils import dump
from models.project_model import UseCase, Scenario, Dto
from copy import deepcopy


def use_cases_to_json(use_cases: str):
    # CONFIGURATION DE GEMINI
    genai.configure(api_key="AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8")
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""convertit ce fichier sous ce format: 
                {USECASE_PATTERN} mon texte  {use_cases} Ensuite convertit en JSON. 
                mets le nom des uses cases sous la forme camelcase de java."""

    response = model.generate_content(prompt)

    json_response = model.generate_content(
        "convertit " + str(response.to_dict()) + "sous format JSON et donne moi uniquement le json")

    json_store = json.loads(json_response.text.replace(
        "json", "").replace("```", "").strip().replace("\n", ""))

    return json_store

def link_between_usecases(usecase: Dict, usecases: Dict) -> Dict:
    
    """
        Cette méthode permet de déterminer les liens include et extend du
        cas d'utilisation usecase, liens pris dans la liste des cas usecases
        issue de la réponse de l'API de chat.
    """
    genai.configure(api_key="AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8")
    model = genai.GenerativeModel('gemini-1.5-flash')
    if "useCases" in usecases.keys() :
        nameOfUseCase = "useCases"
    elif "use_cases" in usecases.keys():
        nameOfUseCase = "use_cases"
    prompt : str = f"""Donne moi pour le cas d'utilisation {json.dumps(usecase)},
        de la liste des cas d'utilisation suivants {usecases[nameOfUseCase]}, que tu me renvoies uniquement un JSON
        sous le format {USECASE_LINK} correspondant à la liste des use cases qui 'extends' et
        qui 'uses'  le cas d'utilisation donné, sans aucun teste superflux.Base toi sur les
        préconditions et les postcondtions. Si tu ne trouves pas de relation tu mets None.
        Enlève les whitespacecs dans tes réponses. Suis rigoureusement le format donné."""

    response = model.generate_content(prompt)

    json_response = model.generate_content(
        "convertit " + str(response.to_dict()) + "sous format JSON et donne moi uniquement le json")

    json_store = json.loads(json_response.text.replace("json", "").replace("```", "").strip().replace("\n", ""))
    return json_store["candidates"][0]["content"]["parts"][0]["text"]

def interprete_usecase(usecases: Dict) -> List[UseCase]:
    """
        Cette methode permet de parser la description textuelle des cas d(utilisations (retourné pas la fonction just au dessus))
        et remplir les autres champs liés à un cas d'utilisation
        
        Regarder la structure du type UseCase pour plus d'infos !        
    """
    useCases : List[UseCase] = list()
    i : int = 0
    length: int = len(usecases)
    if "useCases" in usecases.keys() :
        nameOfUseCase = "useCases"
    elif "use_cases" in usecases.keys():
        nameOfUseCase = "use_cases"
    for case in usecases[nameOfUseCase]:
        useCases.append(UseCase(name=case["name"],
                                action="",
                                actors=case["actors"],
                                scenarios= Scenario(main= case["scenarios"]["principal"],
                                                    alternatif= case["scenarios"]["alternatif"]),
                                preconditons= case["preconditions"],
                                postconditions= case["postcondions"]
                                )
                        )
        if i == length:
            break
        myCase : Dict = link_between_usecases(case, usecases)
        useCases[i].include = myCase["include"]
        useCases[i].extends = myCase["extends"]
        use
        
        

    # TODO implement this 
    pass
