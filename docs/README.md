# uml2code — ER-to-Spring-Boot-CRUD Generator

## Table of contents

1. [What this project is](#1-what-this-project-is)
2. [Architecture overview](#2-architecture-overview)
3. [Component reference](#3-component-reference)
   - [Frontend (Lexer + Parser)](#31-frontend-lexer--parser)
   - [Middle-end (Semantic Analyzer)](#32-middle-end-semantic-analyzer)
   - [Backend (Generator + Templates)](#33-backend-generator--templates)
   - [Core (IR + Ports)](#34-core-ir--ports)
   - [Pipeline](#35-pipeline)
   - [Helpers](#36-helpers)
4. [Intermediate representations](#4-intermediate-representations)
5. [Generated Java code structure](#5-generated-java-code-structure)
6. [Usage](#6-usage)
7. [Extending the project](#7-extending-the-project)
   - [Adding a new input format](#71-adding-a-new-input-format)
   - [Adding a new output target](#72-adding-a-new-output-target)

---

## 1. What this project is

`uml2code` is an **ER-diagram-to-Spring-Boot-CRUD code generator**.

It reads a draw.io file that describes entities and their relationships (inheritance, composition, aggregation, association), then generates a fully compilable **Spring Boot 3 + Java 21** application exposing a REST CRUD API for every entity.

> **Scope note**: The input format is specifically ER-style class diagrams drawn in draw.io. The generator is not a general-purpose UML transpiler — it models entities and relationships, not use cases, sequences, or state machines.

---

## 2. Architecture overview

The project follows a **compiler/transpiler architecture**, divided into three clearly separated stages:

```
┌─────────────────────────────────────────────────────────────────┐
│                        PIPELINE                                 │
│                                                                 │
│  ┌──────────────┐    ┌───────────────┐    ┌─────────────────┐  │
│  │   FRONTEND   │    │  MIDDLE-END   │    │    BACKEND      │  │
│  │              │    │               │    │                 │  │
│  │  DrawIOLexer │───▶│   Semantic    │───▶│  SpringBoot     │  │
│  │  DrawIOParser│    │   Analyzer    │    │  Generator      │  │
│  └──────────────┘    └───────────────┘    └─────────────────┘  │
│         │                   │                     │             │
│       (cells)           ERDiagram             ProjectIR         │
│                         (AST)            (target-agnostic IR)   │
└─────────────────────────────────────────────────────────────────┘
```

Each stage communicates through a **typed intermediate representation (IR)**:

| Stage | Input | Output |
|---|---|---|
| Frontend | Raw draw.io XML source | `ERDiagram` (source AST) |
| Middle-end | `ERDiagram` | `ProjectIR` (target-agnostic IR) |
| Backend | `ProjectIR` | Java source files on disk |

Each end is hidden behind an abstract port interface (`IFrontend`, `IBackend`), making new input formats and output targets independently addable without touching any existing code.

---

## 3. Component reference

### 3.1 Frontend (Lexer + Parser)

**Location:** `frontend/drawio/`

The frontend is responsible for reading a raw draw.io XML file and producing a typed AST (`ERDiagram`) that represents the diagram content in a source-format-agnostic way.

It is split into two classes following the classic compiler frontend pattern:

#### `DrawIOLexer` (`frontend/drawio/lexer.py`)

Tokenizes the draw.io XML source into a flat list of raw `mxCell` dictionaries. This is a pure structural transformation — no interpretation is done here.

```
draw.io XML  ──▶  [mxCell, mxCell, mxCell, ...]
```

Key behaviors:
- Uses `xmltodict` to parse XML into Python dicts
- Normalizes all keys to lowercase to handle draw.io's mixed-case attribute names
- Handles both single-diagram and multi-diagram `mxfile` structures
- Flattens the cell list so downstream code never needs to navigate XML structure

#### `DrawIOParser` (`frontend/drawio/parser.py`)

Interprets the flat cell list and builds an `ERDiagram` AST in three passes:

**Pass 1 — Entity extraction**: Identifies cells that are direct children of the diagram root and have a `vertex` attribute. Each becomes an `EREntity`.

**Pass 2 — Field and method extraction**: Identifies cells whose parent is a known entity. Parses their `value` attribute using regexes:
- `+ fieldName: Type` → `ERField`
- `+ methodName(params): ReturnType` → `ERMethod`
- Supports generic types: `List<String>`, `Map<K, V>`, `Optional<T>`, etc.

**Pass 3 — Relationship extraction**: Identifies cells with both `source` and `target` attributes. Resolves each endpoint to an entity by walking the parent chain (O(1) cell index lookup). Interprets the arrow style to classify the relationship:

| draw.io style | Relationship kind |
|---|---|
| `endArrow=block` | INHERITANCE |
| `endArrow=diamondThin` + `endFill=1` | COMPOSITION |
| `endArrow=diamondThin` + `endFill=0` | AGGREGATION |
| `endArrow=open/classic/classicThin` | ASSOCIATION |

---

### 3.2 Middle-end (Semantic Analyzer)

**Location:** `middleend/semantic_analyzer.py`

The semantic analyzer transforms the source-specific `ERDiagram` into a `ProjectIR` that is completely independent of both the input format and the output target.

Responsibilities:
- Converts each `EREntity` into an `IREntity`
- Normalizes Java type aliases: `string → String`, `int → Integer`, `bool → Boolean`, `datetime → LocalDateTime`, `uuid → UUID`, etc.
- Applies relationships to the IR entities:
  - `INHERITANCE` → sets `IREntity.parent`
  - `COMPOSITION` → appends to `IREntity.compositions`
  - `AGGREGATION` / `ASSOCIATION` → appends to `IREntity.aggregations`

The resulting `ProjectIR` carries no trace of draw.io and could be fed to any backend (Spring Boot, Django, NestJS, etc.).

---

### 3.3 Backend (Generator + Templates)

**Location:** `backend/spring_boot/`

The backend takes a `ProjectIR` and produces Java source files using Jinja2 templates.

#### `SpringBootGenerator` (`backend/spring_boot/generator.py`)

- Initializes a Jinja2 `Environment` with `FileSystemLoader` pointing at the `templates/` directory
- Uses `StrictUndefined` so any undefined template variable raises an error immediately rather than silently rendering empty
- Registers two custom Jinja2 filters:
  - `lower_first`: lowercases only the first character (`Person → person`)
  - `pkg_path`: converts a Java package to a directory path (`com.example.app → com/example/app`)
- Generates **8 files per entity** and **4 global files** (see section 5)

#### Templates (`backend/spring_boot/templates/`)

All templates use the `.j2` extension and are organized by Java layer:

```
templates/
├── domain/
│   ├── entity.j2                          # JPA entity class
│   ├── repository_port.j2                 # Driven port interface
│   ├── service_port.j2                    # Driving port interface
│   └── exceptions/
│       ├── base_not_found.j2              # EntityNotFoundException (base)
│       ├── base_already_exists.j2         # EntityAlreadyExistsException (base)
│       ├── entity_not_found.j2            # {Entity}NotFoundException
│       └── entity_already_exists.j2       # {Entity}AlreadyExistsException
├── infrastructure/
│   ├── jpa_repository.j2                  # Spring Data JPA repository
│   ├── service_impl.j2                    # CRUD service implementation
│   └── jackson_config.j2                  # ObjectMapper with JavaTimeModule
└── presentation/
    ├── controller.j2                      # REST controller
    └── global_exception_handler.j2        # @RestControllerAdvice
```

Template context variables available in every template:

| Variable | Type | Description |
|---|---|---|
| `ir` | `ProjectIR` | The full project IR (package name, all entities) |
| `entity` | `IREntity` | The current entity (absent in global templates) |

Key template behaviors:
- `entity.is_root` is `True` when the entity has no parent. Only root entities get `@Id`, `@GeneratedValue`, `createdAt`, and `updatedAt` fields (correct JPA Single-Table Inheritance behavior).
- Compositions generate `@OneToMany(cascade = ALL, orphanRemoval = true)` with a join column.
- Aggregations/associations generate `@ManyToOne(fetch = LAZY)` with a join column.
- `service_impl.j2` preserves `createdAt` on `PUT` by copying it from the existing entity before saving.
- `jackson_config.j2` registers `JavaTimeModule` globally so `LocalDateTime` fields serialize as ISO strings, not timestamps.

---

### 3.4 Core (IR + Ports)

**Location:** `core/`

Contains the two intermediate representations and the abstract port interfaces. This package has **zero dependencies** on any specific frontend or backend.

#### `core/ir/er_diagram.py` — Source AST

Typed representation of what was read from the input diagram. Mirrors the source language concepts:

```
ERDiagram
├── entities: dict[id → EREntity]
│   ├── id: str
│   ├── name: str
│   ├── fields: list[ERField]     # name, type, visibility
│   └── methods: list[ERMethod]   # name, return_type, params
└── relationships: list[ERRelationship]
    ├── source_id: str
    ├── target_id: str
    ├── kind: RelationshipKind     # INHERITANCE | COMPOSITION | AGGREGATION | ASSOCIATION
    └── label: str
```

#### `core/ir/project_ir.py` — Target-agnostic IR

Typed representation passed to the backend. Contains only what any code generator needs:

```
ProjectIR
├── package: str
└── entities: list[IREntity]
    ├── name: str
    ├── fields: list[IRField]       # name, type, visibility
    ├── parent: IREntity | None     # set by INHERITANCE relationship
    ├── compositions: list[IREntity]
    ├── aggregations: list[IREntity]
    └── is_root: bool (property)    # True when parent is None
```

#### `core/ports/frontend_port.py` — `IFrontend`

```python
class IFrontend(ABC):
    @abstractmethod
    def parse(self, source: str) -> ERDiagram: ...
```

Any new input format (PlantUML, Mermaid, etc.) implements this interface and is immediately usable by the pipeline.

#### `core/ports/backend_port.py` — `IBackend`

```python
class IBackend(ABC):
    @abstractmethod
    def generate(self, ir: ProjectIR) -> list: ...

    @abstractmethod
    def write(self, files: list, output_dir: Path) -> None: ...
```

Any new output target (Django, NestJS, FastAPI, etc.) implements this interface.

---

### 3.5 Pipeline

**Location:** `pipeline/pipeline.py`

Thin orchestrator that wires the three stages together:

```python
@dataclass
class Pipeline:
    lexer: DrawIOLexer
    parser: DrawIOParser
    analyzer: SemanticAnalyzer
    generator: SpringBootGenerator

    def run(self, source, package, output_dir) -> list[GeneratedFile]:
        cells   = self.lexer.tokenize(source)
        diagram = self.parser.parse(cells)
        ir      = self.analyzer.analyze(diagram, package)
        files   = self.generator.generate(ir)
        self.generator.write(files, output_dir)
        return files
```

The pipeline has no logic of its own — it only defines the execution order. Swapping a frontend or backend means changing the types injected at construction.

---

### 3.6 Helpers

**Location:** `helpers/utils.py`

Stateless utility functions shared across all stages:

| Function | Description |
|---|---|
| `lowercase_keys(data)` | Recursively lowercases all dict keys (used by the lexer to normalize draw.io attributes) |
| `capitalize(s)` | Uppercases the first character only |
| `lower_first(s)` | Lowercases the first character only |
| `snake_to_pascal(s)` | Converts `snake_case` to `PascalCase` |

---

## 4. Intermediate representations

### Why two IRs?

The `ERDiagram` (source AST) is **source-language-specific**: it contains draw.io concepts like cell IDs, visibility symbols, and raw type strings. It is not suitable for code generation because a PlantUML frontend would produce a different AST.

The `ProjectIR` is **target-agnostic**: it contains only normalized, backend-ready information. A Spring Boot generator and a Django generator can both consume the same `ProjectIR` without any changes.

```
draw.io XML ──▶ ERDiagram  ──▶  ProjectIR  ──▶  Java files
PlantUML   ──▶ ERDiagram  ──/
Mermaid    ──▶ ERDiagram  ──/               \──▶  Python files
                                             \──▶  NestJS files
```

---

## 5. Generated Java code structure

For a given `--package com.example.myapp`, the generator produces:

```
com/example/myapp/
│
├── domain/
│   ├── entities/
│   │   └── {Entity}.java                     # JPA entity (@Entity, @Getter, @Setter, ...)
│   ├── ports/
│   │   ├── driven/
│   │   │   └── I{Entity}Repository.java      # Driven port (data access interface)
│   │   └── driving/
│   │       └── I{Entity}Service.java         # Driving port (business logic interface)
│   └── exceptions/
│       ├── EntityNotFoundException.java       # Base exception (404)
│       ├── EntityAlreadyExistsException.java  # Base exception (422)
│       ├── {Entity}NotFoundException.java     # Entity-specific (404)
│       └── {Entity}AlreadyExistsException.java
│
├── infrastructure/
│   ├── adapters/
│   │   ├── persistence/
│   │   │   └── {Entity}Repository.java       # JPA adapter (extends JpaRepository + driven port)
│   │   └── services/
│   │       └── {Entity}ServiceImpl.java      # Service adapter (implements driving port)
│   └── config/
│       └── JacksonConfig.java                # ObjectMapper with JavaTimeModule
│
└── presentation/
    └── rest/
        ├── {Entity}Controller.java            # REST controller (CRUD endpoints)
        └── GlobalExceptionHandler.java        # @RestControllerAdvice (404, 422, 500)
```

### Hexagonal architecture of the generated code

The generated application follows **Hexagonal Architecture (Ports & Adapters)**:

```
┌─────────────────────────────────────────────────────┐
│                    DOMAIN                           │
│                                                     │
│   Entities          Driving ports   Driven ports    │
│   (JPA classes)  ◀──I{E}Service  ──I{E}Repository   │
└──────────────────────────┬──────────────┬───────────┘
                           │              │
          ┌────────────────▼──┐    ┌──────▼──────────────┐
          │   PRESENTATION    │    │   INFRASTRUCTURE     │
          │                   │    │                      │
          │  {E}Controller    │    │  {E}ServiceImpl      │
          │  (REST adapter)   │    │  {E}Repository       │
          │                   │    │  (JPA adapter)       │
          └───────────────────┘    └──────────────────────┘
```

- **Driving ports** (`I{Entity}Service`): define what the application can do — called by the controllers
- **Driven ports** (`I{Entity}Repository`): define what the application needs — implemented by JPA repositories
- **Domain entities** know nothing about Spring, JPA adapters, or HTTP — they only declare their fields and relationships

---

## 6. Usage

### Prerequisites

```bash
pip install -r requirements.txt
# Python 3.10+ required (uses match statements and PEP 604 union types)
```

### Run the generator

```bash
python3 main.py <path-to-diagram.drawio> --package <java.package> --output <output-dir>
```

**Example:**

```bash
python3 main.py data/class-diagram-example.drawio \
    --package org.enspy.snappy.server \
    --output /tmp/generated-app
```

The generator prints the number of files created and exits.

### Compile and run the generated app

The generated source files must be placed inside a Spring Boot project. Copy them into `src/main/java/`:

```bash
cp -r /tmp/generated-app/* existing-spring-boot-project/src/main/java/

cd existing-spring-boot-project
./mvnw spring-boot:run
```

Swagger UI is available at: `http://localhost:8080/swagger-ui/index.html`

---

## 7. Extending the project

### 7.1 Adding a new input format

To support PlantUML, Mermaid, or any other ER notation, you only need to implement the `IFrontend` port. No existing code changes.

**Step 1** — Create `frontend/plantuml/lexer.py`:
```python
class PlantUMLLexer:
    def tokenize(self, source: str) -> list:
        # tokenize PlantUML syntax into a list of raw tokens
        ...
```

**Step 2** — Create `frontend/plantuml/parser.py`:
```python
from core.ir.er_diagram import ERDiagram
from core.ports.frontend_port import IFrontend

class PlantUMLParser(IFrontend):
    def parse(self, source: str) -> ERDiagram:
        # build ERDiagram from PlantUML tokens
        ...
```

**Step 3** — Wire it in `main.py`:
```python
pipeline = Pipeline(
    lexer=PlantUMLLexer(),
    parser=PlantUMLParser(),
    analyzer=SemanticAnalyzer(),
    generator=SpringBootGenerator(TEMPLATE_DIR),
)
```

The middle-end and backend are unchanged.

---

### 7.2 Adding a new output target

To generate Django models, a NestJS app, or any other target, implement the `IBackend` port and write the corresponding templates.

**Step 1** — Create `backend/django/generator.py`:
```python
from core.ir.project_ir import ProjectIR
from core.ports.backend_port import IBackend

class DjangoGenerator(IBackend):
    def generate(self, ir: ProjectIR) -> list:
        # render Jinja2 templates for Django models, views, urls, etc.
        ...

    def write(self, files, output_dir):
        ...
```

**Step 2** — Add templates under `backend/django/templates/`.

**Step 3** — Wire it in `main.py`:
```python
pipeline = Pipeline(
    lexer=DrawIOLexer(),
    parser=DrawIOParser(),
    analyzer=SemanticAnalyzer(),
    generator=DjangoGenerator(DJANGO_TEMPLATE_DIR),
)
```

The frontend and middle-end are unchanged.
