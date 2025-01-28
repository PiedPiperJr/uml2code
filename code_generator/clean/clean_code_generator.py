
from enum import Enum
import os
from pathlib import Path
from typing import Dict, List, Union

from jinja2 import Template
from helpers.utils import Utils
from models.class_model import Class
from models.project_model import Project


class CleanCodeGenerator:
    def __init__(self, project: Project, template_path: Union[str, Path], output_dir: Union[str, Path], files_extension: str = "java"):
        self.project = project

        if type(template_path) == str:
            self.template_path = Path(template_path)
        else:
            self.template_path = template_path

        if type(output_dir) == str:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = output_dir

        self.files_extension = files_extension

    def execute(self):
        layers = {
            "domain": {
                "entities": {"template": "entities/entities_class.html", "output": "entities", "generator": self.generate_entities},
                "exceptions": {"template": "exceptions", "output": "exceptions", "generator": self.generate_exceptions},
                "repositories": {"template": "repositories/repositories.html", "output": "repositories", "generator": self.generate_domain_repositories},
                "services": {"template": "services/crud/crud_service.html", "output": "services/crud", "generator": self.generate_domain_crud_service},
                "usecases": {"template": "usecases", "output": "usecases", "generator": self.generate_usecases},
                # TODO sercices, dto, resource
            },
            "infrastructure": {
                "repositories": {"template": "repositories/jpa_repositories.html", "output":  "repositories", "generator": self.generate_infra_repositories},
                "utils": {"template":  "utils/utils.html", "output":  "utils", "generator": self.generate_utils},
                "services": {"template": "services/crud/crud_service.html", "output": "services/crud", "generator": self.generate_infrastructure_crud_service},
                "config": {"template": "config/config.html", "output": "config", "generator": self.generate_config},
                # TODO services
            },
            "presentation": {
                "api": {"template": "api", "output": "api", "generator": self.generate_api},
                "crud_repo": {"template": "api/crud/crud_controllers.html", "output": "api/crud", "generator": self.generate_crud_controller},
                # TODO
            },
        }

        for layer_name, layer_info in layers.items():
            self.generate_layer(self.template_path /
                                layer_name, self.output_dir/layer_name, layer_info)

    def generate_layer(self, layer_templates: Path, layer_output: Path, sub_layers: Dict):
        for layer_name, layer_info in sub_layers.items():
            layer_info["generator"](
                layer_templates/layer_info["template"], layer_output/layer_info["output"])

    def generate_usecases(self, template_path: Path, output_path: Path):

        # generate interface
        self.generate_single_file(
            template_path/"usecase_interface.html", output_path, "UseCase.java")

        # generate use cases
        os.makedirs(output_path, exist_ok=True)
        template = Template(
            (template_path/"usecase_class.html").read_text("utf-8"))

        for usecase in self.project.useCases:
            java_code = template.render(
                route=self.project.route, usecase=usecase)
            file_path = output_path / \
                Utils.capitalize(f"{usecase.name}.java")
            file_path.write_text(java_code)
    
    def generate_domain_crud_service(self, template_path: Path, output_path: Path):
        self.render_templates_class(template_path, output_path,
                                    lambda class_data: f"I{Utils.capitalize(class_data.name)}CrudService.java")

    def generate_crud_controller(self, template_path: Path, output_path: Path):
        self.render_templates_class(template_path, output_path,
                                    lambda class_data: f"{Utils.capitalize(class_data.name)}Controller.java")

    def generate_infrastructure_crud_service(self, template_path: Path, output_path: Path):
        self.render_templates_class(template_path, output_path,
                                    lambda class_data: f"{Utils.capitalize(class_data.name)}CrudService.java")

    def generate_domain_repositories(self, template_path: Path, output_path: Path):
        self.render_templates_class(template_path, output_path,
                                    lambda class_data: f"I{Utils.capitalize(class_data.name)}Repository.java")

    def generate_entities(self, template_path: Path, output_path: Path):
        self.render_templates_class(template_path, output_path,
                                    lambda class_data: f"{Utils.capitalize(class_data.name)}.java")

    def generate_exceptions(self, template_path: Path, output_path: Path):
        exception_types = ["already_exists", "not_found"]

        for exception in exception_types:
            current_template_path = template_path / exception
            current_output_path = output_path / exception
            os.makedirs(current_output_path, exist_ok=True)

            # Generate main exception file
            main_template = Template(
                (current_template_path / f"{exception}_exception.html").read_text("utf-8"))
            main_code = main_template.render(route=self.project.route)
            (current_output_path /
             f"{Utils.snake_to_pascal(exception)}Exception.java").write_text(main_code)

            # Generate entity-specific exceptions
            entity_template = current_template_path / \
                f"entity_{exception}_exception.html"
            self.render_templates_class(entity_template, current_output_path,
                                        lambda class_data: f"{Utils.capitalize(class_data.name)}{Utils.snake_to_pascal(exception)}Exception.java")

    def render_templates_class(self, template_path: Path, output_path: Path, file_naming_function):
        os.makedirs(output_path, exist_ok=True)
        template = Template(template_path.read_text("utf-8"))

        for class_data in self.project.classes:
            java_code = template.render(
                route=self.project.route, data=class_data)
            file_path = output_path / file_naming_function(class_data)
            file_path.write_text(java_code)

    def generate_utils(self,  template_path: Path, output_path: Path):
        self.generate_single_file(template_path, output_path, "Utils.java")

    def generate_config(self, template_path: Path, output_path: Path):
        self.generate_single_file(template_path, output_path, "Config.java")

    def generate_single_file(self, template_path: Path, output_path: Path, filename):
        os.makedirs(output_path, exist_ok=True)
        template = Template(template_path.read_text("utf-8"))
        java_code = template.render(
            route=self.project.route, project=self.project, use_cases=self.project.useCases)
        file_path = output_path / filename
        file_path.write_text(java_code)

    def generate_infra_repositories(self, template_path: Path, output_path: Path):
        self.render_templates_class(template_path, output_path,
                                    lambda class_data: f"{Utils.capitalize(class_data.name)}Repository.java")

    def generate_api(self, template_path: Path, output_path: Path):
        # generate global exception handler
        self.generate_single_file(
            template_path/"GlobalExceptionHandler.html", output_path, "GlobalExceptionHandler.java")

        # generate the app controller
        self.generate_single_file(
            template_path/"controllers.html", output_path, "AppController.java")
