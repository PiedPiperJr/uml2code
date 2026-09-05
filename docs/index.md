# uml2code

**uml2code** is a diagram-to-code transpiler built around a compiler architecture.  
Draw an ER diagram → get a fully functional, compilable backend with CRUD for every entity.

The built-in implementation targets **draw.io → Spring Boot 3 / Java 21 (Clean Architecture)**.  
Any input format and any output target can be plugged in without touching the core.

---

## Quick start

```bash
# 1 — install dependencies
pip install -r requirements.txt

# 2 — generate Java sources from a draw.io diagram
python3 main.py data/class-diagram-example.drawio \
    --package com.example.myapp \
    --output /tmp/generated
```

For a fully automated experience (download → patch → generate → compile):

```bash
cd examples/spring_boot
bash init.sh \
  --diagram ../../data/class-diagram-example.drawio \
  --package com.example.server \
  --app-name my-server \
  --port 8080
```

Then run:

```bash
cd my-server && ./mvnw spring-boot:run
# Swagger UI → http://localhost:8080/swagger-ui/index.html
```

---

## What is generated

For every entity in your diagram, uml2code produces a full Clean Architecture slice:

| Layer | Files |
|---|---|
| Domain | Entity POJO, `I{E}Repository`, exceptions |
| Application | 5 use-case interfaces + implementations, DTOs, mapper |
| Infrastructure | JPA entity, Spring Data repo, MapStruct mapper, adapter |
| Presentation | REST controller, `GlobalExceptionHandler`, `ApiError` |

See [Generated structure](architecture/generated-structure.md) for the full package layout.
