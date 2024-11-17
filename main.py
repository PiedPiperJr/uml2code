#!/usr/bin/env python
# coding: utf-8

# # Convertif un diagramme UML en code
# ## Principe
# - Convertir le xml (drawio) en json (equivalent simple)
# - Convertir le json en json structuré: Hierarchiser pour que la classe contienne ses attributs et que les relations soient mentionnées à coté
# - Interpreter les relations et appliquer les changement qui s'imposent sur les classes (json)
# - Interpreter le json en classes java 

# Import des librairies
import json
import xmltodict
import re
from jinja2 import Template

from typing import List, Dict



# Chargement des données
XML_FILE_PATH = f"./data/class_diagram.drawio"
INITIAL_JSON_FILE_PATH = "./data/json_files/[0] - initial_diagram.json"
STRUCTURED_JSON_FILE_PATH = "./data/json_files/[1] - structured_diagram.json"
INTERPRETED_JSON_FILE_PATH = "./data/json_files/[2] - interpreted_diagram.json"
APP_FOLDER = "./data/generated_app"

# Chemin d'acess aux templates
SIMPLE_JAVA_CLASS_TEMPLATE = "./templates/java/simple_class.html"

with open(XML_FILE_PATH, "r") as xml_file:
    xml_data = xml_file.read()




initial_json_data = xmltodict.parse(xml_data)

# mettre tout en miniscule
initial_json_data_str = json.dumps(initial_json_data).lower()
initial_json_data = json.loads(initial_json_data_str)



# TODO: traiter le json avant de stocker, en outre, retirer le @ sur les ids
# TODO: implementer la gestion des pages multiples
with open(INITIAL_JSON_FILE_PATH, 'w') as initial_json_file:
    diagram = initial_json_data["mxfile"]["diagram"]
    if isinstance(diagram, dict):
        initial_json_file.write(json.dumps(diagram["mxgraphmodel"]["root"]["mxcell"], indent=4))
    elif isinstance(diagram, list):
        initial_json_file.write(json.dumps(diagram[0]["mxgraphmodel"]["root"]["mxcell"], indent=4))


# ## Etape2: Conversion du json initial en json hierarchisé

# helpers
def is_class(object: Dict, sub_root_id: str) -> bool:
    if not object.get("@vertex"):
        return False
    if object.get("@parent") is None or object.get("@parent") != sub_root_id:
        return False
    return True


def is_relation(object: Dict, sub_root_id: str) -> bool:
    if object.get("@parent") is None or object.get("@parent") != sub_root_id:
        return False
    if object.get("@source") is None or object.get("@target") is None:
        return False
    return True


def is_attribute(object: Dict, sub_root_id: str) -> bool:
    if object.get("@parent") is None or object.get("@parent") == sub_root_id:
        return False
    if object.get("@vertex") is None or object.get("@value") is None:
        return False

    return True


def is_method(object: Dict, sub_root_id: str) -> bool:
    if not is_attribute(object, sub_root_id):
        return False
    value: str = object.get("@value")
    if value.find("(") != -1 and value.find(")") != -1:
        return True

    return False

# factories:
def class_factory(object: Dict)->Dict:
    return {
        "name": object.get("@value"),
        "type": "classe",
        "attributes": list(),
        "methods": list()
    }

def attribute_factory(object: Dict)->Dict:
    # TODO: update this to take in account methods
    def parse_value(value:str):
        pattern = r'(?P<visibility>[+#-])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)'
    
        # Recherche des correspondances
        match = re.match(pattern, value)
        if match:
            # Extraction des groupes nommés
            visibility:str = match.group("visibility")
            nom:str = match.group("name")
            type_:str = match.group("type")
            return visibility, nom, type_
        return "+", "name", "void"
    
    value = parse_value(object.get("@value"))
    def interprete_visibility(visibility:str):
        if visibility == "+":
            return "public"
        if visibility == "#":
            return "protected"
        if visibility == "-":
            return "private"
        
    return {
        "visibility": interprete_visibility(value[0]),
        "name": value[1].strip(),
        "type": value[2].strip(),
    }

