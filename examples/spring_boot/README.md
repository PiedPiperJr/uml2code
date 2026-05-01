# Spring Boot example — Quick start

This example shows how to generate and run a full Spring Boot CRUD application
from a draw.io ER diagram in a single command.

## Prerequisites

| Tool | Version |
|---|---|
| Python | 3.10+ |
| Java | 21 |
| Maven | 3.8+ |
| curl + unzip | any |

Install Python dependencies from the project root:

```bash
pip install -r ../../requirements.txt
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
  --package org.enspy.snappy.server \
  --app-name snappy-server \
  --port 8080
```

This will:

1. Download a Spring Boot 3.5 project from Spring Initializr (web, JPA, H2, Lombok, Validation)
2. Add the `springdoc-openapi` dependency for Swagger UI
3. Write a pre-configured `application.properties`
4. Generate all Java source files from the diagram

Then start the application:

```bash
cd snappy-server
./mvnw spring-boot:run
```

---

## What is generated

For each entity in the diagram, the generator produces:

```
src/main/java/{package}/
├── domain/
│   ├── entities/            # JPA entities
│   ├── ports/driven/        # Repository interfaces (driven ports)
│   ├── ports/driving/       # Service interfaces (driving ports)
│   └── exceptions/          # Typed exceptions (404, 422)
├── infrastructure/
│   ├── adapters/persistence/ # Spring Data JPA repositories
│   ├── adapters/services/    # CRUD service implementations
│   └── config/              # JacksonConfig (LocalDateTime serialization)
└── presentation/
    └── rest/                # REST controllers + GlobalExceptionHandler
```

---

## Available endpoints (per entity)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/{entity}` | Create |
| `GET` | `/api/{entity}/{id}` | Find by ID |
| `GET` | `/api/{entity}?page=0&size=20` | Find all (paginated) |
| `PUT` | `/api/{entity}/{id}` | Update |
| `DELETE` | `/api/{entity}/{id}` | Delete |

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
