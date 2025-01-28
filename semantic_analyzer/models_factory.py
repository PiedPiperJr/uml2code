from typing import Dict, List
from models.attribute_model import Attribute
from models.class_model import Class
from models.arg_model import Arg
from models.method_model import Method
from models.relationship_model import Relationship


class ModelsFactory:

    @staticmethod
    def build_relationship_model(relationship: Dict, structured_data: Dict) -> Relationship:
        return Relationship(relationship['name'],
                            relationship['source'],
                            relationship['target'],
                            relationship['_type'],
                            ModelsFactory._get_class_name_by_id(
                                structured_data, relationship["source"]),
                            ModelsFactory._get_class_name_by_id(structured_data, relationship["target"]))

    @staticmethod
    def _get_class_name_by_id(structured_data: Dict, id: str) -> str:
        for class_id in structured_data['classes'].keys():
            if class_id == id:
                return structured_data['classes'][class_id]['name']
            
        return ""

    @staticmethod
    def build_arg_model(arg: Dict) -> Arg:
        return Arg(arg['name'], arg['type'])

    @staticmethod
    def build_attribute_model(attribute: Dict) -> Attribute:
        return Attribute(attribute['visibility'],
                         attribute['name'],
                         attribute['type'])

    @staticmethod
    def build_method_model(method: Dict) -> Method:
        args: List[Arg] = []
        for arg in method['args']:
            args.append(ModelsFactory.build_arg_model(arg))
        return Method(method['visibility'], method['name'], method['type'], args)

    @staticmethod
    def build_class_model(_class: Dict) -> Class:
        attributes: List[Attribute] = []
        for attribute in _class['attributes']:
            attributes.append(ModelsFactory.build_attribute_model(attribute))

        methods: List[Method] = []
        for method in _class['methods']:
            methods.append(ModelsFactory.build_method_model(method))

        return Class(_class['name'], attributes, methods, [], [], None)