def method_factory(object: Dict)->Dict:
    def parse_value(value:str):
        pattern = r'(?P<visibility>[+#-])\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*\((?P<args>[a-zA-Z0-9_,\s]*)\)\s*:\s*(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)'
    
        # Recherche des correspondances
        match = re.match(pattern, value)
        if match:
            # Extraction des groupes nommés
            visibility:str = match.group("visibility")
            nom:str = match.group("name")
            args = [arg.strip() for arg in match.group("args").split(",") if arg.strip()]
            type_:str = match.group("type")
            return visibility, nom, type_, args
        return "+", "name","void", []
    
    value = parse_value(object.get("@value"))
    def interprete_visibility(visibility:str):
        if visibility == "+":
            return "public"
        if visibility == "#":
            return "protected"
        if visibility == "-":
            return "private"
        
    return {
        "visibility": interprete_visibility(value[0]),
        "name": value[1].strip(),
        "type": value[2].strip(),
        "args": value[3]
    }
def relationship_factory(object: Dict)->Dict:
    def get_type_and_visibility(style:str):
        # TODO: ecris ceci (analyse pour sortir le type de relation)
        # type, cardinalités
        return "", ""
    
    type_and_multiplicity = get_type_and_visibility(object.get("@style"))
    return {
        "name": object.get("@value"),
        "source": object.get("@source"),
        "target": object.get("@target"),
        "edge": object.get("@edge"),
        "style": object.get("@style"),
        "type": type_and_multiplicity[0],
        "multipliity": type_and_multiplicity[1],
    }


structured_json_data = {"classes": dict(), "relationships": list()}

# charger le json du diagramme
with open(INITIAL_JSON_FILE_PATH, 'r') as initial_json_file:
    initial_json_data: List[Dict] = json.loads(initial_json_file.read())

root_id, sub_root_id = None, None

# reconnaitre le root, et le sub root
for mxcell in initial_json_data:
    if len(mxcell.keys()) == 1:
        root_id = mxcell["@id"]
        continue
    if len(mxcell.keys()) == 2 and mxcell.get("@parent") and mxcell["@parent"] == root_id:
        sub_root_id = mxcell["@id"]
        continue
    if root_id is not None and sub_root_id is not None:
        break

# maintenant on parse les classes et les relations
for mxcell in [*initial_json_data]: 
    if mxcell.get("@id") in [root_id, sub_root_id]:
        initial_json_data.remove(mxcell)
        continue
    if is_class(mxcell, sub_root_id): 
        structured_json_data["classes"][mxcell.get("@id")] = class_factory(mxcell)
        initial_json_data.remove(mxcell)
        continue
    if is_relation(mxcell, sub_root_id):
        structured_json_data["relationships"].append(relationship_factory(mxcell))
        initial_json_data.remove(mxcell)
        continue

# maintenant on parse pour ajouter les attributs aux classes
for mxcell in [*initial_json_data]:
    if is_method(mxcell, sub_root_id):
        initial_json_data.remove(mxcell)
        
        # chercher la classe qui lui correspond
        classes: Dict = structured_json_data.get("classes")
        for class_id in classes.keys():
            # des qu'on trouve la classe on l'y ajoute et on s'arrete
            if class_id == mxcell["@parent"]:
                classes[class_id]["methods"].append(method_factory(mxcell))
                break
        continue


    if is_attribute(mxcell, sub_root_id):
        initial_json_data.remove(mxcell)
        
        # chercher la classe qui lui correspond
        classes: Dict = structured_json_data.get("classes")
        for class_id in classes.keys():
            # des qu'on trouve la classe on l'y ajoute et on s'arrete
            if class_id == mxcell["@parent"]:
                classes[class_id]["attributes"].append(attribute_factory(mxcell))
                break

with open(STRUCTURED_JSON_FILE_PATH, 'w') as structured_json_file:
    structured_json_file.write(json.dumps(structured_json_data, indent=4))

initial_json_data

  
with open(STRUCTURED_JSON_FILE_PATH, 'r') as structured_json_file:
    structured_json_data = json.loads(structured_json_file.read())

with open(INTERPRETED_JSON_FILE_PATH, 'w') as interpreted_json_file:
    interpreted_json_file.write(json.dumps(list(structured_json_data["classes"].values()), indent=4))


with open(INTERPRETED_JSON_FILE_PATH, 'r') as interpreted_json_file:
    interpreted_json_data:Dict = json.loads(interpreted_json_file.read())

# Charger le template pour les classes simples
with open(SIMPLE_JAVA_CLASS_TEMPLATE,  'r') as simple_java_class_template_file:
    simple_java_class_template_str = simple_java_class_template_file.read()
template = Template(simple_java_class_template_str)

for class_ in interpreted_json_data:
    generated_java_code = template.render(class_data=class_)
    
    with open(f"{APP_FOLDER}/{class_['name'].capitalize()}.java", 'w') as generated_java_file:
        generated_java_file.write(generated_java_code)

