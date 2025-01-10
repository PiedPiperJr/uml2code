<<<<<<< HEAD
from typing import Dict, List
import google.generativeai as genai

def is_class(object: Dict, sub_root_id: str) -> bool:
    return (
        object.get("@vertex") and
        object.get("@parent") == sub_root_id
    )

def is_relation(object: Dict, sub_root_id: str) -> bool:
    return (
        object.get("@parent") == sub_root_id and
        object.get("@source") and
        object.get("@target")
    )

def is_attribute(object: Dict, sub_root_id: str) -> bool:
    return (
        object.get("@parent") and
        object.get("@parent") != sub_root_id and
        object.get("@vertex") and
        object.get("@value")
    )

def is_method(object: Dict, sub_root_id: str) -> bool:
    if not is_attribute(object, sub_root_id):
        return False
    value: str = object.get("@value", "")
    return "(" in value and ")" in value

def validate_data_types(interpreted_data: Dict | List, api_key: str, language: str = "java") -> None:
    """use google gemini ai for attribute type verification"""

    memory = f"""
                Hello gemini, I'll give you a supposed list of  data types (separated by spaces) in the {language} programming langauge, and you'll return only
                the real data types in this programming language. The response will only contain the typreal types, separated by spaces, with no decorators.
                """
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    chat = model.start_chat(history=[{'role':'user', 'parts':memory}])

    types_dict = {}
    for class_data in interpreted_data:
        # attribute type validation
        for attrib in class_data['attributes']:
            if attrib['type'] in types_dict:
                attrib['type'] = types_dict[attrib['type']]
            else:
                real_type = chat.send_message(attrib['type']).text.strip()
                types_dict[attrib['type']] = real_type
                attrib['type'] = real_type

        # method type validation
        for method in class_data['methods']:
            if method['type'] in types_dict:
                method['type'] = types_dict[method['type']]
            else:
                real_type = chat.send_message(method['type']).text.strip()
                types_dict[method['type']] = real_type
                method['type'] = real_type

            # method arguments validation
            for arg in method['args']:
                if arg['type'] in types_dict:
                    arg['type'] = types_dict[arg['type']]
                else:
                    real_type = chat.send_message(arg['type']).text.strip()
                    types_dict[arg['type']] = real_type
                    arg['type'] = real_type
=======
from typing import Dict, List
import google.generativeai as genai

def is_class(object: Dict, sub_root_id: str) -> bool:
    return (
        object.get("@vertex") and
        object.get("@parent") == sub_root_id
    )

def is_relation(object: Dict, sub_root_id: str) -> bool:
    return (
        object.get("@parent") == sub_root_id and
        object.get("@source") and
        object.get("@target")
    )

def is_attribute(object: Dict, sub_root_id: str) -> bool:
    return (
        object.get("@parent") and
        object.get("@parent") != sub_root_id and
        object.get("@vertex") and
        object.get("@value")
    )

def is_method(object: Dict, sub_root_id: str) -> bool:
    if not is_attribute(object, sub_root_id):
        return False
    value: str = object.get("@value", "")
    return "(" in value and ")" in value

def validate_data_types(interpreted_data: Dict | List, api_key: str, language: str = "java") -> None:
    """use google gemini ai for attribute type verification"""

    memory = f"""
                Hello gemini, I'll give you a supposed data type in the {language} programming langauge, and you'll return only
                the real data type in this programming language. The response will only contain the type, with no decorators.
                """
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[{'role':'user', 'parts':memory}])

    for class_data in interpreted_data:
        for attrib in class_data['attributes']:
            attrib['type'] = chat.send_message(attrib["type"]).text.strip()

        for method in class_data['methods']:
            method['type'] = chat.send_message(method['type']).text.strip()
            for arg in method['args']:
                arg['type'] = chat.send_message(arg['type']).text.strip()
>>>>>>> d598bcdb5763c0553a737c71d46b5b100a15560d
