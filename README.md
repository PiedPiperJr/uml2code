# uml2code

> Draw an ER diagram. Get a production-ready backend.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-blueviolet)](https://piedpiperjr.github.io/uml2code)

**uml2code** is a diagram-to-code transpiler built around a compiler architecture.  
It reads an entity-relationship diagram and generates a fully functional, compilable backend with CRUD operations for every entity — no boilerplate, no scaffolding by hand.

```
draw.io diagram  ──▶  uml2code  ──▶  Spring Boot 3 / Clean Architecture / Java 21
```

The architecture is designed so that **input formats** and **output targets** are fully interchangeable. Any diagram notation and any framework can be plugged in without touching the core.

---

## Features

- **Clean Architecture** output — Domain, Application, Infrastructure, Presentation, strict dependency rules
- **5 CRUD endpoints** per entity out of the box (POST, GET, paginated GET, PUT, DELETE)
- **Relationships** — inheritance, composition, aggregation mapped to JPA + domain model
- **OpenAPI / Swagger UI** auto-generated via springdoc
- **MapStruct + Lombok** — zero manual mapping code
- **Extensible** — add a new input format or output target by implementing one interface

---

## Quick start

**Prerequisites:** Python 3.10+, Java 21, Maven 3.8+

```bash
# Install dependencies
pip install -r requirements.txt

# Generate Java sources from a draw.io diagram
python3 main.py data/class-diagram-example.drawio \
    --package com.example.myapp \
    --output /tmp/generated
```

### Automated bootstrap (download → patch → generate → compile)

```bash
cd examples/spring_boot

bash setup.sh          # install Java 21 + Maven (once)

bash init.sh \
  --diagram ../../data/class-diagram-example.drawio \
  --package com.example.server \
  --app-name my-server \
  --port 8080

cd my-server && ./mvnw spring-boot:run
```

Open **http://localhost:8080/swagger-ui/index.html**

---

## Project structure

```
uml2code/
├── src/
│   ├── core/               # IR definitions + abstract port interfaces
│   ├── frontend/           # Input parsers (draw.io built-in)
│   ├── middleend/          # Semantic analyzer (format-agnostic)
│   ├── backend/            # Code generators (Spring Boot Clean built-in)
│   ├── pipeline/           # Thin orchestrator wiring the three stages
│   └── helpers/            # Shared utilities
├── data/                   # Example diagrams
├── examples/spring_boot/   # init.sh + setup.sh bootstrap scripts
├── docs/                   # MkDocs documentation source
└── main.py                 # CLI entry point
```

---

## Extending

Add a new **input format** (PlantUML, Mermaid, …) → implement `IFrontend`  
Add a new **output target** (Django, NestJS, Laravel, …) → implement `IBackend`

No existing code changes. See the **[documentation](https://piedpiperjr.github.io/uml2code)** for a step-by-step guide.

---

## Documentation

```bash
mkdocs serve        # local preview → http://localhost:8000
mkdocs gh-deploy    # publish to GitHub Pages
```

---

## License

[MIT](LICENSE) © 2024 PiedPiperJr
