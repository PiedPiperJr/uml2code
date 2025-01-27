from typing import Dict, List
from models.attribute_model import Attribute
from models.class_model import Class
from models.arg_model import Arg
from models.project_model import Method
from models.relationship_model import Relationship
from semantic_analyzer.interpreters import Interpreter


class ModelsFactory:

    @staticmethod
    def build_relationship_model(relationship: Dict, structured_data: Dict) -> Relationship:
        return Relationship(relationship['name'],
                            relationship['source'],
                            relationship['target'],
                            Interpreter.interpret_relationship_style(
                                relationship['style']),
                            structured_data['classes'][relationship["source"]]['name'],
                            structured_data['classes'][relationship["target"]]['name'])

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
        return Method(method['name'], args, method['type'], method['visibility'])

    @staticmethod
    def build_class_model(_class: Dict) -> Class:
        attributes: List[Attribute] = []
        for attribute in _class['attributes']:
            attributes.append(ModelsFactory.build_attribute_model(attribute))

        methods: List[Method] = []
        for method in _class['methods']:
            methods.append(ModelsFactory.build_method_model(method))

        return Class(_class['name'], attributes, methods)
