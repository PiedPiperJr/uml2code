import os
from pathlib import Path
from jinja2 import Template
from typing import List, Union
from helpers.utils import Utils
from models.class_model import Class

class PoJoCodeGenerator:
    def __init__(self, classes: List[Class], template_path: Union[str, Path], output_dir: Union[str, Path], files_extension:str = "java"):
        self.classes = classes

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
        os.makedirs(self.output_dir, exist_ok=True)
        template = Template(self.template_path.read_text())

        for _class in self.classes:
            _class.name = Utils.capitalize(_class.name)
            java_code = template.render(data=_class)
            file_path = self.output_dir / f"{_class.name}.{self.files_extension}"
            file_path.write_text(java_code, encoding="utf-8")
