import json
import xmltodict
from typing import Dict

def convert_xml_to_json(xml_data: str) -> Dict:
    """Convertit les données XML en JSON initial"""
    initial_json_data = xmltodict.parse(xml_data)
    
    # Conversion en minuscules
    initial_json_data_str = json.dumps(initial_json_data).lower()
    initial_json_data = json.loads(initial_json_data_str)
    
    # Extraction du diagramme
    diagram = initial_json_data["mxfile"]["diagram"]
    if isinstance(diagram, dict):
        return diagram["mxgraphmodel"]["root"]["mxcell"]
    elif isinstance(diagram, list):
        return diagram[0]["mxgraphmodel"]["root"]["mxcell"]
    
    return {}