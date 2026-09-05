# Spring Boot example — Quick start

This example shows how to generate and run a full Clean-Architecture Spring Boot CRUD
application from a draw.io ER diagram in two commands.

## Prerequisites

| Tool | Version |
|---|---|
| Python | 3.10+ |
| Java | 21 |
| Maven | 3.8+ |
| curl + unzip | any |

Install all prerequisites with the bundled setup script:

```bash
bash setup.sh
```

---

## Usage

```bash
bash init.sh \
  --diagram <path-to-diagram.drawio> \
  --package <java.base.package> \
  [--app-name <folder-name>] \
  [--port <port>]
```

### Options

| Option | Required | Default | Description |
|---|---|---|---|
| `--diagram` | yes | — | Path to the draw.io file |
| `--package` | yes | — | Java base package (e.g. `com.example.myapp`) |
| `--app-name` | no | `generated-app` | Output folder name |
| `--port` | no | `8080` | HTTP port |

---

## Example with the built-in diagram

```bash
bash init.sh \
  --diagram ../../data/class-diagram-example.drawio \
  --package com.example.server \
  --app-name example-server \
  --port 8080
```

This will:

1. Download a Spring Boot 3.5 project from Spring Initializr (web, JPA, H2, Lombok, Validation)
2. Patch `pom.xml` with `springdoc-openapi` (Swagger UI) and `mapstruct` (mapping)
3. Write a pre-configured `application.properties`
4. Generate all Java source files from the diagram
5. Compile the project to catch errors immediately

Then start the application:

```bash
cd example-server
./mvnw spring-boot:run
```

---

## What is generated

For each entity in the diagram, the generator produces 21 files across 4 layers:

```
src/main/java/{package}/
├── domain/
│   ├── entities/              # Pure Java POJOs (zero framework dependency)
│   ├── ports/                 # I{E}Repository driven-port interfaces
│   └── exceptions/            # EntityNotFoundException, EntityAlreadyExistsException
├── application/
│   ├── ports/                 # ICreate{E}, IFindById{E}, IFindAll{E}, IUpdate{E}, IDelete{E}
│   ├── usecases/              # Use-case implementations (execute() + private methods)
│   └── dto/                   # {E}Request, {E}Response, {E}SummaryResponse, {E}DtoMapper
├── infrastructure/
│   ├── persistence/           # {E}JpaEntity, {E}JpaRepository, {E}EntityMapper, {E}RepositoryAdapter
│   └── config/                # BeanConfig (use-case wiring), JacksonConfig
└── presentation/
    └── rest/                  # {E}Controller, GlobalExceptionHandler, ApiError
```

---

## Available endpoints (per entity)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/{entity}s` | Create |
| `GET` | `/api/v1/{entity}s/{id}` | Find by ID |
| `GET` | `/api/v1/{entity}s?page=0&size=20` | Find all (paginated) |
| `PUT` | `/api/v1/{entity}s/{id}` | Full update |
| `DELETE` | `/api/v1/{entity}s/{id}` | Delete |

---

## Useful URLs (once running)

| URL | Description |
|---|---|
| `http://localhost:8080/swagger-ui/index.html` | Swagger UI |
| `http://localhost:8080/api-docs` | OpenAPI JSON spec |
| `http://localhost:8080/h2-console` | H2 database console |

> **In a GitHub Codespace**: replace `localhost:8080` with your forwarded port URL.
> The `server.forward-headers-strategy=framework` property in `application.properties`
> ensures Swagger UI uses the correct public URL automatically.

---

## Adding a different input diagram

Point `--diagram` to any compatible draw.io file:

```bash
bash init.sh \
  --diagram /path/to/my-diagram.drawio \
  --package com.example.myapp \
  --app-name my-app
```

The diagram must contain entities (classes with fields) and optionally
relationships (inheritance, composition, aggregation, association).
