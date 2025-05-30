
from typing import Dict, List


class Factories:
    @staticmethod
    def create_class_structure(mxcell: Dict) -> Dict:
        return {
            "name": mxcell.get("@value"),
            "type": "class",
            "attributes": [],
            "methods": []
        }

    @staticmethod
    def create_relationship_structure(mxcell: Dict) -> Dict:
        return {
            "id": mxcell.get("@id"),
            "name": mxcell.get("@value"),
            "source": mxcell.get("@source"),
            "target": mxcell.get("@target"),
            "edge": mxcell.get("@edge"),
            "vertex": mxcell.get("@vertex"),
            "style": mxcell.get("@style"),
            "args":[],
            "type": "",
            "multiplicity": "",
            "source_role": None,
            "target_role": None,
            "source_multiplicity": None,
            "target_multiplicity": None,
            "edge_labels": [],
            "is_navigable_to_source": False,
            "is_navigable_to_target": False
        }

    @staticmethod
    def create_attribute_structure(visibility: str, name: str, type_: str):
        return {
            "visibility": visibility,
            "name": name.strip(),
            "type": type_.strip()
        }

    @staticmethod
    def create_method_structure(visibility: str, name: str, type_: str, args: List[str]):
        return {
            "visibility": visibility,
            "name": name.strip(),
            "type": type_.strip(),
            "args": args
        }

    @staticmethod
    def create_arg_structure(arg: str):
        values = arg.strip().split()
        if len(values) >= 2:
            return {'type':values[0], 'name':values[1]}
        else:
            return {'type':'Object', 'name':values[0]}