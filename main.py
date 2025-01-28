from code_generator.clean.clean_code_generator import CleanCodeGenerator
from code_generator.pojo.pojo_code_generator import PoJoCodeGenerator
from lexer.lexer import Lexer
from pathlib import Path
import json

from models.project_model import Project
from semantic_analyzer.semantic_analyzer import SemanticAnalyzer


def main():

    diagram = Path("0ld/data/class-diagram-example.drawio")
    lexer = Lexer(diagram.read_text("utf-8"))
    

    result = Path("lexer.json")
    lexer_result = lexer.execute()
    result.write_text(json.dumps(lexer_result))

    semantic_analyzer = SemanticAnalyzer(lexer_result)
    classes = semantic_analyzer.execute()

    pojo_generator = PoJoCodeGenerator(classes, "0ld/templates/java/simple_class.html", "out")
    
    pojo_generator.execute()
    # print(classes)

    project = Project("mwm", classes, [])
    clean_generator = CleanCodeGenerator(project, "templates/java-clean", "out_clean")
    clean_generator.execute()


if __name__ == '__main__':
    main()