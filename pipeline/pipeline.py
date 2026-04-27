from dataclasses import dataclass
from pathlib import Path

from backend.spring_boot.generator import GeneratedFile, SpringBootGenerator
from frontend.drawio.lexer import DrawIOLexer
from frontend.drawio.parser import DrawIOParser
from middleend.semantic_analyzer import SemanticAnalyzer


@dataclass
class Pipeline:
    lexer: DrawIOLexer
    parser: DrawIOParser
    analyzer: SemanticAnalyzer
    generator: SpringBootGenerator

    def run(self, source: str, package: str, output_dir: Path) -> list[GeneratedFile]:
        cells   = self.lexer.tokenize(source)
        diagram = self.parser.parse(cells)
        ir      = self.analyzer.analyze(diagram, package)
        files   = self.generator.generate(ir)
        self.generator.write(files, output_dir)
        return files
