from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from core.ir.project_ir import IREntity, ProjectIR
from helpers.utils import lower_first


@dataclass
class GeneratedFile:
    relative_path: str
    content: str


def _pkg_to_path(package: str) -> str:
    return package.replace('.', '/')


class SpringBootGenerator:
    """Generates a full Spring Boot CRUD application from a ProjectIR."""

    def __init__(self, template_dir: Path):
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        self.env.filters['lower_first'] = lower_first
        self.env.filters['pkg_path'] = _pkg_to_path

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

    # ------------------------------------------------------------------ #
    # Private helpers
    # ------------------------------------------------------------------ #

    def _render(self, template_name: str, **ctx) -> str:
        return self.env.get_template(template_name).render(**ctx)

    def _path(self, ir: ProjectIR, entity: IREntity, layer: str, sub: str,
               suffix: str = '', prefix: str = '') -> str:
        base = _pkg_to_path(ir.package)
        return f"{base}/{layer}/{sub}/{prefix}{entity.name}{suffix}.java"

    def _gen_entity_files(self, ir: ProjectIR, entity: IREntity) -> list[GeneratedFile]:
        ctx = dict(ir=ir, entity=entity)
        return [
            # Domain
            GeneratedFile(
                self._path(ir, entity, 'domain', 'entities'),
                self._render('domain/entity.j2', **ctx),
            ),
            GeneratedFile(
                self._path(ir, entity, 'domain', 'ports/driven', prefix='I', suffix='Repository'),
                self._render('domain/repository_port.j2', **ctx),
            ),
            GeneratedFile(
                self._path(ir, entity, 'domain', 'ports/driving', prefix='I', suffix='Service'),
                self._render('domain/service_port.j2', **ctx),
            ),
            GeneratedFile(
                self._path(ir, entity, 'domain', 'exceptions', suffix='NotFoundException'),
                self._render('domain/exceptions/entity_not_found.j2', **ctx),
            ),
            GeneratedFile(
                self._path(ir, entity, 'domain', 'exceptions', suffix='AlreadyExistsException'),
                self._render('domain/exceptions/entity_already_exists.j2', **ctx),
            ),
            # Infrastructure
            GeneratedFile(
                self._path(ir, entity, 'infrastructure', 'adapters/persistence', suffix='Repository'),
                self._render('infrastructure/jpa_repository.j2', **ctx),
            ),
            GeneratedFile(
                self._path(ir, entity, 'infrastructure', 'adapters/services', suffix='ServiceImpl'),
                self._render('infrastructure/service_impl.j2', **ctx),
            ),
            # Presentation
            GeneratedFile(
                self._path(ir, entity, 'presentation', 'rest', suffix='Controller'),
                self._render('presentation/controller.j2', **ctx),
            ),
        ]

    def _gen_global_files(self, ir: ProjectIR) -> list[GeneratedFile]:
        base = _pkg_to_path(ir.package)
        ctx = dict(ir=ir)
        return [
            GeneratedFile(
                f"{base}/domain/exceptions/EntityNotFoundException.java",
                self._render('domain/exceptions/base_not_found.j2', **ctx),
            ),
            GeneratedFile(
                f"{base}/domain/exceptions/EntityAlreadyExistsException.java",
                self._render('domain/exceptions/base_already_exists.j2', **ctx),
            ),
            GeneratedFile(
                f"{base}/infrastructure/config/JacksonConfig.java",
                self._render('infrastructure/jackson_config.j2', **ctx),
            ),
            GeneratedFile(
                f"{base}/presentation/rest/GlobalExceptionHandler.java",
                self._render('presentation/global_exception_handler.j2', **ctx),
            ),
        ]
