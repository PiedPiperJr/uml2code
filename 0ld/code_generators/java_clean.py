from models.project_model import *
from typing import List
from pathlib import Path
from jinja2 import Template
import os
from utils.utils import snake_to_pascal, capitalize


def generate_clean_project(project: Project, template_path: str, output_dir: str):
    
    for clas in project.classes:
        clas["name"] = capitalize(clas["name"])
    for usc in project.useCases:
        usc["name"] = capitalize(usc["name"])

    project_path = Path(output_dir)
    templates = Path(template_path)
    # Generate the domain layer
    generate_domain_layer(project, templates / "domain",
                          project_path / "domain")

    # Generate the infrastructure layer
    generate_infrastructure_layer(
        project, templates / "infrastructure", project_path / "infrastructure")

    # Generate the presentation layer
    generate_presentation_layer(project, templates / "presentation", project_path / "presentation")
    

def generate_presentation_layer(project: Project, presentation_template: Path, presentation_output: Path):
    layers = {
        "api": {"template": presentation_template / "api", "output": presentation_output / "api", "generator": generate_api},
        # TODO 
    }

    for layer_name, layer_info in layers.items():
        layer_info["generator"](
            project, layer_info["template"], layer_info["output"])

    pass

def generate_api(project: Project, template_path: Path, output_path: Path):
    # generate global exception handler
    generate_single_file(project, template_path/"GlobalExceptionHandler.html", output_path, "GlobalExceptionHandler.java")

    # generate the app controller
    generate_single_file(project, template_path/"controllers.html", output_path, "AppController.java")

def generate_infrastructure_layer(project: Project, infrastructure_template: Path, infrastructure_output: Path):
    layers = {
        "repositories": {"template": infrastructure_template / "repositories/jpa_repositories.html", "output": infrastructure_output / "repositories", "generator": generate_infra_repositories},
        "utils": {"template": infrastructure_template / "utils/utils.html", "output": infrastructure_output / "utils", "generator": generate_utils},
        "config": {"template": infrastructure_template / "config/config.html", "output": infrastructure_output / "config", "generator": generate_config},
        # TODO services
    }

    for layer_name, layer_info in layers.items():
        layer_info["generator"](
            project, layer_info["template"], layer_info["output"])

    pass

def generate_utils(project: Project, template_path: Path, output_path: Path):
    generate_single_file(project, template_path, output_path, "Utils.java")

def generate_config(project: Project, template_path: Path, output_path: Path):
    generate_single_file(project, template_path, output_path, "Config.java")

def generate_single_file(project: Project, template_path: Path, output_path: Path, filename):
    os.makedirs(output_path, exist_ok=True)
    template = Template(template_path.read_text("utf-8"))
    java_code = template.render(route=project.route, project=project, use_cases=project.useCases)
    file_path = output_path / filename
    file_path.write_text(java_code)

def generate_infra_repositories(project: Project, template_path: Path, output_path: Path):
    render_templates_class(project, template_path, output_path,
                     lambda class_data: f"{capitalize(class_data['name'])}Repository.java")



def generate_domain_layer(project: Project, domain_template: Path, domain_output: Path):
    layers = {
        "entities": {"template": domain_template / "entities/entities_class.html", "output": domain_output / "entities", "generator": generate_entities},
        "exceptions": {"template": domain_template / "exceptions", "output": domain_output / "exceptions", "generator": generate_exceptions},
        "repositories": {"template": domain_template / "repositories/repositories.html", "output": domain_output / "repositories", "generator": generate_domain_repositories},
        "usecases": {"template": domain_template / "usecases", "output": domain_output / "usecases", "generator": generate_usecases},
        # TODO sercices, dto, resource
    }

    for layer_name, layer_info in layers.items():
        layer_info["generator"](
            project, layer_info["template"], layer_info["output"])

    

    pass


def generate_usecases(project: Project, template_path: Path, output_path: Path):

    #generate interface 
    generate_single_file(project, template_path/"usecase_interface.html", output_path, "UseCase.java" )

    # generate use cases
    os.makedirs(output_path, exist_ok=True)
    template = Template((template_path/"usecase_class.html").read_text("utf-8"))


    for usecase in project.useCases:
        java_code = template.render(route=project.route, usecase=usecase)
        file_path = output_path / capitalize(f"{usecase['name']}.java")
        file_path.write_text(java_code)
        

def generate_domain_repositories(project: Project, template_path: Path, output_path: Path):
    render_templates_class(project, template_path, output_path,
                     lambda class_data: f"I{capitalize(class_data['name'])}Repository.java")


def generate_entities(project: Project, template_path: Path, output_path: Path):
    render_templates_class(project, template_path, output_path,
                     lambda class_data: f"{capitalize(class_data['name'])}.java")


def generate_exceptions(project: Project, template_path: Path, output_path: Path):
    exception_types = ["already_exists", "not_found"]

    for exception in exception_types:
        current_template_path = template_path / exception
        current_output_path = output_path / exception
        os.makedirs(current_output_path, exist_ok=True)

        # Generate main exception file
        main_template = Template(
            (current_template_path / f"{exception}_exception.html").read_text("utf-8"))
        main_code = main_template.render(route=project.route)
        (current_output_path /
         f"{snake_to_pascal(exception)}Exception.java").write_text(main_code)

        # Generate entity-specific exceptions
        entity_template = current_template_path / \
            f"entity_{exception}_exception.html"
        render_templates_class(project, entity_template, current_output_path,
                         lambda class_data: f"{capitalize(class_data['name'])}{snake_to_pascal(exception)}Exception.java")


def render_templates_class(project: Project, template_path: Path, output_path: Path, file_naming_function):
    os.makedirs(output_path, exist_ok=True)
    template = Template(template_path.read_text("utf-8"))

    for class_data in project.classes:
        java_code = template.render(route=project.route, data=class_data)
        file_path = output_path / file_naming_function(class_data)
        file_path.write_text(java_code)
