from lexer.lexer import Lexer
from pathlib import Path
import json

from semantic_analyzer.semantic_analyzer import SemanticAnalyzer

diagram = Path("0ld/data/class-diagram-example.drawio")
lexer = Lexer(diagram.read_text("utf-8"))
 

result = Path("lexer.json")
lexed = lexer.execute()
result.write_text(json.dumps(lexed))

semantic = SemanticAnalyzer(result.read_text())