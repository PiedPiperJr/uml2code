# uml2code — ER Diagram to Code Generator

## Table of contents

1. [What this project is](#1-what-this-project-is)
2. [Architecture overview](#2-architecture-overview)
3. [Component reference](#3-component-reference)
   - [Core (IR + Ports)](#31-core-ir--ports)
   - [Frontend](#32-frontend)
   - [Middle-end (Semantic Analyzer)](#33-middle-end-semantic-analyzer)
   - [Backend](#34-backend)
   - [Pipeline](#35-pipeline)
   - [Helpers](#36-helpers)
4. [Intermediate representations](#4-intermediate-representations)
5. [The draw.io frontend (built-in implementation)](#5-the-drawio-frontend-built-in-implementation)
6. [The Spring Boot backend (built-in implementation)](#6-the-spring-boot-backend-built-in-implementation)
7. [Generated Java code structure](#7-generated-java-code-structure)
8. [Usage](#8-usage)
9. [Extending the project](#9-extending-the-project)
   - [Adding a new input format](#91-adding-a-new-input-format)
   - [Adding a new output target](#92-adding-a-new-output-target)

---

## 1. What this project is

`uml2code` is a **diagram-to-code transpiler** built around a compiler architecture.

It reads an entity-relationship diagram, extracts entities and their relationships (inheritance, composition, aggregation, association), and generates a fully functional backend application with CRUD operations for every entity.

The architecture is designed so that **input formats** and **output targets** are completely interchangeable:

- Any diagram notation (draw.io, PlantUML, Mermaid, …) can serve as input
- Any framework or language (Spring Boot, Django, Laravel, NestJS, …) can be the output target

The built-in implementation supports **draw.io → Spring Boot 3 / Java 21**. It serves as the reference implementation of the extension points.

> **Scope note**: The transpiler models **entity-relationship** concepts — entities, fields, and structural relationships. It is not a general-purpose UML transpiler and does not handle use-case, sequence, activity, or state machine diagrams.

---

## 2. Architecture overview

The project follows a **compiler / transpiler architecture** with three clearly separated stages:

```
 ┌───────────────────────────────────────────────────────────────────────┐
 │                            PIPELINE                                   │
 │                                                                       │
 │   ┌─────────────────┐   ┌──────────────────┐   ┌──────────────────┐  │
 │   │    FRONTEND      │   │   MIDDLE-END      │   │    BACKEND       │  │
 │   │   «IFrontend»    │   │ SemanticAnalyzer  │   │   «IBackend»     │  │
 │   │                  │──▶│                  │──▶│                  │  │
 │   │  parse(source)   │   │ analyze(diagram,  │   │ generate(ir)     │  │
 │   │  → ERDiagram     │   │   package) → IR   │   │ write(files,dir) │  │
 │   └─────────────────┘   └──────────────────┘   └──────────────────┘  │
 │           ▲                                              ▲             │
 │    implements                                     implements           │
 │    DrawIOFrontend                             SpringBootGenerator      │
 │    PlantUMLFrontend (future)                  DjangoGenerator (future) │
 └───────────────────────────────────────────────────────────────────────┘
```

Each stage communicates through a **typed intermediate representation**:

| Stage | Consumes | Produces |
|---|---|---|
| Frontend | Raw source string (file content) | `ERDiagram` (source-specific AST) |
| Middle-end | `ERDiagram` | `ProjectIR` (target-agnostic IR) |
| Backend | `ProjectIR` | Source files written to disk |

The `Pipeline` depends **only on the abstract port interfaces** (`IFrontend`, `IBackend`). Swapping a frontend or a backend requires no change to the pipeline or to any other stage.

---

## 3. Component reference

### 3.1 Core (IR + Ports)

**Location:** `src/core/`

The core package defines the two intermediate representations and the two abstract port interfaces. It has **zero dependencies** on any specific frontend or backend — it is the contract shared by all stages.

#### Port interfaces

**`IFrontend`** (`src/core/ports/frontend_port.py`)

```python
class IFrontend(ABC):
    @abstractmethod
    def parse(self, source: str) -> ERDiagram: ...
```

Any class that can read a diagram notation and produce an `ERDiagram` is a valid frontend. The source string is the raw file content (XML, text, etc.).

**`IBackend`** (`src/core/ports/backend_port.py`)

```python
class IBackend(ABC):
    @abstractmethod
    def generate(self, ir: ProjectIR) -> list: ...

    @abstractmethod
    def write(self, files: list, output_dir: Path) -> None: ...
```

Any class that can turn a `ProjectIR` into files on disk is a valid backend.

---

### 3.2 Frontend

**Location:** `src/frontend/`

A frontend is responsible for reading a raw diagram source string and producing an `ERDiagram` AST. Every frontend implements `IFrontend`.

The frontend folder is organized by input format:

```
src/frontend/
└── drawio/              ← draw.io implementation
    ├── drawio_frontend.py   ← IFrontend façade
    ├── lexer.py             ← XML tokenizer
    └── parser.py            ← ERDiagram builder
```

Internally, a frontend implementation is typically split into:

- **Lexer**: tokenizes the raw source into an intermediate token list (format-specific)
- **Parser**: interprets the token list and builds the `ERDiagram` AST
- **Façade**: wraps both behind a single `IFrontend.parse()` call

This internal split is an implementation detail — the pipeline only ever calls `frontend.parse(source)`.

---

### 3.3 Middle-end (Semantic Analyzer)

**Location:** `src/middleend/semantic_analyzer.py`

The semantic analyzer is the only component with no implementation variants — it is intentionally **format-agnostic and target-agnostic**.

Responsibilities:
- Converts each `EREntity` from the `ERDiagram` into an `IREntity` in the `ProjectIR`
- Resolves relationships and applies them to the IR:
  - `INHERITANCE` → sets `IREntity.parent`
  - `COMPOSITION` → appends to `IREntity.compositions`
  - `AGGREGATION` / `ASSOCIATION` → appends to `IREntity.aggregations`
- Passes **type names through unchanged** — it does not know what language the backend will generate, so it never maps types to language-specific equivalents

> Type normalization (`string → String`, `int → Integer`, etc.) is the backend's responsibility. It belongs in the backend's type system, not in the middle-end.

---

### 3.4 Backend

**Location:** `src/backend/`

A backend takes a `ProjectIR` and generates files. Every backend implements `IBackend`.

The backend folder is organized by output target:

```
src/backend/
└── spring_boot/             ← Spring Boot implementation
    ├── generator.py             ← IBackend implementation
    └── templates/               ← Jinja2 templates (.j2)
        ├── domain/
        ├── infrastructure/
        └── presentation/
```

Each backend is free to:
- Define its own language-specific type mapping
- Use any templating system
- Generate any file structure

---

### 3.5 Pipeline

**Location:** `src/pipeline/pipeline.py`

The pipeline is a thin orchestrator that wires the three stages in sequence. It depends **only on the abstract port interfaces** and on `SemanticAnalyzer`:

```python
@dataclass
class Pipeline:
    frontend: IFrontend
    analyzer: SemanticAnalyzer
    backend: IBackend

    def run(self, source: str, package: str, output_dir: Path) -> list:
        diagram = self.frontend.parse(source)
        ir      = self.analyzer.analyze(diagram, package)
        files   = self.backend.generate(ir)
        self.backend.write(files, output_dir)
        return files
```

The pipeline has no logic of its own. Adding a new frontend or backend means injecting a different implementation at construction — the pipeline stays unchanged.

---

### 3.6 Helpers

**Location:** `src/helpers/utils.py`

Stateless utility functions shared across all stages:

| Function | Description |
|---|---|
| `lowercase_keys(data)` | Recursively lowercases all dict keys |
| `capitalize(s)` | Uppercases the first character only |
| `lower_first(s)` | Lowercases the first character only |
| `snake_to_pascal(s)` | Converts `snake_case` to `PascalCase` |

---

## 4. Intermediate representations

### Why two IRs?

**`ERDiagram`** (source AST) is **source-language-specific**. It carries concepts that belong to the input format: cell IDs, visibility symbols, raw type strings as written in the diagram. A draw.io frontend and a PlantUML frontend may produce different `ERDiagram` structures, but both produce an `ERDiagram`.

**`ProjectIR`** (target-agnostic IR) carries only **normalized, backend-ready information**: entity names, resolved parent chains, composition and aggregation lists, raw field types. It contains no trace of draw.io, no Java-specific types — nothing that ties it to a particular input or output.

```
draw.io  ──▶ ERDiagram ──┐
PlantUML ──▶ ERDiagram ──┤                    ┌──▶ Spring Boot files
Mermaid  ──▶ ERDiagram ──┘                    │
                          └──▶ ProjectIR ──────┤──▶ Django files
                                               └──▶ NestJS files
```

### `ERDiagram` structure (`src/core/ir/er_diagram.py`)

```
ERDiagram
├── entities: dict[id → EREntity]
│   ├── id: str                  (source-specific cell identifier)
│   ├── name: str
│   ├── fields: list[ERField]    (name, type as written, visibility symbol)
│   └── methods: list[ERMethod]  (name, return_type, params)
└── relationships: list[ERRelationship]
    ├── source_id: str
    ├── target_id: str
    ├── kind: RelationshipKind   (INHERITANCE | COMPOSITION | AGGREGATION | ASSOCIATION)
    └── label: str
```

### `ProjectIR` structure (`src/core/ir/project_ir.py`)

```
ProjectIR
├── package: str                 (e.g. "com.example.myapp")
└── entities: list[IREntity]
    ├── name: str
    ├── fields: list[IRField]    (name, type as-is from diagram, visibility)
    ├── parent: IREntity | None  (set by INHERITANCE relationship)
    ├── compositions: list[IREntity]
    ├── aggregations: list[IREntity]
    └── is_root: bool (property) (True when parent is None)
```

---

## 5. The draw.io frontend (built-in implementation)

**Location:** `src/frontend/drawio/`

### `DrawIOFrontend` (façade)

Implements `IFrontend`. Wraps `DrawIOLexer` and `DrawIOParser` behind a single `parse()` call. This is the class the pipeline depends on — the Lexer and Parser are internal implementation details.

### `DrawIOLexer`

Tokenizes the draw.io XML source into a flat list of raw `mxCell` dictionaries using `xmltodict`. All attribute keys are lowercased to normalize draw.io's mixed-case naming. No interpretation happens here.

### `DrawIOParser`

Builds an `ERDiagram` from the cell list in three passes:

**Pass 1 — Entities**: cells that are direct children of the diagram root with a `vertex` attribute become `EREntity` objects.

**Pass 2 — Fields and methods**: cells whose parent is a known entity are parsed using regex patterns. A `value` containing `()` is treated as a method; otherwise it is treated as a field. Generics (`List<String>`, `Map<K,V>`) are supported.

**Pass 3 — Relationships**: cells with both `source` and `target` attributes. The endpoint IDs are resolved to entities by walking the parent chain (O(1) lookup). The arrow style is interpreted:

| draw.io style | Relationship |
|---|---|
| `endArrow=block` | INHERITANCE |
| `endArrow=diamondThin` + `endFill=1` | COMPOSITION |
| `endArrow=diamondThin` + `endFill=0` | AGGREGATION |
| `endArrow=open/classic/classicThin` | ASSOCIATION |

---

## 6. The Spring Boot backend (built-in implementation)

**Location:** `src/backend/spring_boot/`

### `SpringBootGenerator`

Implements `IBackend`. Uses a Jinja2 `Environment` with `FileSystemLoader` pointing at the `templates/` directory.

**Type normalization**: the generator defines `_JAVA_TYPE_MAP` and registers a `java_type` Jinja2 filter. Templates apply `{{ field.type | java_type }}` to resolve diagram type names to canonical Java types (`string → String`, `int → Integer`, `datetime → LocalDateTime`, etc.). This mapping is entirely internal to this backend — other backends define their own.

**Custom Jinja2 filters**:

| Filter | Example |
|---|---|
| `java_type` | `"string"` → `"String"`, `"datetime"` → `"LocalDateTime"` |
| `lower_first` | `"Person"` → `"person"` |
| `pkg_path` | `"com.example.app"` → `"com/example/app"` |

### Templates

All templates use the `.j2` extension and are organized by Java architectural layer:

```
templates/
├── domain/
│   ├── entity.j2                          # JPA entity class
│   ├── repository_port.j2                 # Driven port interface (IXxxRepository)
│   ├── service_port.j2                    # Driving port interface (IXxxService)
│   └── exceptions/
│       ├── base_not_found.j2              # EntityNotFoundException (shared base)
│       ├── base_already_exists.j2         # EntityAlreadyExistsException (shared base)
│       ├── entity_not_found.j2            # {Entity}NotFoundException
│       └── entity_already_exists.j2       # {Entity}AlreadyExistsException
├── infrastructure/
│   ├── jpa_repository.j2                  # Spring Data JPA adapter
│   ├── service_impl.j2                    # CRUD service implementation
│   └── jackson_config.j2                  # ObjectMapper (JavaTimeModule)
└── presentation/
    ├── controller.j2                      # REST controller (5 CRUD endpoints)
    └── global_exception_handler.j2        # @RestControllerAdvice (404, 422, 500)
```

Template context variables:

| Variable | Available in | Description |
|---|---|---|
| `ir` | all templates | The full `ProjectIR` (package, entity list) |
| `entity` | per-entity templates | The current `IREntity` |

Key behaviors:
- Only root entities (no parent) receive `@Id`, `@GeneratedValue`, `createdAt`, `updatedAt` — correct for JPA Single-Table Inheritance
- Compositions → `@OneToMany(cascade = ALL, orphanRemoval = true)`
- Aggregations / associations → `@ManyToOne(fetch = LAZY)`
- `PUT` preserves `createdAt` by copying from the existing entity before saving
- `JacksonConfig` registers `JavaTimeModule` globally so `LocalDateTime` serializes as ISO strings

---

## 7. Generated Java code structure

For `--package com.example.myapp`:

```
com/example/myapp/
│
├── domain/
│   ├── entities/
│   │   └── {Entity}.java                      # JPA entity
│   ├── ports/
│   │   ├── driven/
│   │   │   └── I{Entity}Repository.java        # Driven port
│   │   └── driving/
│   │       └── I{Entity}Service.java           # Driving port
│   └── exceptions/
│       ├── EntityNotFoundException.java         # Base (404)
│       ├── EntityAlreadyExistsException.java    # Base (422)
│       ├── {Entity}NotFoundException.java
│       └── {Entity}AlreadyExistsException.java
│
├── infrastructure/
│   ├── adapters/
│   │   ├── persistence/
│   │   │   └── {Entity}Repository.java         # JPA adapter
│   │   └── services/
│   │       └── {Entity}ServiceImpl.java        # Service adapter
│   └── config/
│       └── JacksonConfig.java
│
└── presentation/
    └── rest/
        ├── {Entity}Controller.java             # REST controller
        └── GlobalExceptionHandler.java         # Exception → HTTP mapping
```

The generated application follows **Hexagonal Architecture (Ports & Adapters)**:

```
             HTTP requests
                  │
     ┌────────────▼────────────┐
     │  PRESENTATION           │
     │  {Entity}Controller     │
     └────────────┬────────────┘
                  │  calls driving port
     ┌────────────▼────────────┐
     │  DOMAIN                 │
     │  I{Entity}Service  ◀────────── {Entity}ServiceImpl (infrastructure)
     │  I{Entity}Repository ◀──────── {Entity}Repository  (infrastructure)
     └─────────────────────────┘
```

---

## 8. Usage

### Prerequisites

```bash
pip install -r requirements.txt
# Python 3.10+ required (match statements, PEP 604 union types)
```

### Run the generator

```bash
python3 main.py <diagram-file> --package <java.package> --output <output-dir>
```

**Example with draw.io:**

```bash
python3 main.py data/class-diagram-example.drawio \
    --package com.example.myapp \
    --output /tmp/generated
```

### Compile and run the generated app

Copy the generated files into an existing Spring Boot project:

```bash
cp -r /tmp/generated/* my-spring-boot-project/src/main/java/

cd my-spring-boot-project
./mvnw spring-boot:run
```

Swagger UI: `http://localhost:8080/swagger-ui/index.html`

---

## 9. Extending the project

### 9.1 Adding a new input format

To support PlantUML, Mermaid, or any other notation, implement `IFrontend`. **No existing code changes.**

**Step 1** — Implement the frontend:

```python
# src/frontend/plantuml/plantuml_frontend.py
from core.ir.er_diagram import ERDiagram
from core.ports.frontend_port import IFrontend

class PlantUMLFrontend(IFrontend):
    def parse(self, source: str) -> ERDiagram:
        # tokenize and parse PlantUML source into an ERDiagram
        ...
```

Internally you may split this into a `PlantUMLLexer` + `PlantUMLParser`, following the same pattern as the draw.io frontend.

**Step 2** — Inject it in `main.py`:

```python
pipeline = Pipeline(
    frontend=PlantUMLFrontend(),
    analyzer=SemanticAnalyzer(),
    backend=SpringBootGenerator(TEMPLATE_DIR),
)
```

The middle-end and backend are unchanged.

---

### 9.2 Adding a new output target

To generate Django, NestJS, Laravel, or any other target, implement `IBackend`. **No existing code changes.**

**Step 1** — Implement the backend:

```python
# src/backend/django/generator.py
from pathlib import Path
from core.ir.project_ir import ProjectIR
from core.ports.backend_port import IBackend

class DjangoGenerator(IBackend):
    def generate(self, ir: ProjectIR) -> list:
        # render Jinja2 (or any) templates for Django models, views, urls…
        ...

    def write(self, files: list, output_dir: Path) -> None:
        ...
```

Define your own type mapping inside this class (e.g., `string → str`, `integer → int` for Python).

**Step 2** — Inject it in `main.py`:

```python
pipeline = Pipeline(
    frontend=DrawIOFrontend(),
    analyzer=SemanticAnalyzer(),
    backend=DjangoGenerator(DJANGO_TEMPLATE_DIR),
)
```

The frontend and middle-end are unchanged.
