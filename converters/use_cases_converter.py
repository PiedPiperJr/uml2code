import google.generativeai as genai
from config import *
import json
from typing import List
from utils.utils import dump

def use_cases_to_json(use_cases: str):
    # CONFIGURATION DE GEMINI
    genai.configure(api_key="AIzaSyBfCOw1YjmEB-Ed-AonWIpF7BjhE60_aL8")
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""convertit ce fichier sous ce format: 
                {USECASE_PATTERN} mon texte  {use_cases} Ensuite convertit en JSON. 
                mets le nom des uses caes sous la forme camelcase de java."""

    response = model.generate_content(prompt)

    json_response = model.generate_content(
        "convertit " + str(response.to_dict()) + "sous formt JSON et donne moi uniquement le json")

    json_store = json.loads(json_response.text.replace(
        "json", "").replace("```", "").strip().replace("\n", ""))

    return json_store

