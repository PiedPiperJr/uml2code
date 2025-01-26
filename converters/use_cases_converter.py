import google.generativeai as genai
from config import *
import json
from typing import List, Dict
from utils.utils import dump
from models.project_model import UseCase, Scenario


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


def interprete_usecase(usecases: Dict) -> List[UseCase]:
    """
        Cette methode permet de parser la description textuelle des cas d(utilisations (retourné pas la fonction just au dessus))
        et remplir les autres champs liés à un cas d'utilisation
        
        Regarder la structure du type UseCase pour plus d'infos !        
    """
    useCases : List[UseCase] = list()
    for case in usecases["use_cases"]:
        useCases.append(UseCase(name=case["name"],
                                action="",
                                actors=case["actors"],
                                scenarios= Scenario(main= case["scenarios"]["principal"],
                                                    alternatif= case["scenarios"]["alternatif"]),
                                preconditons= case["preconditions"],
                                postconditions= case["postcondions"]))

    # TODO implement this 
    pass