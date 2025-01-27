
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
            "name": mxcell.get("@value"),
            "source": mxcell.get("@source"),
            "target": mxcell.get("@target"),
            "edge": mxcell.get("@edge"),
            "style": mxcell.get("@style"),
            "type": "",
            "multiplicity": ""
        }

    @staticmethod
    def create_attribute_structure(visibility: str, name: str, type_: str):
        return {
            # TODO do this in semantic analysis

            # "visibility": Parsers.interpret_visibility(visibility),
            "visibility": visibility,
            "name": name.strip(),
            "type": type_.strip()
        }

    @staticmethod
    def create_method_structure(visibility: str, name: str, type_: str, args: List[str]):
        return {
            # TODO do this in semantic analysis
            # "visibility": Parsers.interpret_visibility(visibility),
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