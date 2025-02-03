from dataclasses import dataclass
from typing import List


@dataclass
class Scenario:
    main: List[str]
    alternative: List[str]

