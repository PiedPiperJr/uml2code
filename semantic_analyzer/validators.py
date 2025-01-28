from typing import Dict, List
import google.generativeai as genai

from models.class_model import Class


class SemanticValidator:

    @staticmethod
    def verify_types(classes: List[Class], api_key: str, language: str = "java") -> List[Class]:
        memory = f"""
                    Hello gemini, I'll give you a supposed data type in the {language} programming langauge, and you'll return only
                    the real data type in this programming language. The response will only contain the type, with no decorators.
                    """

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash-8b")
        chat = model.start_chat(history=[{'role': 'user', 'parts': memory}])
        types_dict = {}
        for _class in classes:
            # attribute type validation
            for attrib in _class.attributes:
                if attrib._type in types_dict:
                    attrib._type = types_dict[attrib._type]
                else:
                    real_type = chat.send_message(attrib._type).text.strip()
                    types_dict[attrib._type] = real_type
                    attrib._type = real_type

            # method type validation
            for method in _class.methods:
                if method._type in types_dict:
                    method._type = types_dict[method._type]
                else:
                    real_type = chat.send_message(method._type).text.strip()
                    types_dict[method._type] = real_type
                    method._type = real_type

                # method arguments validation
                for arg in method.args:
                    if arg._type in types_dict:
                        arg._type = types_dict[arg._type]
                    else:
                        real_type = chat.send_message(arg._type).text.strip()
                        types_dict[arg._type] = real_type
                        arg._type = real_type

        return classes
