import json
import xmltodict
from typing import Dict, List, Tuple
from helpers.utils import Utils
from lexer.validators import Validators
from lexer.factories import Factories
from lexer.parsers import Parsers


class Lexer:

    def __init__(self, xml_data: str):
        self.xml_data = xml_data
        self.initial_json_data: List[Dict] = list()
        self.structured_data = dict()
        self.root_id = None
        self.sub_root_id = None

    def execute(self):
        self.convert_xml_to_json()
        self.convert_json_to_structure()
        
        return self.structured_data

    def convert_xml_to_json(self) -> None:
        initial_json_data = xmltodict.parse(self.xml_data)

        # Conversion des clés en minuscules
        initial_json_data = Utils.lowercase_keys(initial_json_data)

        # Extraction du diagramme
        diagram = initial_json_data["mxfile"]["diagram"]
        if isinstance(diagram, dict):
            self.initial_json_data = diagram["mxgraphmodel"]["root"]["mxcell"]
            return
        elif isinstance(diagram, list):
            self.initial_json_data = diagram[0]["mxgraphmodel"]["root"]["mxcell"]
            return

        raise "No diagram detected during the xml to json conversion"
    
    def convert_json_to_structure(self) -> Dict:
        """Convertit le JSON initial en structure hiérarchique"""
        self.structured_data = {"classes": {}, "relationships": []}
        self.root_id, self.sub_root_id = self._find_root_ids(self.initial_json_data)
        
        # Premier passage : classes et relations
        remaining_cells = []
        for mxcell in self.initial_json_data:
            if mxcell.get("@id") in [self.root_id, self.sub_root_id]:
                continue
                
            if Validators.is_class(mxcell, self.sub_root_id):
                self.structured_data["classes"][mxcell.get("@id")] = Factories.create_class_structure(mxcell)
            elif Validators.is_relation(mxcell, self.sub_root_id):
                relationship = Factories.create_relationship_structure(mxcell)
                self._fix_relationship_attribs(relationship, self.initial_json_data)

                self.structured_data["relationships"].append(relationship)
            else:
                remaining_cells.append(mxcell)
        
        # Deuxième passage : attributs et méthodes
        for mxcell in remaining_cells:
            parent_id = mxcell.get("@parent")
            if parent_id not in self.structured_data["classes"]:
                continue
                
            if Validators.is_method(mxcell, self.sub_root_id):
                visibility, name, type_, _args = Parsers.parse_method_value(mxcell.get("@value", ""))
                args = []
                for arg in _args:
                    args.append(Factories.create_arg_structure(arg))

                method = Factories.create_method_structure(visibility, name, type_, args)
                self.structured_data["classes"][parent_id]["methods"].append(method)

            elif Validators.is_attribute(mxcell, self.sub_root_id):
                visibility, name, type_ = Parsers.parse_attribute_value(mxcell.get("@value", ""))
                attribute = Factories.create_attribute_structure(visibility, name, type_)
                self.structured_data["classes"][parent_id]["attributes"].append(attribute)
        

    def _find_root_ids(self, json_data: List[Dict]) -> Tuple[str, str]:
        """Trouve les IDs root et sub_root"""
        self.root_id = next((cell["@id"] for cell in json_data if len(cell.keys()) == 1), None)
        self.sub_root_id = next((cell["@id"] for cell in json_data 
                        if len(cell.keys()) == 2 and cell.get("@parent") == self.root_id), None)
        return self.root_id, self.sub_root_id
    
    def _fix_relationship_attribs(self, relationship: Dict, initial_json_data: List[Dict]) -> None:
        # fix bad source and target in relationships 
        for mxcell in initial_json_data:
            parent = mxcell.get('@parent')
            if not Validators.is_class(mxcell, self.sub_root_id):
                if relationship['source'].lower() == mxcell.get('@id') :
                    relationship['source'] = parent if not parent is None else relationship['source']

            if not Validators.is_class(mxcell, self.sub_root_id):
                if relationship['target'].lower() == mxcell.get('@id'):
                    relationship['target'] = parent if not parent is None else relationship['target']
        
        