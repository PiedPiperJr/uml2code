import google.generativeai as genai
from typing import Dict, List, Optional

from helpers.utils import Utils
from models.class_model import Class
from models.relationship_model import Relationship, RelationshipType
from semantic_analyzer.interpreters import Interpreter
from semantic_analyzer.validators import SemanticValidator
from semantic_analyzer.models_factory import ModelsFactory


class SemanticAnalyzer:

    def __init__(self, structured_json_data: Dict, api_key: Optional[str] = None, language: Optional[str] = "java"):
        self.api_key = api_key
        self.language = language
        self.structured_data = structured_json_data

    def execute(self):
        classes = self.build_classes()
        Interpreter.interpret_visibility(classes)

        if not self.api_key is None:
            SemanticValidator.verify_types(
                classes, self.api_key, self.language)

        relationships = self.build_relationships()
        Interpreter.interpret_relationships(classes, relationships)

        return classes

    def build_relationships(self) -> List[Relationship]:
        relationships: List[Relationship] = list()
        for relationship in self.structured_data['relationships']:
            relationships.append(ModelsFactory.build_relationship_model(
                relationship, self.structured_data))

        return relationships

    def build_classes(self) -> List[Class]:
        classes: List[Class] = list()
        for _class in self.structured_data["classes"].values():
            classes.append(ModelsFactory.build_class_model(_class))

        return classes

    
