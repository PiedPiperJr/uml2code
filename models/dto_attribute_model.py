from dataclasses import dataclass
from typing import List

from models.arg_model import Arg
from models.decorator_model import Decorator


@dataclass
class DtoAttribute(Arg):
    decorators: List[Decorator]
