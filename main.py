#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from backend.spring_boot_clean.generator import SpringBootCleanGenerator
from frontend.drawio.drawio_frontend import DrawIOFrontend
from middleend.semantic_analyzer import SemanticAnalyzer
from pipeline.pipeline import Pipeline

TEMPLATE_DIR = Path(__file__).parent / "src" / "backend" / "spring_boot_clean" / "templates"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="uml2code",
        description="ER-to-Spring-Boot-CRUD generator (Clean Architecture)",
    )
    parser.add_argument("input", help="Path to the input diagram file")
    parser.add_argument(
        "--package", required=True,
        help="Java base package (e.g. com.example.myapp)",
    )
    parser.add_argument(
        "--output", required=True,
        help="Root output directory for generated source files",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not input_path.exists():
        print(f"Error: input file '{input_path}' not found", file=sys.stderr)
        sys.exit(1)

    pipeline = Pipeline(
        frontend=DrawIOFrontend(),
        analyzer=SemanticAnalyzer(),
        backend=SpringBootCleanGenerator(TEMPLATE_DIR),
    )

    files = pipeline.run(
        source=input_path.read_text("utf-8"),
        package=args.package,
        output_dir=output_dir,
    )

    print(f"Generated {len(files)} files -> {output_dir}")


if __name__ == "__main__":
    main()
