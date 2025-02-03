from code_generator.clean.clean_code_generator import CleanCodeGenerator
from code_generator.pojo.pojo_code_generator import PoJoCodeGenerator
from lexer.lexer import Lexer
from pathlib import Path
import json

from models.project_model import Project
from semantic_analyzer.semantic_analyzer import SemanticAnalyzer
import os
import shutil


def main():

    diagram = Path("data/class-diagram-example.drawio")
    lexer = Lexer(diagram.read_text("utf-8"))

    result = Path("lexer.json")
    lexer_result = lexer.execute()
    result.write_text(json.dumps(lexer_result))

    semantic_analyzer = SemanticAnalyzer(lexer_result)
    classes = semantic_analyzer.execute()

    pojo_generator = PoJoCodeGenerator(
        classes, "templates/java/simple_class.html", "out")

    pojo_generator.execute()

    project = Project("org.enspy.snappy.server", classes, [])
    shutil.rmtree("demo\src\main\java\org\enspy\snappy\server\domain")
    shutil.rmtree("demo\src\main\java\org\enspy\snappy\server\infrastructure")
    shutil.rmtree("demo\src\main\java\org\enspy\snappy\server\presentation")
    clean_generator = CleanCodeGenerator(
        project, "templates/java-clean", "demo\src\main\java\org\enspy\snappy\server")

    clean_generator.execute()


"""pom.xml

        <dependency>
            <groupId>com.fasterxml.jackson.datatype</groupId>
            <artifactId>jackson-datatype-jsr310</artifactId>
            <version>2.17.2</version>
        </dependency>
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>2.5.0</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-core</artifactId>
        </dependency>
"""


if __name__ == '__main__':
    main()
