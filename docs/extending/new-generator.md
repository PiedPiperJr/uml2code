# Add a new generator (backend)

A generator is any class that implements `IBackend`. It receives a `ProjectIR` and writes files to disk.  
**No existing code changes** — you only add files and inject your class in `main.py`.

---

## Step 1 — Create the generator class

```
src/backend/
└── django/               ← new folder
    ├── __init__.py
    ├── generator.py       ← IBackend implementation
    └── templates/         ← Jinja2 templates
        ├── models.py.j2
        ├── serializers.py.j2
        └── views.py.j2
```

Implement both methods of `IBackend`:

```python title="src/backend/django/generator.py"
from dataclasses import dataclass
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from core.ir.project_ir import IREntity, ProjectIR
from core.ports.backend_port import IBackend

# Map diagram type names → Django/Python types
_PYTHON_TYPE_MAP = {
    'string':    'str',
    'int':       'int',
    'integer':   'int',
    'bool':      'bool',
    'float':     'float',
    'date':      'date',
    'datetime':  'datetime',
    'uuid':      'UUID',
}

def _python_type(raw: str) -> str:
    return _PYTHON_TYPE_MAP.get(raw.strip().lower(), raw.strip())


@dataclass
class GeneratedFile:
    relative_path: str
    content: str


class DjangoGenerator(IBackend):

    def __init__(self, template_dir: Path):
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters['python_type'] = _python_type  # (1)

    def generate(self, ir: ProjectIR) -> list[GeneratedFile]:
        files = []
        for entity in ir.entities:
            ctx = dict(ir=ir, entity=entity)
            files.append(self._render(
                f"{entity.name.lower()}/models.py",
                'models.py.j2', **ctx
            ))
            # add serializers, views, urls …
        return files

    def write(self, files: list[GeneratedFile], output_dir: Path) -> None:
        for f in files:
            dest = output_dir / f.relative_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(f.content, encoding='utf-8')

    def _render(self, path: str, template: str, **ctx) -> GeneratedFile:
        return GeneratedFile(path, self.env.get_template(template).render(**ctx))
```

1. Register your type filter here — the `ProjectIR` carries raw diagram type names (`string`, `int`, `datetime`). Your filter maps them to the target language's types.

---

## Step 2 — Write Jinja2 templates

Templates receive two context variables:

| Variable | Type | Description |
|---|---|---|
| `ir` | `ProjectIR` | The full IR (package name, all entities) |
| `entity` | `IREntity` | The current entity being rendered |

Key attributes of `IREntity`:

| Attribute | Type | Description |
|---|---|---|
| `entity.name` | `str` | PascalCase entity name (`Student`) |
| `entity.fields` | `list[IRField]` | Each field has `.name` and `.type` |
| `entity.parent` | `IREntity \| None` | Set when the entity inherits from another |
| `entity.is_root` | `bool` | `True` when `parent is None` |
| `entity.compositions` | `list[IREntity]` | Owned sub-entities (cascade delete) |
| `entity.aggregations` | `list[IREntity]` | Referenced entities (no cascade) |

Example — Django model template:

```django title="src/backend/django/templates/models.py.j2"
from django.db import models
import uuid

class {{ entity.name }}(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

{% for field in entity.fields if field.name != 'id' %}
    {{ field.name }} = models.CharField(max_length=255)  {# map field.type | python_type #}
{% endfor %}

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "{{ entity.name | lower }}s"
```

---

## Step 3 — Wire it in `main.py`

```python title="main.py" hl_lines="4 5 16"
from backend.spring_boot_clean.generator import SpringBootCleanGenerator
from backend.django.generator import DjangoGenerator          # (1)
from frontend.drawio.drawio_frontend import DrawIOFrontend
from middleend.semantic_analyzer import SemanticAnalyzer
from pipeline.pipeline import Pipeline

TEMPLATE_DIR = Path(__file__).parent / "src" / "backend" / "django" / "templates"  # (2)

pipeline = Pipeline(
    frontend=DrawIOFrontend(),
    analyzer=SemanticAnalyzer(),
    backend=DjangoGenerator(TEMPLATE_DIR),                    # (3)
)
```

1. Import your new generator
2. Point to your template directory
3. Inject it — the frontend and middle-end are unchanged

!!! tip "Add a `--backend` flag instead of hardcoding"
    If you want to support multiple generators from the CLI, add an `argparse` argument:
    ```python
    parser.add_argument('--backend', choices=['spring-boot', 'django'], default='spring-boot')
    backend = DjangoGenerator(DJANGO_TEMPLATES) if args.backend == 'django' \
              else SpringBootCleanGenerator(SB_TEMPLATES)
    ```

---

## Checklist

- [ ] `IBackend.generate(ir)` returns a list of `GeneratedFile(relative_path, content)`
- [ ] `IBackend.write(files, output_dir)` creates parent directories and writes each file
- [ ] A type map filter is registered on the Jinja2 `Environment`
- [ ] Templates use `{{ entity.name }}`, `{% for field in entity.fields %}`, etc.
- [ ] Generator is injected in `main.py` (or behind a `--backend` flag)
