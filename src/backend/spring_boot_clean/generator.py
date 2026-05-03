from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from core.ir.project_ir import IREntity, ProjectIR
from core.ports.backend_port import IBackend
from helpers.utils import capitalize, lower_first

_JAVA_TYPE_MAP: dict[str, str] = {
    'int':       'Integer',
    'integer':   'Integer',
    'string':    'String',
    'str':       'String',
    'bool':      'Boolean',
    'boolean':   'Boolean',
    'float':     'Float',
    'double':    'Double',
    'long':      'Long',
    'char':      'Character',
    'byte':      'Byte',
    'short':     'Short',
    'void':      'void',
    'date':      'LocalDate',
    'datetime':  'LocalDateTime',
    'timestamp': 'LocalDateTime',
    'uuid':      'UUID',
    'object':    'Object',
    'list':      'List',
    'set':       'Set',
    'map':       'Map',
}


def _java_type(raw: str) -> str:
    return _JAVA_TYPE_MAP.get(raw.strip().lower(), raw.strip())


def _pkg_to_path(package: str) -> str:
    return package.replace('.', '/')


@dataclass
class GeneratedFile:
    relative_path: str
    content: str


class SpringBootCleanGenerator(IBackend):
    """Generates a Clean-Architecture Spring Boot application from a ProjectIR."""

    def __init__(self, template_dir: Path):
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            extensions=['jinja2.ext.do'],
        )
        self.env.filters['lower_first'] = lower_first
        self.env.filters['upper_first'] = capitalize   # first char upper, rest unchanged
        self.env.filters['pkg_path']    = _pkg_to_path
        self.env.filters['java_type']   = _java_type

    # ── IBackend ──────────────────────────────────────────────────────────────

    def generate(self, ir: ProjectIR) -> list[GeneratedFile]:
        files: list[GeneratedFile] = []
        for entity in ir.entities:
            files.extend(self._gen_entity_files(ir, entity))
        files.extend(self._gen_global_files(ir))
        return files

    def write(self, files: list[GeneratedFile], output_dir: Path) -> None:
        for f in files:
            dest = output_dir / f.relative_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(f.content, encoding='utf-8')

    # ── Per-entity file generation ────────────────────────────────────────────

    def _gen_entity_files(self, ir: ProjectIR, entity: IREntity) -> list[GeneratedFile]:
        ctx  = dict(ir=ir, entity=entity)
        base = _pkg_to_path(ir.package)
        name = entity.name
        e    = name.lower()

        return [
            # Domain
            self._f(f"{base}/domain/entities/{name}.java",
                    'domain/entity.j2', **ctx),
            self._f(f"{base}/domain/repositories/I{name}Repository.java",
                    'domain/repositories/repository.j2', **ctx),

            # Application — ports grouped by operation family then entity
            self._f(f"{base}/application/ports/crud/{e}/ICreate{name}.java",
                    'application/ports/create_port.j2', **ctx),
            self._f(f"{base}/application/ports/crud/{e}/IFindById{name}.java",
                    'application/ports/find_by_id_port.j2', **ctx),
            self._f(f"{base}/application/ports/crud/{e}/IFindAll{name}.java",
                    'application/ports/find_all_port.j2', **ctx),
            self._f(f"{base}/application/ports/crud/{e}/IUpdate{name}.java",
                    'application/ports/update_port.j2', **ctx),
            self._f(f"{base}/application/ports/crud/{e}/IDelete{name}.java",
                    'application/ports/delete_port.j2', **ctx),

            # Application — use cases grouped by operation family then entity
            self._f(f"{base}/application/usecases/crud/{e}/Create{name}UseCase.java",
                    'application/usecases/create_use_case.j2', **ctx),
            self._f(f"{base}/application/usecases/crud/{e}/FindById{name}UseCase.java",
                    'application/usecases/find_by_id_use_case.j2', **ctx),
            self._f(f"{base}/application/usecases/crud/{e}/FindAll{name}UseCase.java",
                    'application/usecases/find_all_use_case.j2', **ctx),
            self._f(f"{base}/application/usecases/crud/{e}/Update{name}UseCase.java",
                    'application/usecases/update_use_case.j2', **ctx),
            self._f(f"{base}/application/usecases/crud/{e}/Delete{name}UseCase.java",
                    'application/usecases/delete_use_case.j2', **ctx),

            # Application — use-case-centric DTOs
            self._f(f"{base}/application/dto/Create{name}Request.java",
                    'application/dto/create_request.j2', **ctx),
            self._f(f"{base}/application/dto/Update{name}Request.java",
                    'application/dto/update_request.j2', **ctx),
            self._f(f"{base}/application/dto/{name}Response.java",
                    'application/dto/response.j2', **ctx),
            self._f(f"{base}/application/dto/{name}SummaryResponse.java",
                    'application/dto/summary_response.j2', **ctx),

            # Application — mapper (in its own sub-package)
            self._f(f"{base}/application/mappers/{name}DtoMapper.java",
                    'application/mappers/dto_mapper.j2', **ctx),

            # Infrastructure — persistence split into 4 sub-packages
            self._f(f"{base}/infrastructure/persistence/entities/{name}JpaEntity.java",
                    'infrastructure/persistence/entities/jpa_entity.j2', **ctx),
            self._f(f"{base}/infrastructure/persistence/repositories/{name}JpaRepository.java",
                    'infrastructure/persistence/repositories/jpa_repository.j2', **ctx),
            self._f(f"{base}/infrastructure/persistence/mappers/{name}EntityMapper.java",
                    'infrastructure/persistence/mappers/entity_mapper.j2', **ctx),
            self._f(f"{base}/infrastructure/persistence/adapters/{name}RepositoryAdapter.java",
                    'infrastructure/persistence/adapters/repository_adapter.j2', **ctx),

            # Presentation
            self._f(f"{base}/presentation/rest/{name}Controller.java",
                    'presentation/rest/controller.j2', **ctx),
        ]

    # ── Global file generation ────────────────────────────────────────────────

    def _gen_global_files(self, ir: ProjectIR) -> list[GeneratedFile]:
        base = _pkg_to_path(ir.package)
        ctx  = dict(ir=ir)
        return [
            self._f(f"{base}/domain/exceptions/EntityNotFoundException.java",
                    'domain/exceptions/entity_not_found.j2', **ctx),
            self._f(f"{base}/domain/exceptions/EntityAlreadyExistsException.java",
                    'domain/exceptions/entity_already_exists.j2', **ctx),
            self._f(f"{base}/infrastructure/config/BeanConfig.java",
                    'infrastructure/config/bean_config.j2', **ctx),
            self._f(f"{base}/infrastructure/config/JacksonConfig.java",
                    'infrastructure/config/jackson_config.j2', **ctx),
            self._f(f"{base}/presentation/exception/GlobalExceptionHandler.java",
                    'presentation/exception/global_exception_handler.j2', **ctx),
            self._f(f"{base}/presentation/exception/ApiError.java",
                    'presentation/exception/api_error.j2', **ctx),
        ]

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _f(self, path: str, template: str, **ctx) -> GeneratedFile:
        return GeneratedFile(path, self.env.get_template(template).render(**ctx))
