<<<<<<< HEAD
from typing import List, Dict
from models.relationship_model import *
from utils.parsers import parse_relationship_type, extract_class_name_by_id


def extract_relationships(structured_data: Dict) -> List[Relationship]:
    relationships : List[Relationship] = list()
    for relationship in structured_data['relationships']:
        relationships.append(Relationship(relationship['name'],
                                            relationship['source'],
                                            relationship['target'],
                                            parse_relationship_type(relationship['style']),
                                            extract_class_name_by_id(structured_data, relationship["source"]), 
                                            extract_class_name_by_id(structured_data, relationship["target"])))

=======
from typing import List, Dict
from models.relationship_model import *
from utils.parsers import parse_relationship_type, extract_class_name_by_id


def extract_relationships(structured_data: Dict) -> List[Relationship]:
    relationships : List[Relationship] = list()
    for relationship in structured_data['relationships']:
        relationships.append(Relationship(relationship['name'],
                                            relationship['source'],
                                            relationship['target'],
                                            parse_relationship_type(relationship['style']),
                                            extract_class_name_by_id(structured_data, relationship["source"]), 
                                            extract_class_name_by_id(structured_data, relationship["target"])))

>>>>>>> d598bcdb5763c0553a737c71d46b5b100a15560d
    return relationships